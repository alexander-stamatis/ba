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
        self.scales = {}
        self.data_clock = .01

        if exists('settings.json'):
            settings_file = open('settings.json')
            data = json.load(settings_file)
            settings_file.close()
            data_key_bindings = data['key_bindings']
            for item in data_key_bindings:
                self.key_bindings.__setitem__(
                    int(item), str.lower(data_key_bindings[item]))
                self.data_clock = float(data['settings']['clock'])
            self.strum = float(data['settings']['strum'])
            self.key_bindings_values = list(self.key_bindings.values())
            self.key_bindings_keys = list(self.key_bindings.keys())
            self.active_scale = str(data['settings']['active_scale'])
            data_scales = data['scales']
            for scale in data_scales:
                self.scales.__setitem__(
                    str(scale), data_scales[scale])
            self.active_scale_notes = []
            for note in self.scales[self.active_scale]:
                self.active_scale_notes.append(note)

    def SaveDefaultMidiInput(input):
        settings_file = open('settings.json')
        data = json.load(settings_file)
        data['settings']['default_midi_input'] = str(input)
        with open('settings.json', 'w') as settings_file:
            settings_file.write(json.dumps(data))
