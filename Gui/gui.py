#!/usr/bin/python3
import sys
#PyQt
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from Gui.tabwidget import TabWidget
from KI.KI_player import KiPlayer
#Gui modules
from Gui.logic_inherited import GuiPlayer, GuiPlanet
#game modules
from util import Size

 
class App(QMainWindow):
    def __init__(self, game_class):
        super().__init__()
        self.game_class = game_class
        self.run_new_game()

#new_game.send_spaceship(player, player.start_planet, planet_map[4], SpaceShip, 4)
        
        self.title = 'Mars 0.2 PyQt5 '
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
        #
        #menu
        #
        self.m_file = self.menuBar().addMenu('File')
        self.m_file.addAction('&Exit')
        self.m_file.addAction('&New Game')
        self.m_file.triggered[QAction].connect(self.m_file_trigger)


        #end menu
        self.show()
        
    def run_new_game(self):
        self.game = self.game_class(Size(10, 10))
        if self.game.DEBUG:
            print('LOADING: gui: create planets')
            for i in range(10):
                self.game.planetmap.add_planet(GuiPlanet, 10,'yellow')
            print('LOADING: gui: add players')
            self.game.add_player(GuiPlayer, 'fred')
            self.game.add_player(KiPlayer, 'ki1')
            self.game.add_player(KiPlayer, 'ki2')
            self.game.add_player(KiPlayer, 'ki3')
            self.game.add_player(KiPlayer, 'ki4')
            self.game.add_player(KiPlayer, 'ki5')
            
        print('\nLOADING: gui: finished')
        self.game.run()
            
    def refresh_game(self):
        self.tab_widget.set_game(self.game)

    def m_file_trigger(self,q):
        print(q.text()+" is triggered")
        if q.text() == '&New Game':
            self.run_new_game()
            self.refresh_game()
 
def run(game):
    app = QApplication(sys.argv)
    ex = App(game)
    sys.exit(app.exec_())
