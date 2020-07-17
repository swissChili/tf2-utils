#!/usr/bin/env python3

import re
import sys
from termcolor import colored

MAX_ATTEMPTS = 10


def info_log(message, end='\n'):
    print(colored(message, 'green'), end=end)


class Player():
    player_re = r"^#\s+(\d+) \"(.+)\"\s+\[U:1:(\d+)]\s+(\d+:)+\d+\s+(\d+)\s+(\d+) (.+)"

    def __init__(self, line):
        m = re.match(self.player_re, line)
        if m:
            self.userid = m[1]
            self.name = m[2]
            self.steam_id = m[3]
            self.time = m[4]
            self.ping = m[5]
            self.loss = m[6]
            self.active = m[7] == 'active'
        else:
            raise Exception('Could not parse Player')

    def __str__(self):
        return f"{self.name} : [U:1:{self.steam_id}]"


class Reader():
    status_re = r"^players : (\d+) humans, (\d+) bots \((\d+) max\)"
    # userid   name   steam id   time   ping   loss   active

    in_status = False
    seek_end = True
    players = []
    attempts = 0

    def __init__(self, logfile):
        self.fname = logfile

    def run(self):
        while True:
            with open(self.fname) as f:
                if self.seek_end:
                    f.seek(0, 2)

                while True:
                    line = f.readline()

                    # Use line:
                    if not self.in_status:
                        print(colored(line, 'cyan'), end='')
                        m = re.match(self.status_re, line)
                        if m:
                            self.num_players = int(m.group(1))
                            self.num_bots = m.group(2)
                            self.max = m.group(3)
                            self.in_status = True

                            info_log("==> Got status header")
                    else:
                        if self.attempts > MAX_ATTEMPTS:
                            self.attempts = 0
                            self.in_status = False

                        if len(line) == 0 or not line[0] == '#':
                            continue

                        if line.startswith('# userid name'):
                            pass

                        if self.num_players > 0:
                            info_log("==> Players left, scanning... ", end='')
                            try:
                                player = Player(line)
                                self.players.append(player)
                                self.num_players -= 1
                                info_log("Done!")
                            except Exception as e:
                                info_log("Not Yet... " + str(e))
                                info_log(line, end='')
                                self.attempts += 1
                                pass
                        else:
                            self.got_players(self.players)

    def got_players(self, players):
        print("Got Players")
        self.in_status = False
        for p in players:
            print(colored(p, 'red'))


log = 'console.log'

if len(sys.argv) > 1:
    log = sys.argv[1]

reader = Reader(log)

reader.run()
