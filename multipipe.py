"""
multi_pipe.py
"""
from multiprocessing import Process, Pipe, Lock
import time
import copy

def heavyWork():
    heavyWork = 0
    for i in range(0, 100000):
        heavyWork = heavyWork + 1

def lightWork():
    lightWork = 0
    for i in range(0, 10000):
        lightWork = lightWork + 1


def reader(lock, pipe, name):
    output_p, input_p = pipe
    read_lock, send_lock = lock
    msg = 0
    while True:
        try:
            read_lock.acquire()
            msg = input_p.recv()    # Read from the output pipe and do nothing
            read_lock.release()
            heavyWork()
            #send_lock.acquire()
            if not output_p.poll():
                input_p.send((name,msg))
            #send_lock.release()
        except EOFError:
            break

if __name__=='__main__':
    output_p, input_p = Pipe()
    lock = (Lock(), Lock())
    read_lock, send_lock = lock

    p1 = Process(target=reader, args=(lock, (output_p, input_p),'1',))
    p1.daemon = True
    p1.start()

    p2 = Process(target=reader, args=(lock, (output_p, input_p),'2',))
    p2.daemon = True
    p2.start()

    p3 = Process(target=reader, args=(lock, (output_p, input_p),'3',))
    p3.daemon = True
    p3.start()

    # p4 = Process(target=reader, args=(lock, (output_p, input_p),'4',))
    # p4.daemon = True
    # p4.start()

    start = time.time()
    processed = 0
    missedProcessed = 0
    latestProcessed = time.time()
    for i in range(0,10000):
        lightWork()
        if not input_p.poll():
            output_p.send((time.time(),i))
        if output_p.poll():
            result = output_p.recv()
            if result[1][0] > latestProcessed:
                processed = processed + 1
                latestProcessed = result[1][0]
                print result
            else:
                missedProcessed = missedProcessed + 1
                print result, 'MISS'
    print 'Performance: ', time.time() - start, processed, missedProcessed
