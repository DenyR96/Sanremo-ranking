from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar, ttk
import platform
import json
from turtle import color
import webbrowser
import pygame
from urllib.request import urlopen
import sys
import os

#window details
win = tk.Tk()
win.title('Sanremo Rankings')
os_name = platform.system()
if os_name == "Windows" or os_name == "Darwin": win.state("zoomed")
else: win.attributes("-zoomed", True)
win.resizable(False, False)

#rankings and songs text files
rankings = open("src/Rankings.json", mode = "r")
rankings_data = json.load(rankings) 
songs_text = open("src/Songs_text.json", mode = "r")
songs_text_data = json.load(songs_text)


class RankingFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        #@Attributes
        self.rank_frame = tk.Frame(self)
        self.rank_canvas = Canvas(self.rank_frame, scrollregion = (0, 0, 600, 770))
        self.rank_vertical_bar = Scrollbar(self.rank_frame, orient = "vertical", command = self.rank_canvas.yview)
        self.rank_title = Label(self.rank_canvas, text = "Ranking", bg = bg_color_canvas, fg = color_text, font = font_title)
        self.rank_frame_center = int(win.winfo_screenwidth() / 4.5)
        self.rank_entries_left = int(win.winfo_screenwidth() / 55)
        
        self.__create_widgets()

    def __create_widgets(self):
        self.rank_canvas.config(yscrollcommand = self.rank_vertical_bar.set)
        self.rank_canvas.configure(bg = bg_color_canvas, highlightbackground = bg_color_canvas)
        self.rank_frame.pack(expand = "True", fill = "both", side = "left")
        self.rank_vertical_bar.pack(side = "right", fill = "y")
        self.rank_canvas.pack(expand = "True", fill = "both")
        
    
class SongTextFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        #@Attributes
        self.song_text_frame = tk.Frame(self)
        self.song_text_canvas = Canvas(self.song_text_frame, scrollregion = (0, 0, 500, 1800))
        self.song_text_vertical_bar = Scrollbar(self.song_text_frame, orient = "vertical", command = self.song_text_canvas.yview)
        self.text_title = Label(self.song_text_canvas, bg = bg_color_canvas, anchor = "n", fg = color_text, font = font_title)
        self.song_text = Label(self.song_text_canvas, bg = bg_color_canvas, fg = color_text, font = font_text, justify = "center", anchor = "n")
        self.song_text_frame_center = int(win.winfo_screenwidth() / 4.5)

        self.__create_widgets()

    def __create_widgets(self):
        self.song_text_canvas.config(yscrollcommand = self.song_text_vertical_bar.set)
        self.song_text_canvas.configure(bg = bg_color_canvas, highlightbackground = bg_color_canvas)
        self.song_text_frame.pack(expand = "True", fill = "both", side = "right")
        self.song_text_vertical_bar.pack(side = "right", fill = "y")
        self.song_text_canvas.pack(expand = "True", fill = "both")


class MusicPlayer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        pygame.init()
        pygame.mixer.init()

        self.pause_resume = StringVar()
        self.pause_resume.set("Pause")

        #creation of play, pause and stop buttons        
        self.play_button = tk.Button(container, text = "Play", bg = bg_btn, font = font_btn, fg = color_text, command = self.play, state = "disabled", cursor = "hand2")
        self.play_button.config(highlightthickness = 0, activebackground = bg_btn, activeforeground = color_text)
        self.play_button.place(relheight = 0.05, relwidth = 0.08, relx = 0.15, rely = 0.15, anchor = "center")
        
        self.pause_button = tk.Button(container, textvariable = self.pause_resume, bg = bg_btn, font = font_btn, fg = color_text, command = self.pause, state = "disabled", cursor = "hand2")
        self.pause_button.config(highlightthickness = 0, activebackground = bg_btn, activeforeground = color_text)
        self.pause_button.place(relheight = 0.05, relwidth = 0.08, relx = 0.25, rely = 0.15, anchor = "center")

        self.stop_button = tk.Button(container, text = "Stop", bg = bg_btn, font = font_btn, fg = color_text, command = self.stop, state = "disabled", cursor = "hand2")
        self.stop_button.config(highlightthickness = 0, activebackground = bg_btn, activeforeground = color_text)
        self.stop_button.place(relheight = 0.05, relwidth = 0.08, relx = 0.35, rely = 0.15, anchor = "center")
        
        self.playing_state = False
        
    def load(self, year, song_index): #fetch the song and create the mp3 file with the song in the directory  
        song_title = rankings_data[year][song_index]['title']
        song_title = song_title.replace(" ", "%20")

        mp3_link = "https://denyr96.github.io/Sanremo-ranking/assets/songs/"
        mp3_link = mp3_link + year + "/" + song_title + ".mp3"
        self.file_path = "assets/songs/file.mp3"
        try:
            url_song = urlopen(mp3_link)
        except Exception as e:
            print(e) 
            sys.exit()

        if os_name == "Windows":
            self.mp3_file = os.open(self.file_path, os.O_WRONLY | os.O_CREAT | os.O_BINARY)
        else:
            self.mp3_file = os.open(self.file_path, os.O_WRONLY | os.O_CREAT)
        os.write(self.mp3_file, url_song.read())
        self.play_button['state'] = "active"
        self.pause_button['state'] = "disabled"
        self.stop_button['state'] = "disabled"
    
    def play(self):
        if os.path.isfile(self.file_path):
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()
            self.play_button['state'] = "disable"
            self.pause_button['state'] = "active"
            self.stop_button['state'] = "active"
            self.playing_state = True
            self.pause_resume.set("Pause")

    def pause(self):
        if self.playing_state:
            pygame.mixer.music.pause()
            self.playing_state = False
            self.pause_resume.set("Resume")
        else:
            pygame.mixer.music.unpause()
            self.playing_state = True
            self.pause_resume.set("Pause")

    def stop(self):
        pygame.mixer.music.stop()
        self.playing_state = False
        self.play_button['state'] = "active"
        self.pause_button['state'] = "disabled"
        self.stop_button['state'] = "disabled"
        os.close(self.mp3_file)


class App(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        #@Attributes
        self.year_chosen = tk.StringVar()
        self.radVar = tk.IntVar()
        self.radVar.set(99) #Select a non-existing index value for radVar
        self.app_frame = tk.Frame(win, bg = bg_color_frame)
        
        #colors and fonts
        global color_text
        color_text = "#ffffff"

        global bg_color_canvas
        bg_color_canvas = "#5e269d"

        global bg_color_frame
        bg_color_frame = "#00008b"

        global font_btn
        font_btn = ("Lao UI", 14)

        global bg_btn
        bg_btn = "#5e269d"

        global font_title
        font_title = ("MS Serif", 22, "bold")

        global font_text
        font_text = ("Comic Sans MS", 16, "italic")

        #create Ranking frame, Song text frame and Music player instances
        self.ranking_instance = RankingFrame(self.app_frame)
        self.song_text_instance = SongTextFrame(self.app_frame)
        self.music_player_instance = MusicPlayer(self.app_frame)
        
        self.__create_widgets()

    def __create_widgets(self):
        self.app_frame.pack(expand = "True", fill = "both")
        
        #combobox that displays available years
        select_year = ttk.Combobox(self.app_frame, state = "readonly", cursor = "hand2")
        select_year.set("Choose a year:")
        select_year['values'] = (2022, 2021, 2020)
        select_year.bind("<<ComboboxSelected>>", self.show_ranking)
        select_year.configure(font = font_btn)
        select_year.place(relheight = 0.05, relwidth = 0.15, relx = 0.150, rely = 0.04)
        
		#button that displays song's text inside frame
        self.text_button = tk.Button(self.app_frame, text = "Show text", font = font_btn, fg = color_text, bg = bg_btn, command = self.show_text, cursor = "hand2", state = "disabled")
        self.text_button.config(highlightthickness = 0, activebackground = bg_btn, activeforeground = color_text)
        self.text_button.place(relheight = 0.05, relwidth = 0.1, relx = 0.650, rely = 0.15, anchor = "center")

        #button that opens song's url into browser window
        self.video_button = tk.Button(self.app_frame, text = "Go to video", font = font_btn, fg = color_text, bg = bg_btn, command = self.show_video, cursor = "hand2", state = "disabled")
        self.video_button.config(highlightthickness = 0, activebackground = bg_btn, activeforeground = color_text)
        self.video_button.place(relheight = 0.05, relwidth = 0.1, relx = 0.830, rely = 0.15, anchor = "center")
    
    def song_choice(self):     
        song_chosen = self.radVar.get()
        self.music_player_instance.load(self.year_chosen, song_chosen)
        self.text_button['state'] = "active"
        self.video_button['state'] = "active"
        return song_chosen
    
    def show_ranking(self, event):
        self.year_chosen = event.widget.get()
        rank_canvas = self.ranking_instance.rank_canvas
        rank_frame = self.ranking_instance.rank_frame
        rank_canvas.delete("all")
        self.text_button['state'] = "disabled"
        self.video_button['state'] = "disabled"
        self.music_player_instance.play_button['state'] = "disabled"
        self.ranking_instance.place(relheight = 0.78, relwidth = 0.47, relx = 0.02, rely = 0.2)
        rank_canvas.create_window(self.ranking_instance.rank_frame_center, 20, window = self.ranking_instance.rank_title, anchor = "n")

        posizione_classifica = 1
        pos_y = 90
        for canzone in rankings_data[self.year_chosen]:
            dati_canzone = str(posizione_classifica) + " \"" + canzone['title'] + "\" " + canzone['singer']
            curRad = tk.Radiobutton(rank_frame, text = dati_canzone, font = font_text, variable = self.radVar, value = posizione_classifica - 1, command = self.song_choice, bg = bg_color_canvas, cursor = "hand2")
            curRad.config(highlightthickness = 0, activebackground = bg_color_canvas, activeforeground = "#46ebfc")
            rank_canvas.create_window(self.ranking_instance.rank_entries_left, pos_y, anchor = 'w', window = curRad)
            pos_y = pos_y + 30
            posizione_classifica = posizione_classifica + 1
        self.radVar.set(99)
    
    def show_text(self):
        text_vbar = self.song_text_instance.song_text_vertical_bar
        text_canvas = self.song_text_instance.song_text_canvas
        num_canzone_scelta = self.song_choice()
        self.song_text_instance.place(relheight = 0.78, relwidth = 0.47, relx = 0.51, rely = 0.2)
        text_vbar.pack(side = "right", fill = "y")
        song_title = rankings_data[self.year_chosen][num_canzone_scelta]['title']
        self.song_text_instance.text_title.configure(text = song_title)
        text_canvas.create_window(self.song_text_instance.song_text_frame_center, 20, window = self.song_text_instance.text_title, anchor = "n")
        canzone = songs_text_data[self.year_chosen][num_canzone_scelta]["song_text"]
        self.song_text_instance.song_text.configure(text = canzone)
        text_canvas.create_window(self.song_text_instance.song_text_frame_center, 80, window = self.song_text_instance.song_text, anchor = "n")
    
    def show_video(self):
        num_canzone_scelta = self.song_choice()
        canzoni = rankings_data[self.year_chosen]
        webbrowser.open_new(canzoni[num_canzone_scelta]['url'])
    
if __name__ == "__main__":
    app = App(win)
    app.mainloop()
