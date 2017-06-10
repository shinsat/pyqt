import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import time

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

def run(loop):
  nc = NATS()

  yield from nc.connect(io_loop=loop)

  @asyncio.coroutine
  def message_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print("Received a message on '{subject} {reply}': {data}".format(
      subject=subject, reply=reply, data=data))

  time.sleep(10)
  # Simple publisher and async subscriber via coroutine.
  sid = yield from nc.subscribe("foo", cb=message_handler)

  # Stop receiving after 2 messages.
  yield from nc.auto_unsubscribe(sid, 2)
  yield from nc.publish("foo", b'Hello')
  yield from nc.publish("foo", b'World')
  yield from nc.publish("foo", b'!!!!!')

  @asyncio.coroutine
  def help_request(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print("Received a message on '{subject} {reply}': {data}".format(
      subject=subject, reply=reply, data=data))
    yield from nc.publish(reply, b'I can help')

  # Use queue named 'workers' for distributing requests
  # among subscribers.
  yield from nc.subscribe("help", "workers", help_request)

  # Send a request and expect a single response
  # and trigger timeout if not faster than 50 ms.
  try:
    response = yield from nc.timed_request("help", b'help me', 0.050)
    print("Received response: {message}".format(message=response.data.decode()))
  except ErrTimeout:
    print("Request timed out")

  yield from asyncio.sleep(1, loop=loop)
  yield from nc.close()

class Model(QAbstractItemModel):
    headers = 'ID','記事','分類器2','分類器2','分類器3'
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = [
            ['1','ニュース１','0.5','0.1','0.6'],
            ['2', 'ニュース2', '0.5', '0.1', '0.6'],
            ['3', 'ニュース3', '0.5', '0.1', '0.6'],
            ['4', 'ニュース4', '0.5', '0.1', '0.6'],
            ['5', 'ニュース5', '0.5', '0.1', '0.6'],
        ]

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row,column,None)

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

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role != Qt.DisplayRole:
            return
        if Qt_Orientation == Qt.Horizontal:
            return self.headers[p_int]

    def removeRows(self, rowIndexes):
        for row in sorted(rowIndexes, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row + 1)
            del self.items[row]
            self.endRemoveRows()

    def addRow(self, id, title, res1, res2, res3):
        self.beginInsertRows(QModelIndex(), len(self.items),1)
        self.items.append([id,title,res1,res2,res3])
        self.endInsertRows()


class Me(QMainWindow):
    def __init__(self):
        #self.nc = NATS()

        #self.nc.connect()

        '''
        try:
            yield from nc.connect()
        except:
            pass
        '''

        super().__init__()
        self.ui = loadUi('ms_main.ui', self)
        self.model = Model(self)
        self.ui.lv_news.setModel(self.model)
        #self.setCentralWidget(ui)

        self.ui.lv_news.setItemsExpandable(False)
        self.ui.lv_news.setIndentation(0)
        self.ui.lv_news.setSelectionMode(QAbstractItemView.ExtendedSelection)

        toolBar = QToolBar()
        self.addToolBar(toolBar)

        delButton = QPushButton('削除')
        delButton.clicked.connect(self.removeItems)
        toolBar.addWidget(delButton)

        addButton = QPushButton('追加')
        addButton.clicked.connect(self.rcv_nats)
        toolBar.addWidget(addButton)

        self.addToolBar(toolBar)

    def rcv_nats(self):
        print('nats')
        #response = yield from self.nc.timed_request("foo", b'help me', 0.050)
        print('Hi')
        #print(response)
        #print("Received response: {message}".format(message=response.data.decode()))
        self.model.addRow('999','added item', '0.1','0.2','0.3')

    def selectedRows(self):
        rows = []
        for index in self.ui.lv_news.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        return rows

    def removeItems(self):
        self.model.removeRows(self.selectedRows())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = Me()
    my_window.show()
    my_window.raise_()

#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(run(loop))


    app.exec_()

#    loop.close()
    sys.exit(0)