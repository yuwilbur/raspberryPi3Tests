"""
multi_pipe.py
"""
from multiprocessing import Process, Pipe, Lock
import time
import copy

def heavyWork():
    total = 0
    for x in range(0,200000):
        total += 1
        total /= 3
    return total

def lightWork():
    total = 0
    for x in range(0,2000):
        total += 1
        total /= 3
    return total

def yImageWorker(pipe):
    main_conn, worker_conn = pipe
    while True:
        #data = worker_conn.recv()    # Read from the output pipe and do nothing
        #if not worker_conn.poll:
        #heavyWork()
        pass

class MockConsumer(object):
    def __init__(self):
        self._main1_conn, self._worker1_conn = Pipe()
        self._worker1 = Process(target=yImageWorker, args=((self._main1_conn, self._worker1_conn),))
        self._worker1.daemon = True
        self._worker1.start()

        self._main2_conn, self._worker2_conn = Pipe()
        self._worker2 = Process(target=yImageWorker, args=((self._main2_conn, self._worker2_conn),))
        self._worker2.daemon = True
        self._worker2.start()

    def consume(self):
        if not self._main1_conn.poll():
            self._main1_conn.send(0)
        if not self._main2_conn.poll():
            self._main2_conn.send(0)

class MockProducer(object):
    def __init__(self, consumer):
        self._consumer = consumer

    def update(self):
        consumer.consume()

if __name__=='__main__':
    consumer = MockConsumer()
    producer = MockProducer(consumer)
    n = 100
    start = time.time()
    cycles = 0
    for i in range(0, n):
        #print i
        cycles += 1
        lightWork()
        producer.update()
    print 'Performance: ', time.time() - start, ' ', cycles
