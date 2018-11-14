from pyparsing import *

data = """\
IF CONST > CONST { IDENT = CONST }
IF CONST == IDENT { IDENT = CONST EOS IDENT = IDENT EOS }
IF CONST != IDENT { IDENT = CONST } ELSE { IDENT = CONST + IDENT }
"""
# IDENT = CONST Optional(opArith IDENT) ->  
# IF CONST opLogic (CONST | IDENT) lparen IDENT EQ CONST rparen
# ELSE lparen IDENT opeLogic rparen  

data2 = """\
IF CONST == IDENT IDENT = CONST EOS
IF CONST != IDENT IDENT = CONST EOS ELSE IDENT = CONST + IDENT EOS
"""

declare   = Literal( 'DECLARE' )
ident     = Literal( 'IDENT' )
const     = Literal( 'CONST' )
rsvIf     = Literal( 'IF' )
revElse   = Literal( 'ELSE')
opAssign  = Literal( '=' )
lparen    = Literal( '{' )
rparen    = Literal( '}' )

opLogic   = oneOf( '== != <= < >= > && || !')
opArith   = oneOf( '+ - * / ** %' )

factor  = (const ^ itent) + ope + (const ^ itent)
term    = factor + ZeroOrMore()

# condition = CONST opLogic (CONST ^ IDENT)
condition = 
IF_STMT = 
ELSE_STMT  =
# oneof(const | itent) ope oneof(const | itent)