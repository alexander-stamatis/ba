#!/usr/bin/env python3.9
#
# settings.py
#

'''
Loads settings such as key bindings, strum rate, and main while loop rate from settings.json file
'''

from genericpath import exists
import json


class Settings:
    def __init__(self):
        self.key_bindings = {}
        self.play_note_on_directional_release = False
        self.data_clock = .01
        self.port = None

        if exists('settings.json'):
            settings_file = open('settings.json')
            data = json.load(settings_file)
            settings_file.close()
            self.port = int(data['settings']['default_midi_input'])
            data_key_bindings = data['key_bindings']
            if data['settings']['play_note_on_directional_release'] == str.capitalize("TRUE"):
                self.play_note_on_directional_release = True
            else:
                self.play_note_on_directional_release = False
            for item in data_key_bindings:
                self.key_bindings.__setitem__(
                    int(item), str.lower(data_key_bindings[item]))
                self.data_clock = float(data['settings']['clock'])

        self.key_bindings_values = list(self.key_bindings.values())
        self.key_bindings_keys = list(self.key_bindings.keys())

    def SaveDefaultMidiInput(input):
        settings_file = open('settings.json')
        data = json.load(settings_file)
        data['settings']['default_midi_input'] = str(input)
        with open('settings.json', 'w') as settings_file:
            settings_file.write(json.dumps(data))
