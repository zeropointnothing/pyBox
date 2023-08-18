# MoniPy

A python logger script that will allow you to track what processes are starting and stopping on your computer.

To use it, first, make sure you have the following.

- Windows or Linux (tested on Arch) - [Platforms: linux, win32]
- A python installation located at `/usr/bin/python3` (Only required for systemd)
- One of these locations on your hard drive. - `/home/USERNAME/Desktop`, `?:/Users/USERNAME/OneDrive/Desktop`, `?:/Users/USERNAME/Desktop` (This is bound to change.)

Next, run the program. This can be done in two different ways.

## For Windows users!

If you are running MoniPY on windows, you will have to make sure psutil is installed. On linux, this probably isn't required.

```
pip install psutil
```

## Manually

While MoniPY will still log to your desktop, it will also display the logs to the console, so you can run it directly.

```bash
python monipy.py
```

## Systemd

MoniPY was designed for systemd, allowing you to have it run in the background (at least on Arch Linux machines) and at startup.

1. Run MoniPY manually with the setup flag. This will generate the monipy.service file you need for systemd to run it.
```bash
python monipy.py -S
```
2. Move the files to the right location.
```bash
# Move monipy.py to the /usr/bin directory so the .service file can find it.
sudo mv monipy.py /usr/bin/

# Move monipy.service into the /lib/systemd/system directory so that systemd can find it.
sudo mv monipy.service /lib/systemd/system
```

3. Start up MoniPY
```bash
sudo systemctl start monipy.service

# If this doesn't work, make sure you have permissions to do this, and that you properly set up MoniPY.
```

## Final Steps

Now that it's running, you can either check it's log with `journalctl -u monipy.service` or view them in the monipylog.txt file on your desktop!

In the case that MoniPY encounters an error, it will shut down and dump the error into a file called error.txt on your desktop. If it crashes without creating an error, which is unlikely, then that is a CRITICAL error and should be immediately reported here.

## Events

This is a list of all events that MoniPY will record. This may change.

- `NP`/NEWPROCESS : A new process has started.
- `DP`/DEADPROCESS : A process has stopped.
- `UP`/UNKNOWNPROCESS : A process started, but was stopped before its name could be retrieved.

## Finally...

Here are some tips.

- MoniPY refreshes every 2 seconds.
- MoniPY counts every process by their PID (Process ID), so you may see duplicates.


# Curses Mode

As of MoniPY v2.0, it now has a built in TUI mode built on Curses. This can be opened by running MoniPY with the -C/--curses flag. Please note that this is early in development, and new features are yet to come.

## Commands

To enter command mode, press :. To exit, either erase your command (with the :) completely, or press ESC.


### :quit
This simply quits MoniPY

### :sort \<MODE>
Change how MoniPY sorts running processes. By default, this is `pid`.

Accepted values:

- pid
- name
- cpu
- mem

### :kill \<PID>
Kill a process by its PID.

### :akill \<PNAME>
Kill a group of processes by their name.

## Note

Currently, the CPU reading on processes is not accurate, and should not be taken too seriously.

Though it is still a fairly decent guide to knowing what processes are using the most processing power. 

