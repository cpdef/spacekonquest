from grounds import GROUNDS
from random import randrange
from collections import namedtuple

#Production = namedtuple('Procduction', 'use produce')
Resource = namedtuple('Resource', 'name num')

class Production():
    def __init__(self, use, produce):
        self.use = use
        self.produce = produce
        
    def make(self, resources):
        status = True
        for resource in self.use:
            if resources[resource.name] < resource.num:
                status = False
        if status:
            for resource in self.produce:
                resources[resource.name] += resource.num
            return True
        return False
    
    def __repr__(self):
        return '<Production: use:{},produce:{}'.format(self.use, self.produce)


class Building():
    need = []
    def __init__(self, field, map, resources=None):
        if resources == None: 
            #to make building of CommandoCentral while planet-init possible
            return
        for resource in self.need:
            resources[resource.name] -= resource.num
        
    @classmethod
    def can_build(cls, field, map, resources):
        print('buildings:    canbuild on ', field, '?')
        if (not field.content) and field.ground == GROUNDS['DIRT']:
            for resource in cls.need:
                if not resources[resource.name] >= resource.num:
                    print('buildings:    use-recource not', 
                          resources[resource.name], '>=', resource.num, '!')
                    print('buildings:    canbuild false')
                    return False
            print('buildings:    canbuild true')
            return True
        else:
            print('buildings:    canbuild field has building! false')
            return False
        
    def get_production(self):
        return Production([], [])
        
    def turn_start(self, resources):
        return resources
        
    def __repr__(self):
        return '<Building>'
        
class CommandoCentral(Building):
    need = [Resource('energy', 0)]
    def __init__(self, field, map):
        super().__init__(field, map)
        print('buildings:    builded CommandoCentral at: ', field)
        
    def can_build(self):
        print('buildings:    CommandoCentral not buildiable by player!')
        return False
        
    def get_production(self):
        steel = Resource('steel', 10)
        people = Resource('people', 10)
        return Production([], [steel, people])

    def __repr__(self):
        return '<Farm>'
                
class Farm(Building):
    need = [Resource('energy', 5)]
    def __init__(self, field, map, resources):
        super().__init__(field, map, resources)
        
    def get_production(self):
        energy = Resource('energy', 5)
        food = Resource('food', 10)
        return Production([energy, ], [food, ])

    def __repr__(self):
        return '<Farm>'


class Mine(Building):
    need = [Resource('energy', 100)]
    def __init__(self, field, map, resources):
        super().__init__(field, map, resources)
        
    def get_production(self):
        energy = Resource('energy', 20)
        coal = Resource('food', randrange(10))
        steel = Resource('steel', randrange(5))
        uranium = Resource('uranium', randrange(2))
        return Production([energy, ], [coal, steel, uranium])
    
    def __repr__(self):
        return '<Mine>'

                
class RobotProduction(Building):
    need = [Resource('energy', 200),  Resource('steel', 100)]
    def __init__(self, field, map, resources):
        super().__init__(field, map, resources)
        
    def get_production(self):
        energy = Resource('energy', 10)
        robots = Resource('robots', 5)
        return Production([energy, ], [robots, ])
    
    def __repr__(self):
        return '<RobotProduction>'
        
        
class WindGenerator(Building):
    need = [Resource('steel', 10)]
    def __init__(self, field, map, resources):
        super().__init__(field, map, resources)
        
    def get_production(self):
        energy = Resource('energy', 10)
        return Production([], [energy, ])
    
    def __repr__(self):
        return '<WindGenerator>'
        
        
class NuclearGenerator(Building):
    need = [Resource('energy', 300), Resource('steel', 200)]
    def __init__(self, field, map, resources):
        super().__init__(field, map, resources)
        
    def get_production(self):
        energy = Resource('energy', 100)
        uranium = Resource('uranium', 1)
        return Production([uranium, ], [energy, ])
    
    def __repr__(self):
        return '<Farm>'
        
        
class CoalGenerator(Building):
    need = [Resource('energy', 150),  Resource('steel', 50)]
    def __init__(self, field, map, resources):
        super().__init__(field, map, resources)
        
    def get_production(self):
        energy = Resource('energy', 30)
        coal = Resource('coal', 2)
        return Production([coal, ], [energy, ])
    
    def __repr__(self):
        return '<Farm>'
        

class SpaceshipProduction(Building):
    need = [Resource('energy', 400),  Resource('steel', 500)]
    def __init__(self, field, map, resources):
        super().__init__(field, map, resources)
            
    def turn_start(self, resources):
        if resources['energy'] > 10 and resources['steel'] > 10:
            resources['energy'] -= 10
            resources['steel'] -= 10
            resources['spaceships'] += 10
        return resources
        
    def get_production(self):
        energy = Resource('energy', 10)
        steel = Resource('steel', 10)
        spaceships = Resource('spaceships', 5)
        return Production([energy, steel], [spaceships, ])
    
    def __repr__(self):
        return '<Farm>'
