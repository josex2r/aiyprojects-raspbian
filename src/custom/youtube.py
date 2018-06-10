import subprocess
import aiy.voicehat

def play_song(song):
    print('Playing song: ', song)
    aiy.audio.say('Downloading ' + song)
    song_player = subprocess.Popen(['/usr/local/bin/mpsyt', ''], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # Search the song
    song_player.stdin.write(bytes('/' + song + '\n', 'utf-8'))
    # Select the first song
    song_player.stdin.write(bytes('1\n', 'utf-8'))
    song_player.stdin.flush()


def stop_song():
    print('Stopping songs')
    vlc = subprocess.Popen(['/usr/bin/pkill', 'vlc'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    vlc.stdin.flush()

