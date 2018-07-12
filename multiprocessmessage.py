from multiprocessing import Pool, Queue
import time

class testObject:
	x = 0

COUNT = 5000000
def worker(queue):
	print 'starting work'
	while True:
		item = queue.get(True)
		print 'got work', item.x

queue = Queue()
pool = Pool(4, worker, (queue,))

start = time.time()
for i in range(6):
	test = testObject()
	test.x = i
	queue.put(test)
pool.close()
pool.join()
end = time.time()
print('Time taken in seconds -', end - start)
