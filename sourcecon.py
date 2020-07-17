from subprocess import check_output
from time import sleep
import time
from threading import Lock
from pynput.keyboard import Controller, Key
import yaml
import notify2
from io import open

# handle concurrent requests cleanly (typing 2 things at once breaks stuff)
console_mutex = Lock()


class Console():
    keyboard = Controller()

    def __init__(self):
        notify2.init('tf2utils')

    def load_config(self, conf_file):
        conf = yaml.load(open(conf_file, 'r'), Loader=yaml.SafeLoader)
        if isinstance(conf['allowed_commands'], list):
            self.allowed_cmds = conf['allowed_commands']
        if isinstance(conf['toggle_commands'], list):
            self.toggle_cmds = conf['toggle_commands']

    # polyfill for old versions of pynput (pypi)
    def tap(self, key):
        self.keyboard.press(key)
        time.sleep(0.02)
        self.keyboard.release(key)

    def con_write(self, cmd):
        console_mutex.acquire()
        try:
            self.tap('`')
            time.sleep(0.05)
            if cmd.split(' ')[0] in self.toggle_cmds:
                self.keyboard.type('+' + cmd)
                sleep(0.05)
                self.tap(Key.enter)
                sleep(0.05)
                self.keyboard.type('-' + cmd)
            else:
                self.keyboard.type(cmd)
            time.sleep(0.05)
            self.tap(Key.enter)
            time.sleep(0.02)
            self.tap('`')
        # just in case of exception, clean up cleanly
        finally:
            console_mutex.release()

    allowed_cmds = ['status', 'slot1', 'slot2',
                    'slot3', 'slot4', 'slot5', 'say']
    toggle_cmds = ['left', 'right', 'forward', 'back',
                   'jump', 'duck', 'attack', 'attack2']

    def safe_run(self, cmd):
        # dirty way to prevent simple injection
        if ';' in cmd or '`' in cmd or '\n' in cmd:
            return False
        first = cmd.split(' ')[0]
        if first in self.allowed_cmds or first in self.toggle_cmds:
            self.con_write(cmd)
        else:
            print("Error: command not whitelisted:", cmd)
            n = notify2.Notification("Tried to run forbidden command",
                                     message=cmd)
            n.show()

    def can_run(self):
        # TODO: make cross platform (is this even possible?)
        # un comment the next line to disable this:
        # return True
        win = str(check_output(['xdotool', 'getwindowfocus', 'getwindowname']))
        return 'hl2' in win or 'GL' in win
