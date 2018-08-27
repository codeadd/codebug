from Modelo.lexclass import *
import ply.yacc as yacc
import queue as queue
import networkx as nx
import time
import threading
import math
from Modelo.colores import *
from Modelo.n_ary_tree import *



# -------------------------------------------------------------------------------------------------
#       clase Semantico:
#              contiene todo lo relacionado con el analisis sintactico y semantico
#              de los algoritmos digitados por el usuario
# -------------------------------------------------------------------------------------------------
class Semantico:
    # -------------------------------------------------------------------------------------------------
    #       constructor de la clase Semantico:
    #           recibe:
    #
    #           terminal -> para imprimir errores y los contenidos del Writeln del los algoritmos
    #           editor   -> para mover la linea en el editor a la sentencia que se este ejecutando
    #                       para ver el analisis paso a paso
    #
    # -------------------------------------------------------------------------------------------------
    def __init__(self,a = None,trm = None, e = None,):


        self.lexer = Lexico()       #instancia del analizador lexico

        self.tokens = self.lexer.tokens #tokens del analizdor lexico para construir las reglas

        self.avanzar = False        #variable de control para el paso a paso

        #funciones reservadas del lenguaje
        self.funciones_reservadas = ['GET_P', 'GET_Q', 'GET', 'WIDTH', 'DEEP', 'DEQUEUE', 'POP', 'SIZE', 'SIZE_QUEUE',
                                     'SIZE_STACK']

        #procedimientos reservados del lenguaje
        self.procedimientos_reservadas = ['ADD', 'ENQUEUE', 'PUSH', 'SORT', 'ADD_NODE', 'ADD_EDGE', 'REMOVE',
                                          'REMOVE_NODE',
                                          'REMOVE_TRANS', 'TO_LIST']  # para convertir un arreglo en una lista

        #tipos basicos del lenguaje
        self.tipos_lenguaje = {int: 'INTEGER', str: 'STRING', float: 'DOUBLE', bool: 'BOOLEAN'}

        self.variables_globales = {}  # aqui guardaremos las variables, su tipo y su valor respectivo
        self.variables_actuales = None # con esta variable sabemos si debemos o no imprimir
        self.funciones = {}        #funciones creadas por el usuario
        self.procedimientos = {}   #procedimientos creados por el usuario
        self.registros = {}        #registros creados por el usuario
        self.detener = False
        self.lineas_marcadas = {}   #lineas marcadas por el usuario
        self.ambiente_actual = 0    #variable para determinar el ambiente actual

        self.arbolito = n_ary_tree()    #arbol de entornos
        self.ambientes = 0              #contador de ambientes para determinar el padre de cada entorno

        self.tiempito = 0               #tiempo que se demora la ejecucion
        self.dicci = {}                 #contiene las ejecuciones y sus tiempos reales
        self.dicci_break={}             #contiene las ejecuciones y sus tiempos teoricos(conteo de breackpoints)
        self.contador = 0

        self.area = a
        self.terminal = trm
        self.editor = e

        self.t = None

    # -------------------------------------------------------------------------------------------------
    #   produccion principal de el analizador sintactico - semantico
    #
    #   las producciones se definen de la siguiente manera:
    #       siempre se utilizan metodos para definirla con el prefijo p_ y reciben como parametro un p
    #       que contiene lo que ha subido el arbol mediante las reglas semanticas
    #       ejemplo:
    #               para una sola produccion
    #               def p_nombreprocuccion(p):
    #                   'nombreProduccion : produccion'
    #
    #               para varias producciones
    #               def p_nombreproduccion(p):
    #                   ''' nombreProduccion : produccion1
    #                                        | produccion2 '''
    #
    #               para reglas semanticas
    #               def p_nombreproduccion(p):
    #                   #aqui se pone la produccion de las formas ya especificadas
    #                   'nombreproduccion : token1 token2 prodcuccion1 token3'
    #                   #reglas semanticas
    #                   p[0] = p[1] + p[3]
    #
    #                   donde p[0] -> nombreproduccion , p[1] -> token1 , p[2] -> lo que devuelve produccion1
    #
    # -------------------------------------------------------------------------------------------------
    def p_bloqueP(self,p):
        'bloqueP : declaracionPrincipal bloque'
        self.tabla_principal = p[2] #-> tabla principal que tiene como forma una tupla ((),((),()))
        # print("Tabla principal : "+str(tabla_principal))


        #self.mostrar_variables(self.variables_globales)


        self.arbolito.add1(self.ambientes,"ROOT") #se añade el primer ambiene
        self.run(self.tabla_principal, self.variables_globales,self.ambientes) # se llama el metodo con la tupla


        #self.mostrar_variables(self.variables_globales)


        #self.limpiar_variables()  # limpiamos las variables despues de que termine la ejecucion
        print(self.tiempito)
        self.terminal.append("Terminado en :"+str(self.tiempito))
        self.dicci[self.contador] = self.tiempito #se añade el tiempito al diccionario

        sum=0
        for i in self.lineas_marcadas.values():
            sum += i

        self.dicci_break[self.contador] = sum   #se añade los breackpoints al diccionario de breackpoints

        exit(0)

    # Meotodo main
    # -------------------------------------------------------------------------------------------------
    #           metodo principal-> contiene la logica de ejecucion de los algoritmos
    #           dijitados por el usuario
    #           recibe una tubla como entrada y hace llamados recursivos dividiendo la tupla en tuplas mas
    #           pequeñas
    #           recibe la tupla,las variables del entorno y el padre del ambiente
    # -------------------------------------------------------------------------------------------------
    def run(self,tabla, variables: {},padre = 0):


        # avanzar = True # para que lo vuelva true cada ves que dentre a run

        # print(tabla_principal[1])
        # print(len(tabla_principal[0]))
        # print(tabla[1][1])
        # print(len(tabla[1][1][1]))
        self.ambiente_actual = padre  # movemos el ambiente
        print(self.ambiente_actual)


        while self.avanzar == True:
            x = 1  # esto es para que no me saque error porque el while no tiene nada
        # print("Avanzo") # cuando es false entonces imprime esto y sigue con el proceso

        if (self.detener == True): # detenemos el programa
            self.limpiar_variables()  # limpiamos variables antes se salir
            exit(1)

        self.avanzar = True # lo hacemos true para que se detenga en la siguiente ejecucion

        self.variables_actuales = None


        time.sleep(1)
        if type(tabla) == list:
            # area.append("Funcion")
            # mostrar_variables(variables)
            self.run(tabla[0], variables,self.ambientes)
            return self.run((tabla[1]), variables,self.ambientes)  # retornamos
        else:
            if tabla[0][0] == 'asignar':
                iniciot = time.time()
                self.variables_actuales = variables

                #self.mostrar_variables(variables)

                #rint("\nEntro a assig")
                # area.append("Asignar")

                # time.sleep(1)
                asig = tabla[0][1]
                if type(asig[0]) == tuple:  # si es una tupla es porque lo ahi dentro es un diccionario
                    var_name = asig[0][0]
                    if var_name in variables.keys():
                        var = variables[var_name]

                        var_indice_max = var[0][1]  # tamaño del arreglo
                        var_indice = asig[0][1]
                        if var_indice > var_indice_max:
                            print("Error semantico, se desbordo el arreglo " + var_name, file=sys.stderr)
                            self.terminal.append(spanh_rojo + "Error semantico, se desbordo el arreglo " + var_name + spanb)
                        else:
                            tipo_var = var[0][0]
                            valor = asig[1]

                            valor = self.organizar_valor(valor, variables,padre)  # organizamos el valor
                            tipo_valor = type(valor)
                            tipo_valor = self.tipos_lenguaje[tipo_valor]
                            if (tipo_valor == tipo_var):
                                var_value = var[1]
                                var_value[var_indice] = valor

                                # print(valor)

                                # print("Asigancion Arreglo : "+str(tabla[2]))
                                self.editor.setCursorPosition(tabla[2] - 1, 0)
                                #print(tabla[2])
                                if tabla[2] in self.lineas_marcadas.keys():
                                    self.lineas_marcadas[tabla[2]] += 1


                                fint = time.time()
                                #self.tiempito = (fint-iniciot)
                                self.run(tabla[1], variables,padre)

                            else:
                                print("Error semantico, no puede asginar a un " + tipo_var + " un " + tipo_valor,
                                      file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no puede asginar a un " + tipo_var + " un " + tipo_valor + spanb)
                                exit(1)
                                # var.insert(var_indice,)

                    else:
                        print("Error semantico, esta variable no existe " + var_name, file=sys.stderr)
                        self.terminal.append(spanh_rojo + "Error semantico, esta variable no existe " + var_name + spanb)
                else:
                    var_name = asig[0]
                    if var_name in variables.keys():
                        var = variables[var_name]
                        tipo_var = var[0]
                        if tipo_var in ("INTEGER", "DOUBLE", "STRING"):  # el tipo debe hacer parte de esto

                            valor = asig[1]
                            valor = self.organizar_valor(valor, variables, padre)
                            tipo_valor = type(valor)
                            tipo_valor = self.tipos_lenguaje[tipo_valor]
                            if (tipo_valor == tipo_var):
                                var[1] = valor

                                # print(valor)
                                # print("Asigancion Normal : " + str(tabla[2]))
                                self.editor.setCursorPosition(tabla[2] - 1, 0)
                                #print(tabla[2])
                                if tabla[2] in self.lineas_marcadas.keys():
                                    self.lineas_marcadas[tabla[2]] += 1

                                fint = time.time()
                                self.tiempito = (fint - iniciot)
                                self.run(tabla[1], variables,padre)

                            else:
                                print("Error semantico, no puede asginar a un " + tipo_var + " un " + tipo_valor,
                                      file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no puede asginar a un " + tipo_var + " un " + tipo_valor + spanb)
                        else:
                            print("Error semantico, no se puede operar con este tipo de datos " + tipo_var,
                                  file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, no se puede operar con este tipo de datos " + tipo_var + spanb)
                            exit(1)

            elif tabla[0][0] == 'si':
                iniciot = time.time()
                # area.append("If")
                # mostrar_variables(variables)
                # mostrar_variables(variables)
                # print("entro a un si")
                # print(tabla)   #('si',(condicion,contenidoBloque,sino),contenidoBloque)
                primera_parte_si = tabla[0][1]  # lo que contiene el si (condicion,contenidoBloque,sino)
                # print(primera_parte_si)
                condicion_temp = primera_parte_si[0]  # saco la condicion
                # print(type(condicion_temp))
                cad_eval = self.organizar_condicion(condicion_temp,
                                               variables, padre)  # organizo la condicion , para esto agrege una coma en la produccion condicion
                # que deriva en continuidad
                # print(cad_eval)


                result_cond = eval(cad_eval)  # evaluo la cadena y lo guardo el resultado de la condicion
                # print(result_cond)

                if result_cond:  # utilizo la condicion
                    # print("cumple condicion")
                    # print("Sentencia Si: " + str(tabla[2]))
                    self.editor.setCursorPosition(tabla[2] - 1, 0)
                    if tabla[2] in self.lineas_marcadas.keys():
                        self.lineas_marcadas[tabla[2]] += 1

                    fint = time.time()
                    self.tiempito = (fint-iniciot)
                    self.run(primera_parte_si[1],
                        variables,padre)  ## ejecuto el metodo con lo que viene dentro del si es decir contenidoBloque
                else:
                    # en caso de que no se cumpla la condicion
                    # print("no cumple condicion")
                    # print("Sentencia Si no: " + str(tabla[2]))
                    fint = time.time()
                    self.tiempito = (fint - iniciot)
                    self.run(primera_parte_si[2], variables,padre)  ## ejecuto el metodo con lo que tiene el sino contenidoSino

                fint = time.time()
                self.tiempito = (fint - iniciot)

                self.run(tabla[1],
                    variables,padre)  ##llamo el metodo con el hermano derecho es decir con el bloqueContenido externo


            elif tabla[0][0] == 'mientras':
                iniciot = time.time()
                # area.append("While")
                # mostrar_variables(variables)
                # mostrar_variables(variables)
                # print("entro a while")
                # print(tabla) #('while',(condicion,bloque dentro del while),bloque despues del while)
                primera_parte_mientras = tabla[0][
                    1]  # obtengo (condicion,bloqueContenidodento del while,bloqueContenido depues while)
                # print(primera_parte_mientras)
                condicion_temp = primera_parte_mientras[0]  # obtengo la condicion
                cad_eval = self.organizar_condicion(condicion_temp, variables, padre)  ## llamo a organizar condicion
                # print(cad_eval)
                result_cond = eval(cad_eval)  # evaluo la condicion
                while result_cond:
                    self.editor.setCursorPosition(tabla[2] - 1, 0)
                    if tabla[2] in self.lineas_marcadas.keys():
                        self.lineas_marcadas[tabla[2]] += 1
                    self.run(primera_parte_mientras[1],
                        variables,padre)  # ejecuto el metodo con el bloque contenido que esta dentro del while
                    cad_eval = self.organizar_condicion(condicion_temp,
                                                   variables, padre)  # reorganizo la condicion, funciona como actualizar la condicion
                    # print(cad_eval)
                    result_cond = eval(cad_eval)  # evaluo la condicon que reorganize para que la tome el while
                    # print("Sentencia Mientras: " + str(tabla[2]))

                    # print(variables['i'][1])
                    # print(cad_eval)
                    # result_cond = eval(cad_eval)
                    # print(result_cond)

                fint = time.time()
                self.tiempito = (fint - iniciot)

                self.run(tabla[1], variables,padre)
            elif tabla[0][0] == 'para':
                iniciot = time.time()
                # area.append("For")
                # mostrar_variables(variables)
                # print("entro a un para")
                # print(tabla) #('para',(var,inicio,fin,(('asignar',(var,valor),bloquedepues de asignar)),bloque despues de for))
                segunda_parte_para = tabla[0][1]  # (var,inicio,fin,bloquedentro del for)
                # print(segunda_parte_para)
                var_key = segunda_parte_para[0]  # obtengo la variable
                if (var_key in variables.keys()):
                    inicio = self.organizar_valor(segunda_parte_para[1], variables, padre)  # obtengo el inicio
                    limite = self.organizar_valor(segunda_parte_para[2],
                                             variables, padre)  # obtengo el fin, lo envaluamos por si nos envian una variable

                    if (type(limite) != int):
                        print("Error semantico, el limite del for debe ser un entero", file=sys.stderr)
                        self.terminal.append(spanh_rojo + "Error semantico, el limite del for debe ser un entero" + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # print('inicio : '+str(inicio)+'limite : '+str(limite))

                    # variables[var_key][1] = int(inicio)

                    for i in range(inicio, limite):  # construyo un for desde inicio hasta fin
                        variables[var_key][
                            1] = i  # a la variable que va a estar en el for le asigno lo que hay en i para que vaya
                        # cambiando su estado
                        # print("Sentencia Para: " + str(tabla[2]))
                        self.editor.setCursorPosition(tabla[2] - 1, 0)
                        if tabla[2] in self.lineas_marcadas.keys():
                            self.lineas_marcadas[tabla[2]] += 1
                        # print(variables[var_key])
                        self.run(segunda_parte_para[3], variables,padre)  # ejecuto el metodo con el bloque que esta dentro del for

                    fint = time.time()
                    self.tiempito = (fint - iniciot)

                    self.run(tabla[1], variables,padre)  # ejecuto lo que hay en el bloque despues del for
                else:
                    print("Error semantico, no existe esta variable" + var_key, file=sys.stderr)
                    self.terminal.append(spanh_rojo + "Error semantico, no existe esta variable" + var_key + spanh)
                    self.limpiar_variables()
                    exit(1)
                    # print(var)
            elif tabla[0][0] == 'repetir':
                iniciot = time.time()
                # area.append("Repeat")
                # mostrar_variables(variables)
                # (('repetir', ('condicion', bloqueCOntenido_repetir), bloqueContenido_despuesRepetir)
                segunda_parte_repetir = tabla[0][1]
                condicion = segunda_parte_repetir[0]

                self.run(segunda_parte_repetir[1], variables,padre)

                cad_eval = self.organizar_condicion(condicion, variables, padre)
                # print("condicion ---- " + str(cad_eval))

                result_cond = eval(cad_eval)

                while (result_cond):
                    self.editor.setCursorPosition(tabla[2] - 1, 0)
                    if tabla[2] in self.lineas_marcadas.keys():
                        self.lineas_marcadas[tabla[2]] += 1
                    self.run(segunda_parte_repetir[1], variables,padre)

                    cad_eval = self.organizar_condicion(condicion, variables, padre)
                    # print(cad_eval)
                    result_cond = eval(cad_eval)

                fint = time.time()
                self.tiempito = (fint - iniciot)

                self.run(tabla[1], variables,padre)

            elif tabla[0][0] == 'escribir':
                iniciot = time.time()
                # ('escribir', '"Hola mundo"'),
                valor = tabla[0][1]
                valor_evaluado = self.organizar_valor(valor, variables, padre)
                valor_evaluado = str(valor_evaluado)

                self.editor.setCursorPosition(tabla[2] - 1, 0)
                if tabla[2] in self.lineas_marcadas.keys():
                    self.lineas_marcadas[tabla[2]] += 1

                #print(">>>> " + valor_evaluado)

                self.terminal.append(spanh_azul_claro + ">>>>>>   " + spanb + spanh_verde + valor_evaluado + spanb)
                # print("Sentencia escribir: " + str(tabla[2]))
                fint = time.time()
                self.tiempito = (fint - iniciot)
                self.run(tabla[1], variables,padre)


            elif tabla[0][0] == 'llamarProcedimiento':
                # ('llamarProcedimiento', ('sumatoria', '1,10,&sumRes&')
                # area.append("Procedure")
                # mostrar_variables(variables
                iniciot = time.time()
                variables_procedimientos = {}
                # print(tabla[0])
                nombre_procedure_llamado = tabla[0][1][0]

                parametros_pasados = tabla[0][1][1]

                # print(procedimientos)
                # print("Sentencia call procedure: " + str(tabla[2]))
                self.editor.setCursorPosition(tabla[2] - 1, 0)
                if tabla[2] in self.lineas_marcadas.keys():
                    self.lineas_marcadas[tabla[2]] += 1
                self.variables_actuales = variables

                #si es un procedimiento reservado
                if nombre_procedure_llamado.upper() in self.procedimientos_reservadas:
                    if nombre_procedure_llamado == 'ENQUEUE':
                        cola = ''
                        valor_encolar = ''
                        lista_parametros = parametros_pasados.split(",")
                        # print(lista_parametros)
                        if len(lista_parametros) == 2:
                            indice = 0
                            for m in range(0, len(lista_parametros)):
                                if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                                    temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                                    if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                        temp_var = variables[temp_var_name]  # entonces la sacamos

                                        tipo_var = temp_var[0]

                                        if (tipo_var == 'QUEUE' and indice == 0):  # ees porque es el primer parametro
                                            cola = temp_var[1]
                                        elif indice == 1:  # esporque es el segundo parametro
                                            if (tipo_var not in self.tipos_lenguaje.values()):
                                                print(
                                                    "Error semantico, a las colas solo se les puede insertar tipos primitivos de datos, nada de arreglos o estructuras de datos",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a las colas solo se les puede insertar tipos primitivos de datos, nada de arreglos o estructuras de datos" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_encolar = temp_var[1]

                                        else:
                                            print(
                                                "Error semantico, no se puede realizar una operacion de encolar en una variable diferente a una QUEUE",
                                                file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, no se puede realizar una operacion de encolar en una variable diferente a una QUEUE" + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                    else:
                                        print(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                else:

                                    if (indice == 0):
                                        print(
                                            "Error semantico, se esperaba una variable de tipo QUEUE, no un escalar",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, se esperaba una variable de tipo QUEUE, no un escalar" + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                    else:
                                        valor_encolar = lista_parametros[m]
                                indice += 1

                            # termino el for
                            # encolamos
                            cola.append(valor_encolar)  # encolamos
                            fint = time.time()
                            self.tiempito = (fint - iniciot)
                            self.run(tabla[1], variables,padre)

                        else:
                            print(
                                "Error sintaxicosemantico, la funcion encolar solo recive dos parametros, la cola y el valor a encolar ",
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error sintaxicosemantico, la funcion encolar solo recive dos parametros, la cola y el valor a encolar " + spanb)
                            self.limpiar_variables()
                            exit(1)
                    elif nombre_procedure_llamado == 'PUSH':
                        pila = ''
                        valor_apilar = ''
                        lista_parametros = parametros_pasados.split(",")
                        # print(lista_parametros)
                        if len(lista_parametros) == 2:
                            indice = 0
                            for m in range(0, len(lista_parametros)):
                                if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                                    temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                                    if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                        temp_var = variables[temp_var_name]  # entonces la sacamos

                                        tipo_var = temp_var[0]

                                        if (tipo_var == 'STACK' and indice == 0):  # ees porque es el primer parametro
                                            pila = temp_var[1]
                                        elif indice == 1:  # esporque es el segundo parametro
                                            if (tipo_var not in self.tipos_lenguaje.values()):
                                                print(
                                                    "Error semantico, a las pilas solo se les puede insertar tipos primitivos de datos, nada de arreglos o estructuras de datos",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a las pilas solo se les puede insertar tipos primitivos de datos, nada de arreglos o estructuras de datos" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_apilar = temp_var[1]

                                        else:
                                            print(
                                                "Error semantico, no se puede realizar una operacion push en una variable diferente a una STACK",
                                                file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, no se puede realizar una operacion push en una variable diferente a una STACK" + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                    else:
                                        print(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                else:

                                    if (indice == 0):
                                        print(
                                            "Error semantico, se esperaba una variable de tipo STACK, no un escalar",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, se esperaba una variable de tipo STACK, no un escalar" + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                    else:
                                        valor_apilar = lista_parametros[m]
                                indice += 1

                            # termino el for

                            pila.append(valor_apilar)  # apilamos
                            fint = time.time()
                            self.tiempito = (fint-iniciot)
                            self.run(tabla[1], variables, padre)

                        else:
                            print(
                                "Error sintaxicosemantico, la funcion push solo recive dos parametros, la pila y el valor a añadir ",
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error sintaxicosemantico, la funcion push solo recive dos parametros, la pila y el valor a añadir " + spanb)
                            self.limpiar_variables()
                            exit(1)
                    elif nombre_procedure_llamado == 'ADD':
                        lista = ''
                        valor_adicionar = ''
                        lista_parametros = parametros_pasados.split(",")
                        # print(lista_parametros)
                        if len(lista_parametros) == 2:
                            indice = 0
                            for m in range(0, len(lista_parametros)):
                                if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                                    temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                                    if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                        temp_var = variables[temp_var_name]  # entonces la sacamos

                                        tipo_var = temp_var[0]

                                        if (tipo_var == 'LIST' and indice == 0):  # ees porque es el primer parametro
                                            lista = temp_var[1]
                                        elif indice == 1:  # esporque es el segundo parametro
                                            if (tipo_var not in self.tipos_lenguaje.values()):
                                                print(
                                                    "Error semantico, a las listas solo se les puede insertar tipos primitivos de datos, nada de arreglos o estructuras de datos",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a las listas solo se les puede insertar tipos primitivos de datos, nada de arreglos o estructuras de datos" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_adicionar = temp_var[1]

                                        else:
                                            print(
                                                "Error semantico, no se puede realizar una operacion add en una variable diferente a una LIST",
                                                file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, no se puede realizar una operacion add en una variable diferente a una LIST" + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                    else:
                                        print(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                else:

                                    if (indice == 0):
                                        print(
                                            "Error semantico, se esperaba una variable de tipo LIST, no un escalar",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, se esperaba una variable de tipo LIST, no un escalar" + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                    else:
                                        valor_adicionar = lista_parametros[m]
                                indice += 1

                            # termino el for
                            lista.append(valor_adicionar)  # adicionamos
                            fint = time.time()
                            self.tiempito = (fint - iniciot)
                            self.run(tabla[1], variables,padre)

                        else:
                            print(
                                "Error sintaxicosemantico, la funcion add solo recive dos parametros, la lista y el valor a añadir ",
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error sintaxicosemantico, la funcion add solo recive dos parametros, la lista y el valor a añadir " + spanb)
                            self.limpiar_variables()
                            exit(1)

                    elif nombre_procedure_llamado == 'REMOVE':
                        lista = ''
                        valor_remover = 0
                        lista_parametros = parametros_pasados.split(",")
                        # print(lista_parametros)
                        if len(lista_parametros) == 2:
                            indice = 0
                            for m in range(0, len(lista_parametros)):
                                if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                                    temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                                    if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                        temp_var = variables[temp_var_name]  # entonces la sacamos

                                        tipo_var = temp_var[0]

                                        if (tipo_var == 'LIST' and indice == 0):  # ees porque es el primer parametro
                                            lista = temp_var[1]
                                        elif indice == 1:  # esporque es el segundo parametro
                                            if (tipo_var not in self.tipos_lenguaje.values()):
                                                print(
                                                    "Error semantico, a las listas solo se les puede remover datos de tipo primitivos, nada de arreglos o estructuras de datos",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a las listas solo se les puede remover datos de tipo primitivos, nada de arreglos o estructuras de datos" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_remover = temp_var[1]

                                        else:
                                            print(
                                                "Error semantico, no se puede realizar una operacion remove en una variable diferente a una LIST",
                                                file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, no se puede realizar una operacion remove en una variable diferente a una LIST" + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                    else:
                                        print(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                else:

                                    if (indice == 0):
                                        print(
                                            "Error semantico, se esperaba una variable de tipo LIST, no un escalar",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, se esperaba una variable de tipo LIST, no un escalar" + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                    else:
                                        valor_remover = lista_parametros[m]
                                indice += 1

                            # termino el for
                            lista.remove(valor_remover)  # adicionamos
                            fint = time.time()
                            self.tiempito = (fint - iniciot)
                            self.run(tabla[1], variables,padre)

                        else:
                            print(
                                "Error sintaxicosemantico, la funcion remove solo recive dos parametros, la cola y el valor a encolar ",
                                file=sys.stderr)
                            exit(1)
                    elif nombre_procedure_llamado == 'SORT':
                        lista = ''
                        lista_parametros = parametros_pasados.split(",")
                        # print(lista_parametros)
                        if len(lista_parametros) == 1:
                            indice = 0
                            for m in range(0, len(lista_parametros)):
                                if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                                    temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                                    if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                        temp_var = variables[temp_var_name]  # entonces la sacamos

                                        tipo_var = temp_var[0]

                                        if (tipo_var == 'LIST' and indice == 0):  # ees porque es el primer parametro
                                            lista = temp_var[1]

                                        else:
                                            print(
                                                "Error semantico, no se puede realizar una operacion sort en una variable diferente a una LIST",
                                                file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, no se puede realizar una operacion sort en una variable diferente a una LIST" + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                    else:
                                        print(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                            file=sys.stderr)
                                        self.terminal.append(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado)
                                        self.limpiar_variables()
                                        exit(1)
                                else:

                                    if (indice == 0):
                                        print(
                                            "Error semantico, se esperaba una variable de tipo LIST, no un escalar",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            "Error semantico, se esperaba una variable de tipo LIST, no un escalar")
                                        self.limpiar_variables()
                                        exit(1)
                                indice += 1

                            # termino el for
                            lista.sort()  # adicionamos
                            fint = time.time()
                            self.tiempito = (fint - iniciot)
                            self.run(tabla[1], variables,padre)

                        else:
                            print(
                                "Error sintaxicosemantico, la funcion sort, solo recibe un parametro que es la lista a ordenar ",
                                file=sys.stderr)
                            self.terminal.append(
                                "Error sintaxicosemantico, la funcion sort, solo recibe un parametro que es la lista a ordenar ")
                            self.limpiar_variables()
                            exit(1)
                    elif nombre_procedure_llamado == 'ADD_NODE':
                        grafo = ''
                        valor_nodo = 0
                        lista_parametros = parametros_pasados.split(",")
                        # print(lista_parametros)
                        if len(lista_parametros) == 2:
                            indice = 0
                            for m in range(0, len(lista_parametros)):
                                if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                                    temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                                    if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                        temp_var = variables[temp_var_name]  # entonces la sacamos

                                        tipo_var = temp_var[0]

                                        if (tipo_var == 'GRAPH' and indice == 0):  # ees porque es el primer parametro
                                            grafo = temp_var[1]
                                        elif indice == 1:  # esporque es el segundo parametro
                                            if (tipo_var not in self.tipos_lenguaje.values()):
                                                print(
                                                    "Error semantico, a los grafos solo se les puede añadir nodos de tipo primitivos, nada de arreglos o estructuras de datos",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a los grafos solo se les puede añadir nodos de tipo primitivos, nada de arreglos o estructuras de datos" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_nodo = temp_var[1]

                                        else:
                                            print(
                                                "Error semantico, no se puede realizar una operacion add_node en una variable diferente a un GRPAH",
                                                file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, no se puede realizar una operacion add_node en una variable diferente a un GRPAH" + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                    else:
                                        print(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                else:

                                    if (indice == 0):
                                        print(
                                            "Error semantico, se esperaba una variable de tipo GRAPH, no un escalar",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, se esperaba una variable de tipo GRAPH, no un escalar" + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                    else:
                                        valor_nodo = lista_parametros[m]
                                indice += 1

                            # termino el for
                            grafo.add_node(valor_nodo)  # adicionamos
                            fint = time.time()
                            self.tiempito = (fint - iniciot)
                            self.run(tabla[1], variables,padre)

                        else:
                            print(
                                "Error sintaxicosemantico, la funcion add_node solo recive dos parametros, el grafo y el valor a añadir ",
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error sintaxicosemantico, la funcion add_node solo recive dos parametros, el grafo y el valor a añadir " + spanb)
                            self.limpiar_variables()
                            exit(1)
                    elif nombre_procedure_llamado == 'ADD_EDGE':
                        grafo = ''
                        valor_nodo_origen = 0
                        valor_nodo_destino = 0
                        valor_nodo_peso = 0.0
                        lista_parametros = parametros_pasados.split(",")
                        # print(lista_parametros)
                        if len(lista_parametros) == 4:
                            indice = 0
                            for m in range(0, len(lista_parametros)):
                                if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                                    temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                                    if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                        temp_var = variables[temp_var_name]  # entonces la sacamos

                                        tipo_var = temp_var[0]

                                        if (tipo_var == 'GRAPH' and indice == 0):  # ees porque es el primer parametro
                                            grafo = temp_var[1]
                                        elif indice == 1:  # esporque es el segundo parametro
                                            if (tipo_var not in self.tipos_lenguaje.values()):
                                                print(
                                                    "Error semantico, a los grafos solo tiene nodos de tipo primitivos, nada de arreglos o estructuras de datos",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a los grafos solo tiene nodos de tipo primitivos, nada de arreglos o estructuras de datos" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_nodo_origen = temp_var[1]
                                        elif indice == 2:
                                            if (tipo_var not in self.tipos_lenguaje.values()):
                                                print(
                                                    "Error semantico, a los grafos solo tiene nodos de tipo primitivos, nada de arreglos o estructuras de datos",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a los grafos solo tiene nodos de tipo primitivos, nada de arreglos o estructuras de datos" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_nodo_destino = temp_var[1]
                                        elif indice == 3:
                                            if (tipo_var == 'DOUBLE'):
                                                print(
                                                    "Error semantico, a los grafos solo puede tener pesos de tipo DOUBLE en las aristas",
                                                    file=sys.stderr)
                                                self.terminal.append(
                                                    spanh_rojo + "Error semantico, a los grafos solo puede tener pesos de tipo DOUBLE en las aristas" + spanb)
                                                self.limpiar_variables()
                                                exit(1)
                                            else:
                                                valor_nodo_peso = temp_var[1]

                                        else:
                                            print(
                                                "Error semantico, no se puede realizar una operacion add_edge en una variable diferente a un GRPAH",
                                                file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, no se puede realizar una operacion add_edge en una variable diferente a un GRPAH" + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                    else:
                                        print(
                                            "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                else:  # es porque no es una variable, sino un valor normal

                                    if (indice == 0):
                                        print(
                                            "Error semantico, se esperaba una variable de tipo GRAPH, no un escalar",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, se esperaba una variable de tipo GRAPH, no un escalar" + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                    elif (indice == 1):
                                        valor_nodo_origen = lista_parametros[m]

                                    elif (indice == 2):
                                        valor_nodo_destino = lista_parametros[m]

                                    elif (indice == 3):
                                        valor_nodo_peso = lista_parametros[m]
                                indice += 1

                            # termino el for
                            grafo.add_edge(valor_nodo_origen, valor_nodo_destino, weight=valor_nodo_peso)  # adicionamos
                            fint = time.time()
                            self.tiempito = (fint - iniciot)
                            self.run(tabla[1], variables,padre)

                        else:
                            print(
                                "Error sintaxicosemantico, la funcion add_trans solo recive dos parametros, el grafo y el valor a añadir ",
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error sintaxicosemantico, la funcion add_trans solo recive dos parametros, el grafo y el valor a añadir " + spanb)
                            self.limpiar_variables()
                            exit(1)







                #sino, es un procedimiento creado por el usuario
                elif nombre_procedure_llamado in self.procedimientos.keys():  # verificamos si esta en la tabla de procedimientos


                    self.ambientes += 1


                    iniciot = time.time()
                    # {'sumatoria': ('E,INTEGER,numero1-E,INTEGER,numero2-ES,INTEGER,resultado', (('para', ('numero', 0, 'numero2', (('asignar', ('resultado', '&resultado&+&numero&')), 'omitaBloque'))), 'omitaBloque'))}


                    procedimiento_llamado = self.procedimientos[nombre_procedure_llamado]  # obtenemos el procedimiento
                    parametros_esperado = procedimiento_llamado[0]  # obtenemos los parametros esperados

                    parametros_esperado = parametros_esperado.split('-')  # spliteamos los parametros

                    parametros_esperado_organizado = []
                    for n in parametros_esperado:
                        temp_p = n.split(',')
                        parametros_esperado_organizado.append(temp_p)
                    tabla_procedimiento = procedimiento_llamado[1]
                    lista_parametros = parametros_pasados.split(",")
                    for m in range(0, len(lista_parametros)):
                        if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                            temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                            if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                temp_var = variables[temp_var_name]  # entonces la sacamos

                                if parametros_esperado_organizado[m][
                                    0] == 'E':  # sacamos el tipo de parametros que recibe # sacamos el tipo de parametro que recibe
                                    nombre_variable = parametros_esperado_organizado[m][
                                        2]  # obtenemos el nombre de la variable
                                    tipo_variable = parametros_esperado_organizado[m][
                                        1]  # obtenemos el tipo de variable

                                    if temp_var[0] == tipo_variable:  # si los tipos corresponden
                                        if temp_var[
                                            0] not in self.tipos_lenguaje.values():  # si es una estructura de datos # miramos si es una estuctura de datos
                                            print(
                                                "!!!!!!!!Advertencia, los tipos de estrucutras de datos se pasan por referencia si o si")
                                            self.terminal.append(
                                                spanh_amarillo + "!!!!!!!!Advertencia, los tipos de estrucutras de datos se pasan por referencia si o si" + spanb)
                                        variables_procedimientos[nombre_variable] = [
                                            tipo_variable, temp_var[1]]  # enviamos la variable


                                    else:
                                        print(
                                            "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                            + " y se encontro con " + str(temp_var[0]), file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                            + " y se encontro con " + str(temp_var[0]) + spanb)
                                        self.limpiar_variables()
                                        exit(1)

                                else:  # por referencia
                                    nombre_variable = parametros_esperado_organizado[m][2]
                                    tipo_variable = parametros_esperado_organizado[m][1]

                                    if temp_var[0] == tipo_variable:
                                        variables_procedimientos[nombre_variable] = temp_var  # enviamos la variable


                                    else:
                                        print(
                                            "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                            + " y se encontro con " + str(temp_var[0]), file=sys.stderr)
                                        self.terminal.append(spanh_rojo +
                                                        "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                                        + " y se encontro con " + str(temp_var[0]) + spanb)
                                        self.limpiar_variables()
                                        exit(1)

                            else:
                                print(
                                    "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado,
                                    file=sys.stderr)
                                self.terminal.append(spanh_rojo +
                                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_procedure_llamado + spanb)
                                self.limpiar_variables()
                                exit(1)

                        else:
                            if parametros_esperado_organizado[m][0] == 'E':
                                variable_pasada = lista_parametros[m]

                                try:
                                    variable_pasada = eval(variable_pasada)
                                    nombre_variable = parametros_esperado_organizado[m][2]
                                    tipo_variable = parametros_esperado_organizado[m][1]
                                    if (type(variable_pasada) in self.tipos_lenguaje.keys()):
                                        tipo_variable_pasada = self.tipos_lenguaje[type(variable_pasada)]
                                        if (tipo_variable_pasada == tipo_variable):
                                            variables_procedimientos[nombre_variable] = [tipo_variable,
                                                                                         variable_pasada]  # creamos una variable
                                        else:
                                            print(
                                                "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                                + " y se encontro con " + str(variable_pasada), file=sys.stderr)
                                            self.terminal.append(
                                                spanh_rojo + "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                                + " y se encontro con " + str(variable_pasada) + spanb)
                                            self.limpiar_variables()
                                            exit(1)
                                except Exception as e:
                                    print(
                                        "Error semantico, no se permite este tipo de parametros " + variable_pasada + " " + str(
                                            e), file=sys.stderr)
                                    self.terminal.append(
                                        spanh_rojo + "Error semantico, no se permite este tipo de parametros " + variable_pasada + " " + str(
                                            e) + spanb)
                                    self.limpiar_variables()
                                    exit(1)
                            else:
                                print("Error semantico, un escalar no se puede pasar por referencia ", file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, un escalar no se puede pasar por referencia " + spanb)
                                self.limpiar_variables()
                                exit(1)

                    # print(procedimiento_llamado[1])
                    fint = time.time()
                    self.tiempito = (fint - iniciot)

                    print("agrego ambiente", self.arbolito.add2(self.ambientes, padre, "Procedimiento : " + str(
                        nombre_procedure_llamado) + "\nParametros pasados " + str(variables_procedimientos)))

                    print("Ambiente : ", self.ambientes, " Padre : ", padre)

                    self.run(procedimiento_llamado[1], variables_procedimientos,self.ambientes)
                    self.run(tabla[1], variables,padre)  # llamamos lo que sigue
                else:
                    print("Error semantico, Este procedimiento no existe  " + nombre_procedure_llamado, file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error semantico, Este procedimiento no existe  " + nombre_procedure_llamado + spanb)
                    self.limpiar_variables()
                    exit(1)


            elif tabla[0] == 'retorno':  # esto se cumple cuando es una funcion
                # ('retorno', '&n3&')
                iniciot = time.time()
                # print("ENTRO A RETORNO")
                valor = self.organizar_valor(tabla[1], variables, padre)
                #self.editor.setCursorPosition(tabla[2] - 1, 0)
                #print(tabla)
                fint = time.time()
                self.tiempito = (fint - iniciot)
                if tabla[2] in self.lineas_marcadas.keys():
                    self.lineas_marcadas[tabla[2]] += 1
                return valor

    # -------------------------------------------------------------------------------------------------
    #   metodo que organiza las condiciones de los while, for, if y repeat
    #   hace uso del metodo organizar variables
    # -------------------------------------------------------------------------------------------------
    def organizar_condicion(self, valor, variables: {}, padre = 0):
        cad_eval = ''
        lista_condicion = valor.split(',')  # separo por coma en una lista los valores que entran
        # print(lista_condicion)
        lista_oplog = ['<', '>', '<=', '>=', 'and', 'or', '!=', '=']  # lista con los operadores logicos

        for i in lista_condicion:  # recorro la lista cad_temp
            if i not in lista_oplog:  # si no esta en los operadores e por que es un id o valor exlicito
                val_temp = self.organizar_valor(i, variables, padre)  # obtengo el valor de la cadena
                # print(val_temp)
                cad_eval += str(val_temp)  # la concateno en la cadena que vamos a devolver para evaluar
            else:
                # si esta en los operadores logicos
                if i == '=':  # si es igual =
                    cad_eval += '=='  # concateno ==
                elif i == 'and' or i == 'or':
                    cad_eval += ' ' + i + ' '  # si es and u or concateno espacios y en medio la operacio
                    # si no hago esto queda la cadena pegada y no se puede evaluar
                else:
                    cad_eval += i  # en otro caso simplemente concateno el operador
        # print(cad_eval)

        return cad_eval  # devuelvo la cadena lista para ser evaluada

    # -------------------------------------------------------------------------------------------------
    #   metodo que crea las funciones indicadas en los algoritmos del usuario
    # -------------------------------------------------------------------------------------------------
    def crear_funciones(self,valor, variables,padre=0):


        # valor
        # ('sumar', 'True,&i&,&sumpar&')
        variables_funcion = {}  # variables que le pasaremos a la funcion
        funcion_temp = ()
        nombre_funcion = valor[0]  # Obtenemos el nombre de la funcion
        #si es una funcion reservada del lenguaje
        if nombre_funcion.upper() in self.funciones_reservadas:

            parametros_pasados = valor[1]

            if nombre_funcion == 'GET_P':
                pila = ''

                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                # print(lista_parametros)


                # Recordar optimizar
                if len(lista_parametros) == 1:
                    if lista_parametros[0].find('&') != -1:  # si la encontro es porque es una variable
                        temp_var_name = lista_parametros[0].replace("&", "")  # quitamos el ampersand
                        if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                            temp_var = variables[temp_var_name]  # entonces la sacamos

                            tipo_var = temp_var[0]

                            if (tipo_var == 'STACK'):  # ees porque es el primer parametro
                                pila = temp_var[1]


                            else:
                                print(
                                    "Error semantico, no se puede realizar una operacion de obtener sin remover STACK en una variable diferente a una STACK",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener sin remover STACK en una variable diferente a una STACK" + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:
                            print(
                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                            self.limpiar_variables()
                            exit(1)

                    else:
                        print(
                            "Error semantico, no se puede realizar una operacion de operacion de obtener sin remover en un escalar " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede realizar una operacion de operacion de obtener sin remover en un escalar " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # termino el for
                    # encolamos
                    if (len(pila) == 0):
                        print(
                            "Error semantico, no se puede obtener sin remover sobre una pila vacia " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede obtener sin remover sobre una pila vacia " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)
                    else:
                        retorno = pila.pop()  # sacamos
                        pila.append(retorno)  # ingresamos nuevamente por la izquierda
                        retorno = eval(retorno)  # y retornamos
                        return retorno

                else:
                    print(
                        "Error sintaxicosemantico, la funcion obtener sin remover STACK solo recive la pila",
                        file=sys.stderr)

                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion obtener sin remover STACK solo recive la pila" + spanb)
                    self.limpiar_variables()
                    exit(1)

            elif nombre_funcion == 'POP':
                pila = ''

                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                # print(lista_parametros)


                # Recordar optimizar
                if len(lista_parametros) == 1:
                    if lista_parametros[0].find('&') != -1:  # si la encontro es porque es una variable
                        temp_var_name = lista_parametros[0].replace("&", "")  # quitamos el ampersand
                        if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                            temp_var = variables[temp_var_name]  # entonces la sacamos

                            tipo_var = temp_var[0]

                            if (tipo_var == 'STACK'):  # ees porque es el primer parametro
                                pila = temp_var[1]


                            else:
                                print(
                                    "Error semantico, no se puede realizar una operacion de pop en una variable diferente a una STACK",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no se puede realizar una operacion de pop en una variable diferente a una STACK" + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:
                            print(
                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                            self.limpiar_variables()
                            exit(1)

                    else:
                        print(
                            "Error semantico, no se puede realizar una operacion de operacion de pop en un escalar " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede realizar una operacion de operacion de pop en un escalar " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # termino el for
                    # encolamos
                    if (len(pila) == 0):
                        print(
                            "Error semantico, no se puede pop sobre una pila vacia " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede pop sobre una pila vacia " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)
                    else:
                        retorno = pila.pop()  # sacamos
                        return eval(retorno)

                else:
                    print(
                        "Error sintaxicosemantico, la funcion pop solo recive la pila",
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion pop solo recive la pila" + spanb)
                    self.limpiar_variables()
                    exit(1)


            elif nombre_funcion == 'DEQUEUE':
                cola = ''

                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                # print(lista_parametros)


                # Recordar optimizar
                if len(lista_parametros) == 1:
                    if lista_parametros[0].find('&') != -1:  # si la encontro es porque es una variable
                        temp_var_name = lista_parametros[0].replace("&", "")  # quitamos el ampersand
                        if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                            temp_var = variables[temp_var_name]  # entonces la sacamos

                            tipo_var = temp_var[0]

                            if (tipo_var == 'QUEUE'):  # ees porque es el primer parametro
                                cola = temp_var[1]


                            else:
                                print(
                                    "Error semantico, no se puede realizar una operacion de deseencolar en una variable diferente a una QUEUE",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no se puede realizar una operacion de deseencolar en una variable diferente a una QUEUE" + spanb)
                                exit(1)
                        else:
                            print(
                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                            self.limpiar_variables()
                            exit(1)

                    else:
                        print(
                            "Error semantico, eno se puede realizar una operacion de desencolar en un escalar " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, eno se puede realizar una operacion de desencolar en un escalar " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # termino el for
                    # encolamos
                    if (len(cola) == 0):
                        print(
                            "Error semantico, no se puede desencolar sobre una cola vacia " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede desencolar sobre una cola vacia " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)
                    else:
                        retorno = cola.popleft()  # recordar mirar lo que hemos encolado
                        retorno = eval(retorno)
                        return retorno

                else:
                    print(
                        "Error sintaxicosemantico, la funcion desencolar solo recive dos parametros, la cola y el valor a encolar ",
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion desencolar solo recive dos parametros, la cola y el valor a encolar " + spanb)
                    self.limpiar_variables()
                    exit(1)


            elif nombre_funcion == 'GET_Q':
                cola = ''

                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                # print(lista_parametros)


                # Recordar optimizar
                if len(lista_parametros) == 1:
                    if lista_parametros[0].find('&') != -1:  # si la encontro es porque es una variable
                        temp_var_name = lista_parametros[0].replace("&", "")  # quitamos el ampersand
                        if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                            temp_var = variables[temp_var_name]  # entonces la sacamos

                            tipo_var = temp_var[0]

                            if (tipo_var == 'QUEUE'):  # ees porque es el primer parametro
                                cola = temp_var[1]


                            else:
                                print(
                                    "Error semantico, no se puede realizar una operacion de obtener sin remover QUEUE en una variable diferente a una QUEUE",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener sin remover QUEUE en una variable diferente a una QUEUE" + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:
                            print(
                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                            self.limpiar_variables()
                            exit(1)

                    else:
                        print(
                            "Error semantico, no se puede realizar una operacion de operacion de obtener sin remover en un escalar " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede realizar una operacion de operacion de obtener sin remover en un escalar " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # termino el for
                    # encolamos
                    if (len(cola) == 0):
                        print(
                            "Error semantico, no se puede obtener sin remover QUEUE sobre una cola vacia " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede obtener sin remover QUEUE sobre una cola vacia " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)
                    else:
                        retorno = cola.popleft()  # sacamos
                        cola.appendleft(retorno)  # ingresamos nuevamente por la izquierda
                        retorno = eval(retorno)  # y retornamos
                        return retorno

                else:
                    print(
                        "Error sintaxicosemantico, la funcion obtener sin remover solo recive la cola",
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion obtener sin remover solo recive la cola" + spanb)
                    self.limpiar_variables()
                    exit(1)

            elif nombre_funcion == 'SIZE_QUEUE':
                cola = ''

                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                # print(lista_parametros)


                # Recordar optimizar
                if len(lista_parametros) == 1:
                    if lista_parametros[0].find('&') != -1:  # si la encontro es porque es una variable
                        temp_var_name = lista_parametros[0].replace("&", "")  # quitamos el ampersand
                        if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                            temp_var = variables[temp_var_name]  # entonces la sacamos

                            tipo_var = temp_var[0]

                            if (tipo_var == 'QUEUE'):  # ees porque es el primer parametro
                                cola = temp_var[1]

                            else:
                                print(
                                    "Error semantico, no se puede realizar una operacion de obtener longitud de cola en una variable diferente a una QUEUE",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener longitud de cola en una variable diferente a una QUEUE" + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:
                            print(
                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                            self.limpiar_variables()
                            exit(1)

                    else:
                        print(
                            "Error semantico, eno se puede realizar una operacion de obtener longitud de cola sobre un escalar " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener longitud de cola sobre un escalar " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # termino el for
                    # encolamos
                    return len(cola)

                else:
                    print(
                        "Error sintaxicosemantico, la funcion tamaño de cola solo recive la cola ",
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion tamaño de cola solo recive la cola " + spanb)
                    self.limpiar_variables()
                    exit(1)
            elif nombre_funcion == 'SIZE_STACK':
                pila = ''

                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                # print(lista_parametros)


                # Recordar optimizar
                if len(lista_parametros) == 1:
                    if lista_parametros[0].find('&') != -1:  # si la encontro es porque es una variable
                        temp_var_name = lista_parametros[0].replace("&", "")  # quitamos el ampersand
                        if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                            temp_var = variables[temp_var_name]  # entonces la sacamos

                            tipo_var = temp_var[0]

                            if (tipo_var == 'STACK'):  # ees porque es el primer parametro
                                pila = temp_var[1]

                            else:
                                print(
                                    "Error semantico, no se puede realizar una operacion de obtener longitud de pila en una variable diferente a una STACK",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener longitud de pila en una variable diferente a una STACK" + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:
                            print(
                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                            self.limpiar_variables()
                            exit(1)

                    else:
                        print(
                            "Error semantico, eno se puede realizar una operacion de obtener longitud de pila sobre un escalar " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, eno se puede realizar una operacion de obtener longitud de pila sobre un escalar " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # termino el for
                    # encolamos
                    return len(pila)

                else:
                    print(
                        "Error sintaxicosemantico, la funcion tamaño de pila solo recive la pila ",
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion tamaño de pila solo recive la pila " + spanb)
                    self.limpiar_variables()
                    exit(1)
            elif nombre_funcion == 'SIZE':
                lista_arreglo = ''

                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                # print(lista_parametros)


                # Recordar optimizar
                if len(lista_parametros) == 1:
                    if lista_parametros[0].find('&') != -1:  # si la encontro es porque es una variable
                        temp_var_name = lista_parametros[0].replace("&", "")  # quitamos el ampersand
                        if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                            temp_var = variables[temp_var_name]  # entonces la sacamos

                            if (type(temp_var[0]) == tuple):  # porque puede ser un arreglo
                                tipo_var = 'ARRAY'
                            else:
                                tipo_var = temp_var[0]

                            if (tipo_var == 'LIST' or tipo_var == 'ARRAY'):  # ees porque es el primer parametro
                                lista_arreglo = temp_var[1]

                            else:
                                print(
                                    "Error semantico, no se puede realizar una operacion de obtener longitud  en una variable diferente a una LIST o un ARRAY",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener longitud  en una variable diferente a una LIST o un ARRAY" + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:
                            print(
                                "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                            self.limpiar_variables()
                            exit(1)

                    else:
                        print(
                            "Error semantico, eno se puede realizar una operacion de obtener longitud sobre un escalar " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, eno se puede realizar una operacion de obtener longitud sobre un escalar " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                    # termino el for
                    # encolamos
                    return len(lista_arreglo)

                else:
                    print(
                        "Error sintaxicosemantico, la funcion tamaño de LIST o ARRAY solo recive la lista o el arreglo ",
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion tamaño de LIST o ARRAY solo recive la lista o el arreglo " + spanb)
                    self.limpiar_variables()
                    exit(1)
            elif nombre_funcion == 'GET':
                lista = ''
                valor_indice = ''
                lista_parametros = parametros_pasados.split(",")
                # print(lista_parametros)
                if len(lista_parametros) == 2:
                    indice = 0
                    for m in range(0, len(lista_parametros)):
                        if lista_parametros[m].find('&') != -1:  # si la encontro es porque es una variable
                            temp_var_name = lista_parametros[m].replace("&", "")  # quitamos el ampersand
                            if temp_var_name in variables.keys():  # si esta en la tabla de variables de contexto
                                temp_var = variables[temp_var_name]  # entonces la sacamos

                                tipo_var = temp_var[0]

                                if (tipo_var == 'LIST' and indice == 0):  # ees porque es el primer parametro
                                    lista = temp_var[1]
                                elif indice == 1:  # esporque es el segundo parametro
                                    if (tipo_var != 'INTEGER'):
                                        print(
                                            "Error semantico, no se puede realizar una operacion de obtener, con un indice diferente a un INTEGER ",
                                            file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener, con un indice diferente a un INTEGER " + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                    else:
                                        valor_indice = temp_var[1]

                                else:
                                    print(
                                        "Error semantico, no se puede realizar una operacion get en una variable diferente a una LIST",
                                        file=sys.stderr)
                                    self.terminal.append(
                                        spanh_rojo + "Error semantico, no se puede realizar una operacion get en una variable diferente a una LIST" + spanb)
                                    self.limpiar_variables()
                                    exit(1)
                            else:
                                print(
                                    "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion,
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de este procedimiento " + nombre_funcion + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:

                            if (indice == 0):
                                print(
                                    "Error semantico, se esperaba una variable de tipo LIST, no un escalar",
                                    file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, se esperaba una variable de tipo LIST, no un escalar" + spanb)
                                self.limpiar_variables()
                                exit(1)
                            else:
                                if (type(eval(lista_parametros[m])) != int):
                                    print(
                                        "Error semantico, no se puede realizar una operacion de obtener, con un indice diferente a un INTEGER ",
                                        file=sys.stderr)
                                    self.terminal.append(
                                        spanh_rojo + "Error semantico, no se puede realizar una operacion de obtener, con un indice diferente a un INTEGER " + spanb)
                                    self.limpiar_variables()
                                    exit(1)
                                else:
                                    valor_indice = int(lista_parametros[m])
                        indice += 1

                    # termino el for
                    try:
                        retorno = eval(lista[valor_indice])  # adicionamos
                        return retorno
                    except IndexError as e:
                        print(
                            "Error semantico, esa posicion no existe en la lista " + str(e),
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, esa posicion no existe en la lista " + str(e) + spanb)
                        self.limpiar_variables()
                        exit(1)
                else:
                    print(
                        "Error sintaxicosemantico, la funcion get de LIST de la lista no tiene el numero de parametros correctos ",
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error sintaxicosemantico, la funcion get de LIST de la lista no tiene el numero de parametros correctos" + spanb)
                    self.limpiar_variables()
                    exit(1)


        #sino, es una funcion creada por el usuario
        elif nombre_funcion in self.funciones.keys():
            self.ambientes += 1
            x = self.ambientes

            #print("agrego ambiente",self.arbolito.add2(x, padre,"Funcion :" +str(nombre_funcion)))
            #print("Ambiente : ",x," Padre :",padre)

            parametros_pasados = valor[1]

            funcion_temp = self.funciones[nombre_funcion]  # obtenemos la funcion

            # print(funcion_temp)

            parametros_esperado = funcion_temp[0]

            parametros_esperado = parametros_esperado.split('-')

            parametros_esperado_organizado = []
            for n in parametros_esperado:
                temp_p = n.split(',')
                parametros_esperado_organizado.append(temp_p)

            # print(parametros_esperado_organizado)

            # [['E', 'INTEGER', 'n1'], ['E', 'INTEGER', 'n2'], ['ES', 'INTEGER', 'n3']]
            tabla_funcion = funcion_temp[1]
            lista_parametros = parametros_pasados.split(",")
            for m in range(0, len(lista_parametros)):
                if lista_parametros[m].find('&') != -1:
                    temp_var_name = lista_parametros[m].replace("&", "")
                    if temp_var_name in variables.keys():
                        temp_var = variables[temp_var_name]
                        if parametros_esperado_organizado[m][0] == 'E':  # sacamos el tipo de parametros que recibe
                            nombre_variable = parametros_esperado_organizado[m][2]
                            tipo_variable = parametros_esperado_organizado[m][1]

                            if temp_var[0] == tipo_variable:
                                if temp_var[0] not in self.tipos_lenguaje.values():  # si es una estructura de datos
                                    print(
                                        "!!!!!!!!Advertencia, los tipos de estrucutras de datos se pasan por referencia si o si")
                                    self.terminal.append(
                                        spanh_amarillo + "!!!!!!!!Advertencia, los tipos de estrucutras de datos se pasan por referencia si o si" + spanb)

                                # variables[i] = [tipo, valor]
                                variables_funcion[nombre_variable] = [tipo_variable,
                                                                      temp_var[1]]  # enviamos la variable


                            else:
                                print(
                                    "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                    + " y se encontro con " + str(temp_var[0]), file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                    + " y se encontro con " + str(temp_var[0]) + spanb)
                                self.limpiar_variables()
                                exit(1)

                        else:  # por referencia
                            nombre_variable = parametros_esperado_organizado[m][2]
                            tipo_variable = parametros_esperado_organizado[m][1]

                            if temp_var[0] == tipo_variable:
                                variables_funcion[nombre_variable] = temp_var  # enviamos la variable

                            else:
                                print(
                                    "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                    + " y se encontro con " + str(temp_var[0]), file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                    + " y se encontro con " + str(temp_var[0]) + spanb)
                                self.limpiar_variables()
                                exit(1)

                    else:
                        print(
                            "Error semantico, esta variable no esta definida en el alcance de esta funcion " + nombre_funcion,
                            file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, esta variable no esta definida en el alcance de esta funcion " + nombre_funcion + spanb)
                        self.limpiar_variables()
                        exit(1)

                else:
                    if parametros_esperado_organizado[m][0] == 'E':
                        variable_pasada = lista_parametros[m]
                        try:
                            variable_pasada = eval(variable_pasada)
                            nombre_variable = parametros_esperado_organizado[m][2]
                            tipo_variable = parametros_esperado_organizado[m][1]
                            if (type(variable_pasada) in self.tipos_lenguaje.keys()):
                                tipo_variable_pasada = self.tipos_lenguaje[type(variable_pasada)]
                                if (tipo_variable_pasada == tipo_variable):
                                    variables_funcion[nombre_variable] = [tipo_variable,
                                                                          variable_pasada]  # creamos una variable
                                else:
                                    print(
                                        "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                        + " y se encontro con " + str(variable_pasada), file=sys.stderr)
                                    self.terminal.append(
                                        spanh_rojo + "Error semantico, se esperaba un parametro de tipo  " + tipo_variable + " en el parametro " + nombre_variable
                                        + " y se encontro con " + str(variable_pasada) + spanb)
                                    self.limpiar_variables()
                                    exit(1)
                        except Exception as e:
                            print(
                                "Error semantico, no se permite este tipo de parametros en la funcion " + nombre_funcion + " " + variable_pasada + " " + str(
                                    e), file=sys.stderr)
                            self.terminal.append(
                                spanh_rojo + "Error semantico, no se permite este tipo de parametros en la funcion " + nombre_funcion + " " + variable_pasada + " " + str(
                                    e) + spanb)
                            self.limpiar_variables()
                            exit(1)
                    else:
                        print("Error semantico, un escalar no se puede pasar por referencia ", file=sys.stderr)
                        self.terminal.append(
                            spanh_rojo + "Error semantico, un escalar no se puede pasar por referencia " + spanb)
                        self.limpiar_variables()
                        exit(1)
            # print(funcion_temp[1])
            #print(funcion_temp)
            print("agrego ambiente", self.arbolito.add2(self.ambientes, padre, "Funcion : " + str(
                nombre_funcion) + "\nParametros pasados " + str(variables_funcion)))

            print("Ambiente : ", self.ambientes, " Padre : ", padre)
            retorno = self.run(funcion_temp[1], variables_funcion,self.ambientes)
            # print(variables_funcion)

            return retorno
        else:
            print("Error semantico, la funcion  " + nombre_funcion + " no esta definida", file=sys.stderr)
            self.terminal.append(spanh_rojo + "Error semantico, la funcion  " + nombre_funcion + " no esta definida" + spanb)
            self.limpiar_variables()
            exit(1)

    # para organizar el valor, si es all ise indica una variable y cambiarlo por el valor de dicha variable
    # -------------------------------------------------------------------------------------------------
    #   metodo que organiza el valor de las variables del algoritmo, es decir cambiar el id de la variable
    #   por su respectivo valor evaluado
    # -------------------------------------------------------------------------------------------------
    def organizar_valor(self,valor, variables,padre = 0):
        # print(valor)
        #si es una tupla entonces se esta asignando una funcion
        if type(valor) == tuple:

            return self.crear_funciones(valor, variables, padre)

        else:
            valor_return = ''
            try:  # si ahi algun probmea con eval retornamos un error

                valor_return = eval(valor)

                # print(valor_return)
                return valor_return
            except Exception as e:
                valor_temp = valor
                i = 0
                tipo = ''
                while i < len(valor):
                    if (valor[i] == '&'):
                        temp_pos = ''  # aqui guardaremos lo que reemplazaremos luego en la cadena
                        temp_pos += valor[i]
                        variable_temp = ''
                        j = i + 1
                        while valor[j] != '&':
                            temp_pos += valor[j]
                            j = j + 1
                        temp_pos += valor[j]
                        variable_temp = temp_pos.replace("&", "")  # quitamos los anpersant
                        i = i + j + 1
                        if variable_temp.find("[") != -1:

                            variable_temp = variable_temp.replace("]", "")  # si es un arreglo quitamos ]
                            list_variable = variable_temp.split("[")  # como nos queda [ espliteamos por ese
                            var_name = list_variable[0]
                            indice = int(list_variable[1])

                            if var_name in variables.keys():
                                var = variables[var_name]
                                tipo = var[0][0]
                                tamano = var[0][1]
                                valor_lista = var[1]

                                if (indice < tamano):
                                    if (tipo in ("STRING", "INTEGER", "DOUBLE")):

                                        valor_temp = valor_temp.replace(temp_pos, str(valor_lista[indice]))
                                    else:
                                        print("Error semantico, operacion no permitida con este tipo de datos " + tipo,
                                              file=sys.stderr)
                                        self.terminal.append(
                                            spanh_rojo + "Error semantico, operacion no permitida con este tipo de datos " + tipo + spanb)
                                        self.limpiar_variables()
                                        exit(1)
                                else:
                                    print("Error semantico, se desbordo el arreglo " + var_name, file=sys.stderr)
                                    self.terminal.append(
                                        spanh_rojo + "Error semantico, se desbordo el arreglo " + var_name + spanb)
                                    self.limpiar_variables()
                                    exit(1)
                            else:
                                print("Error semantico, no existe esta variable" + var_name, file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no existe esta variable" + var_name + spanb)
                                self.limpiar_variables()
                                exit(1)
                        else:  # es porque es una variable normnal
                            var_name = variable_temp
                            if var_name in variables.keys():
                                var = variables[var_name]
                                tipo = var[0]
                                if (tipo in ("INTEGER", "DOUBLE")):

                                    valor_var = var[1]
                                    valor_temp = valor_temp.replace(temp_pos, str(valor_var))
                                elif tipo == "STRING":
                                    valor_var = var[1]
                                    valor_var = "\"" + valor_var + "\""  # le concatenamos las comillas para que no tengamos problemas al operarlo con eval
                                    valor_temp = valor_temp.replace(temp_pos, str(valor_var))

                                else:
                                    print("Error semantico, operacion no permitida con este tipo de datos " + tipo,
                                          file=sys.stderr)
                                    self.terminal.append(
                                        spanh_rojo + "Error semantico, operacion no permitida con este tipo de datos " + tipo + spanb)
                                    self.limpiar_variables()
                                    exit(1)
                            else:
                                print("Error semantico, no existe esta variable " + var_name, file=sys.stderr)
                                self.terminal.append(
                                    spanh_rojo + "Error semantico, no existe esta variable " + var_name + spanb)
                                self.limpiar_variables()
                                exit(1)

                    else:
                        i = i + 1

                try:  # si ahi algun probmea con eval retornamos un error
                    valor_return = eval(valor_temp)

                except Exception as e:
                    print(
                        "Error semantico, no se puede realizar esta operacion compruebe los tipos que esta pasando " + valor_temp,
                        file=sys.stderr)
                    self.terminal.append(
                        spanh_rojo + "Error semantico, no se puede realizar esta operacion compruebe los tipos que esta pasando " + valor_temp + spanb)
                    self.limpiar_variables()
                    exit(1)
                # print(valor_temp)
                # print(valor_return)
                # print(type(valor_return))
                return valor_return


    def p_bloque(self,p):
        'bloque : BEGIN bloqueContenido END'
        p[0] = p[2]

    def p_bloqueFuncion(self,p):
        'bloqueFuncion : BEGIN bloqueContenido retorno END'
        p[0] = [p[2], p[3],p.lineno(1)]

    def p_retorno_valor(self,p):
        'retorno : RETURN valor PUNTOCOMA'
        p[0] = ('retorno', p[2], p.lineno(1))

    def p_bloqueContenido_si(self,p):
        'bloqueContenido : si bloqueContenido'
        p[0] = (('si', p[1]), p[2], p.lineno(1))
        # print(p.lineno(1))

    def p_bloqueContenido_para(self,p):
        'bloqueContenido : para bloqueContenido'
        p[0] = (('para', p[1]), p[2], p.lineno(1))

    def p_bloqueContenido_mientras(self,p):
        'bloqueContenido : mientras bloqueContenido'
        p[0] = (('mientras', p[1]), p[2], p.lineno(1))

    def p_bloqueContenido_repeat(self,p):
        'bloqueContenido : repetir bloqueContenido'
        p[0] = (('repetir', p[1]), p[2], p[1][2])  # para que empieze desde el until

    def p_bloqueContenido_escribir(self,p):
        'bloqueContenido : escribir bloqueContenido'
        p[0] = (('escribir', p[1]), p[2], p.lineno(1))

    def p_bloqueContenido_asignar(self,p):
        'bloqueContenido : asignar bloqueContenido'
        p[0] = (('asignar', p[1]), p[2], p.lineno(1))

    def p_bloqueContenido_llamar_procedure(self,p):
        'bloqueContenido : llamarProcedure  bloqueContenido'
        p[0] = (('llamarProcedimiento', p[1]), p[2], p.lineno(1))

    def p_bloqueContenido_empty(self,p):
        'bloqueContenido : empty'
        p[0] = 'omitaBloque'

    def p_escribir(self,p):
        'escribir : WRITELN PA par PC PUNTOCOMA'
        p[0] = p[3]

    def p_para(self,p):
        'para : FOR ID ASIGNACION toFor TO toFor DO bloque'
        p[0] = (p[2], p[4], p[6], p[8])

    def p_to_for_id(self,p):
        'toFor : ID'
        p[0] = "&" + str(p[1]) + "&"

    def p_to_for_integer(self,p):
        'toFor : INTEGERVAL'
        p[0] = str(p[1])

    def p_mientras(self,p):
        'mientras : WHILE PA condicion PC DO bloque'
        p[0] = (p[3], p[6])

    def p_repetir(self,p):
        'repetir : REPEAT bloqueContenido UNTIL PA condicion PC'
        p[0] = (p[5], p[2], p.lineno(3))

    def p_si(self,p):
        'si : IF PA condicion PC THEN bloque sino'
        p[0] = (p[3], p[6], p[7])

    def p_sino_bloq(self,p):
        'sino : ELSE bloque'
        p[0] = p[2]

    def p_sino_empty(self,p):
        'sino : empty'
        p[0] = 'omitaSino'

    # NO SE NECESITA POR EL MOMENTO HACER ALGO SEMANTICO AQUI TAL VEZ

    def p_declaracionPrincipal(self,p):
        'declaracionPrincipal : VAR  declaracion especiales'

    def p_especiales_registro(self,p):
        'especiales : registro especiales'

    def p_especiales_funcion(self,p):
        'especiales : funcion especiales'

    def p_especiales_procedimiento(self,p):
        'especiales : procedimiento especiales'

    def p_parametros_mdoval_id(self,p):
        'parametros : MODOVALOR tipo ID'
        if p[2] == 'ARRAY':
            print("Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista",
                  file=sys.stderr)
            self.terminal.append(
                spanh_rojo + "Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista" + spanb)
            exit(-1)
        p[0] = p[1] + "," + p[2] + "," + p[3]

    def p_parametros_mdoref_id(self,p):
        'parametros : MODOREFERENCIA tipo ID'
        if p[2] == 'ARRAY':
            print("Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista",
                  file=sys.stderr)
            self.terminal.append(
                spanh_rojo + "Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista" + spanb)
            self.limpiar_variables()
            exit(-1)
        p[0] = p[1] + "," + p[2] + "," + p[3]

    def p_parametros_mdoval_id_parm(self,p):
        'parametros : MODOVALOR tipo ID COMA parametros'
        if p[2] == 'ARRAY':
            print("Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista",
                  file=sys.stderr)
            self.terminal.append(
                spanh_rojo + "Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista" + spanb)
            self.limpiar_variables()
            exit(-1)
        p[0] = p[1] + "," + p[2] + "," + p[3] + "-" + p[5]

    def p_parametros_mdoref_id_parm(self,p):
        'parametros : MODOREFERENCIA tipo ID COMA parametros'
        if p[2] == 'ARRAY':
            print("Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista",
                  file=sys.stderr)
            self.terminal.append(
                spanh_rojo + "Erros semantico, no se permiten arreglos como parametros de una funcion, en su lugar use una lista" + spanb)
            self.limpiar_variables()
            exit(-1)
        p[0] = p[1] + "," + p[2] + "," + p[3] + "-" + p[5]

    def p_funcion(self,p):
        'funcion : FUNCTION ID PA parametros PC bloqueFuncion'
        valor_id = p[2]

        if valor_id in self.variables_globales.keys() or valor_id in self.funciones.keys() or valor_id in self.procedimientos or valor_id in self.registros:
            print("Error semantico, usted ya uso este identificador " + valor_id, file=sys.stderr)
            self.terminal.append(spanh_rojo + "Error semantico, usted ya uso este identificador " + valor_id + spanb)
        else:
            self.funciones[valor_id] = (p[4], p[6], p.lineno(1))

    def p_procedimiento(self,p):
        'procedimiento : PROCEDURE ID PA parametros PC bloque'
        valor_id = p[2]

        if valor_id in self.variables_globales.keys() or valor_id in self.funciones.keys() or valor_id in self.procedimientos or valor_id in self.registros:
            print("Error semantico, usted ya uso este identificador " + valor_id, file=sys.stderr)
            self.terminal.append(spanh_rojo + "Error semantico, usted ya uso este identificador " + valor_id + spanb)
        else:
            self.procedimientos[valor_id] = (p[4], p[6], p.lineno(1))

    def p_registro_declar(self,p):
        'registro : RECORD ID BEGIN declaracionReg END'
        valor_id = p[2]

        if valor_id in self.variables_globales.keys() or valor_id in self.funciones.keys() or valor_id in self.procedimientos or valor_id in self.registros:
            print("Error semantico, usted ya uso este identificador " + valor_id, file=sys.stderr)
            self.terminal.append(spanh_rojo + "Error semantico, usted ya uso este identificador " + valor_id + spanb)
        else:
            self.registros[valor_id] = p[4]

    def p_declaracionreg_variablereg(self,p):
        'declaracionReg : variableReg declaracionReg'
        if (p[2] != None):
            p[0] = p[1] + "-" + p[2]
        else:
            p[0] = p[1]

    def p_declaracionreg_empty(self,p):
        'declaracionReg : empty'

    def p_variablereg_tipo(self,p):
        'variableReg : nombresV DOSPUNTOS tipo PUNTOCOMA'
        nombres = p[1] + ":" + p[3]

        p[0] = nombres

    def p_variablereg_array(self,p):
        'variableReg : nombresV DOSPUNTOS tipo ARRAY PUNTOCOMA'
        nombres = p[1] + ":" + p[3] + ",ARRAY"
        p[0] = nombres

    def p_declaracion_variable(self,p):
        'declaracion : variable declaracion'

    def p_declaracion_empty(self,p):
        'declaracion : empty'

    # -------------------------------------------------------------------------------------------------
    #       gramatica para declaracion de varias variables
    # -------------------------------------------------------------------------------------------------
    def p_variable_tipo(self,p):
        'variable : nombresV DOSPUNTOS tipo PUNTOCOMA'
        list_variables = p[1].split(",")
        for i in list_variables:
            if i in self.variables_globales:  # recorremos solo las llaves
                print("Error semantico, ya definio previamente la variable " + i, file=sys.stderr)
                self.terminal.append(spanh_rojo + "Error semantico, ya definio previamente la variable " + i + spanb)
                self.limpiar_variables()
                exit(1)
            else:
                valor_defect = 0
                if p[3] == 'BOOLEAN':
                    valor_defect = False
                elif p[3] == 'INTEGER':
                    valor_defect = 0
                elif p[3] == 'STRING':
                    valor_defect = ""
                elif p[3] == 'DOUBLE':
                    valor_defect = 0.0
                elif p[3] == 'LIST' or p[3] == 'STACK':
                    valor_defect = []
                    # recordar que se usa es como una pila, o lista pero depende de lcaso
                    # https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks
                elif p[3] == 'QUEUE':
                    valor_defect = queue.deque()

                elif p[3] == 'GRAPH':
                    valor_defect = nx.Graph()  # creamos un grafo

                    # http://networkx.readthedocs.io/en/networkx-1.11/reference/introduction.html

                self.variables_globales[i] = [p[3],
                                         valor_defect]  # guardamos la varaible, donde tenemos el tipo, y el valor p[3] es el tipo

    def p_variable_array(self,p):
        'variable : nombresV DOSPUNTOS tipo ARRAY PUNTOCOMA'
        list_variables = p[1].split(",")
        for i in list_variables:
            if i in self.variables_globales:  # recorremos solo las llaves
                print("Error semantico, ya definidio previamente la variable " + i, file=sys.stderr)
                self.terminal.append(spanh_rojo + "Error semantico, ya definidio previamente la variable " + i + spanb)
                self.limpiar_variables()
                exit(1)
            else:
                p[4] = p[4].replace("[", "")
                p[4] = p[4].replace("]", "")
                p[4] = int(p[4])  # indice

                arreglo = []
                for j in range(0, p[4]):
                    arreglo.append(0)
                self.variables_globales[i] = [(p[3], p[4]), arreglo]
                # guardamos la varaible, donde tenemos el tipo, y el valor p[3] es el tipo
                # En este caso tenemos que tener cuidado de si lo que ahi dentro es una tupla o no

    def p_nombresV_id(self,p):
        'nombresV : ID'
        p[0] = p[1]

    def p_nombresV_nom(self,p):
        'nombresV : ID COMA nombresV'
        p[0] = p[1] + "," + p[3]

    def p_tipo_integer(self,p):
        'tipo : INTEGER'
        p[0] = p[1]

    def p_tipo_double(self,p):
        'tipo : DOUBLE'
        p[0] = p[1]

    def p_tipo_string(self,p):
        'tipo : STRING'
        p[0] = p[1]

    def p_tipo_boolean(self,p):
        'tipo : BOOLEAN'
        p[0] = p[1]

    def p_tipo_array(self,p):
        'tipo : ARRAY'
        p[0] = p[1]

    def p_tipo_stack(self,p):
        'tipo : STACK'
        p[0] = p[1]

    def p_tipo_queue(self,p):
        'tipo : QUEUE'
        p[0] = p[1]

    def p_tipo_list(self,p):
        'tipo : LIST'
        p[0] = p[1]

    def p_tipo_graph(self,p):
        'tipo : GRAPH'
        p[0] = p[1]

    def p_tipo_id(self,p):  # una variable es de tipo registro
        'tipo : ID'
        p[0] = p[1]

    def p_especiales_empty(self,p):
        'especiales : empty'

    def p_asignar_arregloIdOp(self,p):
        'asignar : arregloID ASIGNACION operacion PUNTOCOMA'
        p[0] = (p[1], p[3])

    def p_asignar_arreglofunction(self,p):
        'asignar : arregloID ASIGNACION llamarFunction PUNTOCOMA'
        p[0] = (p[1], p[3])

    def p_asignar_arregloIdNull(self,p):
        'asignar : arregloID ASIGNACION NULL PUNTOCOMA'
        p[0] = (p[1], 'NULL')

    def p_asignar_record(self,p):
        'asignar : asignacionRecord'
        p[0] = p[1]

    def p_asignacion_record_oper(self,p):
        'asignacionRecord : idRecord ASIGNACION operacion PUNTOCOMA'
        p[0] = (p[1], p[3])

    def p_idRecord_rec(self,p):
        'idRecord : ID PUNTO idRecord2'
        p[0] = p[1] + "." + p[3]

    def p_idRecord2_ID(self,p):
        'idRecord2 : ID'
        p[0] = p[1]

    def p_arregloID_id(self,p):
        'arregloID : ID'
        p[0] = p[1]

    def p_arregloID_array(self,p):
        'arregloID : ID ARRAY'
        var_name = p[1]

        p[2] = p[2].replace("[", "")  # organizamos los valores dentro del arreglo, para obtener el indice
        p[2] = p[2].replace("]", "")
        p[2] = int(p[2])
        indice = p[2]  # sacamos el indice al que se le va asignar algo en el arreglo

        p[0] = (var_name, indice)  # retornamos el indice con la variable

    def p_operacion_par(self,p):
        'operacion : par'
        p[0] = p[1]

    def p_operacion_subarray(self,p):
        'operacion : SUBARRAY'
        p[0] = p[1]

    def p_par_opmath(self,p):
        'par : opmath'
        p[0] = p[1]

    def p_par_parAux(self,p):
        'par : PA par PC parAux'

        p[0] = '(' + str(p[2]) + ')' + str(p[4])

    def p_parAux_mathsymbol(self,p):
        'parAux : mathsymbol par'
        p[0] = p[1] + p[2]

    def p_parAux_empty(self,p):
        'parAux : empty'
        p[0] = ''

    def p_condicion(self,p):
        'condicion : negacion par comparar par continuidad'
        if (p[1] != None):
            if (p[5] != None):
                p[0] = p[1] + "," + p[2] + "," + p[3] + "," + p[4] + "," + p[5]
            else:
                p[0] = p[1] + "," + p[2] + "," + p[3] + "," + p[4]
        else:
            if (p[5] != None):
                p[0] = p[2] + "," + p[3] + "," + p[4] + "," + p[5]
            else:
                p[0] = p[2] + "," + p[3] + "," + p[4]

    def p_continuidad_condicion(self,p):
        'continuidad : oplogico condicion'
        p[0] = p[1] + ',' + p[2]

    def p_continuidad_empty(self,p):
        'continuidad : empty'

    def p_comparar_mayor(self,p):
        'comparar : MAYOR'
        p[0] = '>'

    def p_comparar_menor(self,p):
        'comparar : MENOR'
        p[0] = '<'

    def p_comparar_mayor_igual(self,p):
        'comparar : MAYORIGUAL'
        p[0] = '>='

    def p_comparar_menor_igual(self,p):
        'comparar : MENORIGUAL'
        p[0] = '<='

    def p_comparar_igual(self,p):
        'comparar : IGUAL'
        p[0] = '='

    def p_comparar_diferente(self,p):
        'comparar : DIFERENTE'
        p[0] = '!='

    def p_oplogico_and(self,p):
        'oplogico : AND'
        p[0] = 'and'

    def p_oplogico_or(self,p):
        'oplogico : OR'
        p[0] = 'or'

    def p_negacion_not(self,p):
        'negacion : NOT'
        p[0] = 'not'

    def p_negacion_empty(self,p):
        'negacion : empty'

    def p_opmath_valor(self,p):
        'opmath : valor'
        p[0] = str(p[1])

    def p_opmath_mathsymbol(self,p):
        'opmath : valor mathsymbol par'

        p[0] = str(p[1]) + p[2] + str(p[3])

    def p_mathsymbol_mas(self,p):
        'mathsymbol : MAS'
        p[0] = '+'

    def p_mathsymbol_menos(self,p):
        'mathsymbol : MENOS'
        p[0] = '-'

    def p_mathsymbol_por(self,p):
        'mathsymbol : POR'
        p[0] = '*'

    def p_mathsymbol_dividir(self,p):
        'mathsymbol : DIVIDIR'
        p[0] = '/'

    def p_mathsymbol_div(self,p):
        'mathsymbol : DIV'
        p[0] = '//'

    def p_mathsymbol_mod(self,p):
        'mathsymbol : MOD'
        p[0] = '%'

    def p_techo(self,p):
        'techo : CEIL PA opmath PC'
        p[0] = "math.ceil(" + p[3] + ")"

    def p_piso(self,p):
        'piso : FLOOR PA opmath PC'
        p[0] = "math.floor(" + p[3] + ")"

    def p_valor_arregloid(self,p):
        'valor : arregloID'
        if type(p[1]) == tuple:

            p[0] = "&" + str(p[1][0]) + "[" + str(p[1][1]) + "]&"
        else:
            p[0] = "&" + str(p[1]) + "&"

    def p_valor_integerval(self,p):
        'valor : INTEGERVAL'
        p[0] = p[1]

    def p_valor_doubleval(self,p):
        'valor : DOUBLEVAL'
        p[0] = p[1]

    def p_valor_stringval(self,p):
        'valor : STRINGVAL'
        p[0] = p[1]

    def p_valor_true(self,p):
        'valor : TRUE'
        p[0] = True

    def p_valor_false(self,p):
        'valor : FALSE'
        p[0] = False

    def p_valor_techo(self,p):
        'valor : techo'
        p[0] = p[1]

    def p_valor_piso(self,p):
        'valor : piso'
        p[0] = p[1]

    def p_valor_longitud(self,p):
        'valor : longitud'
        p[0] = p[1]

    def p_valor_conversion_cad(self,p):
        'valor : conversionCad'
        p[0] = p[1]

    def p_conversion_cad(self,p):
        'conversionCad : STR PA opmath PC'
        p[0] = "str(" + p[3] + ")"

    def p_longitud(self,p):
        'longitud : LENGTH PA STRINGVAL PC'
        # p[3] = p[3].replace("\"","")
        p[0] = "" + str(len(p[3]))

    def p_llamar_procedure_valoresCall(self,p):
        'llamarProcedure : CALL PROCEDURE ID PA valoresCall PC PUNTOCOMA'
        p[0] = (p[3], p[5])  # si es una tupla es porque es un llamado a una funcion

    def p_llamar_procedure_vacio(self,p):
        'llamarProcedure : CALL PROCEDURE ID PA error PC PUNTOCOMA'
        print(
            "Errror de Sintaxis, los procedimientos necesitan parametros ya que estos actuan como las variables usadas en el procedimiento",
            file=sys.stderr)
        self.terminal.append(
            spanh_rojo + "Errror de Sintaxis, los procedimientos necesitan parametros ya que estos actuan como las variables usadas en el procedimiento" + spanb)
        self.limpiar_variables()
        exit(1)

    def p_llamar_function_valoresCall(self,p):
        'llamarFunction : CALL FUNCTION ID PA valoresCall PC'
        p[0] = (p[3], p[5])  # si es una tupla es porque es un llamado a una funcion

    def p_llamar_function_vacio_error(self,p):
        'llamarFunction : CALL FUNCTION ID PA error PC'
        print(
            "Errror de Sintaxis, las funciones necesitan parametros ya que estos actuan como las variables usadas en la funcion",
            file=sys.stderr)
        self.terminal.append(
            spanh_rojo + "Errror de Sintaxis, las funciones necesitan parametros ya que estos actuan como las variables usadas en la funcion" + spanb)
        self.limpiar_variables()
        exit(1)

    def p_valoresCall_valor(self,p):
        'valoresCall : valor'
        if (str(p[1]).find("[") != -1):
            print(
                "Errror de Sintaxis, no es permitido pasar arreglos, con llamado a indice como parametro ",
                file=sys.stderr)
            self.terminal.append(
                spanh_rojo + "Errror de Sintaxis, no es permitido pasar arreglos, con llamado a indice como parametro " + spanb)
            self.limpiar_variables()
            exit(1)
        else:
            p[0] = str(p[1])

    def p_valoresCall_varios(self,p):
        'valoresCall : valor COMA valoresCall'
        if (str(p[1]).find("[") != -1):
            print(
                "Errror de Sintaxis, no es permitido pasar arreglos, con llamado a indice como parametro ",
                file=sys.stderr)
            self.terminal.append(
                spanh_rojo + "Errror de Sintaxis, no es permitido pasar arreglos, con llamado a indice como parametro " + spanb)
            self.limpiar_variables()
            exit(1)
        else:
            p[0] = str(p[1]) + "," + p[3]

    def p_empty(self,p):
        'empty : '
        pass

    def p_longitud_error(self,p):
        'longitud : LENGTH PA error PC'
        print("Tipo de dato invalido, se esperaba una cadena", file=sys.stderr)
        self.terminal.append(spanh_rojo + "Tipo de dato invalido, se esperaba una cadena" + spanb)

    def p_error(self,p):
        if (p != None):
            print("Errror de Sintaxis en la linea " + str(p.lineno) + " en el token " + str(p.value), file=sys.stderr)
            self.terminal.append(
                spanh_rojo + "Errror de Sintaxis en la linea " + str(p.lineno) + " en el token " + str(p.value) + spanb)
        else:
            print("Errror de Sintaxis", file=sys.stderr)
            self.terminal.append(spanh_rojo + "Errror de Sintaxis" + spanb)
        self.limpiar_variables()
        exit(1)

    # def close():
    #    pass



    # -------------------------------------------------------------------------------------------------
    #       metodo para hacer el inicia el analisis sintactico que a su vez invoca el
    #       analisis semantico mediante el metodo run
    # -------------------------------------------------------------------------------------------------
    def analizar(self,texto,lineas):

        for i in lineas:
            self.lineas_marcadas[i+1] = 0



        self.lexer.build()
        self.parser.parse(texto, tracking=True, lexer= self.lexer.lexer)

    # -------------------------------------------------------------------------------------------------
    #       metodo que inicializa el modulo ply.yacc para realizar los analisis
    #           sintactico y semantico
    # -------------------------------------------------------------------------------------------------
    def construir_parser(self):
        self.parser = yacc.yacc(module=self)

        # parser.parse(datos, tracking=True)

    # -------------------------------------------------------------------------------------------------
    #       metodo que limpia las variables para posteriores ejecuciones
    # -------------------------------------------------------------------------------------------------
    def limpiar_variables(self,):
        self.avanzar = False
        self.variables_globales = {}
        self.variables_actuales = None
        self.funciones = {}
        self.procedimientos = {}
        self.registros = {}
        self.detener = False
        self.lineas_marcadas = {}
        self.ambiente_actual = 0
        self.contador += 1
        self.tiempito = 0
        self.ambientes = 0
        self.arbolito = n_ary_tree()

