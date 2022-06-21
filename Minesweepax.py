import tkinter as tk

from Screens import Screens
from Game import Game

class Minesweepax(object):
  def __init__(self, master):
    self.master = master
    self.master.protocol('VW_DELETE_WINDOW', self.__exit)

    self.frame = None
    self.game = None

    self.difficulty = Game.Difficulty.EASY

    self.__home()

  def __home(self):
    self.__remake_frame()

    Screens.home(self.frame, self.__new_game, self.__difficulty, self.__exit)

  def __new_game(self):
    self.__remake_frame()

    self.game = Game(self.frame)
    self.game.start(self.difficulty, self.__home)

  def __difficulty(self):
    self.__remake_frame()

    def cb_easy():
      self.difficulty = Game.Difficulty.EASY
      self.__home()

    def cb_intermediate():
      self.difficulty = Game.Difficulty.INTERMEDIATE
      self.__home()

    def cb_hard():
      self.difficulty = Game.Difficulty.HARD
      self.__home()

    Screens.difficulty(self.frame, cb_easy, cb_intermediate, cb_hard)

  def __exit(self):
    print('Shutting down systems...')
    self.master.destroy()

  def __remake_frame(self):
    if self.frame is not None:
      self.frame.destroy()
    self.master.geometry('150x250')
    self.frame = tk.Frame(self.master)
    self.frame.pack(fill=tk.BOTH)
