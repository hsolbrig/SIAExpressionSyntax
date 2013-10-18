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
from Parser import *
ParserElement.enablePackrat

output = lambda e: e.asXML()

def proc(str, pp=expression):
    print '<!-- %s -->' % str,
    print output(pp.parseString(str, True))
    print


proc('<<404684003|Clinical finding|')

proc('<<404684003|Clinical finding| AND fullydefined ')

proc('<<*3 404684003|Clinical finding|   ')

# NOTE: this isn't correct in the spec, - waiting input
proc('<<(418925002|Immune hypersensitivity reaction| :246075003|Causitive agent| =all)')

proc('all: 246075003|Causitive agent| = 84676004|Prion|  ')

proc('all ')

# NOTE: this had the wrong check digit in the document
proc('<<34014006|Viral disease| OR  ^60140062|My Virus Reset| ')

proc("""all:{ 363698007|Finding site| = 90785001|Inguinal canal structure|,
   116676008|Associated morphology| = 414402003|Hermial opening|}""")

proc("""all:({363698007|Finding site| = 90785001|Inguinal canal structure|,
116676008|Associated morphology| = 414402003|Hermial opening|}
	AND {363698007|Finding site| = 52731004|Abdominal cavity structure|,
	116676008|Associated morphology| = 414403008|Hernia|})""")

# NOTE: The document has a capital 'F'
# NOTE: The grammar doesn't allow parenthesis where they are - it is
#       string expression (no paren string expr)
proc("""filterOnMatch |chronic c hepatitis| (<<34014006|Viral disease|)""")


proc("""<118956008|Body structure altered from its original|
OR ( <404684003|Clinical finding|
	AND !(<307824009|Administrative statuses|
		OR <405533003|Adverse incident outcome categories|
		OR <420134006|Propensity to adverse reactions|
		OR <365858006|Prognosis/outlook finding|
		OR <285153007|Sequelae of external causes and disorders|))
OR <272379006|Events|
OR <413350009|Finding with explicit context|
OR <57177007|Family history of|
OR <4908009|Past history of| """)


# NOTE: Edited significantly from section 11
proc("""(<404684003|Clinical finding|)
:(116676008|Associated morphology|=(<<23583003|Inflammation|),
363698007|Finding site|=(<<39352004|Joint structure|),
246075003|Causative agent|=(<<410607006|Organism|))""")

# Note: parens required around value
proc("""(^4021000036102|Specimen type reference set|)
:370133003|Specimen substance|=(<406455002|Allergen class|)""")

# Note: parens required around value
proc("""(<64572001|Disease|):(116676008|Associated morphology|=(<<37782003|Damage|),
	363698007|Finding site|=
		(!(<<123037004|Body structure|
		AND !(<<91723000|Anatomical structure|))))""")

# Note: parens required around value
proc("""(<373873005|Pharmaceutical / biologic product|)
	: 127489000|Has active ingredient|=(<<372687004|Amoxicillin|)
	AND (127489000|Has active ingredient|=(<<395938000|Clavulanate|))""")

# Note: parens required around value

proc("""(<404684003|Clinical finding|):( 246454002|Occurrence|=(255398004|Childhood| OR 3658006|Infancy|)
AND 246075003|Causative agent|=(<409822003|Bacteria|))""")
