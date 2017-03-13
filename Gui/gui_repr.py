from buildings import (Farm, Building, Mine, CoalGenerator, WindGenerator, 
                       NuclearGenerator, RobotProduction, SpaceshipProduction, 
                       CommandoCentral)
from grounds import GROUNDS, Ground
from collections import namedtuple

ObjGuiRepr = namedtuple('ObjGuiRepr', 'name image_name description')
#NOTE: giving to ObjGuiRepr instances the same name
#can cause bugs in game!

BUILDING_REPRS = {
Farm: ObjGuiRepr('Farm', 'farm.svg', str(Farm.need)), 
Building: ObjGuiRepr('Building', 'building.svg', str(Building.need)), 
Mine: ObjGuiRepr('Mine', 'mine.svg', str(Mine.need)), 
NuclearGenerator: ObjGuiRepr('Nuclear Generator', 'nucleargen.svg', 
                             str(NuclearGenerator.need)), 
CoalGenerator: ObjGuiRepr('Coal Generator', 'coalgen.svg', 
                          str(CoalGenerator.need)), 
WindGenerator: ObjGuiRepr('Wind Generator', 'windgen.svg',
                          str(WindGenerator.need)), 
RobotProduction: ObjGuiRepr('Robot Production', 'robotproduction.svg',
                            str(RobotProduction.need)), 
SpaceshipProduction: ObjGuiRepr('Spaceship Production', 
                                'spaceshipproduction.svg',
                                str(SpaceshipProduction.need)), 
CommandoCentral: ObjGuiRepr('Commando Central', 
                                'commando_central.svg',
                                str(CommandoCentral.need)), 
}

GROUND_REPRS = {}
for _, ground in GROUNDS.items():
    name = ground.name
    GROUND_REPRS[ground] = ObjGuiRepr(
            name, 'ground_{}.svg'.format(name), '-'
    )

def get_guirepr(obj):
    if type(obj) == Ground:
        return GROUND_REPRS[obj]
    else:
        return BUILDING_REPRS[type(obj)]
      
def get_all_reprs():
    guireprs = []
    for _, guirepr in BUILDING_REPRS.items():
        guireprs.append(guirepr)
    for _, guirepr in GROUND_REPRS.items():
        guireprs.append(guirepr)
    return guireprs

print('load gui_repr done')
