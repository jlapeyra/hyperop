from bignum import Big

SUCC = 0
ADD = 1
MULT = 2
POW = 3

def simplify(string):
    simp = (str(int(string[::-1])))[::-1]
    if simp == '0': return ''
    return '.'+simp

def aprox(num):
    if type(num) == Big: 
        return str(num)
    if num >= 10**9: 
        num = str(num)
        return f'{num[0]}{simplify(num[1:10])}e+{len(num)-1}'
    else:
        return str(num)

class HyperOp:

    def __init__(self, op:int, x, y):
        self.op = op
        self.x = x
        self.y = y

    @staticmethod
    def __value(x) -> int:
        if type(x) == HyperOp:
            return x.value()
        return x
    
    def __str__(self) -> str:
        return f'{HyperOp.__strP__(self.x)}[{self.op}]{HyperOp.__strP__(self.y)}'
    
    @staticmethod
    def __strP__(x):
        if type(x) == HyperOp:
            return f'({x})'
        return f'{aprox(x)}'
    
    def print(self, _print, ident, result=None):
        if _print:
            print('   '*ident + f'{self} = {aprox(result) if result != None else "..."}')


    def value(self, print_=False, ident=0) -> int:
        x = HyperOp.__value(self.x)
        y = HyperOp.__value(self.y)
        op = self.op

        if op == SUCC:   ret = y+1
        elif op == ADD:  ret = x+y
        elif op == MULT:
            ret = x*y
            print(x,y,ret)
        elif op == POW:
            if y >= 10**4: self.print(print_, ident)
            ret = x**y
        elif y == 0: ret = 1
        elif y == 1: ret = x
        else:
            self.print(print_, ident)
            ret = 1
            for i in range(0,int(y)):
                ret = HyperOp(op-1, x, ret).value(print_, ident+1)
        self.print(print_, ident, ret)
        return ret
    
def hyper(op, x, y):
    return HyperOp(op, x, y).value()


