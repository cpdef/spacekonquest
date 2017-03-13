class Spaceshipmap():
    def __init__(self):
        self.spaceships = []
        self.next_id = 1
    
    def add_spaceship(self, spaceship):
        self.spaceships.append(spaceship)
        
    def to_list(self):
        return self.spaceships
        
    def turn_start(self, player):
        for ship in self.spaceships:
            if ship.owner is player:
                ship.on_step()
                
            if ship.touched_ground:
                self.del_spaceship(ship)
                continue
    
    def del_spaceship(self, spaceship):
        self.spaceships.remove(spaceship)
    
    def __repr__(self):
        return '<Spaceshipmap: [\n    {}\n]>'.format(
        ',\n    '.join([str(i) for i in self.spaceships])
        )
