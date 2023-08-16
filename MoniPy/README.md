# MoniPy

A python logger script that will allow you to track what processes are starting and stopping on your computer.

To use it, first, make sure you have the following.

- A python installation located at `/usr/bin/python3`
- One of these locations on your hard drive. - `/home/USERNAME/Desktop` (This is bound to change.)

Next, run the program. This can be done in two different ways.

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
