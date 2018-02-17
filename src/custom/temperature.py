# Load sensor libs
import Adafruit_DHT

# Temperature: Gets data from DHT22
# ================================
# Retrieve the sensor data and say it
#

class Temperature(object):

    """Gets data from DHT22."""

    def __init__(self, say):
        self.sensor = Adafruit_DHT.DHT22
        self.pin = 4
        self.say = say

    def run(self, voice_command):
        self.say('Let me check it')
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        self.say('{0:d} degrees and {1:d} percent of humidity'.format(int(temperature), int(humidity)))
        # self.say('{0:0.1f} degrees and {1:0.1f} percent of humidity'.format(temperature, humidity))
