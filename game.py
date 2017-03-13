import planetmap
import spaceshipmap

class Game():
    DEBUG = 0
    def __init__(
            self, planetmap_size):
        #planet init
        self.planetmap = planetmap.Planetmap(planetmap_size)
         
        #spaceship init
        self.spaceshipmap = spaceshipmap.Spaceshipmap()
        
        #player init
        self.players = []
        self.winner = None
        
        #turn init
        self.turn = 0
        self.current_player = None
        self.turn_finished = True
        
    def run(self):
        self.turn_start()
        print('run game: ok')
        
    def get_start_planet(self, player):
        return player.start_planet
        
    def send_spaceship(
            self, from_planet, to_planet, 
            spaceship_class, num_spaceships):
        player = self.get_current_player()
        print('game:    try to send spaceship:', from_planet, num_spaceships)
        if spaceship_class.can_send(from_planet, num_spaceships, player):
            spaceship = spaceship_class(player, num_spaceships, 
                                        from_planet, to_planet)
            self.spaceshipmap.add_spaceship(spaceship)
            return spaceship
            
    def turn_start(self):
        while True:
            self.next_player()
            self.planetmap.turn_start(self.current_player)
            self.spaceshipmap.turn_start(self.current_player)
            
            auto_skip = True
            if not self.current_player.has_won():
                if not self.current_player.has_lost():
                    auto_skip = self.current_player.turn_start()
                else:
                    print(self.current_player, 'lost already')
            else:
                auto_skip = False
                self.winner = self.current_player
                print(self.current_player.name, 'won the game!')
                
            if not auto_skip:
                break
            
    
    def turn_end(self):
        self.turn_finished = True
        
    def next_player(self):
        if not self.current_player:
            self.current_player = self.players[0]
        
        if self.players[-1] == self.current_player:
            self.current_player = self.players[0]
            self.turn += 1
            print('NEW TURN', self.turn)
        else:
            self.current_player = self.players[
                    self.players.index(self.current_player)+1
                    ]
                    
        return self.current_player
    
    def get_current_player(self):
        if self.current_player:
            return self.current_player
        else:
            return self.players[0]
            
    def add_player(self, player_class, name):
        for planet in self.planetmap.to_list():
            if not planet.owner:
                player = player_class(name, planet, self)
                self.players.append(player)
                return player
    
class TestGame(Game):
    """Only meant for testing purposes"""
    DEBUG = 1
    def _show_all_planets(self):
        print(self.planetmap)
            
    def _show_all_spaceships(self):
        print(self.spaceshipmap)
        
    def _show_all_players(self):
        print('Player list:')
        for player in self.players:
            print(player.id, player.name, player.start_planet.id)
