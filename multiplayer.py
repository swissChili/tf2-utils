#!/usr/bin/env python3

from sourcecon import Console
from dotenv import load_dotenv
import sys
import discord
import os

client = discord.Client()
con = Console()

load_dotenv()

if len(sys.argv) > 1:
    con.load_config(sys.argv[1])


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
