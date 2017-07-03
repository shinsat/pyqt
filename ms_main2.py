import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import time
from threading import Thread

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
from quamash import QEventLoop, QThreadExecutor
from listener import Listener


def run(loop):
  nc = NATS()
  yield from nc.connect(io_loop=loop)

  @asyncio.coroutine
  def message_handler(msg):
    print('received something')
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print("Received a message on '{subject} {reply}': {data}".format(
      subject=subject, reply=reply, data=data))

  # Simple publisher and async subscriber via coroutine.
  sid = yield from nc.subscribe("foo", cb=message_handler)

  # Stop receiving after 2 messages.
  #yield from nc.auto_unsubscribe(sid, 2)
  #yield from nc.publish("foo", b'Hello')
  #yield from nc.publish("foo", b'World')
  #yield from nc.publish("foo", b'!!!!!')

  '''
  @asyncio.coroutine
  def help_request(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print("Received a message on '{subject} {reply}': {data}".format(
      subject=subject, reply=reply, data=data))
    yield from nc.publish(reply, b'I can help')
  '''
  # Use queue named 'workers' for distributing requests
  # among subscribers.
  #yield from nc.subscribe("help", "workers", help_request)

  # Send a request and expect a single response
  # and trigger timeout if not faster than 50 ms.
  #try:
  #  response = yield from nc.timed_request("help", b'help me', 10.050)
  #  print("Received response: {message}".format(message=response.data.decode()))
  #except ErrTimeout:
  #  print("Request timed out")

  yield from asyncio.sleep(1, loop=loop)
  #yield from nc.close()

class Component(object):

    def __init__(self, nc, loop):
        self.nc = nc
        self.loop = loop

    def response_handler(self, msg):
        print("--- Received: ", msg.subject, msg.data)

    @asyncio.coroutine
    def another_handler(self, msg):
        print("--- Another: ", msg.subject, msg.data, msg.reply)
        yield from self.nc.publish(msg.reply, b'I can help!')

    def run(self):
        yield from self.nc.connect(io_loop=self.loop)
        yield from self.nc.subscribe("hello", cb=self.response_handler)
        yield from self.nc.subscribe("another", cb=self.another_handler)
        yield from self.nc.flush()

def another_thread(c):
    # Should have ensured that we are connected by this point.
    if not c.nc.is_connected:
        print("Not connected to NATS!")
        return

    asyncio.run_coroutine_threadsafe(c.nc.subscribe("hi", cb=c.response_handler), loop=c.loop)
    asyncio.run_coroutine_threadsafe(c.nc.flush(), loop=c.loop)
    asyncio.run_coroutine_threadsafe(c.nc.publish("hello", b'world'), loop=c.loop)
    asyncio.run_coroutine_threadsafe(c.nc.publish("hi", b'example'), loop=c.loop)

    future = asyncio.run_coroutine_threadsafe(c.nc.timed_request("another", b'example'), loop=c.loop)
    msg = future.result()
    print("--- Got: ", msg.data)




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

    @asyncio.coroutine
    def request_handler(msg):
        print("[Request on '{} {}']: {}".format(msg.subject, msg.reply, msg.data.decode()))
        yield from msg.nc.publish(msg.reply, b'OK')

    @asyncio.coroutine
    def master(self):
        yield from self.nc.subscribe("help", "workers", cb=self.request_handler)

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

        #self.nc = NATS()
        #self.nc.connect()
        #self.nc.subscribe("help", "workers", cb=self.request_handler)

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

        addButton = QPushButton('publish')
        addButton.clicked.connect(self.nats_pub)
        toolBar.addWidget(addButton)

        self.addToolBar(toolBar)


        #loop = asyncio.get_event_loop()
        #component = Component(nc, loop)
        #thr = Thread(target=another_thread, args=(component,))
        #thr.start()

        #loop.run_forever()

        self.c = Listener(["nats://localhost:4222"])
        tt = TestThread(ccc=self.c)
        tt.start()


    def nats_pub(self):
        print('publishing')
        #self.c.publish('discover', 'hello nats')
        self.c.sync_publish("some message ")

    def request_handler(msg):
        print("[Request on '{} {}']: {}".format(msg.subject, msg.reply, msg.data.decode()))
        msg.self.nc.publish(msg.reply, b'OK')

    def rcv_nats(self):
        print('nats')
        #response = yield from self.nc.timed_request("foo", b'help me', 0.050)
        print('Hi')
        #print(response)
        #print("Received response: {message}".format(message=response.data.decode()))
        self.model.addRow('999','added item', '0.1','0.2','0.3')
        #msg = self.nc.timed_request("help", b'help please', 0.500)
        #print("[Response]: {}".format(msg.data))
        #yield from self.nc.publish("help", b'hello')

    def selectedRows(self):
        rows = []
        for index in self.ui.lv_news.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        return rows

    def removeItems(self):
        self.model.removeRows(self.selectedRows())

class TestThread(Thread):
    def __init__(self, ccc):
        super(TestThread, self).__init__()
        self.c = ccc

    def run(self):
        self.c.loop.run_until_complete(self.c.connect())
        self.c.loop.run_until_complete(self.c.subscribe("minami"))
        self.c.loop.run_forever()


if __name__ == "__main__":
    #loop = asyncio.get_event_loop()

    app = QApplication(sys.argv)
    #loop = QEventLoop(app)
    #asyncio.set_event_loop(loop)  # NEW must set the event loop

    my_window = Me()
    my_window.show()
    #loop.run_until_complete(run(loop))
    #my_window.raise_()
    app.exec_()
#

    #with loop:
    #    loop.run_until_complete(run(loop))

    #loop.close()
    sys.exit(0)