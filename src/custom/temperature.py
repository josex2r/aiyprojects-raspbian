import aiy.voicehat
import logging
# Load sensor libs
import Adafruit_DHT

# Temperature: Gets data from DHT22
# ================================
# Retrieve the sensor data and say it
#

def say_temperature():
    aiy.audio.say('Let me check it')
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    message = '{0:d} degrees and {1:d} percent of humidity'.format(int(temperature), int(humidity))
    logging.info(message)
    aiy.audio.say(message)

