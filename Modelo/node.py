from PyQt5.QtCore import QRect


# -------------------------------------------------------------------------------------------------
#       clase node:
#           representacion de un ambiente
# -------------------------------------------------------------------------------------------------
class node:
    # -------------------------------------------------------------------------------------------------
    #   constructor de la clase node:
    #           recibe:
    #               data -> nombre o numero del ambiente
    #               info -> contenido o nombre del procedimiento o funcion
    # -------------------------------------------------------------------------------------------------
    def __init__(self,data,info):
        self.data = data
        self.x = 0
        self.y = 0
        self.tam = 20
        self.activo = False             #variable para saber si el ambiente esta activo
        self.info = info
        self.childrens = []
        self.listita = []
        self.rect = QRect(self.x,self.y,self.tam,self.tam)  #rect para saber si se clickeo sobre el ambiente

    # -------------------------------------------------------------------------------------------------
    #      metodo que añade un hijo al nodo
    # -------------------------------------------------------------------------------------------------
    def add(self,node):
        self.childrens.append(node)

    # -------------------------------------------------------------------------------------------------
    #   metod que retorna el numero de hijos del nodo
    # -------------------------------------------------------------------------------------------------
    def get_grade(self):
        return len(self.childrens)

    # -------------------------------------------------------------------------------------------------
    #   metodo que dice si el nodo es una hoja
    # -------------------------------------------------------------------------------------------------
    def is_leaf(self):
        return len(self.childrens) == 0

    # -------------------------------------------------------------------------------------------------
    #   metodo publico que llama al imprimir arbol
    # -------------------------------------------------------------------------------------------------
    def print_tree(self):
        self.__print_tree("",True)

    # -------------------------------------------------------------------------------------------------
    #   metodo que imprime el arbol
    #           el parametro prefix es para identar y dar espacio entre el hijo y el padre
    #           el parametro isTail es para saber si es el ultimo hijo del nodo
    # -------------------------------------------------------------------------------------------------
    def __print_tree(self,prefix,isTail):

        x =  "└── " if isTail else "├── "

        print(prefix + x +str(self.data))

        pos = len(self.childrens) - 1

        x = "    " if isTail else "│   "

        for i in range(0,pos):
            self.childrens[i].__print_tree(prefix+x,False)

        if len(self.childrens)>0:
            self.childrens[pos].__print_tree(prefix+x,True)


