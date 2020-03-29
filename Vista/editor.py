import sys
from PyQt5.QtGui import QFont, QFontMetrics, QColor
from PyQt5.Qsci import QsciScintilla, QsciAPIs, QsciLexerPascal
from Modelo.lexclass import *

#CLASE DEL EDITOR
#QUE HEREDA DE LA LIB O CLASE QsciScintilla


# -------------------------------------------------------------------------------------------------
#       class editor: hereda de -> QsciScintilla
#           contiene todo lo realcionado con el editor de codigo
# -------------------------------------------------------------------------------------------------
class editor(QsciScintilla):
    #CONSTANTE QUE PERMITE MOSTRAR ICONO
    #DE LINEA MARCADA SI ES -1 NO SE MUESTRA EL ICONO
    ARROW_MARKER_NUM = 1
    
    #CONSTRUCTOR DE LA CLASE
    # -------------------------------------------------------------------------------------------------
    #       constructor de la clase
    # -------------------------------------------------------------------------------------------------
    def __init__(self,parent=None):
        #CONSTRUCTOR DE LA CLASE HEREDADA
        super(editor,self).__init__(parent)
        
        #DEFINICION DE LA FUENTE Y SUS PROPIEDADES
        font = QFont()
        #font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        self.lineas_marcadas = []
        
        #PROFIEDADES AVANZADAS DE LA FUENTE DEL EDITOR
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        #SE CAMBIA EL MARGEN ANCHO DE LA FUNETE 
        self.setMarginWidth(0,fontmetrics.width("00000")-15)
        #MARGEN DE LOS NUMEROS DE LINEA
        self.setMarginLineNumbers(0,True)
        #COLOR DE FONDO DE LOS NUMEROS DE LINEA
        self.setMarginsBackgroundColor(QColor("#E0E0E0"))
        
        self.setMarginSensitivity(1,True)
        
        #CREAMOS LA SEÑA PARA AGREGAR LINEA MARCADA
        self.marginClicked.connect(self.on_margin_clicked)

        #SE DEFINE EL ICONO A MOSTRAR EN LA LINEA MARCADA
        self.markerDefine(QsciScintilla.Circle ,
            self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#FF6C3B"),
            self.ARROW_MARKER_NUM)
        
        #RESALTADO DE PARENTECIS,CORCHETES Y OTROS
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        
        #RESALTADO DE LA LINEA DONDE SE ENCUENTRA EL CURSOR
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#32f24c"))
        
        #AUTOIDENTACION
        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(True)
        self.setIndentationWidth(4)
        
        #DEFINIMOS EL RESALTADO O LEXER
        self.lexer = QsciLexerPascal()
        self.lexer.setDefaultFont(font)#FUENTE DEL LEXER
        
        #API PARA EL AUTOCOMPETADO
        api = QsciAPIs(self.lexer)
        self.palabraAutocompletar(api)
        api.prepare()
        
        self.cambiarColores()
        self.setLexer(self.lexer)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        
        #ESCONDER SCROLLBAR HORIZONTAL
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        #TAMAÑO MINIMO DEL EDITOR
        self.setMinimumSize(600, 360)
        

    # -------------------------------------------------------------------------------------------------
    #           metodo para marcar las lineas-> asignar breackpoints
    # -------------------------------------------------------------------------------------------------
    def on_margin_clicked(self, nmargin, nline, modifiers):
        #SI LA LINEA YA ESTA MARCADA SE BORRA DE LAS
        #LINEAS MARACADAS, SI NO, SE ADICIONA
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM) # se agrega el breackpoint al editor para visualizarlo
            if self.lineas_marcadas.__contains__(nline):
                self.lineas_marcadas.remove(nline)#se agrega el breackpoint al aplicativo
        else:
            #se desmarca el breackpoint
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
            if not self.lineas_marcadas.__contains__(nline):
                self .lineas_marcadas.append(nline)

    # -------------------------------------------------------------------------------------------------
    #       metodo que inicializa la api, con el contenido de los tokens de la clase Lexico
    #       para el autocompletado del editor
    # -------------------------------------------------------------------------------------------------
    def palabraAutocompletar(self,api):
        lex = Lexico()
        palabras = lex.getpalbras()
        for i in palabras:
            api.add(i)

    # -------------------------------------------------------------------------------------------------
    #      metodo que asigna los colores para las palabras y caracteres reservados
    # -------------------------------------------------------------------------------------------------
    def cambiarColores(self):
        self.lexer.setColor(QColor('#F44336'), QsciLexerPascal.Number)
        self.lexer.setColor(QColor('#34495e'), QsciLexerPascal.Keyword)
        self.lexer.setColor(QColor('#42A5F5'), QsciLexerPascal.SingleQuotedString)
        self.lexer.setColor(QColor('#F06292'), QsciLexerPascal.Operator)
        self.lexer.setColor(QColor('#3498db'), QsciLexerPascal.Character)

    # -------------------------------------------------------------------------------------------------
    #       metodo para obtener la posicion del cursor
    # -------------------------------------------------------------------------------------------------
    def getPosicion(self):
        return self.getCursorPosition()

    # -------------------------------------------------------------------------------------------------
    #       metod para cambiar la posicion del cursor
    # -------------------------------------------------------------------------------------------------
    def set_posicion(self):
        pos = self.getPosicion()
        self.setCursorPosition(pos[0],pos[1])

    # -------------------------------------------------------------------------------------------------
    #       metodo para obtener las lineas marcadas del editor
    # -------------------------------------------------------------------------------------------------
    def getMarcadas(self):
        return self.lineas_marcadas
        
        
