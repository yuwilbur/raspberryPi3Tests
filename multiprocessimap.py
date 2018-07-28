from multiprocessing import Pool, Queue
import threading

import time

def finish(result):
	print 'whoa ', result

def func(x):
	print 'starting...'
	time.sleep(x)
	print 'finishing...'
	return str(x + 2)

p = Pool(4)
start = time.time()
class TestThread(threading.Thread):
	def __init__(self):
		super(TestThread, self).__init__()
		self.stuff = None

	def run(self):
		while True:
			pass
	
	def doStuff(self, value):
		print 'doStuff'
		p.apply_async(func, args=(value,), callback = finish)

test = TestThread()
print 'starting...'
test.start()
print 'started'
print '10'
test.doStuff(10)
print '1'
test.doStuff(1)
print '5'
test.doStuff(5)
test.join()

#for x in p.imap(func, [1,5,3]):
#    print("{} (Time elapsed: {}s)".format(x, int(time.time() - start)))