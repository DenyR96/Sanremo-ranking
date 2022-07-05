import tkinter
from pytest_mock import MockerFixture
from src.common_variables import win, os_name
import src.music_player as mp
import platform




def test_load(mocker:MockerFixture) -> None:
    mocker.patch.object(mp, "os", return_value = {})
    spy_open = mocker.spy(mp.os, "open")
    mocker.patch.object(mp, "os", return_value = {})
    spy_write = mocker.spy(mp.os, "write")
    
    win = tkinter.Tk()
    win.withdraw()
    music_player = mp.MusicPlayer(win)
    music_player.load('2022', 0)
    mock_song_title = 'Brividi'
    assert music_player.song_title == mock_song_title 
    mock_mp3_link = "https://denyr96.github.io/Sanremo-ranking/assets/songs/2022/Brividi.mp3"
    assert music_player.mp3_link == mock_mp3_link
    mock_os_name = platform.system()
    assert os_name == mock_os_name 
    assert music_player.play_button['state'] == 'active'
    assert music_player.pause_button['state'] == 'disabled'
    assert music_player.stop_button['state'] == 'disabled'

    assert spy_open.called_once_with(music_player.file_path)
    assert spy_write.called_once_with(music_player.mp3_file)


def test_play(mocker:MockerFixture) -> None:
    mocker.patch.object(mp, "os", return_value = {})
    spy = mocker.spy(mp.os, "path.isfile")

    win = tkinter.Tk()
    win.withdraw()
    music_player = mp.MusicPlayer(win)
    mock_path = 'assets/songs/file.mp3'
    music_player.file_path = mock_path

    assert music_player.playing_state == False
    music_player.play()
    assert music_player.play_button['state'] == 'disabled'
    assert music_player.pause_button['state'] == 'active'
    assert music_player.stop_button['state'] == 'active'
    assert music_player.playing_state == True
    assert music_player.pause_resume.get() == 'Pause'

    win.destroy()

    assert spy.called_once_with(mock_path)


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

    