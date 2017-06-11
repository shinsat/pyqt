import sys
import asyncio
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
from PyQt5.uic import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QProgressBar
from quamash import QEventLoop, QThreadExecutor
import signal
from threading import Thread


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



#@asyncio.coroutine
def nats_pub(c, msg):
    if not c.nats.nc.is_connected:
        print("Not connected to NATS!")
        return

    #nc = NATS()
    #yield from nc.connect()
    #print("nats_pub Connected to NATS at {}...".format(nc.connected_url.netloc))
    print('ei')
    #yield from nc.publish("discover", b'Hello')
    asyncio.run_coroutine_threadsafe(c.nats.nc.publish("discover", msg.encode('UTF-8')), loop=c.loop)


class Me(QMainWindow, QObject):
    nats_signal = pyqtSignal(str)

    def __init__(self,loop):
        super().__init__()

        #self.nc = NATS()
        self.loop = loop
        self.nats = Nats_control(self)

        self.ui = loadUi('ms_main.ui', self)
        self.model = Model(self)
        self.ui.lv_news.setModel(self.model)

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

        pb = QPushButton('NATS')
        pb.clicked.connect(lambda :self.rcv_nats())
        toolBar.addWidget(pb)

        self.addToolBar(toolBar)

        self.nats_signal.connect(self.rcvd)

    @pyqtSlot(str)
    def rcvd(self, msg):
        print('me')
        aaa = str(msg)
        print(msg)


    def request_handler(msg):
        print("[Request on '{} {}']: {}".format(msg.subject, msg.reply, msg.data.decode()))
        msg.self.nc.publish(msg.reply, b'OK')

    def rcv_nats(self):
        print('nats')
        print('Hi')
        self.model.addRow('999','added item', '0.1','0.2','0.3')
        #self.nc.publish('help.me', u'987654321')
        #yield from self.nc.publish('discover', u'987654321')
        #self.nats.pubpub()
        #self.nats.nats_command.emit()
#        asyncio.run_coroutine_threadsafe(self.nats.nc.publish("hello", b'world'), loop=self.nats.master(loop=None))
        nats_pub(self, '*')

    def selectedRows(self):
        rows = []
        for index in self.ui.lv_news.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        return rows

    def removeItems(self):
        self.model.removeRows(self.selectedRows())

'''
progress = QProgressBar()
progress.setRange(0, 99)
progress.show()
'''
class Nats_control(QObject):
    nats_command = pyqtSignal()

    def __init__(self, parent=None):
        super(Nats_control, self).__init__(parent)

        #self.nc = NATS()
        #self.nc = nc
        #self.my_parent = my_parent
    #    super.__init__()
        #self.nats_command.connect(lambda: self.master.pubpub())

#    def pubpub(self):
        #self.pub()
 #       print('trying publish')
  #      yield from self.nc.publish("help.me", b'test')
        #self.nats_command.connect(lambda : self.pubpub2())

    @asyncio.coroutine
    def master(self,loop):
        self.nc = NATS()

        #self.nats_command.connect(self.master.pubpub)

        #@asyncio.coroutine
        def pubpub():
            # self.pub()
            print('trying publish')
            yield from self.nc.publish("help.me", b'test')

        @asyncio.coroutine
        def closed_cb():
            print("Connection to NATS is closed.")
            yield from asyncio.sleep(0.1, loop=loop)
            loop.stop()

        #@asyncio.coroutine
        #global def pub(self):
        #    yield from self.nc.publish("help.me", b'test')

        options = {
            "servers": ["nats://127.0.0.1:4222"],
            "io_loop": loop,
            "closed_cb": closed_cb
        }

        yield from self.nc.connect(**options)
        print("Connected to NATS at {}...".format(self.nc.connected_url.netloc))

        @asyncio.coroutine
        def subscribe_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            print("Received a message on '{subject} {reply}': {data}".format(
              subject=subject, reply=reply, data=data))
            self.parent().nats_signal.emit(data)

        # Basic subscription to receive all published messages
        # which are being sent to a single topic 'discover'
        yield from self.nc.subscribe("discover", cb=subscribe_handler)
        yield from self.nc.subscribe("help.me", cb=subscribe_handler)

        #yield from self.nc.publish("help.me", b'test')

        def signal_handler():
            if self.nc.is_closed:
                return
            print("Disconnecting...")
            loop.create_task(self.nc.close())

        for sig in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, sig), signal_handler)
                #yield from asyncio.sleep(0.1, loop=loop)

def run(loop):
    nc = NATS()

    @asyncio.coroutine
    def closed_cb():
        print("Connection to NATS is closed.")
        yield from asyncio.sleep(0.1, loop=loop)
        loop.stop()

    options = {
        "servers": ["nats://127.0.0.1:4222"],
        "io_loop": loop,
        "closed_cb": closed_cb
    }

    yield from nc.connect(**options)
    print("Connected to NATS at {}...".format(nc.connected_url.netloc))

    @asyncio.coroutine
    def subscribe_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
          subject=subject, reply=reply, data=data))

    # Basic subscription to receive all published messages
    # which are being sent to a single topic 'discover'
    yield from nc.subscribe("discover", cb=subscribe_handler)

    # Subscription on queue named 'workers' so that
    # one subscriber handles message a request at a time.
    yield from nc.subscribe("help.*", "workers", subscribe_handler)

    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)  # NEW must set the event loop

    ui = Me(loop)
    ui.show()

    # Example using NATS client from another thread.
    #thr = Thread(target=another_thread, args=(component,))
    #thr.start()

    with loop: ## context manager calls .close() when loop completes, and releases all resources
        loop.run_until_complete(ui.nats.master(loop))
#        loop.run_until_complete(run(loop))
        try:
            loop.run_forever()
        finally:
            loop.close()
