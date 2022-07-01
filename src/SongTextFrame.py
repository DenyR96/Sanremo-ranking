from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar
from Commons import color_canvas, color_text, font_text, font_title, win

class SongTextFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        # attributes
        self.song_text_frame = tk.Frame(self)
        self.song_text_canvas = Canvas(self.song_text_frame, scrollregion = (0, 0, 500, 2500))
        self.song_text_vertical_bar = Scrollbar(self.song_text_frame, orient = "vertical", command = self.song_text_canvas.yview)
        self.text_title = Label(self.song_text_canvas, bg = color_canvas, anchor = "n", fg = color_text, font = font_title)
        self.song_text = Label(self.song_text_canvas, bg = color_canvas, fg = color_text, font = font_text, justify = "center", anchor = "n")
        self.song_text_frame_center = int(win.winfo_screenwidth() / 4.5)

        self.__create_widgets()

    def __create_widgets(self):
        self.song_text_canvas.config(yscrollcommand = self.song_text_vertical_bar.set)
        self.song_text_canvas.configure(bg = color_canvas, highlightbackground = color_canvas)
        self.song_text_frame.pack(expand = "True", fill = "both", side = "right")
        self.song_text_vertical_bar.pack(side = "right", fill = "y")
        self.song_text_canvas.pack(expand = "True", fill = "both")