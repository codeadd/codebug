from Modelo.colores import *
import Vista.editor as ed
from Vista.arbol_view import *

#CLASE QUE CONTIENE UN WIDGET
#CON EL EDITOR Y UN TEXEDIT PARA SIMULAR UNA TERMINAL

# -------------------------------------------------------------------------------------------------
#       clase Widget : -> hereda de QWidget
#               contiene los elementos graficos mas importantes del aplicativo
#               editor
#               terminal
#               area de estado
#               area de dibujo de los ambientes
# -------------------------------------------------------------------------------------------------

class widget(QWidget):

    # -------------------------------------------------------------------------------------------------
    #       constructor de la clase widget
    # -------------------------------------------------------------------------------------------------
    def __init__(self, parent=None):
        QWidget.__init__(self) #CONSTRUCTOR HEREDADO
        
        self.editor = ed.editor()       #editor
        self.terminal = QTextEdit()     #terminal del aplicativo
        self.estado = QTextEdit()       #area de estado de las variables del aplicativo
        self.terminal.setReadOnly(True) #hacemos la terminal en modo solo lectura
        self.terminal.append(spanh+"Terminal v0.1 >>>"+spanb)
        self.estado.setReadOnly(True)   #hacemos el area de estado en modo solo lectura
        self.estado.append(spanh+'Estado Variables >>>'+spanb)
        font = QFont('Arial')           #fuente que se utilizara para el area de estado y la terminal
        font.setPointSize(8)
        font.setBold(True)
        self.estado.setFont(font)
        font.setPointSize(10)
        self.terminal.setFont(font)

        self.grafico = panel()          #area de dibujo del arbol de ambientes


        layoutG = QHBoxLayout()         #layout general de tipo horizontal
        
        layouth =QVBoxLayout()          #layout para los elementos del lado derecho del aplicativo (area de estado y area de dibujo)
                                        # de tipo vertical
        layouth.addWidget(self.estado)
        layouth.addWidget(self.grafico)

        #self.estado.hide()


        layout = QVBoxLayout()          #layout para los elementos del lado izquierdo del aplicativo (editor y teminal)
                                        #de tipo vertical
        layout.addWidget(self.editor)
        layout.addStretch()
        layout.addWidget(self.terminal)
        layout.addStretch()
        layoutG.addLayout(layout)
        layoutG.addLayout(layouth)
        layoutG.setAlignment(Qt.AlignHCenter)
        self.setLayout(layoutG) #se asigna el layout general como layout del widget principal
