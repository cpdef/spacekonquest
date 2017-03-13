import random
from vector import Vector as Vec

class Planetmap():
    def __init__(self, size):
        self.size = size
        self._planets = []
        self.num_planets = 0
            
    def turn_start(self, player):
        for planet in self._planets:
            planet.turn_start(player)
        
    def to_list(self):
        return self._planets
        
    def add_planet(self, planet_class, *args):
        while True:
            x = random.randrange(self.size.width)
            y = random.randrange(self.size.height)
            status = True
            for planet in self._planets:
                if Vec([x, y]) == planet.pos:
                    status = False
                    break
            if status:
                break
            else:
                pass
                #TODO: change it so that u choose from all free positions

        self._planets.append(planet_class((x, y), len(self.to_list()), *args))
        self.num_planets += 1

    def __repr__(self):
        return '<Planetmap: [\n    {}\n]>'.format(
        ',\n    '.join([str(i) for i in self._planets])
        )
