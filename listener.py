import asyncio
import time
import logging
import queue
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
from threading import Thread

LOG_FORMAT  = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
LOGGER      = logging.getLogger(__name__)


class Listener:

    def __init__(self, servers, nc=NATS(), loop=asyncio.get_event_loop()):
        self.nc = nc
        self.servers = servers
        self.loop = loop
        self.que = queue.Queue()  # sync control.. looking for alternative now

    @asyncio.coroutine
    def message_handler(self, msg):
        LOGGER.info("[Received on '{}']: {}".format(msg.subject, msg.data.decode()))
        self.que.put(msg.data.decode())

    def connect(self):
        LOGGER.info("connecting to NATS server")
        try:
            yield from self.nc.connect(io_loop=self.loop, servers=self.servers)
        except Exception:
            LOGGER.error("Failed to connect...")

        nc = self.nc

        while not nc.is_connected:
            LOGGER.info("waiting for connection...")
            yield from asyncio.sleep(0.1, loop=self.loop)

        if nc.last_error is not None:
            LOGGER.error("Last Error: {}".format(nc.last_error))

        if nc.is_closed:
            LOGGER.error("Disconnected.")

        LOGGER.info("connecting completed.")

    def subscribe(self, subject):
        LOGGER.info("Subscribing subject [%s]" % subject)
        nc = self.nc

        try:
            yield from nc.subscribe(subject, "", self.message_handler)
        except ErrConnectionClosed:
            LOGGER.error("Connection closed prematurely")

        if nc.last_error is not None:
            LOGGER.warning("Last Error: {}".format(nc.last_error))

        if nc.is_closed:
            LOGGER.error("Disconnected.")

        LOGGER.info("Subscribing [%s] now" % subject)

    def publish(self, subject, msg):
        LOGGER.info("Publishing [%s ...] to subject [%s]" % (msg[:10], subject))
        nc = self.nc

        try:
            yield from nc.publish(subject, msg.encode())
        except ErrConnectionClosed:
            LOGGER.error("Connection closed prematurely")

        if nc.last_error is not None:
            LOGGER.warning("Last Error: {}".format(nc.last_error))

        if nc.is_closed:
            LOGGER.error("Disconnected.")

        LOGGER.info("Published to [%s]" % subject)

    def finalize(self):
        LOGGER.info("Finalizing connection to NATS server")
        nc = self.nc
        if nc.is_connected:
            yield from nc.close()
        else:
            LOGGER.error("Somehow connection was closed before finalization. Check log file.")

        if nc.last_error is not None:
            LOGGER.warning("Last Error: {}".format(nc.last_error))

        if nc.is_closed:
            LOGGER.info("Disconnected.")

        LOGGER.info("Finalization completed.")

    def async_sleep(self, sleep_num):
        LOGGER.info("SLEEP for what???????")
        yield from asyncio.sleep(sleep_num, loop=self.loop)

    def sync_publish(self, msg):
        asyncio.run_coroutine_threadsafe(c.publish("minami", msg), self.loop)
        return self.que.get(self)


# test thread
class TestThread(Thread):
    def __init__(self, ccc):
        super(TestThread, self).__init__()
        self.c = ccc

    def run(self):
        c.loop.run_until_complete(c.connect())
        c.loop.run_until_complete(c.subscribe("minami"))
        c.loop.run_forever()

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN, format=LOG_FORMAT)
    c = Listener(["nats://192.168.2.24:4222"])

    tt = TestThread(ccc=c)
    tt.start()



    time.sleep(3)
    start_time = time.time()
    counter = 100000
    for jj in range(counter):
        # print(c.sync_publish("some message "+jj.__str__()))
        print(c.sync_publish("some message " + jj.__str__()))
    elapsed_time = time.time() - start_time
    print("[%d] was elapsed for [%d] publishing" % (elapsed_time, counter))

