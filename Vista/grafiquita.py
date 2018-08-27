import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import numpy as np


# -------------------------------------------------------------------------------------------------
#        clase grafiquita:
#               diccionario de ejecuciones
#               diccionario de breakpoints
# -------------------------------------------------------------------------------------------------
class grafiquita():

    # -------------------------------------------------------------------------------------------------
    #           constructor de la clase
    #           recibe -> diccionario(tiempos) , breackpoints(breackpoinst del editor)
    # -------------------------------------------------------------------------------------------------
    def __init__(self,diccionario,breackpoints):
        self.ejecuciones = list(diccionario.keys())     #se extrae las ejecuciones hechas
        posicion_y = np.arange(len(self.ejecuciones))   #se asigna un arreglo de posiciones en y para la grafica 1


        self.tiempos = list(diccionario.values())       #se extrae los valores de los tiempos del primer diccionario en una lista
        self.breacks = list(breackpoints.values())      #se extrae los valores de los breackpoins del segundo diccionario en una lista

        plt.style.use("ggplot")                         #se asigna un estilo a las graficas


        plt.subplot(1,2,1)                                      #se asigna espacio(en la ventana) para la primera grafica
        plt.barh(posicion_y, self.tiempos, align="center")      #se crea un grafico de barras
        plt.yticks(posicion_y, self.ejecuciones)                #rangos de x y y para la grafica
        plt.xlabel("Tiempos")                                   # label descriptivo para x
        plt.title("Tiempos de Ejecucion")                       # titulo de la grafica


        plt.subplot(1,2,2)                                      #se asigna espacion(en la ventana) para la segunda grafica

        plt.title("Tiempos de Ejecución Teoricos")              #titulo de la grafica 2

        plt.xlabel("Tiempos Reales")                            #label x de la grafica 2
        plt.ylabel("Tiempos Teoricos")                          #label y de la grafica 2

        x = np.array(self.tiempos)                              #rangos en x para grafica 2
        y = np.array(self.breacks)                              #rangos en y para grafica 2

        plt.plot(x,y)                                           #se grafican los puntos para cada x[i],y[i]

        plt.show()                                              #se muestra la grafica
