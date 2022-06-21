import tkinter as tk
from tkinter import messagebox
from enum import Enum

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
        tile = Tile(x, y)
        self.board[y][x] = tile
        tile.mk_button(board_frame)
        tile.button.grid(row=y, column=x, padx=0, pady=0, sticky='nsew')

  def __set_board_specs(self):
    if self.difficulty == self.Difficulty.EASY:
      self.nb_rows  = self.nb_cols = 8
      self.nb_mines = 10
    elif self.difficulty == self.Difficulty.INTERMEDIATE:
      self.nb_rows  = self.nb_cols = 16
      self.nb_mines = 40
    else:
      self.nb_rows  = 16
      self.nb_cols  = 30
      self.nb_mines = 99

  def __resize_window(self):
    if self.difficulty == self.Difficulty.EASY:
      x, y = 300, 155
    elif self.difficulty == self.Difficulty.INTERMEDIATE:
      x, y = 440, 300
    else:
      x, y = 695, 300
    self.frame.master.geometry('{}x{}'.format(x, y))
