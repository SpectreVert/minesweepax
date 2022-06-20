import tkinter as tk

class Screens(object):
  @staticmethod
  def home(frame, cb_new_game, cb_difficulty, cb_exit):
    btn_new_game = Screens.__button(frame, 'New Game', cb_new_game)
    btn_new_game.pack()

    btn_difficulty = Screens.__button(frame, 'Choose Difficulty', cb_difficulty)
    btn_difficulty.pack()

    btn_exit = Screens.__button(frame, 'Exit', cb_exit)
    btn_exit.pack()

    lbl_mspx = tk.Label(
      frame,
      anchor=tk.S,
      borderwidth=15,
      text='Minesweepax'
    )
    lbl_mspx.pack(fill=tk.X, side=tk.BOTTOM)

    frame.pack(fill=tk.Y, expand=True)

  @staticmethod
  def difficulty(frame, cb_easy, cb_intermediate, cb_hard):
    btn_easy = Screens.__button(frame, 'Noob', cb_easy)
    btn_easy.pack()

    btn_intermediate = Screens.__button(frame, 'Jobless', cb_intermediate)
    btn_intermediate.pack()

    btn_hard = Screens.__button(frame, 'Addict', cb_hard)
    btn_hard.pack()

    lbl_difficulty = tk.Label(
      frame,
      anchor=tk.S,
      borderwidth=15,
      text='Pick your difficulty level'
    )
    lbl_difficulty.pack(fill=tk.X, side=tk.BOTTOM)

    frame.pack(fill=tk.Y, expand=True)

  @staticmethod
  def __button(frame, text, command):
    return tk.Button(frame, text=text, command=command, width=20)
