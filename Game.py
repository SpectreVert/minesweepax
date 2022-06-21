import tkinter as tk
from tkinter import messagebox
from enum import Enum
from functools import partial
from random import randint

from Tile import Tile

class Game(object):
  class Difficulty(Enum):
    EASY = 0,
    INTERMEDIATE = 1,
    HARD = 2

  def __init__(self, frame):
    self.frame = frame

    # board
    self.board = None

    self.nb_rows = 0
    self.nb_cols = 0
    self.nb_mines = 0

    # game status
    self.is_game_running = False
    self.is_mines_inited = False
    self.difficulty      = None
    self.seconds_elapsed = 0

    self.flags_left      = 0
    self.flags_correct   = 0

    # labels n shit
    self.lbl_flags = None
    self.lbl_time  = None

    # callbacks
    self.cb_on_end = None

  def start(self, difficulty, cb_on_end):
    self.is_game_running = True
    self.difficulty = difficulty
    self.cb_on_end = cb_on_end

    self.__set_board_specs()
    self.__resize_window()

    self.__widget_menu()
    self.__widget_board()

  def __widget_menu(self):
    menu_frame = tk.Frame(self.frame)
    menu_frame.pack(
      fill=tk.Y,
      padx=3,
      pady=3,
      side=tk.LEFT
    )

    btn_exit = tk.Button(
      menu_frame,
      command=self.cb_on_end,
      text='Give Up',
      width=15
    )
    btn_exit.pack()

    tk.Frame(menu_frame, height=15).pack()

    self.lbl_time = tk.Label(menu_frame, anchor=tk.W)
    self.lbl_time.pack(fill=tk.X)

    lbl_mines = tk.Label(
      menu_frame,
      anchor=tk.W,
      text='Total Mines: {}'.format(self.nb_mines)
    )
    lbl_mines.pack(fill=tk.X)

    self.lbl_flags = tk.Label(menu_frame, anchor=tk.W)
    self.lbl_flags.pack(fill=tk.X)

  def __widget_board(self):
    board_frame = tk.Frame(self.frame)
    board_frame.pack(padx=5, pady=5, side=tk.LEFT)

    self.board = [[0 for x in range(self.nb_cols)] for y in range(self.nb_rows)]

    for y in range(self.nb_rows):
      for x in range(self.nb_cols):
        cb_left_click = partial(self.__on_left_click, x, y)
        cb_right_click = partial(self.__on_right_click, x, y)

        tile = Tile(x, y)
        self.board[y][x] = tile
        tile.mk_button(board_frame)
        tile.bind(cb_left_click, cb_right_click)

  # Game operations

  def __init_mines(self, the_x, the_y):
    self.is_mines_inited = True
    mines_todo = self.nb_mines

    while mines_todo:
      x = randint(0, self.nb_cols - 1)
      y = randint(0, self.nb_rows - 1)
      if x != the_x and y != the_y and self.board[y][x].type == Tile.Type.ND:
        self.board[y][x].type = Tile.Type.MINE
        mines_todo -= 1

    for y in range(self.nb_rows):
      for x in range(self.nb_cols):
        tile = self.board[y][x]
        if tile.type != Tile.Type.MINE:
          adjacent_tiles = self.__get_adjacent_tiles(tile.x, tile.y)
          mines = list(filter(lambda t: t.type == Tile.Type.MINE, adjacent_tiles))
          tile.type = Tile.Type.EMPTY
          tile.mines_around = len(mines)

  def __open_tile(self, x, y):
    tile = self.board[y][x]
    
    if tile.state == Tile.State.FLAGGED:
      return

    tile.open()

    if tile.type == Tile.Type.MINE:
      self.__end_on_mine()
      return

    adjacent_tiles = self.__get_adjacent_tiles(tile.x, tile.y)
    closed_tiles   = list(filter(lambda t: not t.is_opened, adjacent_tiles))

    if tile.mines_around == 0:
      for t in closed_tiles:
        self.__open_tile(t.x, t.y)
    elif tile.is_opened:
      non_flagged_mines = list(filter(
        lambda t: t.type == Tile.Type.MINE and t.state != Tile.State.FLAGGED,
        adjacent_tiles
      ))
      if len(non_flagged_mines) == 0:
        for t in closed_tiles:
          if t.state != Tile.State.FLAGGED:
            self.__open_tile(t.x, t.y)

  # End of game

  def __end_on_mine(self):
    print('LOST YOU NOOB')
    exit(1)

  # Event callbacks

  def __on_left_click(self, x, y, event=None):
    if self.board[y][x].state != Tile.State.CLEAR:
      # TODO remove this for double click
      return
    if not self.is_mines_inited:
      self.__init_mines(x, y)
    self.__open_tile(x, y)

  def __on_right_click(self, x, y, event=None):
    tile = self.board[y][x]
    if tile.state == Tile.State.CLEAR:
      if self.flags_left != 0:
        tile.update_state(tile.State.FLAGGED)
        self.flags_left -= 1
        if tile.type == tile.Type.MINE:
          self.flags_correct += 1
        if self.flags_correct == self.nb_mines:
          print('KOWABUNGA YOU WON')
          exit(1)
        else:
          # TODO update flag label
          pass
    else:
      tile.update_state(tile.State.CLEAR)
      self.flags_left += 1
      if tile.type == tile.Type.MINE:
        self.flags_correct -= 1
        # TODO update flag label

  # (Re)Usable utilities

  def __set_board_specs(self):
    if self.difficulty == self.Difficulty.EASY:
      self.nb_rows    = self.nb_cols = 8
      self.flags_left = self.nb_mines = 10
    elif self.difficulty == self.Difficulty.INTERMEDIATE:
      self.nb_rows    = self.nb_cols = 16
      self.flags_left = self.nb_mines = 40
    else:
      self.nb_rows    = 16
      self.nb_cols    = 30
      self.flags_left = self.nb_mines = 99

  def __resize_window(self):
    if self.difficulty == self.Difficulty.EASY:
      x, y = 300, 155
    elif self.difficulty == self.Difficulty.INTERMEDIATE:
      x, y = 440, 300
    else:
      x, y = 695, 300
    self.frame.master.geometry('{}x{}'.format(x, y))

  def __get_adjacent_tiles(self, x, y):
    tiles = []
    to_check = [
      (-1, -1), (0, -1), (1, -1), (-1, 0),
      (1, 0), (-1, 1), (0, 1), (1, 1)
    ]

    for t in to_check:
      tx, ty = x + t[0], y + t[1]
      if self.nb_rows > tx >= 0:
        if self.nb_cols > ty >= 0:
          tiles.append(self.board[ty][tx])
    return tiles
