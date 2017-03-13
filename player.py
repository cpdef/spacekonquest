class Player():
    def __init__(self, name, start_planet, game):
        self.start_planet = start_planet
        self.name = name
        self.game = game
        self._lost = False
        
        start_planet.to_start_planet(self)
        
    def __repr__(self):
        return '<Player: {}>'.format(self.name)
        
    def turn_start(self):
        '''can run some commands for especcially ki
        returns weather the game should end the turn after it self'''
        return True
        
    def has_won(self):
        for player in self.game.players:
            if player != self:
                if not player.has_lost():
                    #print(self.name, player.name)
                    return False
        return True
            
        
    def has_lost(self):
        if self._lost:
            return True
        if self.get_own_planets() == []:
            self._lost = True
            self.game.turn_start()
            return True
        return False
        
    def get_own_planets(self):
        def players_planet(planet):
            return planet.owner == self
    
        planets = [i for i in filter(
            players_planet, self.game.planetmap.to_list()
        )]
        return planets
        
    def get_num_planets(self):
        return len(self.get_own_planets())
        
    def get_num_spaceships(self):
        sum = 0
        for ship in self.game.spaceshipmap.to_list():
            if ship.owner == self:
                sum += 1
        return sum
        
        
        
