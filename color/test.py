
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys
from PyQt5.QtGui import QColor

class Widget(QtWidgets.QWidget):

    def __init__(self):
        #super(Widget, self).__init__()
        QtWidgets.QWidget.__init__(self)

        self.resize(300,200)
        layout = QtWidgets.QVBoxLayout(self)

        color1 = QtGui.QColor(255, 0, 0)
        color2 = QtGui.QColor(0, 255, 0)

        self.label = QtWidgets.QLabel("Some sample text")
        font = self.label.font()
        font.setPointSize(20)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton("Start", self)
        layout.addWidget(self.button)

        self.animation = anim = QtCore.QPropertyAnimation(self, b'color')
        anim.setDuration(250)
        anim.setLoopCount(2)
        anim.setStartValue(self.color)
        anim.setEndValue(self.color)
        anim.setKeyValueAt(0.5, QtGui.QColor(0,255,0))

        self.button.clicked.connect(anim.start)

    def getColor(self):
        return self.label.palette().text().color()

    def setColor(self, color):
        palette = self.label.palette()
        palette.setColor(self.label.foregroundRole(), color)
        self.label.setPalette(palette)

#    color = QtCore.pyqtProperty(Qt.QColor, getColor, setColor)
    color = QtCore.pyqtProperty(QtGui.QColor, getColor, setColor)


class AnimatedWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        color1 = QtGui.QColor(255, 0, 0)
        color2 = QtGui.QColor(0, 255, 0)

        self.color_anim = QtCore.QPropertyAnimation(self, b'backColor')
        self.color_anim.setStartValue(color1)
        self.color_anim.setKeyValueAt(0.5, color2)
        self.color_anim.setEndValue(color1)
        self.color_anim.setDuration(1000)
        self.color_anim.setLoopCount(1)
        self.color_anim.start()

    def getBackColor(self):
        return self.palette().color(QtGui.QPalette.Background)

    def setBackColor(self, color):
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Background, color)
        self.setPalette(pal)

    backColor = QtCore.pyqtProperty(QtGui.QColor, getBackColor, setBackColor)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = Widget()
    #w = AnimatedWidget()
    w.show()
    app.exec_()