from random import randrange,  seed
#PyQt
from PyQt5 import QtGui,  QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget
#game modules
from vector import Vector as Vec
#Gui modules
from Gui.images import get_image

def seed_color(obj, range, offset, alpha=None):
    seed(obj)
    saturation = 0
    while saturation < range/1.5:
        c_red = (randrange(range)+offset) % 256
        c_green = (randrange(range)+offset) % 256
        c_blue = (randrange(range)+offset) % 256
        saturation = max([abs(i) for i in [c_red-c_green, 
                                           c_green-c_blue, 
                                           c_blue-c_red
                                          ]])
    seed()
    
    if type(obj) == int and obj < 10:
        colors = [ 
            (255, 0, 0), 
            (0, 255, 0), 
            (0, 0, 255), 
            (255, 255, 0), 
            (0, 255, 255), 
            (255, 0, 255), 
            (200, 50, 0), 
            (0, 200, 50), 
            (50, 0, 200), 
            (50, 200, 0)
        ]
        c_red, c_green, c_blue = colors[obj]
        
    if alpha:
        return QtGui.QColor(c_red, c_blue, c_green, alpha)
    else:
        return QtGui.QColor(c_red, c_blue, c_green)

class MapWidget(QWidget):
    def __init__(self, parent):
        super(MapWidget, self).__init__(parent)
        self.initUI()
        self.game = parent.game
        self.draw_stop = False
        self.text = ['']
        
        self.selected_planet = None
        self.selected_target_planet = None
        self.test_point = None
        
        
        #draw - init
        self.zoom = 20
        self.background_img = get_image('background.png')
        
        self.brushColor = {'white':QtGui.QColor(255, 255, 255),
                           'gray':QtGui.QColor(128, 128, 128),
                           'black':QtGui.QColor(  0,   0,   0)
                          }
        self.pen = {'white':QtGui.QPen(QtGui.QColor(255, 255, 255), 1, 
                                      QtCore.Qt.SolidLine),
                    'gray':QtGui.QPen(QtGui.QColor(128, 128, 128), 2, 
                                      QtCore.Qt.SolidLine),
                    'black':QtGui.QPen(QtGui.QColor(0, 0, 0), 1, 
                                       QtCore.Qt.SolidLine),
                    'highlight':QtGui.QPen(QtGui.QColor(50, 50, 200), 2, 
                                       QtCore.Qt.SolidLine),
                    'no_border':QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 1, 
                                      QtCore.Qt.SolidLine),
                   }
                   
    def initUI(self):
        #self.setMinimumSize(1, 30)
        pass
    
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp, e)
        qp.end()
    
    def drawWidget(self, qp, e):
        qp.setBrush(self.brushColor['black'])
        qp.setPen(self.pen['black'])
        qp.drawImage(0, 0, self.background_img.scaled(self.size()))
        #size = self.size()
        #w = size.width()
        #h = size.height()
        #qp.drawRect(0, 0, w-10, h-10)
            
        #planets
        for planet in self.game.planetmap.to_list():
            self.draw_planet(qp, planet)
            
        #spaceships
        for spaceship in self.game.spaceshipmap.to_list():
            self.draw_spaceship(qp, spaceship)
            
        #selection
        self.draw_selection(qp)
        
        #test_point
        if self.test_point:
            x, y = self.screen_pos_from_pos(self.test_point)
            qp.setPen(self.pen['white'])
            self.draw_circle(x, y, 2, qp)
            
        #qp.drawImage(4, 4, self.planet_img)
            
    def draw_selection(self, qp):
        if self.selected_planet:
            qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1, 
                                      QtCore.Qt.SolidLine))
            qp.setBrush(QtGui.QColor(0, 0, 0, 0))
            x, y = self.screen_pos_from_pos(self.selected_planet.pos)
            self.draw_circle(x, y, self.zoom+4, qp)
            self.draw_circle(x, y, self.zoom+2, qp)
            
        if self.selected_target_planet:
            qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1, 
                                      QtCore.Qt.SolidLine))
            qp.setBrush(QtGui.QColor(0, 0, 0, 0))
            x, y = self.screen_pos_from_pos(self.selected_target_planet.pos)
            self.draw_circle(x, y, self.zoom+4, qp)
            self.draw_circle(x, y, self.zoom+2, qp)
            
    def draw_spaceship(self, qp, spaceship):
        qp.setPen(self.pen['white'])
        if spaceship.owner == self.game.get_current_player():
            qp.setBrush(QtGui.QColor(200, 0, 0))
            x, y = self.screen_pos_from_pos(spaceship.pos)
            self.draw_circle(x, y, self.zoom/7, qp)
            
    def draw_planet(self, qp, planet):
        #pen = QtGui.QPen(QtGui.QColor(255, 255, 255), 1, 
        #                              QtCore.Qt.SolidLine)
        planet_color = seed_color(planet, 100, 0)

        x, y = self.screen_pos_from_pos(planet.pos)
        
        #planet itself
        qp.setPen(self.pen['no_border'])
        qp.setBrush(planet_color)
        self.draw_circle(x, y, self.zoom-4, qp)
        
        #draw player mark
        if planet.owner:
            #qp.setPen(self.pen['black'])
            qp.setPen(self.pen['no_border'])
            seed_nr = (self.game.players.index(planet.owner))
            player_color = seed_color(seed_nr, 100, 0, 100)
            qp.setBrush(player_color)
            self.draw_sqr(x, y, self.zoom*2-2, qp)
        
        #draw current player highlight
        if planet.owner == self.game.get_current_player():
            qp.setBrush(QtGui.QColor(0, 0, 0, 0))
            qp.setPen(self.pen['highlight'])
            self.draw_circle(x, y, self.zoom-4, qp)
        
        #infos (name, num_spaceships)
        qp.setPen(self.pen['white'])
        qp.setFont(QtGui.QFont('Arial', self.zoom/2))
        qp.drawText(x-self.zoom, y-self.zoom/2, str(planet.id))
        
        if planet.owner == self.game.get_current_player():
            qp.setFont(QtGui.QFont('Arial', self.zoom/2))
            nr = planet.resources['people']
            qp.drawText(x-self.zoom, y+self.zoom, str(nr))
        
                         
        #qp.drawEllipse (self, QPoint center, int rx, int ry)
        
    def draw_circle(self, x, y, rad, qp):
        pen_w = qp.pen().width()-1
        qp.drawEllipse (x-rad, y-rad, 2*rad+pen_w, 2*rad+pen_w)
        
    def draw_sqr(self, mx, my, border, qp):
        border += qp.pen().width()
        qp.drawRect(mx-border/2, my-border/2, border, border)
        
    def screen_pos_from_pos(self, pos):
        offset = self.zoom*2
        return (pos.x()*offset+self.zoom, 
                pos.y()*offset+self.zoom)
                
    def reset_selection(self):
        self.selected_planet = None
        self.selected_target_planet = None
        self.repaint()
        
    def selected(self):
        return Selection(self.selected_planet, self.selected_target_planet)

    def mousePressEvent(self, e):
        self.setFocus()
        print('<MousePressEvent: button:{},x:{},y:{}>'.format(e.button(), 
                                                              e.x(), 
                                                              e.y()
                                                              ))
        logic_pos = Vec((
                        (e.x()-self.zoom)/(self.zoom*2), 
                        (e.y()-self.zoom)/(self.zoom*2)
                        ))
        
        #selection
        old_selection = self.selected()
        
        if e.button() == 2:
            self.selected_planet = None
            self.selected_target_planet = None
        else:
            for planet in self.game.planetmap.to_list():
                if abs(logic_pos-planet.pos) < 0.75:
                    if self.selected_planet and not self.selected_target_planet:
                        if self.selected_planet != planet:
                            self.selected_target_planet = planet
                    elif self.selected_target_planet:
                        self.selected_planet = None
                        self.selected_target_planet = None
                    else:
                        if planet.owner == self.game.get_current_player():
                            self.selected_planet = planet
                    break
                    
        new_selection = self.selected()
        if old_selection != new_selection and self.on_selected_func:
            self.on_selected_func(new_selection)
                    
        
        self.repaint()
         
    def keyPressEvent(self, e):
        #K = QtCore.Qt
        print('<KeyPressEvent: text:{},key:{}>'.format(e.text(), 
                                                       e.key(), 
                                                       ))
        text = e.text()
        
        #zoom
        zoom = 0
        if text == '+':
            zoom = self.zoom*2
        
        if text == '-':
            zoom = self.zoom/2
        
        if text in '+-':
            if 5 < zoom < 200:
                self.zoom = zoom
                self.repaint()
                size = self.game.planetmap.size
                self.setGeometry(0, 0, self.zoom*size.width*2, 
                                 self.zoom*size.height*2)
    
    def set_game(self, game):
        self.game = game
        self.draw_stop = False
        self.repaint()
           
    
    def connect(self, function):
        self.on_selected_func = function
    
    def minimumSizeHint(self):
        size = self.game.planetmap.size
        size = max([self.zoom*size[0]*2, self.zoom*size[1]*2])
        return QSize(size, size)
        
    def sizeHint(self):
        return self.minimumSizeHint()




class Selection():
    def __init__(self, start, target):
        self.start = start
        self.target = target
        
    def __eq__(self, selection):
        if selection == None:
            return False
        return selection.start == self.start and selection.target == self.target
