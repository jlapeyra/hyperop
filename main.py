from hyperop import *
from bignum import *
import sys
import time

op = int(sys.argv[1])
x = Big(int(sys.argv[2]))
y = Big(1)
ret = 0
while True:
    ho = HyperOp(op, x, y)
    ho.value(print_=True)
    time.sleep(0.5)
    y = y + 1
    print('------------------')



