import time
from random import seed, randrange
from math import sin
from util import Point, Size

class NoiseMap():
    def __init__(self, size, seed_ = round(time.time()*10**10)):
        self.map = [[]]
        self.size = size
        self.seed = seed_
        
    def _show(self):
        #meant onl for testing purposes
        for line in self.map:
            print(' '.join([str(i) for i in line]))
            
    def _dummy_map(self):
        self.map = [
        [1, 2, 3, 4, 5], 
        [5, 4, 3, 2, 1], 
        [3, 4, 5, 1, 2], 
        [5, 4, 1, 2, 3], 
        [4, 2, 3, 1, 5], 
        ]
        
    def sinussinus_noise(self, pos, seed_ = None):
        if seed_ == None:
            seed(self.seed)
        else:
            seed(seed_)
        
        rnd_size = max(self.size)
        args = [randrange(rnd_size)*(rnd_size/10) for i in range(5)]
        f1 = lambda x: sin(args[0]*x+args[1])
        f2 = lambda x: sin(args[2]*x+args[3])
        return f1(pos.x+f2(pos.y)+args[4]/10)
        
    def sinus_noise(self, pos, seed_ = None):
        if seed_ == None:
            seed(self.seed)
        else:
            seed(seed_)
        
        rnd_size = max(self.size)
        args = [randrange(rnd_size)*(rnd_size/10) for i in range(3)]
        f1 = lambda x: sin(args[0]*x+args[1])
        return f1(pos.x+args[2]/10)
        
    def generate_noise(self, function, seed_ = None):
        self.map = [
                [function(Point(x, y), seed_) for x in range(self.size.width)] 
                for y in range(self.size.height)
        ]
        
        
    def to_ascii_art(self):
        self.round()
        self.map = [
                   [self.n_to_aa(i) for i in line]
                   for line in self.map
                   ]
    
    def normalize(self):
        min_ = self.get_min()
        max_ = abs(min_)+self.get_max()
        self.map = [
                   [((i+min_)/max_)*9 for i in line]
                   for line in self.map
                   ]

    def reverse(self):
        self.size = Size(*[i for i in reversed(self.size)])
        self.map = [
        [line[col] for line in self.map]
        for col in range(self.size.width)
        ]
        
    def __add__(self, noisemap):
        if self.size == noisemap.size:
            new_map = NoiseMap(self.size)
            new_map.map = [
                    [col_a+col_b for col_a, col_b in zip(line_a, 
                                                         noisemap.map[i])
                    ]
                    for i, line_a in enumerate(self.map)
                ]
            return new_map
        else:
            raise ValueError('maps must have same size')
            
    def equalize_range(self, min_, max_, value):
        new_map = []
        for line in self.map:
            new_line = []
            for col in line:
                if min_ <= col <= max_:
                    #print(col)
                    new_line.append(value)
                else:
                    #print(min_, col, max_, min_ <= col, col <= max_)
                    new_line.append(col)
            new_map.append(new_line)
        self.map = new_map
        
    def get_min(self):
        return min([min(line) for line in self.map])
        
    def get_max(self):
        max_ = max([max(line) for line in self.map])
        if max_ == 0:
            max_ = 1
        return max_
        
    def round(self):
        self.map = [
                   [round(i) for i in line]
                   for line in self.map
                   ]
                   
    def for_every(self, func):
        self.map = [
                   [func(i) for i in line]
                   for line in self.map
                   ]
        
    def soft_focus(self):
        def for_one(pos):
            result = 0
            try:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        result += self.map[(pos[0]+i) % self.size.width]\
                                          [(pos[1]+j) % self.size.height]
            except IndexError:
                pass
            #print(result)
            return result/9
            
        new_map = [
                   [for_one((i, j)) for j, value in enumerate(line)]
                   for i, line in enumerate(self.map)
                  ]
        self.map = new_map
        
    def dualize(self):
        medium = self.get_max()-abs(self.get_max()-self.get_min())
        self.for_every((lambda x: int(x > medium)))
        
    
if __name__ == '__main__':
    map = NoiseMap((100, 100), 500*time.time())
    map.generate_noise(map.sinussinus_noise)
    
    #map2 = NoiseMap((100, 100), 23)#3123123*i+time.time())
    #map2.generate_noise(map2.sinus_noise)
    #map2.reverse()
    #map = map+map2
    
    for i in range(10):
        map2 = NoiseMap(Size(100, 100), 3123123*i*time.time())
        map2.generate_noise(map2.sinussinus_noise)
        if i % 2:
           map2.reverse()
        map = map+map2
    
    def sqr(x):
        return abs(x)**1
        
    map.for_every(sqr)
    map.soft_focus()
    map.soft_focus()
    map.soft_focus()
    map.normalize()
    map.equalize_range(7, 10, 9)
    map.equalize_range(0, 6, 0)
    map.equalize_range(6, 8, 9)
    #map.to_ascii_art()
    map.dualize()
    
    map._show()
    
