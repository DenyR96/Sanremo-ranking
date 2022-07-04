from tkinter import *
import tkinter as tk
import json
import platform

#window details
win = tk.Tk()
win.title('Sanremo Rankings')
os_name = platform.system()
if os_name == "Windows" or os_name == "Darwin": win.state("zoomed")
else: win.attributes("-zoomed", True)
win.resizable(False, False)

#opening and loading of rankings and songs text file
rankings = open("src/Rankings.json", mode = "r")
rankings_data = json.load(rankings) 
songs_text = open("src/Songs_text.json", mode = "r")
songs_text_data = json.load(songs_text)

#hexadecimal values for colors
color_text = "#ffffff"
color_canvas = "#5e269d"
color_selection_year = ['#00008b', '#02183c', '#182853'] #[0] = main&2022, [1] = 2021, [2] = 2020
color_btn = "#5e269d"

#font types and dimensions
font_btn = ("Lao UI", 14)
font_title = ("MS Serif", 22, "bold")
font_text = ("Comic Sans MS", 14, "italic")