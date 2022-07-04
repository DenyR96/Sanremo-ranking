from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar
from src.common_variables import color_canvas, color_text, font_title, win

class RankingFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # attributes
        self.rank_frame = tk.Frame(self)
        self.rank_canvas = Canvas(self.rank_frame, scrollregion = (0, 0, 600, 900))
        self.rank_vertical_bar = Scrollbar(self.rank_frame, orient = "vertical", command = self.rank_canvas.yview)
        self.rank_title = Label(self.rank_canvas, text = "Ranking", bg = color_canvas, fg = color_text, font = font_title)
        self.rank_frame_center = int(win.winfo_screenwidth() / 4.5)
        self.rank_entries_left = int(win.winfo_screenwidth() / 55)
        
        self.__create_widgets()

    def __create_widgets(self):
        self.rank_canvas.config(yscrollcommand = self.rank_vertical_bar.set)
        self.rank_canvas.configure(bg = color_canvas, highlightbackground = color_canvas)
        self.rank_frame.pack(expand = "True", fill = "both", side = "left")
        self.rank_vertical_bar.pack(side = "right", fill = "y")
        self.rank_canvas.pack(expand = "True", fill = "both")