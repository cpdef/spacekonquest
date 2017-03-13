import re
from Gui.util import get_file
from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtSvg import QSvgRenderer as SvgRen


def get_image(name, width=None, height=None):
    path = get_file('images/{}'.format(name))
    png = re.compile('.+png$')
    svg = re.compile('.+svg$')
    if png.match(path):
        if width and height:
            return QImage(width, height, path)
        return QImage(path)
    elif svg.match(path):
        if width and height:
            renderer = SvgRen(path)
            img = QImage(width, height, QImage.Format_ARGB32)
            img.fill(QColor(0, 0, 0, 0))
            painter = QPainter(img)
            renderer.render(painter)
            painter.end()
            return img
        print('svg needs width and height!')
        return
    print('can\'t open image:{}'.format(path))
    


if __name__ == '__main__':
    print(get_image('planet'))
