import tkinter as tk
from enum import Enum

from Images import Images

class Tile(object):
  class Status(Enum):
    CLEAR   = 0
    FLAGGED = 1
    UNSURE  = 2

  class Type(Enum):
    ND      = 0
    EMPTY   = 1
    MINE    = 2

  def __init__(self, x, y):
    # coords of the tile
    self.x, self.y = x, y

    # internal state
    self.status = self.Status.CLEAR
    self.type   = self.Type.ND

    self.is_opened = False
    self.mines_around = 0

    # appearance
    self.images = Images()
    self.sprite = 'untouched'

  def mk_button(self, frame):
    self.button = tk.Label(
      frame,
      image=self.images.get(self.sprite),
      bd=1
    )
