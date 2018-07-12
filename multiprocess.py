from multiprocessing import Pool
import time

COUNT = 5000000
def countdown(n):
    print 'countdown'
    while n>0:
        n -= 1

NUM = 4
pool = Pool(processes=NUM)
start = time.time()
for n in range(0, NUM):
    pool.apply_async(countdown, [COUNT//NUM])
pool.close()
pool.join()
end = time.time()
print('Time taken in seconds -', end - start)
