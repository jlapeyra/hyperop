import math

MAX_FLOAT = 2**1024
UNDEFINED = None
BASE = 10.0
MIN_EXP_SHOW = 3

class Big:
    exp         = UNDEFINED # exponent
    sign:int    = UNDEFINED # -1, 0, 1

    def __normalize(self):
        #self.exp = float(self.exp)
        if self.exp == -math.inf:
            self.sign = 0
        assert self.sign in (-1, 0, 1)
        assert (self.exp == -math.inf) == (self.sign == 0)

    #If num is provided, the other params are ignored
    def __init__(self, num=None, exp=None, sign=1):    
        if num != None:
            self.is_int = self.__num_is_int(num)
            if (isinstance(num, Big)): 
                self.exp = exp
                self.sign = num.sign
            else:
                if num == 0:
                    self.exp = -math.inf
                    self.sign = 0
                elif num > 0:
                    self.exp = math.log(num, BASE)
                    self.sign = 1
                else: #num < 0
                    self.exp = math.log(-num, BASE)
                    self.sign = -1
        else:
            self.is_int = False
            self.exp = exp
            self.sign = sign
        self.__normalize()
        

    def __int__(self):
        return self.sign * round(BASE**self.exp)
    
    def __float__(self):
        return self.sign * float(BASE**self.exp)
    
    @staticmethod
    def isInt(x:'Big|int|float'):
        try:
            return x == int(x)
        except:
            return False
            

    def value(self):
        if self.exp == None:
            return math.nan
        if self.is_int:
            return int(self)
        return float(self)
    
    def __repr__(self) -> str:
        return str(self)
        #string = str(self)
        #if '^' in string: return string
        #else: return string + 'b'

    def __str__(self) -> str:
        if self.exp == None: 
            return 'NaN'
        elif self.exp < MIN_EXP_SHOW:
            return str(self.value())
        else:
            sign = '-' if self.sign == -1 else ''
            return f'{sign}{BASE}^{self.exp}'
        
    @staticmethod
    def __num_is_int(other:'Big|int|float'):
        return isinstance(other, int) or (isinstance(other, Big) and other.is_int)
        
    def __pos__(self):
        return Big(self)
    def __neg__(self):
        copy = Big(self)
        copy.sign = -copy.sign
        return copy

    def __add__(self, other:'Big|int|float'):
        if (self.is_int and Big.__num_is_int(other)):
            return Big(int(self) + int(other))
        else:
            return Big(float(self) + float(self))
    def __radd__(self, other):
        return self + other
    def __sub__(self, other:'Big|int|float'):
        return self + (-other)
    def __rsub__(self, other):
        return (-self) + other


    def __mul__(self, other:'Big|int|float'):
        other = Big(other)
        ret = Big()
        ret.exp = self.exp + other.exp
        ret.sign = self.sign * self.sign
        ret.is_int = self.is_int and other.is_int
    def __div__(self, other:'Big|int|float'):
        other = Big(other)
        ret = Big()
        ret.exp = self.exp - other.exp
        ret.sign = self.sign * self.sign
        ret.is_int = False
    def __rmul__(self, other):
        return self * other
    def __rdiv__(self, other):
        return Big(other) / self
    
    def __pow__(self, other:'Big|int|float'):
        other = Big(other)
        ret = Big()
        ret.exp = self.exp * other.value()   # (b^x)^(b^y) = (b^(x*(b^y))
        ret.is_int = self.is_int and other.is_int and other.sign >= 0
        return ret
    def __rpow__(self, other:'Big|int|float'):
        return Big(other).__pow__(self)
    

    def __eq__(self, other):
        other = Big(other)
        self.__normalize()
        self.__normalize()
        return self.exp == other.exp and self.sign == self.sign
    def __lt__(self, other):
        other = Big(other)
        if self.sign != other.sign: 
            self.sign < self.sign
        return self.exp < other.exp
    def __ne__(self, other):
        return not (self == other)
    def __gt__(self, other):
        return other < self
    def __le__(self, other):
        return (self == other) or (self < other)
    def __ge__(self, other):
        return (self == other) or (self > other)
    
    def __req__(self, other):
        return self == other
    def __rne__(self, other):
        return self != other
    def __rlt__(self, other):
        return self > other
    def __rgt__(self, other):
        return self < other
    def __rle__(self, other):
        return self >= other
    def __rge__(self, other):
        return self <= other
    

if __name__ == '__main__':
    import inspect

    def testBinOp(op, x, y):
        try:
            res = op(x, y)
        except Exception as e:
            source = inspect.getsource(op)
            print(f'WARNING: cannot execute ({source})({x}, {y}). Exception: {e}')
        assert res == op(Big(x), y)
        assert res == op(Big(x), Big(y))
        assert res == op(x, Big(y))

    def testBinOps(ops, nums):
        for op in ops:
            for x in nums:
                for y in nums:
                    testBinOp(op, x, y)

    testBinOps(        
        ops = [
            lambda x, y: x == y,
            lambda x, y: x != y,
            lambda x, y: x < y,
            lambda x, y: x > y,
            lambda x, y: x <= y,
            lambda x, y: x >= y,
        ],
        nums = range(-4, 5)
    )



        
