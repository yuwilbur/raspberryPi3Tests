from threading import Thread
import time

global cycle
cycle = 0.0

class Hello5Program(Thread):
    def run(self):
        global cycle
        while True:
            time.sleep(5)
            cycle = cycle + 1.0
            print "5 Second Thread cycle+1.0 - ", cycle

class Hello2Program(Thread):
    def run(self):
        global cycle
        while True:
            time.sleep(2)
            cycle = cycle + 0.5
            print "2 Second Thread cycle+1.0 - ", cycle

FiveSecond = Hello5Program()
FiveSecond.setDaemon(True)
FiveSecond.start()

TwoSecond = Hello2Program()
TwoSecond.setDaemon(True)
TwoSecond.start()

Exit = False
while(Exit==False):
    cycle = cycle + 0.1
    print "Main Program increase cycle+0.1 - ", cycle
    time.sleep(1)
    if (cycle > 5): Exit = True

print "Goodbye :)"
