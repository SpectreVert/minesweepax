from enum import Enum

class Game(object):
  class Difficulty(Enum):
    EASY = 0,
    INTERMEDIATE = 1,
    HARD = 2

  def __init__(self, frame):
    self.frame = frame
    self.board = None

    self.nb_rows = 0
    self.nb_cols = 0
    self.nb_mines = 0

    self.lbl_flags = None

  def start(self, difficulty, cb_on_end):
    self.__set_board_specs(difficulty)

    cb_on_end()

  def __set_board_specs(self, difficulty):
    if difficulty == self.Difficulty.EASY:
      self.nb_rows  = self.nb_cols = 8
      self.nb_mines = 10
    if difficulty == self.Difficulty.INTERMEDIATE:
      self.nb_rows  = self.nb_cols = 16
      self.nb_mines = 40
    if difficulty == self.Difficulty.HARD:
      self.nb_rows  = 16
      self.nb_cols  = 30
      self.nb_mines = 99
