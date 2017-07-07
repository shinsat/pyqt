import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}

class MyDelegate(QItemDelegate):

    def __init__(self, parent, table):
        super(MyDelegate, self).__init__(parent)
        self.table = table

    def sizeHint(self, option, index):
        # Get full viewport size
        table_size = self.table.viewport().size()
        gw = 1  # Grid line width
        rows = self.table.rowCount() or 1
        cols = self.table.columnCount() or 1
        width = (table_size.width() - (gw * (cols - 1))) / cols
        height = (table_size.height() -  (gw * (rows - 1))) / rows
        return QSize(width, height)


class MyTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        f = QFont()
        f.setPointSize(7)
        self.setFont(f)
        #{self.setRowHeight(i, 1) for i in range(5)}
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.setShowGrid(False)
#        self.horizontalHeader().setSectionResizeMode(1)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.setFixedSize(self.sizeHint())
        #vb = QVBoxLayout(self)
        #self.setLayout(vb)
#        mydel = MyDelegate(self, self)
#        self.setItemDelegate(mydel)
    '''
    def sizeHint(self):
        horizontal = self.horizontalHeader()
        vertical = self.verticalHeader()
        frame = self.frameWidth() * 2
        return QSize(horizontal.length() + vertical.width() + frame,
                     vertical.length() + horizontal.height() + frame)
    '''


    def setmydata(self):

        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)

        self.setHorizontalHeaderLabels(horHeaders)

def main(args):
    app = QApplication(args)
    table = MyTable(data, 15, 3)
    table.setGeometry(100, 100, 150, 250)

    table.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)