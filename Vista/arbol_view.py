import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Modelo.n_ary_tree import *


# -------------------------------------------------------------------------------------------------
#       clase panel: -> hereda de QGraphicsView
#              clase que contiene lo referente al arbol de entornos y el panel de dibujo.
#               arbol de entornos
#               escena de dibujo
# -------------------------------------------------------------------------------------------------

class panel(QGraphicsView):

    def __init__(self):
        super(panel, self).__init__()

        self.arbolito = None        #arbol de entornos

        self.y = 50                 #posicion en y inicial
        self.escena = QGraphicsScene()  #escena de dibujo

        self.setScene(self.escena)  #asignamos la escena al QGraphicsView de la clase


    # -------------------------------------------------------------------------------------------------
    #           metodo que verifica cuando se hace click en la escena
    # -------------------------------------------------------------------------------------------------
    def mousePressEvent(self, event):
        print("clicked")
        x = event.pos().x()
        y = event.pos().y()
        print(x,y)
        pt = self.mapToScene(event.pos())       #se escala la posicion de click del QGraphicsView a la escena (QGraphicsScene)

        root = self.arbolito.get_root()         #raiz del arbol
        if(root!=None):
            rect = QRect(int(pt.x()), int(pt.y()), root.tam, root.tam)  # se crea un rectangulo para la colision con el nodo
            self.__colision(root,rect)


    # -------------------------------------------------------------------------------------------------
    #           metodo que verifica si el evento del click se realizo sobre algun nodo
    # -------------------------------------------------------------------------------------------------
    def __colision(self,nodo,rect):

        #si el nodo entrante fue el clickeado
        if nodo.rect.intersects(rect):

           #se muestra un mensaje
           #con la informacion del nodo-> nombre del procedimiento o funcion
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Information)

           msg.setText("Nombre Ambiente: "+str(nodo.info))
           msg.exec_()

           return True
        else:
            #si no se mira si se hizo el click en alguno de los hijos
            for i in nodo.childrens:
                self.__colision(i,rect)


    # -------------------------------------------------------------------------------------------------
    #       metodo que limpia la escena y llama al metodo de pintado del arbol
    # -------------------------------------------------------------------------------------------------
    def dibujar(self):

        #self.arbolito.get_root().print_tree()
        self.escena.clear()
        self.pintar()

    # -------------------------------------------------------------------------------------------------
    #       metodo publico que llama el pintado del arbol y sus lineas desde la razi
    # -------------------------------------------------------------------------------------------------
    def pintar(self):

        root = self.arbolito.get_root()
        self.y = 50
        self.__pintar_arbol(root,10,self.y)
        self.__lineas(root)


    # -------------------------------------------------------------------------------------------------
    #      metodo que pinta todos los nodos del arbol
    # -------------------------------------------------------------------------------------------------
    def __pintar_arbol(self,nodo,x,y):

        pen = QPen(Qt.black)        #lapiz de nodo normal
        pen2 = QPen(Qt.green)       #lapiz de nodo actual
        nodo.x = x                  #se asigna posicion x al nodo
        nodo.y = self.y             #se asigna posicion y al nodo

        nodo.rect = QRect(nodo.x,nodo.y,nodo.tam,nodo.tam)      # se crea un rectangulo para el nodo,para los eventos click

        #print("Pos x : ",nodo.x,"Pos y : ",nodo.y," Dato :",nodo.data," Info : ",nodo.info)

        xp = nodo.tam / 2
        #self.escena.addRect(nodo.rect,pen)
        if nodo.activo:
            self.escena.addEllipse(nodo.x, nodo.y, nodo.tam, nodo.tam, pen2)
        else:
            self.escena.addEllipse(nodo.x,nodo.y,nodo.tam,nodo.tam,pen)

        #texto del nodo
        text = QGraphicsTextItem(None, self.escena)
        text.setPlainText(str(nodo.data))
        text.setPos(QPointF(nodo.x + 2, nodo.y - 3))

        x += 50

        ##pintar los hijos
        for i in nodo.childrens:
            self.y += 40
            self.__pintar_arbol(i,x,self.y)



    # -------------------------------------------------------------------------------------------------
    #   metodo que pinta las lineas de relacion en el arbol
    # -------------------------------------------------------------------------------------------------
    def __lineas(self,nodo):

        pen = QPen(Qt.black)
        xp = nodo.tam / 2
        for i in nodo.childrens:
            xl1_a = nodo.x + nodo.tam + 5
            yl1_a = nodo.y + nodo.tam - 5

            ylb = i.y + xp
            self.escena.addLine(nodo.x + nodo.tam, yl1_a, xl1_a, yl1_a)
            self.escena.addLine(xl1_a, yl1_a, xl1_a, ylb, pen)
            self.escena.addLine(xl1_a, ylb, i.x, ylb, pen)
            self.__lineas(i)