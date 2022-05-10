#!/usr/bin/env python3.9
#
# bard.py
#
'''
Converts MIDI input to computer keyboard input
'''
import gc
import sys
import time
import logging
import rtmidi
from rtmidi.midiutil import open_midiinput
from rtmidi.midiutil import *
from pynput.keyboard import Controller
from settings import Settings
from message import Message, NoteType


class Key():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


if __name__ == "__main__":
    gc.enable()

    settings = Settings()

    midiin = rtmidi.MidiIn(get_api_from_environment(rtmidi.API_UNSPECIFIED))

    keyboard = Controller()

    log = logging.getLogger('midiin_poll')
    logging.basicConfig(level=logging.DEBUG)

    pressedNotesStack = list()
    releasedNotesStack = list()
    step = 1
    timer = step

    print("\n", "The scale selected is:", settings.active_scale, "\n",
          "Active notes:", settings.scales[settings.active_scale], "\n")

    keys = [
        Key("C"),
        Key("C#"),
        Key("D"),
        Key("D#"),
        Key("E"),
        Key("F"),
        Key("F#"),
        Key("G"),
        Key("A#"),
        Key("A"),
        Key("A#"),
        Key("B")
    ]

    for index in range(len(keys)):
        if index == 0:
            keys[index].left = keys[len(keys) - 1]
        elif index == len(keys) - 1:
            keys[index].right = keys[0]
        if keys[index].left == None:
            keys[index].left = keys[index - 1]
        if keys[index].right == None:
            keys[index].right = keys[index + 1]
        if midiin != None:
            midiin.close_port()
            midiin = None

    port = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    def GetNote(message):
        return keys[message % 12].value

    def FlatToSharp():
        converted = []
        for n in settings.active_scale_notes:
            if n.strip().__contains__('b'):
                for k in keys:
                    if k.value == n[0]:
                        converted.append(k.left.value)
            else:
                converted.append(n)
        return converted

    convertedKeys = FlatToSharp()

    def GetKey(message):
        if message in settings.key_bindings:
            if message:
                if message > 0 and message != 127:
                    if settings.active_scale == "Chromatic":
                        return settings.key_bindings[message]
                    else:
                        note = GetNote(message)
                        if note in convertedKeys:
                            return settings.key_bindings[message]
                        else:
                            starting_point = None
                            for k in keys:
                                if k.value == GetNote(message):
                                    starting_point = k
                            offset = 0
                            while starting_point.value not in convertedKeys:
                                starting_point = starting_point.left
                                offset += 1
                            try:
                                return settings.key_bindings[message - offset]
                            except:
                                return None

    def handleMessage(message):
        key = GetKey(message.note)
        if key != None:
            if message.type == NoteType.PRESS:
                keyboard.press(key)
            elif message.type == NoteType.RELEASE:
                keyboard.release(key)

    def getMidiInput(messages):
        midiin_message = midiin.get_message()
        if midiin_message:
            MSG = Message(midiin_message)
            if MSG:
                if MSG.type != None:
                    if MSG.note in settings.key_bindings_keys:
                        messages.append(MSG)
                        if settings.strum == 0:
                            handleMessage(MSG)
                    return getMidiInput(messages)
        else:
            return messages

    try:
        while True:
            messages = getMidiInput(list())

            # strum
            if abs(settings.strum) != 0:
                timer += abs(settings.strum)
                if messages:
                    if messages[0].type is NoteType.PRESS:
                        if len(pressedNotesStack) == 0:
                            for m in messages:
                                if settings.strum < 0:
                                    pressedNotesStack.append(m)
                                else:
                                    pressedNotesStack.insert(0, m)
                    if messages[0].type is NoteType.RELEASE:
                        if len(releasedNotesStack) == 0:
                            for m in messages:
                                if settings.strum < 0:
                                    releasedNotesStack.append(m)
                                else:
                                    releasedNotesStack.insert(0, m)

                if len(releasedNotesStack) > 0:
                    for releasedNote in releasedNotesStack:
                        handleMessage(releasedNote)
                        releasedNotesStack.remove(releasedNote)
                    for pressedNote in pressedNotesStack:
                        pressedNotesStack.remove(pressedNote)

                if timer > step and len(releasedNotesStack) == 0:
                    if len(pressedNotesStack) > 0:
                        handleMessage(
                            pressedNotesStack[len(pressedNotesStack) - 1])
                        pressedNotesStack.pop()
                        timer = 0

            time.sleep(settings.data_clock)
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin
