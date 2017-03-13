from player import Player
from planet import Planet 
 
class GuiPlayer(Player):
    def turn_start(self):
        if not self.has_lost():
            return False
        return True
        
    def get_planets(self):
        return []
        
        
class GuiPlanet(Planet):
    def __init__(self, pos, id, size, color):
        super().__init__(pos, id, size)
        self.color = color
        
    def get_info(self, player):
        if player == self.owner:
            resources_string = ''
            for key,  value in self.resources.items():
                resources_string += '\n       {}:{}'.format(key, value)
                
            return """Owner:{}
    recources:{}""".format(self.owner, resources_string)
                   
        else:
            return str(self.owner)+' is owner'
            
    def __repr__(self):
        return '<GuiPlanet: id:{},pos:{},people:{},owner:{}, color:{}>'.format(
                self.id, self.pos, self.resources['people'], 
                self.owner, self.color)
                
