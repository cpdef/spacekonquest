#Gui modules
from Gui.mapwidget import MapWidget
from Gui.gui_repr import BUILDING_REPRS
from Gui.images import get_image
#game modules
from spaceship import SpaceShip
#PyQt
from Gui.planetmapwidget import PlanetMapWidget
from PyQt5.QtGui import QDoubleValidator, QIcon, QPixmap
from PyQt5.QtWidgets import (QPushButton, QWidget, QTabWidget, 
                             QVBoxLayout, QHBoxLayout, QLineEdit,
                             QLabel, QScrollArea, QComboBox, QDialog
                             ) 
#from PyQt5.QtMultimedia import QSound

def get_planet_infostr(planet, player):
    if planet == None:
        return ''
    else:
        str = '''Name: {}
        
        '''
        return str

class TabWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.game = parent.game
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(800,600) 
 
        # Add tabs
        self.tabs.addTab(self.tab1,"Map")
        self.tabs.addTab(self.tab2,"Planet")
        self.tabs.addTab(self.tab3,"Spaceships")

        #
        #MAP-TAB:
        #
        self.tab1.layout = QVBoxLayout(self)
        
        #layouts
        self.tab1.hbox1 = QHBoxLayout(self)
        self.tab1.hbox2 = QHBoxLayout(self)
        
        #widgets
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.on_send_button_press)
        self.next_turn_button = QPushButton("Next Turn")
        self.next_turn_button.clicked.connect(self.on_next_turn_button_press)
        #-scroll area, map
        self.map_ = MapWidget(self)
        self.map_.connect(self.on_selected)
        self.scroll_area2 = QScrollArea(self)
        self.scroll_area2.setWidget(self.map_)
        
        #edit
        objValidator = QDoubleValidator(self)
        objValidator.setRange(0, 10**20, 1)
        self.send_edit = QLineEdit(self)
        self.send_edit.setValidator(objValidator)
        self.send_edit.setEchoMode(QLineEdit.Password)
        
        #main vbox
        self.tab1.layout.addLayout(self.tab1.hbox1, 4)
        self.tab1.layout.addLayout(self.tab1.hbox2)
        #Map hbox
        self.tab1.hbox1.addWidget(self.scroll_area2, 4)
        #Send hbox
        self.tab1.hbox2.addWidget(self.send_edit,  3)
        self.tab1.hbox2.addWidget(self.send_button)
        self.tab1.hbox2.addWidget(self.next_turn_button)
        
        self.tab1.setLayout(self.tab1.layout)
        
        #
        #PLANET-TAB
        # 
        
        #layouts
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.hbox = QHBoxLayout(self)
        self.tab2.vbox = QVBoxLayout(self)
        #widgets
        #-scroll area, map
        self.map_of_planet = PlanetMapWidget(self)
        self.map_of_planet.connect(self.refresh_planet_tab)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.map_of_planet)
        #-others
        self.building_choose_box = QComboBox()
        self.building_choose_box.currentIndexChanged.connect(
                self.building_change)
        self.selected_planet_label = QLabel('selected planet')
        self.selected_target_label = QLabel('selected target planet')
        #main vbox
        self.tab2.layout.addLayout(self.tab2.vbox, 2)
        self.tab2.layout.addLayout(self.tab2.hbox)
        
        self.tab2.vbox.addWidget(self.scroll_area, 2)
        self.tab2.vbox.addWidget(self.building_choose_box)
        
        self.tab2.hbox.addWidget(self.selected_planet_label)
        self.tab2.hbox.addWidget(self.selected_target_label)
        #set layout
        self.tab2.setLayout(self.tab2.layout)
        
        
        #widgets
        
        #
        #Add tabs to TabWidget  
        #      
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    def on_send_button_press(self):
        selection = self.map_.selected()
        from_pl = selection.start
        to_pl = selection.target
        text = self.send_edit.text()
        print('tabwidget-TAB1:   try to send spaceships:', text)
        if from_pl and to_pl and text:
            self.game.send_spaceship(from_pl, to_pl, SpaceShip, int(text))
        self.send_edit.clear()
        self.map_.reset_selection()
        self.map_.repaint()
        
    def on_next_turn_button_press(self):
        #soundpath = get_file('sounds/spaceship4.aiff')
        #print(soundpath)
        #sound = QSound(soundpath)
        #sound.play()
        self.game.turn_start()
        self.map_.reset_selection()
        self.map_.repaint()
        self.send_edit.clear()
        self.refresh_planet_tab()
        if self.game.winner:
            self.show_winner_dialog(self.game.winner)
    
    def set_game(self, game):
        self.game = game
        self.map_.set_game(game)
        self.map_of_planet.set_game(game)
        self.game = game
        
    def on_selected(self, selection):
        self.refresh_planet_tab()
            
    def building_change(self, count):
        text = self.building_choose_box.currentText()
        print('tabwidget-TAB2:    change Building to: ', text)
        if text != 'Choose building here!':
            for building_cls, guirepr in BUILDING_REPRS.items():
                #UGLY hack for get the building from the items text
                name = '{}    {}'.format(guirepr.name, guirepr.description)
                print('tabwidget-TAB2:    ', name, '==', text, '?')
                if name == text:
                    self.map_of_planet.building = building_cls
        else:
            self.map_of_planet.building = None
        print('tabwidget-TAB2:    changed Building to:', 
              self.map_of_planet.building)
            
    def refresh_planet_tab(self):
        selection = self.map_.selected()
        self.selected_planet_label.setText('no planet selected')
        self.selected_target_label.setText('no target selected')
        #self.map_of_planet.set_planet(None)
        if selection != None:
            player = self.game.get_current_player()
            if selection.start:
                self.map_of_planet.set_planet(selection.start)
                start_string = str(selection.start.get_info(player))
                self.selected_planet_label.setText(start_string)
                #Combobox
                self.building_choose_box.clear()
                self.building_choose_box.addItem('Choose building here!')
                for building_cls in selection.start.buildings:
                    guirepr = BUILDING_REPRS[building_cls]
                    text = '{}    {}'.format(guirepr.name, guirepr.description)
                    img = get_image(guirepr.image_name, 20, 20)
                    icon = QIcon(QPixmap.fromImage(img))
                    self.building_choose_box.addItem(icon, text)
            if selection.target:
                target_string = str(selection.target.get_info(player))
                self.selected_target_label.setText(target_string)  
        self.map_of_planet.refresh()
        
    def show_winner_dialog(self, winner):
        self.draw_stop = True
        d = QDialog()
        b1 = QLabel('{} it won the game!'.format(winner.name),d)
        b1.move(50,50)
        d.setWindowTitle("End of the game")
        d.setGeometry(0, 0, 300, 140)
        #d.setWindowModality(Qt.ApplicationModal)
        d.exec_() 
        



