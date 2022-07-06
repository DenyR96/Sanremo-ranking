from tkinter import *
import tkinter as tk
from tkinter import Canvas, Scrollbar
from src.common_variables import color_canvas, color_text, font_text, font_title, win
from pytest_mock import MockerFixture
import src.song_text_frame as stf

def test_song_text_frame(mocker:MockerFixture) -> None:
    mock_constructor_frame = tk.Frame()
    song_text_instance = stf.SongTextFrame(mock_constructor_frame)
     
    assert isinstance(song_text_instance.song_text_frame, tk.Frame) == True 
    assert isinstance(song_text_instance.song_text_canvas, tk.Canvas) == True  
    assert isinstance(song_text_instance.song_text_vertical_bar, tk.Scrollbar) == True
    assert isinstance(song_text_instance.text_title, tk.Label) == True
    assert isinstance(song_text_instance.song_text, tk.Label) == True
    
def test_create_widgets(mocker:MockerFixture) -> None:
    mock_constructor_frame = tk.Frame()
    song_text_instance = stf.SongTextFrame(mock_constructor_frame)
    assert song_text_instance.song_text_canvas.cget('bg') == color_canvas
    assert song_text_instance.song_text_canvas.cget('highlightbackground') == color_canvas
    assert song_text_instance.song_text_frame.pack_info()['expand'] == True
    assert song_text_instance.song_text_frame.pack_info()['fill'] == "both"
    assert song_text_instance.song_text_frame.pack_info()['side'] == "right"
    assert song_text_instance.song_text_vertical_bar.pack_info()['side'] == "right"
    assert song_text_instance.song_text_vertical_bar.pack_info()['fill'] == "y"
    assert song_text_instance.song_text_canvas.pack_info()['expand'] == True
    
    




