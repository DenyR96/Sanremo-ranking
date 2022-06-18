import tkinter as tk
from tkinter import ANCHOR, Canvas, Scrollbar, ttk
import json
import webbrowser


class RankingFrame(ttk.Frame):

    
    def __init__(self, container):
        super().__init__(container)
        
        # ranking  frame dimensions
        self.frame_width = 600
        self.frame_height = 600
    
        
        self.__create_widgets()

    def __create_widgets(self):
        # FrameRanking
        rank_frame = ttk.Frame(self)
        rank_vertical_bar = Scrollbar(rank_frame, orient = "vertical")
        rank_canvas = Canvas(rank_frame, width = self.frame_width, height = self.frame_height, scrollregion = (0, 0, 600, 800))
        rank_canvas.config(yscrollcommand = rank_vertical_bar.set)
        rank_canvas.configure(bg = "light blue")
        rank_vertical_bar.config(command = rank_canvas.yview)
        rank_frame.pack(expand = "True", side = "left", anchor = "n", pady = (0,10))
        rank_vertical_bar.pack(side = "right", fill = "y")
        rank_canvas.pack()
        
        

class SongTextFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        # song_text  frame dimensions
        self.frame_width = 600
        self.frame_height = 600
        self.__create_widgets()

    def __create_widgets(self):
        
        # FrameSongText
        song_text_frame = ttk.Frame(self)
        song_text_vertical_bar = Scrollbar(song_text_frame, orient = "vertical")
        song_text_canvas = Canvas(song_text_frame, width = self.frame_width, height = self.frame_height, scrollregion = (0, 0, 500, 1100))
        song_text_canvas.config(yscrollcommand = song_text_vertical_bar.set)
        song_text_canvas.configure(bg = "light blue")
        song_text_vertical_bar.config(command = song_text_canvas.yview)
        song_text_frame.pack(expand = "True", side = "right", anchor = "n", pady = (0,10))
        song_text_vertical_bar.pack(side = "right", fill = "y")
        song_text_canvas.pack()
        

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sanremo Rankings')
        
        #configure the root window
        window_width = 1600        
        window_height = 750
		
		# get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
		
		# find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

		# set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        

        
        
        # @Attribute
        self.year_chosen = tk.StringVar()
        self.classifiche = open("src/Rankings.json")
        self.dati_classifiche = json.load(self.classifiche) 
        self.radVar = tk.IntVar()
        self.radVar.set(99) #Select a non-existing index value for radVar



        # create the Ranking frame
        self.ranking_instance = RankingFrame(self)
        self.ranking_instance.place(x = 20, y = 120 )

        #access to child element
        #list_widget = self.ranking_instance.winfo_children()
       
        
        
        # create the Song text frame
        self.song_text_instance = SongTextFrame(self)
        self.song_text_instance.place(x = 970, y = 120)  
        

        self.__create_widgets()

    def __create_widgets(self):
        
    
          


        
		#current_year = tk.StringVar()
        self.select_year = ttk.Combobox(self, width = 20, state = 'readonly')
        self.select_year['values'] = ("choose a year",2022, 2021, 2020)
        self.select_year.place(x = 0, y = 20)
        self.select_year.pack()
        self.select_year.bind("<<ComboboxSelected>>",self.show_ranking)        
        # button that opens song's url into browser window
        self.video_button = ttk.Button(self, text = "Go to video")  
        self.video_button.place(x = 700, y = 20)
        self.video_button.pack()
        self.video_button['command'] = self.show_video
        
		
		# button that displays song's text inside frame
        self.text_button = ttk.Button(self, text = "Show text")
        #self.text_button.place(x = 850, y = 20)
        self.text_button.pack()
        self.text_button['command'] = self.show_text
		# button that hides song's text inside frame
        self.hide_button = ttk.Button(self, text = "Hide text")
        #self.hide_button.place(x = 1000, y = 20)
        self.hide_button.pack()
        self.hide_button['command'] = self.hide_text
    

    def song_choice(self):     
        song_chosen = self.radVar.get()
        return song_chosen



     
    def draw_radio_button(self,rank_canvas,lunghezza_classifica):
    
        pos_y = 75
        for numero_canzone in range(lunghezza_classifica):
            curRad = tk.Radiobutton(rank_canvas, variable = self.radVar, value = numero_canzone , command = self.song_choice)
            curRad.place(x = 5, y = pos_y)
            pos_y = pos_y + 20


    def show_ranking(self,event):
         
        self.year_chosen = event.widget.get()
        rank_canvas = self.get_rank_frame_widget(tk.Canvas) 
        rank_canvas.delete("all")
        rank_canvas.create_text(300, 40, text = "Ranking", font = ('sans-serif', '18','bold'))
        posizione_classifica=1
        pos_y = 85
        
        for canzone in self.dati_classifiche[self.year_chosen]:
            dati_canzone = str(posizione_classifica) + " \"" + canzone['title'] + "\" " + canzone['singer']
            rank_canvas.create_text(300, pos_y, text = dati_canzone, font = ('sans-serif', '14') ,  )
            pos_y = pos_y + 25
            posizione_classifica = posizione_classifica + 1
            self.draw_radio_button(rank_canvas,len(self.dati_classifiche[self.year_chosen]))        
    def get_rank_frame_widget(self,widget_class_name):

        for widget in self.ranking_instance.winfo_children():
            #print(widget)
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, widget_class_name):
                        return child
    
    def get_song_text_widget(self,widget_class_name):

        for widget in self.song_text_instance.winfo_children():
            #print(widget)
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, widget_class_name):
                        return child

    def get_song_text_frame(self):

        for widget in self.song_text_instance.winfo_children():
            
            if isinstance(widget, ttk.Frame):
                return widget 

    def get_rank_frame(self):

        for widget in self.ranking_instance.winfo_children():
            
            if isinstance(widget, ttk.Frame):
                return widget 



    def show_video(self):
        text_canvas = self.get_song_text_widget(tk.Canvas)
        num_canzone_scelta = self.song_choice()
        if num_canzone_scelta == 99: text_canvas.create_text(300, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = ('Helvetica', '15','bold'))
        else:
            canzoni=self.dati_classifiche[self.year_chosen]
            webbrowser.open_new(canzoni[num_canzone_scelta]['url'])
    
    def show_text(self):
        text_canvas = self.get_song_text_widget(tk.Canvas)
        text_frame = self.get_song_text_frame()
        text_vbar =  self.get_song_text_widget(tk.Scrollbar)
        num_canzone_scelta = self.song_choice()
        text_canvas.delete("all")
        text_frame.pack_forget()
        text_frame.pack(expand = "True", side = "right", anchor = "n", pady = (60, 0))
        text_vbar.pack(side = "right", fill = "y")
        if num_canzone_scelta == 99: text_canvas.create_text(300, 60, fill = "red", text = "PLEASE, SELECT A SONG FIRST!", font = ('Helvetica', '15','bold'))
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
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
