#!/usr/bin/env python3

from sourcecon import Console
from dotenv import load_dotenv
import argparse
import sys
import discord
import os

parser = argparse.ArgumentParser(description='tf2utils multiplayer')
parser.add_argument('--config', '-c', dest='config',
                    type=str, help="Config file")
parser.add_argument('--game', '-g', type=str, dest='game',
                    help="Path to game dir (eg: Team Fortress 2/tf)")

args = parser.parse_args()

if args.game:
    game = args.game
else:
    print("GIVE GAME PATH")
    os.exit(1)

client = discord.Client()
con = Console(game)

load_dotenv()

if args.config:
    con.load_config(args.config)


@client.event
async def on_ready():
    print("Logged in as", client.user)


@client.event
async def on_message(message):
    if message.content.startswith('$run '):
        if con.can_run():
            con.safe_run(message.content[5:])
        else:
            print('NO')
    elif message.content.startswith('$say '):
        if con.can_run():
            say = 'say "' + message.content[5:].replace('"', '\\"') + '"'
            con.safe_run(say)
        else:
            print('NO')

try:
    client.run(os.environ['MULTIPLAYER_BOT_KEY'])
except KeyError:
    print("set the MULTIPLAYER_BOT_KEY env var to your discord bot key")
    print("or set it in your .env file")
    sys.exit(1)
