import tkinter as tk

from Minesweepax import Minesweepax

if __name__ == '__main__':
  master = tk.Tk()
  master.title('Minesweepax')
  master.geometry('150x250+200+200')
  master.resizable(width=False, height=False)

  mspx = Minesweepax(master)

  master.mainloop()
