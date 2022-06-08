import tkinter as tk
from tkinter import Y, Canvas, Frame, Scrollbar, ttk
import webbrowser

win = tk.Tk()
win.geometry('1200x650')
win.title("Python GUI")

rank_filename = "Classifica 2022.txt"
file_rank = open(rank_filename, "r", encoding = "utf8")
rank_data = file_rank.read()

rank_filename2 = "Classifica 2021.txt"
file_rank2 = open(rank_filename2, "r", encoding = "utf8")
rank_data2 = file_rank2.read()

text_filename1 = "Testo Brividi.txt"
file_text1 = open(text_filename1, "r", encoding = "utf8")
text_data1 = file_text1.read()

text_filename2 = "Testo O forse sei tu.txt"
file_text2 = open(text_filename2, "r", encoding = "utf8")
text_data2 = file_text2.read()

ex_rank_frame = Frame(win, bg = "light green")
ex_rank_frame.pack_propagate(0)
ex_rank_frame.pack(expand = "True", fill = "both", side = "left")

ex_text_frame = Frame(win, bg = "light green")
ex_text_frame.pack_propagate(0)
ex_text_frame.pack(expand = "True", fill = "both", side = "right")

rank_frame = Frame(ex_rank_frame)
rank_vbar = Scrollbar(rank_frame, orient = "vertical")
rank_canvas = Canvas(rank_frame, width = 600, height = 600, scrollregion = (0, 0, 500, 500))
rank_canvas.config(yscrollcommand = rank_vbar.set)
rank_canvas.configure(bg = "light blue")
rank_vbar.config(command = rank_canvas.yview)
rank_frame.pack(expand = "True", side = "left", anchor = "n", pady = (60, 0))
rank_vbar.pack(side = "right", fill = Y)
rank_canvas.pack()

text_frame = Frame(ex_text_frame)
text_vbar = Scrollbar(text_frame, orient = "vertical")
text_canvas = Canvas(text_frame, width = 600, height = 600, scrollregion = (0, 0, 500, 1100))
text_canvas.config(yscrollcommand = text_vbar.set)
text_canvas.configure(bg = "light blue")
text_vbar.config(command = text_canvas.yview)

radVar = tk.IntVar()
radVar.set(99) #Select a non-existing index value for radVar

def song_choice():
	global song_chosen
	song_chosen = 0
	radSel = radVar.get()
	if radSel == 0: song_chosen = 1
	elif radSel == 1: song_chosen = 2
	return song_chosen
	
i = 75
for col in range(2):
	curRad = tk.Radiobutton(rank_frame, variable = radVar, value = col, command = song_choice)
	curRad.place(x = 5, y = i)
	i = i + 20

def show_video():
	sc = song_choice()
	if sc == 0: text_canvas.create_text(300, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = ('Helvetica', '15','bold'))
	elif sc == 1: webbrowser.open_new("https://www.youtube.com/watch?v=MA_5P3u0apQ") #Brividi
	elif sc == 2: webbrowser.open_new("https://www.youtube.com/watch?v=0vrbQcOiq-k") #O forse sei tu

def show_text():
	sc = song_choice()
	text_canvas.delete("all")
	text_frame.pack_forget()
	text_frame.pack(expand = "True", side = "right", anchor = "n", pady = (60, 0))
	text_vbar.pack(side = "right", fill = Y)
	if sc == 0: text_canvas.create_text(300, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = ('Helvetica', '15','bold'))
	else:
		text_canvas.create_text(300, 40, text = "Song text", font = ('Helvetica', '15','bold'))
		if sc == 1:
			text_canvas.create_text(250, 530, text = text_data1, font = ('Helvetica', '12'))
		elif sc == 2:
			text_canvas.create_text(250, 530, text = text_data2, font = ('Helvetica', '12'))
	text_canvas.pack()

def hide_text():
	text_canvas.delete("all")
	text_frame.pack_forget()

def show_ranking(event):
	year_chosen = event.widget.get()
	rank_canvas.delete("all")
	rank_canvas.create_text(300, 40, text = "Ranking", font = ('Helvetica', '15','bold'))
	if year_chosen == "2022": rank_canvas.create_text(300, 300, text = rank_data, font = ('Helvetica', '12'))
	elif year_chosen == "2021": rank_canvas.create_text(300, 300, text = rank_data2, font = ('Helvetica', '12'))

ttk.Label(win, text = "Choose a year: ").place(x = 150, y = 20)
year = tk.StringVar()
year_chosen = ttk.Combobox(win, width = 20, textvariable = year, state = 'readonly')
year_chosen['values'] = (2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000)
year_chosen.place(x = 250, y = 20)

year_chosen.bind("<<ComboboxSelected>>", show_ranking)

video_button = ttk.Button(win, text = "Go to video", command = show_video)
video_button.place(x = 700, y = 20)

text_button = ttk.Button(win, text = "Show text", command = show_text)
text_button.place(x = 850, y = 20)

hide_button = ttk.Button(win, text = "Hide text", command = hide_text)
hide_button.place(x = 1000, y = 20)

win.mainloop()
