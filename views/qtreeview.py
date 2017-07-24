import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(MyModel, self).__init__(parent)
        self.get_contents()

    def get_contents(self):
        self.clear()
        contents=["path1","path2"]
        for path in contents:
            date = self.get_date(path)
            self.add_item(path,date)

    def add_item(self,name,date):
        item1 = QStandardItem(name)
        item2 = QStandardItem(date)
        self.appendRow([item1, item2])
        #to append child items
        childItem = QStandardItem("child")
        item1.appendRow(childItem)

    def get_date(self, path):
        return "a date"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model=MyModel()
    treeView= QTreeView()
    treeView.setModel(model)
    model.setHorizontalHeaderLabels(["name","date"])
    treeView.show()
    sys.exit(app.exec_())