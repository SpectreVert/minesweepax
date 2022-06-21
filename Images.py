from PIL import Image, ImageTk
from os import getcwd

from Singleton import Singleton

class Images(metaclass=Singleton):
  def __init__(self):
    path = getcwd() + '/images/'

    self.size = 16
    self.images = {
      'empty': self.__open_image(path + 'empty.png'),
      'flag': self.__open_image(path + 'flag.png'),
      'mine': self.__open_image(path + 'mine.png'),
      'mine_clicked': self.__open_image(path + 'mine_clicked.png'),
      'mine_wrong': self.__open_image(path + 'mine_wrong.png'),
      'numbers': [],
      'untouched': self.__open_image(path + 'untouched.png'),
      'unsure': self.__open_image(path + 'unsure.png'),
    }
    for nb in range(1, 9):
      self.images['numbers̈́'] = []
      #.append(self.__open_image(path + str(nb) + '.png'))

  def get(self, image_name, nb=None):
    if image_name != 'numbers':
      return self.images[image_name]
    return self.images['numbers'][nb]

  def __open_image(self, path):
    return ImageTk.PhotoImage(Image.open(path).resize((self.size, self.size)))
