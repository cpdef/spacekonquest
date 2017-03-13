#PyQt
from PyQt5 import QtGui,  QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget
#game modules
from vector import Vector as Vec
#Gui modules
from Gui.images import get_image
from Gui.gui_repr import get_guirepr, get_all_reprs


class PlanetMapWidget(QWidget):
    def __init__(self, parent):
        super(PlanetMapWidget, self).__init__(parent)
        self.initUI()
        self.parent = parent
        self.game = parent.game
        self.planet = None
        self.building = None
        self.selected_field = None
        def on_change():
            pass
        self.on_change = on_change
        
        #draw - init
        self.zoom = 25
        
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
        
        self.set_svg_images()
                   
    def set_svg_images(self):
        self.svg_images = {}
        size = self.zoom
        guireprs = get_all_reprs()
        for guirepr in guireprs:
            image_name = guirepr.image_name
            img = get_image(image_name, size, size)
            self.svg_images[image_name] = img
                   
    def initUI(self):
        #self.setMinimumSize(1, 30)
        pass
    
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp, e)
        qp.end()
    
    def drawWidget(self, qp, e):
        if self.planet:
            qp.setBrush(self.brushColor['black'])
            qp.setPen(self.pen['black'])
            s = self.planet.size
            qp.drawRect(0, 0, s*self.zoom, s*self.zoom)
            
            fields = self.planet.map_.to_list()
            for field in fields:
                self.draw_field(field, qp)
                
        else:
            qp.setBrush(self.brushColor['gray'])
            qp.setPen(self.pen['black'])
            size = self.size()
            w = size.width()
            h = size.height()
            qp.drawRect(0, 0, w-1, h-1)
            
    def draw_field(self, field, qp):
        pos = field.pos
        if field.content == None:
            img_name = get_guirepr(field.ground).image_name
        else:
            img_name = get_guirepr(field.content).image_name
        img = self.svg_images[img_name]
        qp.drawImage(pos.x()*self.zoom+1, pos.y()*self.zoom+1, img)
                
    def draw_circle(self, x, y, rad, qp):
        pen_w = qp.pen().width()-1
        qp.drawEllipse (x-rad, y-rad, 2*rad+pen_w, 2*rad+pen_w)
        
    def draw_sqr(self, mx, my, border, qp):
        border += qp.pen().width()
        qp.drawRect(mx-border/2, my-border/2, border, border)
        
    def screen_pos_from_pos(self, pos):
        offset = self.zoom*2
        return (pos[0]*offset+self.zoom, 
                pos[1]*offset+self.zoom)

    def mousePressEvent(self, e):
        self.setFocus()
        print('\nplanetmapwidget: try to build a building ...')
        #print('<MousePressEvent: button:{},x:{},y:{}>'.format(e.button(), 
        #                                                      e.x(), 
        #                                                      e.y()
        #                                                      ))
        logic_field = Vec((e.x() // self.zoom, e.y() // self.zoom))
        print('planetmapwidget:    try to build at',  logic_field, 'on planet:',
              self.planet, 'this building:',  self.building)
        if self.building != None and self.planet != None:
            print('planetmapwidget:    build', self.building)
            self.planet.build_building(self.game.get_current_player(), 
                                   logic_field, self.building)
        
        self.on_change()
        self.repaint()
         
    def keyPressEvent(self, e):
        #K = QtCore.Qt
        print('<KeyPressEvent: text:{},key:{}>'.format(e.text(), 
                                                       e.key(), 
                                                       ))
        text = e.text()
        zoom = 0
        if text == '+':
            zoom = self.zoom*2
        
        if text == '-':
            zoom = self.zoom/2
        
        if text in '+-':
            if 5 < zoom < 200:
                self.zoom = zoom
                self.set_svg_images()
                size = self.planet.map_.size
                self.setGeometry(0, 0, self.zoom*size, 
                                 self.zoom*size)
                self.repaint()
            
    
    def set_planet(self, planet):
        print('planetmapwidget:    setplanet:', self.planet)
        self.planet = planet
        
    def set_game(self, game):
        self.game = game
        self.repaint()
        
    def minimumSizeHint(self):
        size = self.zoom*10
        return QSize(size, size)
        
    def sizeHint(self):
        return self.minimumSizeHint()
        
    def connect(self, function):
        self.on_change = function
        
    def refresh(self):
        self.repaint()
