from PyQt5.QtWidgets import QStatusBar, QLabel

# -------------------------------------------------------------------------------------------------
#   clase StatusBar : -> hereda de QStatusBar
#           contiene la posicion del cursor en el editor
# -------------------------------------------------------------------------------------------------
class StatusBar(QStatusBar):
    # -------------------------------------------------------------------------------------------------
    #       constructor del status bar, inicialmente en la posicion 0,0
    # -------------------------------------------------------------------------------------------------
    def __init__(self):
        super(StatusBar, self).__init__()

        self.posicion_cursor = "Linea: %s, Columna: %s"
        self.linea_columna=QLabel(self.posicion_cursor % (0,0))
        self.addWidget(self.linea_columna)

    # -------------------------------------------------------------------------------------------------
    #       metodo para actualizar el label de la posicion del cursor
    # -------------------------------------------------------------------------------------------------
    def actualizar_label(self,linea,columna):
        self.linea_columna.setText(self.posicion_cursor % (linea,columna))
