from Modelo.node import *

# -------------------------------------------------------------------------------------------------
#       clase n_ary_tree:
#           necesaria para el arbol de entornos
#           contiene la raiz: primer ambiente del arbol
# -------------------------------------------------------------------------------------------------

class n_ary_tree:

    # -------------------------------------------------------------------------------------------------
    #       constructor de la clase n_ary_tree
    # -------------------------------------------------------------------------------------------------
    def __init__(self):
        self.root = None    #raiz de arbol (primer ambiente)


    # -------------------------------------------------------------------------------------------------
    #       metodo para cambiar la raiz del arbol, en el aplicativo no se usa
    # -------------------------------------------------------------------------------------------------
    def set_root(self,root):
        self.root = root

    # -------------------------------------------------------------------------------------------------
    #       metodo para obtener la raiz del arbol
    # -------------------------------------------------------------------------------------------------
    def get_root(self):
        return self.root

    # -------------------------------------------------------------------------------------------------
    #       metodo para añadir por primera vez -> anadir raiz
    #       o para añadir hijos a la raiz
    # -------------------------------------------------------------------------------------------------
    def add1(self,element,info):
        temp = node(element,info)
        if self.root == None:
            self.set_root(temp)
        else:
            self.get_root().add(temp,info)


    # -------------------------------------------------------------------------------------------------
    #       metodo para añadir hijos a un padre especifico
    # -------------------------------------------------------------------------------------------------
    def add2(self,element,parent,info):
        if self.get_root() == None: return False

        temp = self.find(parent,self.get_root())

        if temp != None:
            t = node(element,info)
            temp.add(t)
            return True

        return False

    # -------------------------------------------------------------------------------------------------
    #       metod para encontrar un elemento en el arbol
    # -------------------------------------------------------------------------------------------------
    def find(self,element,tree):
        if tree == None:
            return None

        if tree.data == element:
            return tree

        for i in tree.childrens:
            ref = self.find(element,i)
            if ref != None:
                return ref
        return None

    # -------------------------------------------------------------------------------------------------
    #       metodo publico para imprimir el arbol, con un recorrido preorden
    # -------------------------------------------------------------------------------------------------
    def pre_orden(self):
        return self.__pre_orden(self.get_root())

    # -------------------------------------------------------------------------------------------------
    #     metodo para imprimir el recorrido preorden del arbol
    # -------------------------------------------------------------------------------------------------
    def __pre_orden(self,tree):
        if(tree != None):
            x = tree.data+ " "
            for i in tree.childrens:
                x+= self.__pre_orden(i)
            return x

        return ""