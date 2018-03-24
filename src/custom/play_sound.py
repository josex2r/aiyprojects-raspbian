import os.path
import logging
import aiy.audio

def play_sound(path):
    sound_path = os.path.expanduser(path)
    sound_path = os.path.abspath(sound_path)
    if os.path.exists(sound_path):    
        logging.warning('File %s specified exist.',sound_path)
        aiy.audio.get_player().play_wav(sound_path)
    else:
        logger.warning('File %s specified does not exist.',sound_path)
