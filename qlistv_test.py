import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *


class TestListModel(QAbstractListModel):
    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.list = parent

    def rowCount(self, index):
        return 1000

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if not self.list.indexWidget(index):
#                button = QPushButton("This is item #%s" % index.row())
                button = loadUi('ms_item.ui')
                self.list.setIndexWidget(index, button)
            return QVariant()

        if role == Qt.SizeHintRole:
            return QSize(100, 50)

    def columnCount(self, index):
        pass


def main():
    app = QApplication(sys.argv)

    window = QWidget()

    list = QListView()
    model = TestListModel(list)

    list.setModel(model)
    list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    layout = QVBoxLayout(window)
    layout.addWidget(list)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()