from collections import namedtuple
Ground = namedtuple('Ground', 'name')
GROUNDS = {'DIRT':Ground('dirt'), 'WATER':Ground('water')}

if __name__ == '__main__':
    print(GROUNDS['DIRT'].name)
