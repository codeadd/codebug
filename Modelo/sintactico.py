from Modelo.lexico import *
import ply.yacc as yacc




def p_operacion_par(p):
    'operacion : par'

def p_operacion_subarray(p):
    'operacion : SUBARRAY'

def p_par_opmath(p):
    'par : opmath'

def p_par_parAux(p):
    'par : PA par PC parAux'





def p_parAux_mathsymbol(p):
    'parAux : mathsymbol par'

def p_parAux_empty(p):
    'parAux : empty'





def p_opmath_valor(p):
    'opmath : valor'

def p_opmath_mathsymbol(p):
    'opmath : valor mathsymbol par'





def p_mathsymbol_mas(p):
    'mathsymbol : MAS'

def p_mathsymbol_menos(p):
    'mathsymbol : MENOS'

def p_mathsymbol_por(p):
    'mathsymbol : POR'

def p_mathsymbol_dividir(p):
    'mathsymbol : DIVIDIR'

def p_mathsymbol_div(p):
    'mathsymbol : DIV'

def p_mathsymbol_mod(p):
    'mathsymbol : MOD'




def p_techo(p):
    'techo : CEIL PA opmath PC'

def p_piso(p):
    'piso : FLOOR PA opmath PC'



def p_valor_id(p):
    'valor : ID'

def p_valor_integerval(p):
    'valor : INTEGERVAL'

def p_valor_doubleval(p):
    'valor : DOUBLEVAL'

def p_valor_stringval(p):
    'valor : STRINGVAL'

def p_valor_true(p):
    'valor : TRUE'

def p_valor_false(p):
    'valor : FALSE'

def p_valor_techo(p):
    'valor : techo'

def p_valor_piso(p):
    'valor : piso'

def p_valor_longitud(p):
    'valor : longitud'

def p_valor_dequeue(p):
    'valor : dequeue'

def p_valor_pop(p):
    'valor : pop'

def p_valor_get(p):
    'valor : get'

def p_valor_getq(p):
    'valor : getq'

def p_valor_getp(p):
    'valor : getp'

def p_valor_size(p):
    'valor : size'

def p_valor_sizequeue(p):
    'valor : sizequeue'

def p_valor_sizestack(p):
    'valor : sizestack'

def p_valor_deep(p):
    'valor : deep'

def p_valor_width(p):
    'valor : width'

def p_valor_llamar(p):
    'valor : llamar'





def p_longitud(p):
    'longitud : LENGTH PA STRINGVAL PC'

def p_dequeue(p):
    'dequeue : DEQUEUE PA ID PC'

def p_pop(p):
    'pop : POP PA ID PC'

def p_get(p):
    'get : GET PA ID COMA INTEGERVAL PC'

def p_getq(p):
    'getq : GET_P PA ID PC'

def p_getp(p):
    'getp : GET_Q PA ID PC'

def p_size(p):
    'size : SIZE PA ID PC'

def p_sizequeue(p):
    'sizequeue : SIZE_QUEUE PA ID PC'

def p_sizestack(p):
    'sizestack : SIZE_STACK PA ID PC'

def p_deep(p):
    'deep : DEEP PA ID PC'

def p_width(p):
    'width : WIDTH PA ID PC'



def p_llamar_valoresCall(p):
    'llamar : CALL ID PA valoresCall PC'

def p_llamar_vacio(p):
    'llamar : CALL ID PA PC'



def p_valoresCall_valor(p):
    'valoresCall : valor'

def p_valoresCall_varios(p):
    'valoresCall : valor COMA valoresCall'




def p_empty(p):
    'empty : '
    pass


def p_longitud_error(p):
    'longitud : LENGTH PA error PC'
    print("Tipo de dato invalido, se esperaba una cadena", file=sys.stderr)

def p_dequeue_error(p):
    'dequeue : DEQUEUE PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_pop_error(p):
    'pop : POP PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_get_error(p):
    'get : GET PA ID COMA error PC'
    print("Tipo de dato invalido, se esperaba un indice de tipo INTEGER", file=sys.stderr)

def p_getq_error(p):
    'getq : GET_P PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_getp_error(p):
    'getp : GET_Q PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_size_error(p):
    'size : SIZE PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_sizequeue_error(p):
    'sizequeue : SIZE_QUEUE PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_sizestack_error(p):
    'sizestack : SIZE_STACK PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_deep_error(p):
    'deep : DEEP PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)

def p_width_error(p):
    'width : WIDTH PA error PC'
    print("Tipo de dato invalido, se esperaba una variable", file=sys.stderr)




def p_error(p):
    if(p != None):
        print("Errror de Sintaxis en la linea " +  str(p.lineno) + " en el token " + str(p.value))
    else:
        print("Errror de Sintaxis")





parser = yacc.yacc()


while True:
   try:
       s = input('')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)