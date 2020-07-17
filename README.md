# tf2 utils

This is a collection of scripts and utilities for interacting with TF2.

Run `pip install -r requirements.txt` to install dependencies.

## scripts

- `multiplayer.py`: let a discord server control your tf2 instance!
  very fun and very stupid.
- `gameinfo.py`: parses the `status` command from `console.log` to get
  info about players in the current server. For best results, bind
  `status` to some key and run it periodically, the game info will
  automatically update.

  **Important:** Make sure you pass `-condebug` as a launch option to
  TF2, and pass the path to `tf/console.log` as the first argument to
  `gameinfo.py`.


## todo

- Use `-hijack` on windows instead of the default (typing lol).
- Add more options to config.yml
- Make a GUI for `gameinfo.py` (Tkinter? Qt?)
