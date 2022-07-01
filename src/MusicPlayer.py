from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar
import pygame
from Commons import color_btn, font_btn, color_text, rankings_data, os_name
from urllib.request import urlopen
import sys
import os

class MusicPlayer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        pygame.init()
        pygame.mixer.init()

        self.pause_resume = StringVar()
        self.pause_resume.set("Pause")

        #creation of play, pause and stop buttons        
        self.play_button = tk.Button(container, text = "Play", bg = color_btn, font = font_btn, fg = color_text, command = self.play, state = "disabled", cursor = "hand2")
        self.play_button.config(highlightthickness = 0, activebackground = color_btn, activeforeground = color_text)
        self.play_button.place(relheight = 0.05, relwidth = 0.08, relx = 0.15, rely = 0.15, anchor = "center")
        
        self.pause_button = tk.Button(container, textvariable = self.pause_resume, bg = color_btn, font = font_btn, fg = color_text, command = self.pause, state = "disabled", cursor = "hand2")
        self.pause_button.config(highlightthickness = 0, activebackground = color_btn, activeforeground = color_text)
        self.pause_button.place(relheight = 0.05, relwidth = 0.08, relx = 0.25, rely = 0.15, anchor = "center")

        self.stop_button = tk.Button(container, text = "Stop", bg = color_btn, font = font_btn, fg = color_text, command = self.stop, state = "disabled", cursor = "hand2")
        self.stop_button.config(highlightthickness = 0, activebackground = color_btn, activeforeground = color_text)
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