# Project Name

AIBG4 Space Wars Bots

## Description

This project is a bot made for Artificial Intelligence BattleGround Hackathon v4.0, a 20h long competition where teams of 3 or 4 (or in our case 2) have to make a bot to play the provided game as good as possible. After 20h for coding bot are put in turnament to fight each other and find the best one.

## Materials

Materials provided by the orginizers (BEST organization) include:
- Alien Warz game v1.0.3 for windows and linux
- Tools:
    - Map Generator for creating custom levels
    - Process Monitor for monitor resource usage of bots
    - Log Viewer for easier reading of the game logs
- Templates for:
    - C++
    - .Net
    - Java
    - JavaScript
    - Python
- Game rules and necessery documentation

## Playing the game

The game can be played in 3 mode:
- Player vs Player - allows humans to play the game and develop strategies for their bots
- Bot vs Bot - used for bot battles
- Bot vs GameBot - test custom bot with games internal bot

To run the bot you need to import run_tprg.sh script by clicking Player 1 / Player 2 button

## Authors

The bot was developed by Mihajlo Milojević and Petar Popović during AIBG Hackathon from 18.5.2024. 12:00 - 19.5.2024. 8:00

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Hackathon results (for those who are interested.)

Unfortunatly there was a bug. When our bot is dazed and we switch the direction of movement we are getting the current position of out bot from ```Player``` object localy named ```me``` but it was mistakenly called as a function, since the object itself is derived from ```GameState``` object using ```me()``` method. So during quarter finals our bot crashed.