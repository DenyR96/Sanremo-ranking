from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar


global color_text
color_text = "#ffffff"

global color_canvas
color_canvas = "#5e269d"

global font_title
font_title = ("MS Serif", 22, "bold")

global font_text
font_text = ("Comic Sans MS", 14, "italic")

class SongTextFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        # attributes
        self.song_text_frame = tk.Frame(self)
        self.song_text_canvas = Canvas(self.song_text_frame, scrollregion = (0, 0, 500, 2500))
        self.song_text_vertical_bar = Scrollbar(self.song_text_frame, orient = "vertical", command = self.song_text_canvas.yview)
        self.text_title = Label(self.song_text_canvas, bg = color_canvas, anchor = "n", fg = color_text, font = font_title)
        self.song_text = Label(self.song_text_canvas, bg = color_canvas, fg = color_text, font = font_text, justify = "center", anchor = "n")
    
        self.__create_widgets()

    def __create_widgets(self):
        self.song_text_canvas.configure(yscrollcommand = self.song_text_vertical_bar.set, bg = color_canvas, highlightbackground = color_canvas)
        self.song_text_frame.pack(expand = "True", fill = "both", side = "right")
        self.song_text_vertical_bar.pack(side = "right", fill = "y")
        self.song_text_canvas.pack(expand = "True", fill = "both")