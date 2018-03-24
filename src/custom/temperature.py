import aiy.voicehat
# Load sensor libs
# from 'adafruit-dht' import Adafruit_DHT
Adafruit_DHT = __import__('adafruit-dht')

# Temperature: Gets data from DHT22
# ================================
# Retrieve the sensor data and say it
#

def say_temperature():
    aiy.audio.say('Let me check it')
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    aiy.audio.say('{0:d} degrees and {1:d} percent of humidity'.format(int(temperature), int(humidity)))

