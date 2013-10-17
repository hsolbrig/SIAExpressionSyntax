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
        print string.parseString(('|abc de* f??jk*|'))
        #print string.parseString('|Multiple Words and ´stuff|')


class TestSCTID(unittest.TestCase):
    def testChecksum(self):
        self.assertEqual(sctId.parseString('74400008').sctId, 74400008)
        self.assertRaises(ParseException, sctId.parseString, '74400007')

    def testLength(self):
        self.assertRaises(ParseException, sctId.parseString, '12345')
        self.assertEqual(sctId.parseString('123456789012345679').sctId, 123456789012345679)
        self.assertRaises(ParseException, sctId.parseString, '1234567890123456789')

    def testNumeric(self):
        self.assertRaises(ParseException, sctId.parseString, '74400007A')


class TestConcept(unittest.TestCase):
    def testSimple(self):
        self.assertEqual(concept.parseString('74400008').conceptId, 74400008)
        t1 = (concept).parseString('74400008 | Ack A mouse |')
        self.assertEqual(t1.conceptId, 74400008)
        self.assertEqual(t1.term, 'Ack A mouse')
        self.assertEqual((concept).parseString('74400008 | Appendicitis  (Finding) |').term, 'Appendicitis  (Finding)')
        for e in ['all', 'fullydefined', 'primitive', 'active']:
            self.assertEqual((concept).parseString(' %s ' % e).namedRefSet, e)

class TestSubtypeExp(unittest.TestCase):
    def test1(self):
        for i in ['^','!', '<','<<','>','>>']:
            print expression.parseString('%s 74400008' % i, parseAll=True)

    def test2(self):
        print expression.parseString('<< (74400008)')
        print expression.parseString('(<< (74400008))')

class TestStringExp(unittest.TestCase):
    def test1(self):
        print expression.parseString('filterOnMatch |abcde fg| 74400008', True)
        # There is something truly horrible about this call in a debug environment
        # Question - are expressions cumulative?
        print expression.parseString('filterOnNoMatch |A.*| all')

class TestAndOrExp(unittest.TestCase):
    def test1(self):
        # expression.setDebug()
        #print expression.parseString('filterOnMatch |abcde fg| 74400008 OR 7450006', True)
        print expression.parseString('74400008 AND 7450006', parseAll=True)
        print expression.parseString('(<<* 3 74400008) OR  7450006', True)


class TestRefinements(unittest.TestCase):
    def test1(self):
        conceptExp.setDebug()
        #print conceptExp.parseString('<<(418925002|Immune hypersensitivity reaction|) :246075003|Causitive agent| =all')

class TestNSubtypeExp(unittest.TestCase):
    def testNoInt(self):
        self.assertRaises(ParseException, expression.parseString, '<* 74400008')
        self.assertRaises(ParseException, expression.parseString, '<* a 74400008')

    def test1(self):
        for i in ['<*','<<*','>*','>>*','top','tail']:
            print expression.parseString('%s 3 74400008' % i, parseAll=True)
        for i in range(0, 10000000000, 999999999):
            print expression.parseString('<* %d 74400008' % i, parseAll=True)

    def test2(self):
        print expression.parseString('<<* 5 (74400008)')
        print expression.parseString('(>>* 5 (> 74400008))')


class TestExpression(unittest.TestCase):
    def testSimple(self):
        self.assertEqual(expression.parseString('74400008', parseAll=True).statement.conceptId, 74400008)

    def testParens(self):
        print (andor(sctId)).parseString('74400008 OR 74400008', parseAll=True)
        print (parens(sctId)).parseString('( 74400008 )', parseAll=True)
        print (expression).parseString('( 74400008 )', parseAll=True)




if __name__ == '__main__':
    unittest.main()