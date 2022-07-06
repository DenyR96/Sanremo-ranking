import tkinter as tk
from src.common_variables import color_canvas
import src.ranking_frame as rf


def test_ranking_frame() -> None:
    mock_constructor_frame = tk.Frame()
    ranking_frame_instance = rf.RankingFrame(mock_constructor_frame)

    assert isinstance(ranking_frame_instance.rank_frame, tk.Frame) == True 
    assert isinstance(ranking_frame_instance.rank_canvas, tk.Canvas) == True
    assert isinstance(ranking_frame_instance.rank_vertical_bar, tk.Scrollbar) == True
    assert isinstance(ranking_frame_instance.rank_title, tk.Label) == True


def test_create_widgets() -> None:
    mock_constructor_frame = tk.Frame()
    ranking_frame_instance = rf.RankingFrame(mock_constructor_frame)

    assert ranking_frame_instance.rank_canvas.cget('bg') == color_canvas
    assert ranking_frame_instance.rank_canvas.cget('highlightbackground') == color_canvas
    assert ranking_frame_instance.rank_frame.pack_info()['expand'] == True
    assert ranking_frame_instance.rank_frame.pack_info()['fill'] == "both"
    assert ranking_frame_instance.rank_frame.pack_info()['side'] == "left"
    assert ranking_frame_instance.rank_vertical_bar.pack_info()['side'] == "right"
    assert ranking_frame_instance.rank_vertical_bar.pack_info()['fill'] == "y"
    assert ranking_frame_instance.rank_canvas.pack_info()['expand'] == True
    assert ranking_frame_instance.rank_canvas.pack_info()['fill'] == "both"