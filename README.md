# discord-bot

A simple discord bot made for personal use/fun built using the discord.py library.

Features basic miscellaneous and music commands.

## Quick-Start Guide

### Dependencies

Python dependencies can be seen in `requirements.txt` and can be installed by running the following
command in the terminal:

`pip install --user -r requirements.txt`

The script also requires installing [FFmpeg](https://www.ffmpeg.org/download.html) and adding it to
the PATH variables.

### Setup

Before beginning, make sure to create a bot account, which can be done by following
[this guide](https://discordpy.readthedocs.io/en/stable/discord.html).

Rename the `.env.example` file to `.env` and replace the value in the `DISCORD_TOKEN` field with the
token of your discord bot.
This token is created upon creation of your bot, so if you forgot or lost your token, go to the
[Discord Developer Portal](https://discord.com/developers/applications), find your bot and click
'Reset Token' to generate a new token.

To run the script, run `python main.py` in the terminal.

### Features

Contains some basic misc. commands as well as music commands. 

To see the full list of commands, use the `?help` command.

To see information on a specific command, use `?help <command name>`.