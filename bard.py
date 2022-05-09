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

if __name__ == "__main__":
    gc.enable()

    settings = Settings()

    midiin = rtmidi.MidiIn(get_api_from_environment(rtmidi.API_UNSPECIFIED))

    keyboard = Controller()

    log = logging.getLogger('midiin_poll')
    logging.basicConfig(level=logging.DEBUG)

    strum = .5
    pressedNotesStack = list()
    releasedNotesStack = list()
    step = 1
    timer = step

    if midiin != None:
        midiin.close_port()
        midiin = None

    port = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    def GetKey(message):
        if message in settings.key_bindings:
            if message:
                if message > 0 and message != 127:
                    return settings.key_bindings[message]

    def handleMessage(message):
        if message.type == NoteType.PRESS:
            keyboard.press(GetKey(message.note))
        elif message.type == NoteType.RELEASE:
            keyboard.release(GetKey(message.note))

    def getMidiInput(messages):
        midiin_message = midiin.get_message()
        if midiin_message:
            MSG = Message(midiin_message)
            if MSG and MSG.type != None:
                if MSG.note in settings.key_bindings_keys:
                    messages.append(MSG)
                    if strum == 0:
                        handleMessage(MSG)
                return getMidiInput(messages)
        else:
            return messages

    try:
        while True:
            messages = getMidiInput(list())

            # strum
            if abs(strum) != 0:
                timer += abs(strum)
                if messages:
                    if messages[0].type is NoteType.PRESS:
                        if len(pressedNotesStack) == 0:
                            for m in messages:
                                if strum < 0:
                                    pressedNotesStack.append(m)
                                else:
                                    pressedNotesStack.insert(0, m)
                    if messages[0].type is NoteType.RELEASE:
                        if len(releasedNotesStack) == 0:
                            for m in messages:
                                if strum < 0:
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
