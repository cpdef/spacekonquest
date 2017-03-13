from collections import namedtuple
from time import clock
Size = namedtuple('Size', 'width height')
Point = namedtuple('Point', 'x y')

def infomsg(module, msg):
    print(clock(), module, msg)
