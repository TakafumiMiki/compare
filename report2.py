from pyparsing import *

data2 = """\
IF CONST > CONST { IDENT = COST }
IF CONST == IDENT { IDENT = CONST EOS IDENT = IDENT EOS }
IF CONST != IDENT { IDENT = CONST } ELSE { IDENT = CONST + IDENT }
"""

data1 = """\
IF CONST == IDENT IDENT = CONST EOS
IF CONST != IDENT IDENT = CONST EOS ELSE IDENT = CONST + IDENT EOS
"""

ident     = Literal( 'IDENT' )
const     = Literal( 'CONST' )
eos       = Literal( 'EOS' )
lparen    = Literal( '{' )
rparen    = Literal( '}' )
rsvIf     = Literal( 'IF' )
rsvElse   = Literal( 'ELSE')
opAssign  = Literal( '=' )

opLogic   = oneOf( '== != <= < >= > && || !')
opArith   = oneOf( '+ - * / ** %' )

_condition = const + opLogic + (ident ^ const)
conditionS = _condition.setResultsName("CON")

_assign = ident + opAssign + const + Optional(opArith + ident) 
assignS = _assign.setResultsName('ASN')

_if = rsvIf + _condition + SkipTo( eos | lparen)
ifS = _if.setResultsName("IF_STMT")

_else = rsvElse + SkipTo(eos | lparen)
elseS = _else.setResultsName("ELSE_STMT")

statatement =  ifS ^ elseS ^ conditionS ^ assignS 
r = statatement

print('line   col  stmt\tDSL')
print('----- ----- ---------- ---------------------')
for i in r.scanString(data1):
    isElse = False
#    print(i)
    ty=[x for x in i[0].asDict().keys()]
    if 'IF_STMT' in ty:
        ty='IF_STMT'
    elif 'ELSE_STMT' in ty:
        ty='ELSE_STMT'
    else: ty=ty[0]
    print('%5d %5d %-6s %-s'%(
            lineno(i[1], data1), col(i[1], data1),
            ty,
            ' '.join([x for x in i[0]]) ) )