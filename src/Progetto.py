from textwrap import fill
import tkinter as tk
from tkinter import Canvas, Scrollbar, ttk
import json
from turtle import color
import webbrowser
import tkinter.font

from pygments import highlight
win = tk.Tk()
win.title('Sanremo Rankings')
win.attributes("-zoomed",True)
win.resizable(False, False)

# window dimensions
window_width = win.winfo_width()
window_height = win.winfo_height()
		
	
class RankingFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # attributes
        self.rank_frame = tk.Frame(self)
        self.rank_canvas = Canvas(self.rank_frame, scrollregion = (0, 0, 600, 800))
        self.rank_vertical_bar = Scrollbar(self.rank_frame, orient = "vertical", command = self.rank_canvas.yview)

        self.__create_widgets()

    def __create_widgets(self):
        self.rank_canvas.config(yscrollcommand = self.rank_vertical_bar.set)
        self.rank_canvas.configure(bg = bg_color_canvas)
        self.rank_frame.pack(expand = "True", fill = "both", side = "left")
        self.rank_vertical_bar.pack(side = "right", fill = "y")
        self.rank_canvas.pack(expand = "True", fill = "both")
        
    
class SongTextFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        # attributes
        self.song_text_frame = tk.Frame(self)
        self.song_text_canvas = Canvas(self.song_text_frame, scrollregion = (0, 0, 500, 1800))
        self.song_text_vertical_bar = Scrollbar(self.song_text_frame, orient = "vertical", command = self.song_text_canvas.yview)

        self.__create_widgets()

    def __create_widgets(self):
        self.song_text_canvas.config(yscrollcommand = self.song_text_vertical_bar.set)
        self.song_text_canvas.configure(bg = bg_color_canvas)
        self.song_text_frame.pack(expand = "True", fill = "both", side = "right")
        self.song_text_vertical_bar.pack(side = "right", fill = "y")
        self.song_text_canvas.pack(expand = "True", fill = "both")


class App(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        #color for text
        global color_text
        color_text = "#ffffff"

        #bgcolor for canvas
        global bg_color_canvas
        bg_color_canvas = "#5e269d" 

        #font & bgcolor for button
        self.font_btn =('Lao UI', 14)
        self.bg_btn = "#5e269d"
        #font for title
        self.font_title = ('MS Serif',22,'bold')

        #font for text
        self.font_text = ('Comic Sans MS',16,'italic')

        #font for warnings
        self.font_warning = ('Courier New',16,'bold')


        # @Attribute
        self.year_chosen = tk.StringVar()
        self.rankings = open("src/Rankings.json")
        self.rankings_data = json.load(self.rankings) 
        self.songs_text = open("src/Songs_text.json")
        self.songs_text_data = json.load(self.songs_text)
        self.radVar = tk.IntVar()
        self.radVar.set(99) #Select a non-existing index value for radVar
        self.app_frame = tk.Frame(win, bg = "dark blue")

        # create the Ranking frame and the Song text frame instances
        self.ranking_instance = RankingFrame(self.app_frame)
        self.song_text_instance = SongTextFrame(self.app_frame)
        
        self.__create_widgets()

    def __create_widgets(self):
        self.app_frame.pack(expand = "True", fill = "both")
        
        select_year = ttk.Combobox(self.app_frame, state = 'readonly')
        select_year.set("Choose a year:")
        select_year['values'] = (2022, 2021, 2020)
        select_year.bind("<<ComboboxSelected>>", self.show_ranking)
        select_year.place(relheight = 0.03, relwidth = 0.1, relx = 0.150, rely = 0.04)
        select_year.configure(font= (self.font_btn))
             
        # button that opens song's url into browser window
        video_button = tk.Button(self.app_frame, text = "Go to video", font = (self.font_btn), fg = color_text, bg = self.bg_btn ,command = self.show_video)
        video_button.config(highlightthickness = 0, activebackground= self.bg_btn,activeforeground = color_text)
        video_button.place(relheight = 0.03, relwidth = 0.08, relx = 0.550, rely = 0.04)
        

		# button that displays song's text inside frame
        text_button = tk.Button(self.app_frame, text = "Show text", font = (self.font_btn), fg = color_text, bg = self.bg_btn, command = self.show_text)
        text_button.config(highlightthickness = 0, activebackground= self.bg_btn,activeforeground = color_text)
        text_button.place(relheight = 0.03, relwidth = 0.08, relx = 0.690, rely = 0.04)
		
        # button that hides song's text inside frame
        hide_button = tk.Button(self.app_frame, text = "Hide text", font = (self.font_btn), fg = color_text, bg = self.bg_btn, command = self.hide_text)
        hide_button.config(highlightthickness = 0, activebackground= self.bg_btn,activeforeground = color_text)
        hide_button.place(relheight = 0.03, relwidth = 0.08, relx = 0.830, rely = 0.04)
    
    def song_choice(self):     
        song_chosen = self.radVar.get()
        return song_chosen
    
    def show_ranking(self, event):
        self.year_chosen = event.widget.get()
        rank_canvas = self.ranking_instance.rank_canvas
        rank_canvas.delete("all")
        self.ranking_instance.place(relheight = 0.78, relwidth = 0.4, relx = 0.02, rely = 0.2)
        rank_canvas.create_text(250, 40, text = "Ranking",font = self.font_title, fill = color_text )
        
        
        
        posizione_classifica = 1
        pos_y = 74
        for canzone in self.rankings_data[self.year_chosen]:
            dati_canzone = str(posizione_classifica) + " \"" + canzone['title'] + "\" " + canzone['singer']
            curRad = tk.Radiobutton(rank_canvas, text = dati_canzone, font = (self.font_text), fg = color_text, variable = self.radVar, value = posizione_classifica - 1, command = self.song_choice, bg = bg_color_canvas)
            curRad.config( highlightthickness=0, activebackground= bg_color_canvas, activeforeground = "#46ebfc")
            curRad.place(x = 20, y = pos_y)
            rank_canvas.create_window(20, pos_y, anchor = 'w', window = curRad, height = 30)
            
            pos_y = pos_y + 25
            posizione_classifica = posizione_classifica + 1
       
    def show_text(self):
        text_canvas = self.song_text_instance.song_text_canvas
        text_vbar = self.song_text_instance.song_text_vertical_bar 
        num_canzone_scelta = self.song_choice()
        text_canvas.delete("all")
        self.song_text_instance.place(relheight = 0.78, relwidth = 0.4, relx = 0.58, rely = 0.2)
        text_vbar.pack(side = "right", fill = "y")
        if num_canzone_scelta == 99:
            text_canvas.create_text(260, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = (self.font_warning))
        else:
            text_canvas.create_text(260, 40, text = "Song text", font = (self.font_title), fill = color_text)
            canzone = self.songs_text_data[self.year_chosen][num_canzone_scelta]["song_text"]
            self.song_text_id = text_canvas.create_text(248, 74, text = canzone, font = (self.font_text), fill = color_text, justify = "center", anchor = "n")

    def hide_text(self):
        text_canvas = self.song_text_instance.song_text_canvas
        text_canvas.delete(self.song_text_id)
    
    def show_video(self):
        text_canvas = self.song_text_instance.song_text_canvas
        num_canzone_scelta = self.song_choice()
        if num_canzone_scelta == 99:
            text_canvas.create_text(300, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = (self.font_warning))
        else:
            canzoni = self.rankings_data[self.year_chosen]
            webbrowser.open_new(canzoni[num_canzone_scelta]['url'])
    
if __name__ == "__main__":
    app = App(win)
    app.mainloop()
