from player import Player
from spaceship import SpaceShip
from random import choice

class KiPlayer(Player):
    def __init__(self, name, start_planet, game):
        super().__init__(name, start_planet, game)
        self.targets = []
        
    def turn_start(self):
        print('Ki_player:    ', self, 'start turn')
        self.set_targets()
        if self.has_lost() or not self.targets:
            self.game.turn_start()
            return
        best_planets = self.get_best_planets(5)
        #print('Ki_player:    best planets:', best_planets)
        for _ in best_planets:
            planet = choice(best_planets)
            print(planet)
            people = planet.resources['people']
            can_send = people-self.game.turn   
            target = choice(self.targets)
            if ( 
                    target.owner == None
                    or people > self.get_num_planets()*5
                    or people > self.game.turn*4
                ):
                self.send_spaceship(
                    planet, target, SpaceShip,
                    can_send
                                   )
        #print('ki', self,'played')
        return True
        
    def set_targets(self):
        num_planets = self.get_num_planets()
        #remove old targets
        new_targets = []
        for target in self.targets:
            if target.owner != self:
                new_targets.append(target)
        self.targets = new_targets[:num_planets]
        num_all_planets = self.game.planetmap.num_planets
        
        while (len(self.targets) < num_planets 
               and len(self.targets) < num_all_planets - num_planets):
            planet = choice(self.game.planetmap.to_list())
            if planet.owner != self and planet not in self.targets:
                self.targets.append(planet)
            
    def send_spaceship(self, planet, target, spaceship_class, num):
        if self.get_num_spaceships() < 20:
            self.game.send_spaceship(planet, target, spaceship_class, num)
            
    def get_best_planets(self, num):
        own_planets = self.get_own_planets()
        planet_sort_list = [(i.resources['people'], id(i)) for i in own_planets]
        planet_sort_list.sort(reverse=True)
        result = []
        for _, good_planet_id in planet_sort_list[:num]:
            for planet in own_planets:
                if id(planet) == good_planet_id:
                    result.append(planet)
        return result
        
        
