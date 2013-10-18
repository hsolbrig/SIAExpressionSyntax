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
from pyparsing import *
from CheckDigit import validateVerhoeff, calcsum


# @@@ string from section 10

# Everything except a star and a bar
# Question: What is the character set of 'string'?  Will it ever need a star or a bar?
nonstarnonbar = printables.replace('*','').replace('|','')
string = Suppress('|') + Group(OneOrMore( (Word(nonstarnonbar) + Optional('*')).setParseAction(lambda l:''.join(l))("word")))("string") + Suppress('|')
# Recommend an alternative - optional quoted string (vs. bars but...)


# @@@ ws= *( SP | HTAB | CR | LF )
# This is built in.  We need to check the rules but we would propose matching standard parsers

# @@@ integer is not defined in the spec.
# Question: We're assuming non-negative (should it be positive)?
integer = Word(nums).setParseAction(lambda n: int(n[0]))
# @@@ digit= %x30-39
digit = nums
# @@@ digitNonZero= %x31-39
digitNonZero = nums.replace('0','')

# And / or operators.
# Question: Precedence (AND over OR or equal?) (We assume AND precedence
# Question: Left or Right associative (We assume left)
andorOperators = [(Literal('AND')("setop"), 2, opAssoc.LEFT),
                  (Literal('OR')("setop"), 2, opAssoc.LEFT)]


# @@@ stringOperator = “filterOnMatch” / “filterOnNoMatch”
stringOp = oneOf('filterOnMatch filterOnNoMatch')
# @@@ namedRefSet = “all” / “fullydefined” / “primitive” / “active”
namedRefSet = oneOf('all fullydefined primitive active')('namedRefSet')
# @@@ nonwsnonpipe= %x21-7B / %x7D-7E / UTF8-2 / UTF8-3 / UTF8-4
# TODO: need to verify that all of the UTF characters are in
nonwsnonpipe = (printables + alphas8bit).replace('|','')

# @@@ unaryOperator = “^” / “!” / “>>” / “>” / “<” / “<<”
# Question: Wouldn't it make more sense to have a SUBTRACT set operator?  What *does* complement mean anyway?
nft = lambda c,t : Literal(c).setParseAction(lambda _:t)
vsOp = nft('^','valueset')
complementOp = nft('!', 'complement')
subTypeOp = nft('<', 'subtypes')
pSubTypeOp = nft('<<', 'subtypesAndBase')
superTypeOp = nft('>>','supertypesAndBase')
pSuperTypeOp = nft('>',"supertypes")
subTypeOps = (vsOp ^ complementOp ^ subTypeOp ^ pSubTypeOp ^ superTypeOp ^ pSuperTypeOp)("operator")

# @@@ binaryOperator = “>>*” / “>*” / “<*” / “<<*” / “top” / “tail”
# Question: 'top' and 'tail' are only meaningful if there is some sort of ordering, no?  It definitely needs
#           further explanation
nsubTypeOp = nft('<*', 'nsubtypes')
npSubTypeOp = nft('<<*', 'nsubtypesAndBase')
nsuperTypeOp = nft('>>*','nsupertypesAndBase')
npSuperTypeOp = nft('>*',"nsupertypes")
ntop = nft('top','top')
ntail = nft('tail','tail')
constraintOps = (nsubTypeOp ^ npSubTypeOp ^ npSuperTypeOp ^ nsuperTypeOp ^ ntop  ^ ntail)("operator")

parens = lambda e: Group(Suppress('(') + e + Suppress(')'))
pipes = lambda t: Suppress('|') + t + Suppress('|')

# sctId = digitNonZero 5*17( digit )
def validateSCTID(num):
    if not validateVerhoeff(num):
        raise ParseException("Bad SCTID Checksum (%s) - last digit should be %d" % (num, calcsum(str(num)[:-1])))
    return num


sctId   = Word(digitNonZero,digit,6,18).setParseAction(lambda n:validateSCTID(int(n[0])))('sctId')
# @@@ term = 1*nonwsnonpipe *( 1*SP 1*nonwsnonpipe )
term = OneOrMore(Word(nonwsnonpipe + ' ')).setParseAction(lambda n:''.join(n).strip()).setResultsName('term')
concept = Group((sctId("sctId") + Optional(pipes(term("term")))))("concept") ^ namedRefSet("namedRefset")

expression = Forward()
refinements = Forward()

# =====================
# Expression Section
# =====================
# @@ expression =  “(“ expression “)” / expression ( “AND” / “OR” ) expression /
#                     unaryOperator expression / integerOperator integer expression /
#                     stringOperator string expression / ( concept /
#                    “(“ expression “)” ) *("+" (concept / “(“ expression “)” ) [":" ws refinements]

# concept / “(“ expression “)”
conceptOrParenExp = concept("concept") | parens(expression)("expression")
# unaryOperator expression
subTypeExp = Group(subTypeOps + conceptOrParenExp)("subTypeExp")
# integerOperator integer expression
nsubTypeExp = Group(constraintOps + integer("integer") + conceptOrParenExp)("nsubTypeExp")
# stringOperator string expression
stringExp = Group(stringOp + string + conceptOrParenExp)("stringExp")
# ( concept / “(“ expression “)” ) *("+" (concept / “(“ expression “)” ) [":" ws refinements]
conceptOrParenList = conceptOrParenExp + ZeroOrMore('+' + conceptOrParenExp)
refinementsClause = Optional(Group(Suppress(':') + refinements)("refinements"))
conceptExp = (conceptOrParenList + refinementsClause)

statement = (subTypeExp ^ nsubTypeExp ^ stringExp ^ conceptExp)("statement")
expression << Group(infixNotation(statement, andorOperators))("expression")

# ====================
# Refinements Section
# =====================

# @@@ attributeName =  concept / (ws "(" expression ")" ws)
# @@@ attributeValue = concept / (ws "(" expression ")" ws)
# @@@ attribute = attributeName "=" attributeValue
# @@@ attributeSet = “(“ attributeSet “)” / attributeSet (“AND” / “OR” ) attributeSet / attribute *("," attribute)
# @@@ attributeGroup = “(“ attributeGroup “)” / attributeGroup (“AND” / “OR” ) attributeGroup /
#                      "{" attributeSet "}" ws
# @@@ refinements = “(“ refinements “)” / refinements ( “AND” / “OR” ) refinements /
#                   ( attributeSet *attributeGroup ) / 1*attributeGroup

attributeName = conceptOrParenExp("name")
attributeValue = conceptOrParenExp("value")
attribute = Group(attributeName + Suppress('=') + attributeValue)("attribute")
attributeSet = infixNotation(attribute, andorOperators + [(Suppress(','), 2, opAssoc.LEFT)])
attributeGroup = infixNotation(Group(Suppress('{') + attributeSet + Suppress('}'))("group"), andorOperators)
attributeRefinements = (attributeSet + ZeroOrMore(attributeGroup)) ^ attributeGroup
refinements << infixNotation(attributeRefinements, andorOperators)






































