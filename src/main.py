#!/usr/bin/env python3

import logging
import platform
import subprocess
import sys
import os.path

import aiy.assistant.auth_helpers
import aiy.assistant.device_helpers
import aiy.audio
import aiy.voicehat
import aiy.i18n
from aiy.assistant.library import Assistant
from google.assistant.library.event import EventType

# Custom scripts
from custom.temperature import say_temperature
from custom.youtube import play_song
from custom.youtube import stop_song
from custom.dialogflow import call
from custom.madrid_opendata import get_timetable_for


aiy.i18n.set_language_code('en-GB')
# aiy.audio.set_tts_volume(100)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))


def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.set_trigger_sound_wave('sounds/google_notification.wav')

    if event.type == EventType.ON_START_FINISHED:
        print('ON_START_FINISHED')
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print('ON_CONVERSATION_TURN_STARTED')
        status_ui.status('listening')

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
            or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
            or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('ON_RECOGNIZING_SPEECH_FINISHED')
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text:
            flow_response = call(text)
            action = flow_response['result']['action']
        else:
            action = 'unknown'
        if 'unknown' not in action:
            print('Dialogflow action received:', action)
            assistant.stop_conversation()
            if action == 'temperature.inside':
                say_temperature()
            if action == 'timetable.bus':
                get_timetable_for(flow_response['result']['parameters']['number-integer'])
            if action == 'youtube.play':
                parameters = flow_response['result']['parameters']
                query = parameters['music-genre']
                if parameters['music-artist']:
                    query = parameters['music-artist']
                if parameters['any']:
                    query = parameters['any']
                if query:
                    play_song(query)
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif text == 'stop':
            assistant.stop_conversation()
            stop_song()

def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)

if __name__ == '__main__':
    main()
