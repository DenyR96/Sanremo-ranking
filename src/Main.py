from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar, ttk
import webbrowser
from RankingFrame import RankingFrame
from SongTextFrame import SongTextFrame
from MusicPlayer import MusicPlayer
from Commons import color_selection_year, font_btn, color_btn, color_text, font_text, rankings_data, color_canvas, songs_text_data, win

# sanremo's logos image
logo_sanremo_2020 = PhotoImage(file = "assets/images/logo_sanremo_2020.png")
logo_sanremo_2021 = PhotoImage(file = "assets/images/logo_sanremo_2021.png")
logo_sanremo_2022 = PhotoImage(file = "assets/images/logo_sanremo_2022.png")

class Main(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # @Attribute
        self.year_chosen = tk.StringVar()
        self.radVar = tk.IntVar()
        self.radVar.set(99) #Select a non-existing index value for radVar
        self.main_frame = tk.Frame(win, bg = color_selection_year[0])
        self.logo_label = Label(self.main_frame, anchor = "n")

        # create Ranking frame, Song text frame and Music player instances
        self.ranking_instance = RankingFrame(self.main_frame)
        self.song_text_instance = SongTextFrame(self.main_frame)
        self.music_player_instance = MusicPlayer(self.main_frame)
        
        self.__create_widgets()

    def __create_widgets(self):
		# combobox with the available editions of sanremo's festival
        select_year = ttk.Combobox(self.main_frame, state = "readonly", cursor = "hand2")
        select_year.set("Choose a year:")
        select_year['values'] = (2022, 2021, 2020)
        select_year.bind("<<ComboboxSelected>>", self.show_ranking)
        select_year.configure(font = font_btn)
        self.main_frame.pack(expand = "True", fill = "both")
        select_year.place(relheight = 0.05, relwidth = 0.15, relx = 0.175, rely = 0.04)
        
		# button that displays song's text inside frame
        self.text_button = tk.Button(self.main_frame, text = "Show text", font = font_btn, fg = color_text, bg = color_btn, command = self.show_text, cursor = "hand2", state = "disabled")
        self.text_button.config(highlightthickness = 0, activebackground = color_btn, activeforeground = color_text)
        self.text_button.place(relheight = 0.05, relwidth = 0.1, relx = 0.660, rely = 0.15, anchor = "center")

        # button that opens song's url into browser window
        self.video_button = tk.Button(self.main_frame, text = "Go to video", font = font_btn, fg = color_text, bg = color_btn, command = self.show_video, cursor = "hand2", state = "disabled")
        self.video_button.config(highlightthickness = 0, activebackground = color_btn, activeforeground = color_text)
        self.video_button.place(relheight = 0.05, relwidth = 0.1, relx = 0.820, rely = 0.15, anchor = "center")
    
    def song_choice(self):     
        song_chosen = self.radVar.get()
        self.music_player_instance.load(self.year_chosen, song_chosen)
        self.text_button['state'] = "active"
        self.video_button['state'] = "active"
        return song_chosen
    
    def show_ranking(self, event):
		#preparations for the chosen ranking
        self.year_chosen = event.widget.get()
        rank_canvas = self.ranking_instance.rank_canvas
        rank_frame = self.ranking_instance.rank_frame
        rank_canvas.delete("all")

		#depending on the chosen year, the bg color of the main frame and the image will change 
        if self.year_chosen == "2022":
            self.main_frame.configure(bg = color_selection_year[0])
            self.logo_label.configure(image = logo_sanremo_2022, bg = color_selection_year[0])
        elif self.year_chosen == "2021":
            self.main_frame.configure(bg = color_selection_year[1])
            self.logo_label.configure(image = logo_sanremo_2021, bg = color_selection_year[1])
        elif self.year_chosen == "2020":
            self.main_frame.configure(bg = color_selection_year[2])
            self.logo_label.configure(image = logo_sanremo_2020, bg = color_selection_year[2])

        self.main_frame.pack(expand = "True", fill = "both")
        self.logo_label.pack()
        self.text_button['state'] = "disabled"
        self.video_button['state'] = "disabled"
        self.music_player_instance.play_button['state'] = "disabled"
        self.ranking_instance.place(relheight = 0.78, relwidth = 0.47, relx = 0.02, rely = 0.2)
        rank_canvas.create_window(self.ranking_instance.rank_frame_center, 20, window = self.ranking_instance.rank_title, anchor = "n")

        posizione_classifica = 1
        pos_y = 90
        for canzone in rankings_data[self.year_chosen]:
            dati_canzone = str(posizione_classifica) + " \"" + canzone['title'] + "\" " + canzone['singer']
            self.curRad = tk.Radiobutton(rank_frame, text = dati_canzone, font = font_text, variable = self.radVar, value = posizione_classifica - 1, command = self.song_choice, bg = color_canvas, cursor = "hand2")
            self.curRad.config(highlightthickness = 0, activebackground = color_canvas, activeforeground = "#46ebfc", selectcolor = color_canvas, fg = color_text)
            rank_canvas.create_window(self.ranking_instance.rank_entries_left, pos_y, anchor = 'w', window = self.curRad)
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
    main = Main(win)
    main.mainloop()