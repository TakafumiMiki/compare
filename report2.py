from pyparsing import *

data = """\
IF CONST > CONST { IDENT = COST }
IF CONST == IDENT { IDENT = CONST EOS IDENT = IDENT EOS }
IF CONST != IDENT { IDENT = CONST } ELSE { IDENT = CONST + IDENT }
"""

data2 = """\
IF CONST == IDENT IDENT = CONST EOS
IF CONST != IDENT IDENT = CONST EOS ELSE IDENT = CONST + IDENT EOS
"""

_IDENT = Literal("IDENT")
_CONST  = Literal("CONST")
_IF = Literal("IF")
_ELSE = Literal("ELSE")
_EOS = Suppress(Literal("EOS"))
_EQ1 = Literal("=")
_LEFT = Literal("{")
_RIGHT = Literal("}")

opLogic = oneOf( '== != <= < >= > && || !')
_comope = _CONST + opLogic + _CONST
_if = _IF + _comope + Optional(_LEFT)

