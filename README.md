# 🎵 Bard : MIDI Input to Keyboard


## Description

Created as an alternative to BOME for use in FFXIV as a bard. 
Bard.py lets you use any MIDI device like a piano keyboard, convert it to computer keyboard inputs, and play music in FFXIV.

## Instructions
1) Install <a href="https://www.python.org/downloads/">Python</a>
2) Download the <a href="https://github.com/astamatis/bard/releases/tag/v0.1.0" target="blank_">source code</a>
3) Configure the <a href="https://github.com/astamatis/bard/blob/main/settings.json" target="blank_">settings.json</a> file
  - *I have configured the file to work with Bard Music Player for FFXIV and the bard instruments in the game. 
  All FFXIV instruments use 3 octaves, C4 - C6 or notes 48 - 84. My C4 note (48) will trigger 'Q'*
4) Run bard.py
5) Choose your input device and bard.py will run in the background

<img src="https://github.com/astamatis/bard/blob/main/docs/bard-powershell.jpg" alt="Bard in terminal" />


## Features
- Strum : FFXIV instruments have one voice and can play only one note at a time. Strumming helps when trying to press notes simultaneously like a chord. Configurable in the settings.json file. Use '0' to remove strum. A positive value like '.01' strums notes from left to right. A negative value will do it in reverse. The lower the value, the longer the delay between each note.

## Upcoming features
- Graphical User Interface similar to BOME
- Executable file instead of a python script
- Scale and chord mode
