import ply.lex as lex
import sys
from Modelo.colores import *

class Lexico:

    # -------------------------------------------------------------------------------------------------
    #           Constructor de la clase Lexico
    # -------------------------------------------------------------------------------------------------
    def __init__(self):

        #variable para instanciar el modulo ply.lex
        self.lexer = None

        #palabres reservadas con llave-> valor , valor -> token (exp regular)
        self.keywords = {
            # LLAVE = value    VALOR = TOKEN
            'BEGIN': 'BEGIN',
            'END': 'END',
            'VAR': 'VAR',
            'INTEGER': 'INTEGER',
            'DOUBLE': 'DOUBLE',
            'STRING': 'STRING',
            'BOOLEAN': 'BOOLEAN',
            'FOR': 'FOR',
            'WHILE': 'WHILE',
            'REPEAT': 'REPEAT',
            'IF': 'IF',
            'ELSE': 'ELSE',
            'PROCEDURE': 'PROCEDURE',
            'FUNCTION': 'FUNCTION',
            'E': 'MODOVALOR',
            'ES': 'MODOREFERENCIA',
            'CALL': 'CALL',
            'MOD': 'MOD',
            'FLOOR': 'FLOOR',
            'CEIL': 'CEIL',
            'DIV': 'DIV',
            'AND': 'AND',
            'OR': 'OR',
            'NOT': 'NOT',
            'NULL': 'NULL',
            'T': 'TRUE',
            'F': 'FALSE',
            'LENGTH': 'LENGTH',
            'RECORD': 'RECORD',
            'STACK': 'STACK',
            'QUEUE': 'QUEUE',
            'LIST': 'LIST',
            'GRAPH': 'GRAPH',
            'TO': 'TO',
            'DO': 'DO',
            'WRITELN': 'WRITELN',
            'THEN': 'THEN',
            'UNTIL': 'UNTIL',
            'STR': 'STR',
            'RETURN': 'RETURN'
        }

        #tokens con expresiones regulares mas complejas
        self.tokens = [
                     'COMENTARIO',
                     'ID',
                     'DOUBLEVAL',
                     'INTEGERVAL',
                     'STRINGVAL',
                     'ASIGNACION',
                     'POR',
                     'DIVIDIR',
                     'MAS',
                     'MENOS',
                     'PA',
                     'PC',
                     'MENORIGUAL',
                     'MENOR',
                     'MAYORIGUAL',
                     'MAYOR',
                     'IGUAL',
                     'DIFERENTE',
                     'ARRAY',
                     'SUBARRAY',
                     'PUNTOCOMA',
                     'PUNTO',
                     'DOSPUNTOS',
                     'COMA'

                 ] + list(self.keywords.values())


    # -------------------------------------------------------------------------------------------------
    #       metodo que devuelve las palabras reservadas
    # -------------------------------------------------------------------------------------------------
    def getpalbras(self):
        return self.keywords.keys()


    # --------------------------------------------------------------------------------------------------------
    #       los metodos que contienen t_ son para las expresiones regulares de tokens (con exp mas complejas)
    #       y siempre recibe como parametro un t-> indicador de token
    #       normalmente se nombran así: def t_nombretoken(t):
    #                                      r'expresion regular'
    #
    # --------------------------------------------------------------------------------------------------------
    def t_COMENTARIO(self,t):
        r'\#.*'  # el caracter numerico junto a cualquier otra cosa exepto una nueva linea (.), 0 o muchas veces (*)
        pass
        # No retornamos nada, porque descartamos el token

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value, 'ID')  # Si no esta en las palabras reservadas retornamos el ID
        # Sino la palabra reservada
        return t

    def t_DOUBLEVAL(self,t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INTEGERVAL(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRINGVAL(self,t):
        r'\"(\s*\w*\_*\+*\-*\.*\,*\€*\!*\@*\#*\$*\%*\^*\**\(*\)*\;*\:*\\*\/*\|*\<*\>*\!*\¡*\?*\¿*\}*\{*\~*)*\"'
        t.value = str(t.value)
        # t.value = t.value.replace("\"","") # quitamos las comillas

        return t


    # -------------------------------------------------------------------------------------------------
    #        las variables que incian con t_ contienen la expresion regular de tokens que nececitan
    #        exp regular simple, se nombran así : t_nombrevar = r'expresion regular'
    # -------------------------------------------------------------------------------------------------
    t_ASIGNACION = r'\<--'
    t_POR = r'\*'
    t_DIVIDIR = r'\/'
    t_MAS = r'\+'
    t_MENOS = r'-'
    t_PA = r'\('
    t_PC = r'\)'
    t_MENORIGUAL = r'\<\='
    t_MENOR = r'\<'
    t_MAYORIGUAL = r'\>\='
    t_MAYOR = r'\>'
    t_IGUAL = r'\='
    t_DIFERENTE = r'\!\='
    t_ARRAY = r'\[\d+\]'
    t_SUBARRAY = r'\[\d+\s*\.\.\s*\d+\]'
    t_PUNTOCOMA = r'\;'
    t_PUNTO = r'\.'
    t_DOSPUNTOS = r'\:'
    t_COMA = r'\,'

    # -------------------------------------------------------------------------------------------------
    #           metodo que maneja la expresion regular de una nueva linea
    # -------------------------------------------------------------------------------------------------
    def t_newline(self,t):
        r'\n+'  # Regex salto de linea una o mas veces
        t.lexer.lineno += len(t.value)

    # Un string que contiene los caracteres que ingnoraremos en este caso los espacios y tabulaciones
    t_ignore = ' \t'

    # -------------------------------------------------------------------------------------------------
    #       instancia de la terminal de la aplicaicon
    # -------------------------------------------------------------------------------------------------
    terminal = None

    def setTerminal(self,term):
        global terminal
        terminal = term


    # -------------------------------------------------------------------------------------------------
    #           metodo que contiene la expresion regular para los tokens de error
    # -------------------------------------------------------------------------------------------------
    # Regla que manejare los errores, cuando encontramos un caracter no valido
    def t_error(self,t):
        print("Caracter invalido '%s'" % t.value[0], file=sys.stderr)  # imprimimos como error
        terminal.append(spanh_rojo + "Caracter invalido '%s'" % str(t.value[0]) + spanb)
        t.lexer.skip(1)

    # -------------------------------------------------------------------------------------------------
    #           metodo que construye el analizador lexico -> con instancia de ply.lex
    # -------------------------------------------------------------------------------------------------
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # -------------------------------------------------------------------------------------------------
    #           metod para probar el funcionamiento del analizador lexico
    # -------------------------------------------------------------------------------------------------
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
               break
            print(tok)



'''if __name__ == "__main__":
    lexico = Lexico()

    data2 =
         VAR \n
            x : INTEGER [5]; \n
            y : STACK; \n
            m : QUEUE; \n
            a : LIST; \n
            d : GRAPH; \n
            b : INTEGER; \n
            c : STRING; \n
            e : BOOLEAN; \n
            f : DOUBLE; \n
        BEGIN \n
            e <-- STR("HOLA"); \n
            x <-- 5; \n
        END \n


    lexico.build()
    lexico.test(data2)'''

    # GRACIAS A DIOS FUNCIONO MR BRAYAN !!! DIOS LO BENDIGA Y LO GUARDE
