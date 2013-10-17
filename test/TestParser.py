# -*- coding: utf-8 -*-
# Copyright (c) 2013, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the <ORGANIZATION> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
import unittest
from Parser import *

class TestString(unittest.TestCase):
    def test1(self):

        print string.parseString('|abc|', True)
        print string.parseString('|abc de* f??jk*|', True)
        print string.parseString('|Multiple Words and ´stuff|', True)


class TestSCTID(unittest.TestCase):
    def testChecksum(self):
        self.assertEqual(sctId.parseString('74400008', True).sctId, 74400008)
        self.assertRaises(ParseException, sctId.parseString, '74400007')

    def testLength(self):
        self.assertRaises(ParseException, sctId.parseString, '12345')
        self.assertEqual(sctId.parseString('123456789012345679', True).sctId, 123456789012345679)
        self.assertRaises(ParseException, sctId.parseString, '1234567890123456789')

    def testNumeric(self):
        self.assertRaises(ParseException, sctId.parseString, '74400007A')


class TestConcept(unittest.TestCase):
    def testSimple(self):
        self.assertEqual(concept.parseString('74400008', True).concept.sctId, 74400008)
        t1 = (concept).parseString('74400008 | Ack A mouse |', True)
        self.assertEqual(t1.concept.sctId, 74400008)
        self.assertEqual(t1.concept.term, 'Ack A mouse')
        self.assertEqual((concept).parseString('74400008 | Appendicitis  (Finding) |', True).concept.term, 'Appendicitis  (Finding)')
        for e in ['all', 'fullydefined', 'primitive', 'active']:
            self.assertEqual(concept.parseString(' %s ' % e, True).namedRefset, e)

class TestSubtypeExp(unittest.TestCase):
    def test1(self):
        for i in ['^','!', '<','<<','>','>>']:
            print expression.parseString('%s 74400008' % i, True)

    def test2(self):
        print expression.parseString('<< (74400008)', True)
        print expression.parseString('(<< (74400008))', True)

class TestStringExp(unittest.TestCase):
    def test1(self):
        print expression.parseString('filterOnMatch |abcde fg| 74400008', True)
        print expression.parseString('filterOnNoMatch |A.*| all', True)

class TestAndOrExp(unittest.TestCase):
    def test1(self):
        # expression.setDebug()
        #print expression.parseString('filterOnMatch |abcde fg| 74400008 OR 7450006', True)
        print expression.parseString('74400008 AND 7450006', True)
        # This seems to take a really long time
        #print expression.parseString('(<<* 3 74400008) OR  7450006', True)


class TestRefinements(unittest.TestCase):
    def test1(self):
        conceptExp.setDebug()
        #print conceptExp.parseString('<<(418925002|Immune hypersensitivity reaction|) :246075003|Causitive agent| =all', True)

class TestNSubtypeExp(unittest.TestCase):
    def testNoInt(self):
        self.assertRaises(ParseException, expression.parseString, '<* 74400008')
        self.assertRaises(ParseException, expression.parseString, '<* a 74400008')

    def test1(self):
        for i in ['<*','<<*','>*','>>*','top','tail']:
            print expression.parseString('%s 3 74400008' % i, True)
        for i in range(0, 10000000000, 999999999):
            print expression.parseString('<* %d 74400008' % i, True)

    def test2(self):
        print expression.parseString('<<* 5 (74400008)', True)
        print expression.parseString('(>>* 5 (> 74400008))', True)


class TestExpression(unittest.TestCase):
    def testSimple(self):
        t1 = expression.parseString('74400008', True)
        self.assertEqual(expression.parseString('74400008', True).expression.concept.sctId, 74400008)

    def testParens(self):
        print (parens(sctId)).parseString('( 74400008 )', True)
        print (expression).parseString('( 74400008 )', True)




if __name__ == '__main__':
    unittest.main()