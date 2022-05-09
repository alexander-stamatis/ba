#!/usr/bin/env python3.9
#
# message.py
#
''' 
Midi message structure
'''

from enum import Enum


class NoteType(Enum):
    PRESS = 144
    RELEASE = 128

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Message():
    def __init__(self, message) -> None:
        if len(message[0]) == 3:
            if NoteType.has_value(message[0][0]):
                self.type = NoteType(message[0][0])
            else:
                return None
            self.note = message[0][1]
            self.velocity = message[0][2]
