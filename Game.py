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
    self.tiles_done      = 0

    # war of the butons; includes free-of-charge labels
    self.btn_quit_game = None
    self.lbl_flags     = None
    self.lbl_time      = None

    # callbacks
    self.cb_on_end = None
    self.cb_time_loop = None

  def start(self, difficulty, cb_on_end):
    self.is_game_running = True
    self.difficulty = difficulty
    self.cb_on_end = cb_on_end

    self.__set_board_specs()
    self.__resize_window()

    self.__widget_menu()
    self.__widget_board()

  # Widgets

  def __widget_menu(self):
    menu_frame = tk.Frame(self.frame)
    menu_frame.pack(
      fill=tk.Y,
      padx=3,
      pady=3,
      side=tk.LEFT
    )

    self.btn_quit_game = tk.Button(
      menu_frame,
      command=self.__widget_ask_on_quit,
      text='Give Up',
      width=15
    )
    self.btn_quit_game.pack()

    def _time_loop(the_frame):
      if not self.is_game_running:
        return
      self.seconds_elapsed += 1
      self.lbl_time.configure(
        text='Seconds Elapsed: {}'.format(self.seconds_elapsed))
      the_frame.after(1000, _time_loop, the_frame)

    self.lbl_time = tk.Label(menu_frame, anchor=tk.W)
    self.lbl_time.pack(fill=tk.X)
    self.cb_time_loop = partial(_time_loop, menu_frame)

    lbl_mines = tk.Label(
      menu_frame,
      anchor=tk.W,
      text='Total Mines: {}'.format(self.nb_mines)
    )
    lbl_mines.pack(fill=tk.X)

    self.lbl_flags = tk.Label(menu_frame, anchor=tk.W)
    self.lbl_flags.pack(fill=tk.X)
    self.__update_flags()

    lbl_mspx = tk.Label(
      menu_frame,
      anchor=tk.S,
      borderwidth=15,
      text='Minesweepax'
    )
    lbl_mspx.pack(fill=tk.X, side=tk.BOTTOM)

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

    self.cb_time_loop()

  def __widget_end_of_game(self, is_game_won=False):
    def _spawn():
      if is_game_won:
        the_msg = 'You won! You play poker with that luck?'
        self.btn_quit_game.configure(text='Back to glory and fame')
      else:
        the_msg = 'You lost... Try harder!'
        self.btn_quit_game.configure(text='Back to mommy')

      tk.messagebox.showinfo(
        message=the_msg,
        title='Game Finished'
      )

    self.frame.after(250, _spawn)

  def __widget_ask_on_quit(self):
    if not self.tiles_done:
      self.cb_on_end()
      return
    elif self.is_game_running == False:
      self.cb_on_end()
      return

    self.is_game_running = False

    is_coward = tk.messagebox.askyesno(
      message='Are you coward enough to quit?',
      title='Quit Game'
    )
    if is_coward:
      self.cb_on_end()
      return

    self.is_game_running = True
    self.cb_time_loop()

  # Game operations

  def __init_mines(self, the_x, the_y):
    self.is_mines_inited = True
    mines_todo = self.nb_mines

    while mines_todo:
      x = randint(0, self.nb_cols - 1)
      y = randint(0, self.nb_rows - 1)
      bad = False
      if x != the_x and y != the_y and self.board[y][x].type == Tile.Type.ND:
        adjacent_tiles = self.__get_adjacent_tiles(the_x, the_y)
        if self.board[y][x] in adjacent_tiles:
          bad = True
        if not bad:
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

    if tile.type == Tile.Type.MINE:
      tile.open()
      self.__end_on_mine()
      return

    if not tile.is_opened:
      self.tiles_done += 1

    tile.open()
    tile.unbind(do_unbind_left=True)

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
    self.is_game_running = False
    for row in self.board:
      for tile in row:
        tile.unbind()
        if tile.is_opened:
          pass
        elif tile.type == Tile.Type.MINE and tile.state != Tile.State.FLAGGED:
          tile.open(is_game_finished=True)
        elif tile.type != Tile.Type.MINE and tile.state == Tile.State.FLAGGED:
          tile.update_state(tile.State.BAD_FLAG)
    self.__widget_end_of_game()

  def __end_on_victory(self):
    self.is_game_running = False
    for row in self.board:
      for tile in row:
        tile.unbind()
    self.__widget_end_of_game(is_game_won=True)

  # Event callbacks

  def __on_left_click(self, x, y, event=None):
    if self.board[y][x].state != Tile.State.CLEAR:
      return
    if not self.is_mines_inited:
      self.__init_mines(x, y)
    self.__open_tile(x, y)
    if self.tiles_done == self.nb_rows * self.nb_cols:
      self.__end_on_victory()

  def __on_right_click(self, x, y, event=None):
    tile = self.board[y][x]
    if tile.state == Tile.State.CLEAR:
      if self.flags_left != 0:
        if tile.type == Tile.Type.MINE:
          self.tiles_done += 1
        tile.update_state(tile.State.FLAGGED)
        self.flags_left -= 1
        self.__update_flags()
    else:
      if tile.type == Tile.Type.MINE:
        self.tiles_done -= 1
      tile.update_state(tile.State.CLEAR)
      self.flags_left += 1
      self.__update_flags()
    if self.tiles_done == self.nb_rows * self.nb_cols:
      self.__end_on_victory()

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

  def __update_flags(self):
    self.lbl_flags.configure(text='Remaining Flags: {}'.format(
      self.flags_left
    ))

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
      if self.nb_cols > tx >= 0:
        if self.nb_rows > ty >= 0:
          tiles.append(self.board[ty][tx])
    return tiles
