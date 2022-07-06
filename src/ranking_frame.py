from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar


global color_canvas
color_canvas = "#5e269d"

global color_text
color_text = "#ffffff"

global font_title
font_title = ("MS Serif", 22, "bold")


class RankingFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # @Attributes
        self.rank_frame = tk.Frame(self)
        self.rank_canvas = Canvas(self.rank_frame, scrollregion = (0, 0, 600, 900))
        self.rank_vertical_bar = Scrollbar(self.rank_frame, orient = "vertical", command = self.rank_canvas.yview)
        self.rank_title = Label(self.rank_canvas, text = "Ranking", bg = color_canvas, fg = color_text, font = font_title)
        
        self.__create_widgets()


    def __create_widgets(self):
        self.rank_canvas.configure(yscrollcommand = self.rank_vertical_bar.set, bg = color_canvas, highlightbackground = color_canvas)
        self.rank_frame.pack(expand = "True", fill = "both", side = "left")
        self.rank_vertical_bar.pack(side = "right", fill = "y")
        self.rank_canvas.pack(expand = "True", fill = "both")