import multiprocessing
import time
from typing import Iterable

class Timeout:
    pass

import multiprocessing
import time


def work(func, args, ret):
    ret['return'] = func(*args)
    exit()

def timeout(time, func, args):
    # Start bar as a process
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p = multiprocessing.Process(target=work, args=(func, args, return_dict))
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(time)

    # If thread is still active
    if p.is_alive():
        print("running... let's kill it...")

        # Terminate - may not work if process is stuck for good
        p.terminate()
        # OR p.kill - will work for sure, no chance for process to finish nicely however
        p.join()
        return None
    else:
        return return_dict['return']
    
def sleep(x):
    print('sleep')
    time.sleep(x)
    return 'ok'

if __name__ == '__main__':
    print(timeout(2, sleep, (1,)))
    #print(timeout(5, bar, (0.5,)))


'''import signal


def loop_forever():
    import time
    while 1:
        print("sec")
        time.sleep(1)

def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")

signal.signal(signal.SIGALRM, handler)

# Define a timeout for your functiontion
signal.alarm(10)
try:
    loop_forever()
except Exception as e: 
    print(e)'''