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

        self.parent = parent

    headers = 'トッピング', 'うどん/そば', '温/冷'

    def addRow2(self):
        self.beginInsertRows(self.createIndex(1, 1), len(self.items), len(self.items))

        self.w = QWidget()

        self.hbox = QHBoxLayout()
        self.pb = QPushButton('Bt')
        self.hbox.addWidget(self.pb)
        self.pb2 = QPushButton('Bt2')
        self.hbox.addWidget(self.pb2)
        self.pb3 = QPushButton('Bt3')
        self.hbox.addWidget(self.pb3)

        self.w.setLayout(self.hbox)
        self.items.append(['X', 'XX', self.w])

        self.endInsertRows()


    def addRow(self):
#        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        self.beginInsertRows(self.createIndex(1, 1), len(self.items), len(self.items))
        #adding = ['a', 'b', 'c']
        #effect = QGraphicsColorizeEffect(adding)
        #color_anim = QPropertyAnimation(adding, 'background-color')
        #self.color_anim.setStartValue(QColor(255, 0, 0))
        #self.color_anim.setKeyValueAt(0.5, QColor(0, 255, 0))
        #self.color_anim.setEndValue(QColor(255, 0, 0))

        self.w = QWidget()
        self.hbox = QHBoxLayout()
        self.pb = QPushButton('Bt')
        self.hbox.addWidget(self.pb)
        self.w.setLayout(self.hbox)
        #self.items.append(['A', 'B', 'C'])
        self.items.append(['A', 'B', self.w])
        self.endInsertRows()

        #ttt = self.items[1][1]
        #effect = QGraphicsColorizeEffect(self.items[1][1])

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
                if index.row() == 4 and index.column() == 2:
                    self.parent.view.setIndexWidget(index, self.items[index.row()][index.column()])

                    return QVariant()
                elif index.row() == 5 and index.column() == 2:
                    self.parent.view.setIndexWidget(index, self.items[index.row()][index.column()])

                    return QVariant()
                else:
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

    def insertRows(self, position=0, count=1, parent=QModelIndex()):
        """Insert `count` rows after the given row."""

        node = self.nodeFromIndex(parent)
        self.beginInsertRows(parent, position, position + count - 1)
        node.insertChild(['BBB', 'cc'], position)
        self.endInsertRows()
        return True


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.view = QTreeView(self)
        #self.view.setItemsExpandable(False)
        self.view.setIndentation(1)

        h = self.view.header()
        h.setDefaultAlignment(Qt.AlignCenter)       #<---ここ
#        view.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
#        view = QTableView(self)
        #view.resizeRowsToContents()
        #view.verticalHeader().setDefaultSectionSize(view.rowHeight(10))
        #view.verticalHeader().setDefaultSectionSize(15)

        self.view.doubleClicked.connect(self.double_clicked_item)

        model = Model(self)
        self.view.setModel(model)
        self.setCentralWidget(self.view)
        model.addRow()
        model.addRow2()

#model.insertRows()
        model.just_update()

    def double_clicked_item(self):
#        index = self.view.selectedIndexes()
#        id_us = self.view.model().item(index.row(), index.column())
#        print("index : " + id_us)
        pass




def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.raise_()
    app.exec_()

if __name__ == '__main__':
    main()