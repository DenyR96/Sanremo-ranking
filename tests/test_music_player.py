
import tkinter
from pytest_mock import MockerFixture
from src.music_player import MusicPlayer
from src.common_variables import win
from src.main import Main
import os



def test_pause(mocker:MockerFixture) -> None:
    win = tkinter.Tk()
    win.withdraw()
    music_player = MusicPlayer(win)
    assert music_player.playing_state == False
    music_player.pause()
    assert music_player.playing_state == True
    assert music_player.pause_resume.get() == 'Pause'
    music_player.pause()
    assert music_player.pause_resume.get() == 'Resume'
    assert music_player.playing_state == False
    win.destroy()

"""def test_stop(mocker:MockerFixture) -> None:
    win = tkinter.Tk()
    win.withdraw()
    music_player = MusicPlayer(win)
    assert music_player.playing_state == False #perchè lo stato di default è a false
    mock_close_val = None
    mocker.patch.object(music_player, "os", return_value=mock_close_val)
    spy = mocker.spy(music_player, "os.close")
    res = music_player.stop()
    
    assert music_player.playing_state == False #perchè stop() mette a false lo stato
    assert music_player.play_button['state'] == 'active'
    assert music_player.pause_button['state'] == 'disabled'
    assert music_player.stop_button['state'] == 'disabled'
    
    assert res is None
    assert spy.call_count == 1
    assert spy.spy_return == mock_close_val
    win.destroy()"""