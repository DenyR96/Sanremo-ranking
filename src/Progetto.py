import tkinter as tk
from tkinter import Canvas, Scrollbar, ttk
import json
import webbrowser

win = tk.Tk()
win.title('Sanremo Rankings')
win.state("zoomed")
win.resizable(False, False)

# window dimensions
window_width = win.winfo_width()
window_height = win.winfo_height()
		
class RankingFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        
        self.__create_widgets()

    def __create_widgets(self):
        rank_frame = tk.Frame(self)
        rank_vertical_bar = Scrollbar(rank_frame, orient = "vertical")
        rank_canvas = Canvas(rank_frame, scrollregion = (0, 0, 600, 800))
        rank_canvas.config(yscrollcommand = rank_vertical_bar.set)
        rank_canvas.configure(bg = "light blue")
        rank_vertical_bar.config(command = rank_canvas.yview)
        rank_frame.pack(expand = "True", side = "left", anchor = "n", pady = (0,10))
        rank_vertical_bar.pack(side = "right", fill = "y")
        rank_canvas.pack()

class SongTextFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        
        # frame dimensions
        self.frame_width = 600
        self.frame_height = 600
        
        self.__create_widgets()

    def __create_widgets(self):
        song_text_frame = tk.Frame(self)
        song_text_vertical_bar = Scrollbar(song_text_frame, orient = "vertical")
        song_text_canvas = Canvas(song_text_frame, width = self.frame_width, height = self.frame_height, scrollregion = (0, 0, 500, 1100))
        song_text_canvas.config(yscrollcommand = song_text_vertical_bar.set)
        song_text_canvas.configure(bg = "light blue")
        song_text_vertical_bar.config(command = song_text_canvas.yview)
        song_text_frame.pack(expand = "True", fill = "both", side = "right", anchor = "n", pady = (0,10))
        song_text_vertical_bar.pack(side = "right", fill = "y")
        song_text_canvas.pack()
        
class App(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
         # @Attribute
        self.year_chosen = tk.StringVar()
        self.classifiche = open("C:/Users/Deny/mio-progetto/Sanremo-ranking/src/Rankings.json")
        self.dati_classifiche = json.load(self.classifiche) 
        self.radVar = tk.IntVar()
        self.radVar.set(99) #Select a non-existing index value for radVar

        # create the Ranking frame
        self.ranking_instance = RankingFrame()
        self.ranking_instance.place(relheight = 0.7, relwidth = 0.4, relx = 0.05, rely = 0.2) #x = 20, y = 120)

        # create the Song text frame
        self.song_text_instance = SongTextFrame()
        self.song_text_instance.place(relheight = 0.7, relwidth = 0.4, relx = 0.6, rely = 0.2) #x = 960, y = 120)

        self.__create_widgets()

    def __create_widgets(self):
        app_frame = tk.Frame(win, bg = "dark blue")
        app_frame.pack(expand = "True", fill = "both")
        app_frame.pack_propagate(0)
        
        select_year = ttk.Combobox(app_frame, state = 'readonly')
        select_year.set("Choose a year:")
        select_year['values'] = (2022, 2021, 2020)
        select_year.bind("<<ComboboxSelected>>", self.show_ranking)
        select_year.place(relheight = 0.03, relwidth = 0.1, relx = 0.150, rely = 0.04)

        # button that opens song's url into browser window
        video_button = tk.Button(app_frame, text = "Go to video", command = self.show_video)
        video_button.place(relheight = 0.03, relwidth = 0.08, relx = 0.550, rely = 0.04)
        
		# button that displays song's text inside frame
        text_button = tk.Button(app_frame, text = "Show text", command = self.show_text)
        text_button.place(relheight = 0.03, relwidth = 0.08, relx = 0.690, rely = 0.04)
		
        # button that hides song's text inside frame
        hide_button = tk.Button(app_frame, text = "Hide text", command = self.hide_text)
        hide_button.place(relheight = 0.03, relwidth = 0.08, relx = 0.830, rely = 0.04)
    
    def song_choice(self):     
        song_chosen = self.radVar.get()
        return song_chosen
     
    def draw_radio_button(self, rank_canvas, lunghezza_classifica):
        pos_y = 75
        for numero_canzone in range(lunghezza_classifica):
            curRad = tk.Radiobutton(rank_canvas, variable = self.radVar, value = numero_canzone, command = self.song_choice)
            curRad.place(x = 5, y = pos_y)
            pos_y = pos_y + 20

    def show_ranking(self, event):
        self.year_chosen = event.widget.get()
        self.rank_canvas = self.get_rank_frame_widget(tk.Canvas)
        self.rank_canvas.delete("all")
        self.rank_canvas.create_text(300, 40, text = "Ranking", font = ('sans-serif', '18', 'bold'))
        
        posizione_classifica = 1
        pos_y = 85
        for canzone in self.dati_classifiche[self.year_chosen]:
            dati_canzone = str(posizione_classifica) + " \"" + canzone['title'] + "\" " + canzone['singer']
            self.rank_canvas.create_text(300, pos_y, text = dati_canzone, font = ('sans-serif', '14'))
            pos_y = pos_y + 25
            posizione_classifica = posizione_classifica + 1
            self.draw_radio_button(self.rank_canvas, len(self.dati_classifiche[self.year_chosen]))
        
    def get_rank_frame_widget(self, widget_class_name):
        for widget in self.ranking_instance.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, widget_class_name):
                        return child
    
    def get_song_text_widget(self, widget_class_name):
        for widget in self.song_text_instance.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, widget_class_name):
                        return child

    def get_song_text_frame(self):
        for widget in self.song_text_instance.winfo_children():
            if isinstance(widget, tk.Frame):
                return widget 

    def get_rank_frame(self):
        for widget in self.ranking_instance.winfo_children():
            if isinstance(widget, tk.Frame):
                return widget 

    def show_video(self):
        text_canvas = self.get_song_text_widget(tk.Canvas)
        num_canzone_scelta = self.song_choice()
        if num_canzone_scelta == 99:
            text_canvas.create_text(300, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = ('Helvetica', '15','bold'))
        else:
            canzoni = self.dati_classifiche[self.year_chosen]
            webbrowser.open_new(canzoni[num_canzone_scelta]['url'])
    
    def show_text(self):
        text_canvas = self.get_song_text_widget(tk.Canvas)
        text_frame = self.get_song_text_frame()
        text_vbar = self.get_song_text_widget(tk.Scrollbar)
        num_canzone_scelta = self.song_choice()
        text_canvas.delete("all")
        text_frame.pack_forget()
        text_frame.pack(expand = "True", side = "right", anchor = "n", pady = (60, 0))
        text_vbar.pack(side = "right", fill = "y")
        if num_canzone_scelta == 99:
            text_canvas.create_text(300, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = ('Helvetica', '15','bold'))
        else:
            print(num_canzone_scelta)
            text_canvas.create_text(300, 40, text = "Song text", font = ('Helvetica', '15','bold'))
            text_canvas.create_text(250, 85, text = "ciao"+str(num_canzone_scelta), font = ('Helvetica', '12'))

        text_canvas.pack()

    def hide_text(self):
        text_canvas = self.get_song_text_widget(tk.Canvas)
        text_frame = self.get_song_text_frame()
        text_canvas.delete("all")
        text_frame.pack_forget()
    
#if __name__ == "__main__":
app = App(win)
app.mainloop()
