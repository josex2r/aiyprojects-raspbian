import logging
import subprocess

# Temperature: Gets data from Youtube
# ================================
# Retrieve the song data and play it
#

class Youtube(object):

    """Plays Youtube song"""

    def __init__(self, say, keyword):
        self.say = say
        self.keyword = keyword

    def run(self, voice_command):
        getattr(self, self.keyword)(voice_command)

    def stop(self, voice_command):
        subprocess.Popen(['/usr/bin/pkill', 'vlc'], stdin=subprocess.PIPE)

    def play(self, voice_command):
        song = voice_command.replace(self.keyword, '', 1)
        logging.info('Playing song: ', song)
        self.say('Downloading ' + song)
        song_player = subprocess.Popen(['/usr/local/bin/mpsyt', ''], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # Search the song
        song_player.stdin.write(bytes('/' + song + '\n', 'utf-8'))
        # Select the first song
        song_player.stdin.write(bytes('1\n', 'utf-8'))
        song_player.stdin.flush()
