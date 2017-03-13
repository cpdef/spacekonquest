from random import shuffle, choice
#game modules
from grounds import GROUNDS
from vector import Vector as Vec
from mapgen import NoiseMap
from util import Size
from buildings import CommandoCentral


class MapOnPlanet():
    def __init__(self, size):
        self.size = size
        self.fields = []
        self.generate()
        self.generate_commando_central()
        
    def turn_start(self, resources):
        productions = []
        for field in self.fields:
            content = field.content
            if content:
                productions.append(content.get_production())
        status = True
        
        while status:
            shuffle(productions)
            new_productions = []
            status = False
            for prod in productions:
                if prod.make(resources):
                    status = True
                    #print(prod)
                else:
                    new_productions.append(prod)
            productions = new_productions
            
        #for prod in productions:
            #print(prod, 'failed')
                    
                    
                    
    def build_building(self, pos, building_class, resources):
        for field in self.fields:
            if field.pos == pos:
                field.build_building(self, building_class, resources)
                
    def to_list(self):
        return self.fields[:]
        
    def generate(self):
        self.fields = []
        seed = id(self)
        gen_size = Size(self.size, self.size)
        map = NoiseMap(gen_size, seed)
        map.generate_noise(map.sinussinus_noise)
    
        for i in range(10):
            map2 = NoiseMap(gen_size, seed*i)
            map2.generate_noise(map2.sinussinus_noise)
            if i % 2:
                map2.reverse()
            map = map+map2
    
        
        map.for_every(abs)
        map.soft_focus()
        map.normalize()
        map.equalize_range(7, 10, 9)
        map.equalize_range(0, 6, 0)
        map.equalize_range(6, 8, 9)
        map.dualize()
        
        for y, line in enumerate(map.map):
            for x, value in enumerate(line):
                ground_type = GROUNDS['DIRT']
                if value:
                    ground_type = GROUNDS['WATER']
                self.fields.append(Field(ground_type, Vec((x, y))))
                    
    def __repr__(self):
        return self.fields.__repr__()
        
    def get_random_field(self):
        return choice(self.fields)
        
    def generate_commando_central(self):
        while 1:
            comcen_field = self.get_random_field()
            if comcen_field.ground == GROUNDS['DIRT']:
                comcen_field.content = CommandoCentral(comcen_field, self)
                break


class Field():
    def __init__(self, ground, pos):
        self.ground = ground
        self.pos = pos
        self.content = None
        
    def __repr__(self):
        return '<Field:ground:{},content:{},pos:{}>'.format(
                                                            self.ground, 
                                                            self.content, 
                                                            self.pos
                                                            )
    
    def build_building(self, map, building_class, resources):
        print('map_on_planet:    Field test weather can build')
        if building_class.can_build(self, map, resources):
            self.content = building_class(self, map, resources)
        
    
