# APSC246-project: BoyGame™ Console

A custom-built handheld retro gaming console powered by a Rasbperry Pi 4. This project integrates hardware components such as a display, joystick, and push buttons to create an interactive gaming system. The prototype features Pong as the initial game, with plans to expand functionality and add additional games. The project focuses on hardware–software integration, GPIO input handling, and compact system design.

## Features
- Computer opponent with adjustable difficulty
- 8 sound effects & music
- Animated background (speed settings in the settings menu, off by default)
- Full main menu & setings menu
- Full Gameplay loop
- OOP (12 python classes)
- Deployable on any platform supporting Python (Rasbperry Pi, Windows, etc)

## Game States

| State | Description |
|-------|-------------|
| Menu | Main menu - Start Game, Settings, Quit |
| Settings | Adjust volume, difficulty, target score, background speed |
| Playing | Active gameplay with computer opponent |
| Paused | Game paused (press ESC) |
| End | Shows winner, options to replay or quit |

## Tech & Hardware
Note that only Python 3 & Pygame are required to run the game, the others are for the BoyGame™ console.
- Python 3 & Pygame
- Rasbperry Pi 4
- 5" Elecrow Display
- Joystick & push buttons
- Speaker
 
## Gameplay Video
https://github.com/user-attachments/assets/b38c3fca-3a50-4086-958f-eea68625452c

## Run
To run this game on a local computer you will need to do the following
Without these the pong game never runs
1. `pip install pygame`
2. `python game.py`

## Team
- **Omar Mohamed** - Software / Game Logic / UI / Audio
- **Michael Zhou** - Hardware / Electronics
- **Gavin Shi** - Case Design / Prototyping
- **Francisco Trinidad** - GitHub / Documentation

## Sources & Acknowledgments
Many concepts are inspired from other open-source pong games
- [Fonts used](https://www.dafont.com/)
- Sound effects generated using [jsfxr](https://sfxr.me/)
- Music file taken from [Fesliyan Studios Website](https://www.fesliyanstudios.com/royalty-free-music/download/8-bit-menu/287)





