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
    headers = 'トッピング', 'うどん/そば', '温/冷'


    def addRow(self):
        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        self.items.append(['A', 'B', 'C'])
        self.endInsertRows()

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
        elif role == Qt.TextAlignmentRole:              #<---ここ
            return Qt.AlignCenter | Qt.AlignVCenter

        return

    def just_update(self):
        self.items[1][2] = 'HoOh'

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        view = QTreeView(self)
        h = view.header()
        h.setDefaultAlignment(Qt.AlignCenter)       #<---ここ
#        view.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
#        view = QTableView(self)
        #view.resizeRowsToContents()
        #view.verticalHeader().setDefaultSectionSize(view.rowHeight(10))
        #view.verticalHeader().setDefaultSectionSize(15)

        model = Model(self)
        view.setModel(model)
        self.setCentralWidget(view)
        model.addRow()
        model.just_update()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.raise_()
    app.exec_()

if __name__ == '__main__':
    main()