import ply.lex as lex
import sys

keywords = {
    #LLAVE = value    VALOR = TOKEN
    'BEGIN' :    'BEGIN',
    'END'   :   'END',
    'VAR'   :   'VAR',
    'INTEGER'   :   'INTEGER',
    'DOUBLE'    :   'DOUBLE',
    'STRING'    :   'STRING',
    'BOOLEAN'   :   'BOOLEAN',
    'FOR'   :   'FOR',
    'WHILE' :   'WHILE',
    'REPEAT'    :   'REPEAT',
    'IF'    :   'IF',
    'ELSE'  :   'ELSE',
    'PROCEDURE' :   'PROCEDURE',
    'FUNCTION'  :   'FUNCTION',
    'E'     :   'MODOVALOR',
    'ES'    :   'MODOREFERENCIA',
    'CALL'  :   'CALL',
    'MOD'   :   'MOD',
    'FLOOR' :   'FLOOR',
    'CEIL'  :   'CEIL',
    'DIV'   :   'DIV',
    'AND'   :   'AND',
    'OR'    :   'OR',
    'NOT'   :   'NOT',
    'NULL'  :   'NULL',
    'T'     :   'TRUE',
    'F'     :   'FALSE',
    'LENGTH'    :   'LENGTH',
    'RECORD'    :   'RECORD',
    'STACK'     :   'STACK',
    'QUEUE'     :   'QUEUE',
    'LIST'      :   'LIST',
    'GRAPH'     :   'GRAPH',
    'TO'        :   'TO',
    'DO'        :   'DO',
    'WRITELN'   :   'WRITELN',
    'THEN'      :   'THEN',
    'UNTIL'     :   'UNTIL',
    'STR'       :   'STR',
    'RETURN'    :   'RETURN'
    }

tokens  = [
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
    
    ] + list(keywords.values())
    


def t_COMENTARIO(t):
    r'\#.*' # el caracter numerico junto a cualquier otra cosa exepto una nueva linea (.), 0 o muchas veces (*)
    pass
    # No retornamos nada, porque descartamos el token


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID') #Si no esta en las palabras reservadas retornamos el ID
    #Sino la palabra reservada
    return t
 
def t_DOUBLEVAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
    
def t_INTEGERVAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRINGVAL(t):
    r'\"(\s*\w*\_*\+*\-*\.*\,*\€*\!*\@*\#*\$*\%*\^*\**\(*\)*\;*\:*\\*\/*\|*\<*\>*\!*\¡*\?*\¿*\}*\{*\[*\]*\~*)*\"'
    t.value = str(t.value)
    #t.value = t.value.replace("\"","") # quitamos las comillas

    return t



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
    
    
    
def t_newline(t):
    r'\n+' #Regex salto de linea una o mas veces
    t.lexer.lineno += len(t.value)
    
#Un string que contiene los caracteres que ingnoraremos en este caso los espacios y tabulaciones
t_ignore = ' \t'

#Regla que manejare los errores, cuando encontramos un caracter no valido
def t_error(t):
    print("Caracter invalido '%s'" % t.value[0], file=sys.stderr) #imprimimos como error
    t.lexer.skip(1)    


lexer = lex.lex()

data = '''
    VAR
        x : INT [5];
        y : STACK;
        m : QUEUE;
        a : LIST;
        d : GRAPH;
        b : INTEGER;
        c : STRING;
        e : BOOLEAN;
        f : DOUBLE;
    BEGIN
        e <-- T;
        x[2] <-- 5;
        b <-- 0;
        f <-- 5.0;
        FOR i <-- 5 TO 10 DO
        BEGIN
            WHILE( e != F )DO
            BEGIN
                REPEAT
                b <-- CEIL(b DIV 5);
                b <-- FLOOR(b MOD 3);
                UNTIL (f >= 10)
            END
        END
        IF( b = 15 )THEN
            BEGIN
                WRITELN("FUNCIONOOOO GRACIAS A DIOS , DIOS LO BENDIGA " + LENGHT(x));
                ADD(a, 5.023);
                a <-- NULL;
                #ESTO ES UN HERMOSO COMENTARIO \n

            END
        ELSE
            BEGIN
                WRITELN("NO FUNCIONO, INTENELO DENUEVO CON LA AYUDA DE DIOS ");
            END
    END
    
    '''

data2 = '''
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
'''

lexer.input(data2)
while True:
    tok = lexer.token()

    if not tok:
        break
    print(tok.type, tok.value, tok.lineno, tok.lexpos)


    
    
    
    
    
    
