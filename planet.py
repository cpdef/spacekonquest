from vector import Vector as Vec
from map_on_planet import MapOnPlanet
from buildings import (Farm, Building, Mine, CoalGenerator, WindGenerator, 
                       NuclearGenerator, RobotProduction, SpaceshipProduction)

class Planet():
    def __init__(self, pos, id, size):
        print('LOADING: planet: generate', id)
        self.id = id
        self.pos = Vec(pos)
        self.owner = None
        
        self.resources = {'energy':0, 'steel':0, 'food':0, 
                          'coal':0, 'uranium':0, 'people':0, 
                          'robots':0, 'spaceships':0}
        self.buildings = [
                Farm, Building, Mine, CoalGenerator, WindGenerator, 
                NuclearGenerator, RobotProduction, SpaceshipProduction
        ]
        self.satellites = {}
        
        self.size = size
        self.map_ = MapOnPlanet(size)
        #self.build_building(self.owner, Vec((0, 0)), Farm)
        #print(self.map_)
        
    def get_defence(self):
        defence = 0
        if self.resources['robots'] >= self.resources['energy']:
            defence += self.resources['energy']
        else:
            defence += self.resources['robots']
        defence += round(self.resources['people']*1.25)
        #add here builidng defence
        return defence
            
    def to_start_planet(self, new_owner):
        self.owner = new_owner
    
    def turn_start(self, player):
        if not (self.owner == player):
            return
        self.map_.turn_start(self.resources)
        
    def attack(self, obj):
        robots = self.resources['robots']
        people = self.resources['people']
        if self.get_defence() < 1:
            damage = 1000
        else:
            damage = obj.get_attack() / self.get_defence()
        if self.owner and self.owner.name == 'fred':
            print('player attack', obj.people, people, self.pos, damage)
        if self.get_defence() >= obj.get_attack():
            people = round(people*(1-damage))
            robots = round(robots*(1-damage))
        else: #capture!
            people = obj.people
            robots = obj.robots
            self.owner = obj.owner
            
        self.resources['robots'] = robots
        self.resources['people'] = people
    
    def __repr__(self):
        return '<Planet: id:{},pos:{},people:{},owner:{}>'.format(
                self.id, self.pos, self.people, self.owner)
                
    def build_building(self, player, pos, building_class):
        print('planet:    check buildable:', 
              'player == self.owner and building_class in self.buildings', 
              player == self.owner, building_class in self.buildings)
        print('planet:    playercheck:', id(player), id(self.owner))
        if player == self.owner and building_class in self.buildings:
            print('planet:    build', building_class)
            self.map_.build_building(pos, building_class, self.resources)


    
