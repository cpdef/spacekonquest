import os

def get_file(name):
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, name)
    return path
    
if __name__ == '__main__':
    print(get_file('sound'))
