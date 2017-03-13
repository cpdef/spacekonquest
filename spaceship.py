class SpaceShip():
    def __init__(self, player, num, from_planet, to_planet):
        self.target = to_planet
        self.pos = from_planet.pos
        self.owner = player
        
        #pay
        num_robots = num-1
        if from_planet.resources['robots'] < num_robots:
            num_robots = from_planet.resources['robots']
        num_people = num-num_robots
        
        from_planet.resources['people'] -= num_people
        from_planet.resources['robots'] -= num_robots
        from_planet.resources['steel'] -= (num_people+num_robots)
        self.people = num_people
        self.robots = num_robots
        
        
        #for on_step
        self.move_per_turn = 1
        self.stepvector = (self.target.pos - self.pos).norm(self.move_per_turn)
        self.touched_ground = False
    
    @staticmethod
    def can_send(from_planet, num, player):
        people = from_planet.resources['people']
        robots = from_planet.resources['robots']
        print('spaceship:    can_send:', people, robots, num)
        if (
          people >= 1 
          and from_planet.owner == player
          and num >= 1
          and people+robots >= num
          and from_planet.resources['steel'] >= num
          ):
            print('spaceship:    can_send success: ', people, robots)
            return True
        return False
            
    def on_step(self):
        if (abs(self.pos-self.target.pos)) > self.move_per_turn:
            self.pos += self.stepvector
        else:
            self.pos = self.target.pos
            self.touchdown()
            
    def get_attack(self):
        return self.people+self.robots
            
    def touchdown(self):
        #print('Event touchdown: planet:{}'.format(self.target))
        self.touched_ground = True
        if self.owner is self.target.owner:
            self.target.resources['people'] +=self.people
            self.target.resources['robots'] +=self.robots
            return
            
        self.target.attack(self)
            
    def __repr__(self):
        return '<Spaceship: pos:{},num:{},owner:{},target_pos:{}>'.format(
                self.pos, self.people+self.robots, self.owner, self.target.pos)
        
