from pyparsing import *

data = """\
IF CONST > CONST { IDENT = CONST }
IF CONST == IDENT { IDENT = CONST EOS IDENT = IDENT EOS }
IF CONST != IDENT { IDENT = CONST } ELSE { IDENT = CONST + IDENT }
"""
# if const == ident:
#   ident = const eos
#   ident = const eos

# if const != ident:
#   ident = const eos
# else:
#   ident = const + ident eos

data2 = """\
IF CONST == IDENT IDENT = CONST EOS
IF CONST != IDENT IDENT = CONST EOS ELSE IDENT = CONST + IDENT EOS
"""

ident     = Literal( 'IDENT' )
const     = Literal( 'CONST' )
eos       = Literal( 'EOS' )
rsvIf     = Literal( 'IF' )
rsvElse   = Literal( 'ELSE')
opAssign  = Literal( '=' )
# lparen    = Literal( '{' )
# rparen    = Literal( '}' )

opLogic   = oneOf( '== != <= < >= > && || !')
opArith   = oneOf( '+ - * / ** %' )
operator = opLogic ^ opArith
# 代入文として IDENT = CONST
# 比較文として CONST > CONST or IDENT

# IDENT = CONST operator IDENT
# CONST operator (IDENT ^ CONST)
# factor -> IDENT opAssign CONST operator (IDENT ^ CONST) 
factor  = Optional(ident) + Optional(opAssign) + const + Optional(operator) + Optional(ident ^ const)  
term = factor + ZeroOrMore( operator + factor)

# condition = const + operator + (CONST ^ IDENT)


_if = rsvIf + Optional(term)
ifS = _if.setResultsName("IF_STMT")

_else = rsvElse + Optional(term)
elseS = _else.setResultsName("ELSE_STMT")

_assign = ident + opAssign + term
assignS = _assign.setResultsName('ASN')

statatement = assignS  ^ ifS ^ elseS
# statatement = ifS ^ elseS

r = statatement

print('line   col  stmt   DSL')
print('----- ----- ------ ---------------------')
for i in r.scanString(data2):
#    print(i)
    ty=[x for x in i[0].asDict().keys()]
    if 'IF_STMT' in ty:
        ty='IF_STMT'
    elif 'ELSE_STMT' in ty:
        ty='ELSE_STMT'
    else: ty=ty[0] 
    print('%5d %5d %-6s %-s'%(
            lineno(i[1], data2), col(i[1], data2),
            ty,
            ' '.join([x for x in i[0]]) ) )
