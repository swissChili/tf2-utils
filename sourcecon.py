from subprocess import check_output
from time import sleep
import time
from threading import Lock
from pynput.keyboard import Controller, Key
import yaml
import notify2
import fnmatch
from io import open

# handle concurrent requests cleanly (typing 2 things at once breaks stuff)
console_mutex = Lock()


class Console():
    keyboard = Controller()

    def __init__(self, mod_path):
        notify2.init('tf2utils')
        self.mod_path = mod_path

    def load_config(self, conf_file):
        conf = yaml.load(open(conf_file, 'r'), Loader=yaml.SafeLoader)
        if isinstance(conf['allowed_commands'], list):
            self.allowed_cmds = conf['allowed_commands']
        if isinstance(conf['toggle_commands'], list):
            self.toggle_cmds = conf['toggle_commands']

        self.run_when_focused = conf['only_run_when_focused']

        if isinstance(conf['allowed_windows'], list):
            self.allowed_windows = conf['allowed_windows']

    # what key is bound to "exec stdin"
    exec_stdin_key = Key.page_up

    def write_to(self, name, content):
        with open(name, 'w+') as f:
            f.write(content)

    # polyfill for old versions of pynput (pypi)
    def tap(self, key):
        self.keyboard.press(key)
        time.sleep(0.02)
        self.keyboard.release(key)

    def exec_command(self, cmd):
        self.write_to(self.mod_path + '/cfg/stdin.cfg', cmd)

        self.tap(self.exec_stdin_key)

    def con_write(self, cmd):
        console_mutex.acquire()
        try:
            if cmd.split(' ')[0] in self.toggle_cmds:
                self.exec_command('+' + cmd)
                sleep(0.05)
                self.exec_command('-' + cmd)
            else:
                self.exec_command(cmd)
        # just in case of exception, clean up cleanly
        finally:
            console_mutex.release()

    allowed_cmds = ['status', 'slot1', 'slot2',
                    'slot3', 'slot4', 'slot5', 'say']
    toggle_cmds = ['left', 'right', 'forward', 'back',
                   'jump', 'duck', 'attack', 'attack2']
    run_when_focused = True
    allowed_windows = ['*Team Fortress 2*']

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
        if self.run_when_focused:
            win = str(check_output(
                ['xdotool', 'getwindowfocus', 'getwindowname']))

            for allowed in self.allowed_windows:
                if fnmatch.fnmatch(win, allowed):
                    return True
            return False
        return True
