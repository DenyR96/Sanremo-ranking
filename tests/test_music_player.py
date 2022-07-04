import tkinter
from pytest_mock import MockerFixture
from src.common_variables import win
import src.music_player as mp

def test_pause(mocker:MockerFixture) -> None:
    win = tkinter.Tk()
    win.withdraw()
    music_player = mp.MusicPlayer(win)
    assert music_player.playing_state == False
    music_player.pause()
    assert music_player.playing_state == True
    assert music_player.pause_resume.get() == 'Pause'
    music_player.pause()
    assert music_player.pause_resume.get() == 'Resume'
    assert music_player.playing_state == False
    win.destroy()


def test_stop(mocker:MockerFixture) -> None:
    mocker.patch.object(mp, "os", return_value = {})
    spy = mocker.spy(mp.os, "close")

    win = tkinter.Tk()
    win.withdraw()
    music_player = mp.MusicPlayer(win)
    mock_audio_file = 'file.mp3'
    music_player.mp3_file = mock_audio_file

    assert music_player.playing_state == False #perchè lo stato di default è a false
    music_player.stop()
    assert music_player.playing_state == False #perchè stop() mette a false lo stato
    assert music_player.play_button['state'] == 'active'
    assert music_player.pause_button['state'] == 'disabled'
    assert music_player.stop_button['state'] == 'disabled'
    
    win.destroy()

    assert spy.called_once_with(mock_audio_file)