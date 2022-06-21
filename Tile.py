import tkinter as tk
from enum import Enum

from Images import Images

class Tile(object):
  class State(Enum):
    CLEAR    = 0
    FLAGGED  = 1
    BAD_FLAG = 2

  class Type(Enum):
    ND      = 0
    EMPTY   = 1
    MINE    = 2

  def __init__(self, x, y):
    # coords of the tile
    self.x, self.y = x, y

    # internal affairs
    self.state = self.State.CLEAR
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
    self.button.grid(
      column=self.x,
      row=self.y,
      padx=0,
      pady=0,
      sticky='nsew'
    )

  def open(self, is_game_finished=False):
    self.is_opened = True
    self.button.unbind('<Button-2>')

    if self.type == self.Type.MINE:
      if is_game_finished:
        self.sprite = 'mine'
      else:
        self.sprite = 'mine_clicked'
    elif self.mines_around != 0:
      self.sprite = 'numbers'
    else:
      self.sprite = 'empty'

    self.button.configure(
      image=self.images.get(self.sprite, self.mines_around - 1)
    )

  def bind(self, cb_left_click, cb_right_click):
    self.button.bind('<Button-1>', cb_left_click)
    self.button.bind('<Button-3>', cb_right_click)

  def unbind(self):
    self.button.unbind('<Button-1>')
    self.button.unbind('<Button-3>')

  def update_state(self, new_state):
    self.state = new_state
    if self.state == self.State.CLEAR:
      self.sprite = 'untouched'
    elif self.state == self.State.FLAGGED:
      self.sprite = 'flag'
    else:
      self.sprite = 'mine_wrong'

    self.button.configure(image=self.images.get(self.sprite))
