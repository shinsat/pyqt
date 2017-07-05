import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Model(QAbstractItemModel):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = [
            ['たぬき','そば','温'],
            ['きつね','うどん','温'],
            ['月見','うどん','冷'],
            ['天ぷら','そば','温'],
            ]

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, None)

    def parent(self, child):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        if self.items:
            return max([len(item) for item in self.items])
        return 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                return self.items[index.row()][index.column()]
            except:
                return None
        return

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        view = QTableView(self)
        #view.resizeRowsToContents()
        #view.verticalHeader().setDefaultSectionSize(view.rowHeight(10))
        view.verticalHeader().setDefaultSectionSize(15)

        model = Model(self)
        view.setModel(model)
        self.setCentralWidget(view)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.raise_()
    app.exec_()

if __name__ == '__main__':
    main()