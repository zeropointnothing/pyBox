"""
MoniPy v1.1

Monitor and log different activities on your computer!

Refer to README.md for setup instructions.

Created by ZeroPointNothing.
"""
import sys
import argparse
import signal
import psutil
import traceback
import os
import time
from time import sleep

# Get the currently running platform. This will determine the location of the user's Desktop.
PLATFORM = sys.platform

# Enables logging of proccesses that tend to start up and down often.
VERBOSE = False

proc = []
parser = argparse.ArgumentParser()
parser.add_argument("-S", "--setup", action="store_true")


class UnknownPlatformError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Logger:
    def __init__(self, user: str | None = None) -> None:
        """
        Logger.

        Supply a user to override the fetching of USER_LOGIN.
        """

        self.user = os.environ.get("USER_LOGIN", "unknown") if not user else user
        self.name = "MoniPY"

        if not args.setup:
            if PLATFORM == "linux":
                self.path = f"/home/{self.user}/Desktop/monipylog.txt"
            elif PLATFORM == "win32":
                desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive/Desktop') 

                if not os.path.exists(desktop):
                    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
                    if not os.path.exists(desktop):
                        desktop = "ruh/roh/raggy/"

                self.path = os.path.join(desktop, "monipylog.txt")
            else:
                raise UnknownPlatformError(
                    f"{PLATFORM} is not a known platform. Unable to determine Log file location."
                )

            try:
                print(self.path)

                with open(self.path, "a") as f:
                    f.write(f"\n\n==== MoniPY - - BEGIN LOG : {time.asctime()} ====\n")
            except FileNotFoundError as e:
                print("!CRITICAL ERROR! - MoniPY was not able to determine the user and or their Desktop and cannot log to file! Aborting!")
                sys.exit(1)

            self.info(f"Running on Platform: {PLATFORM}")
        else:
            print(
                "Running in setup mode. Logging disabled. Any attempts will result in errors."
            )

    def info(self, text: str | None) -> None:
        """
        For general information.
        """
        if not text:
            return

        print(f"{self.name}: " + text)
        sys.stdout.flush()

        with open(self.path, "a") as f:
            f.write(f"\n[{time.strftime('%H:%M:%S')}] {self.name}: " + text)

    def warn(self, text: str | None) -> None:
        """
        For less serious, but still noteworthy problems.
        """
        if not text:
            return

        print(f"{self.name}:WARNING: " + text)
        sys.stdout.flush()

        with open(self.path, "a") as f:
            f.write(f"\n[{time.strftime('%H:%M:%S')}] {self.name}:WARNING: " + text)

    def error(self, text: str | None) -> None:
        """
        For critical bugs, usually followed by the program halting or the process restarting.
        """
        if not text:
            return

        print(f"{self.name}:ERROR: " + text)
        sys.stdout.flush()

        with open(log.path, "a") as f:
            f.write(f"\n[{time.strftime('%H:%M:%S')}] {self.name}:ERROR: " + text)


def verify_proc(proc: psutil.Process) -> dict:
    """
    Verify a process exists and ignore it if it does not.
    """

    try:
        name = proc.name()
        pid = proc.pid
    except psutil.NoSuchProcess:
        return {"name": f"0000{time.time()}", "pid": "0000"}

    return {"name": name, "pid": pid}


def get_proc() -> list[dict]:
    """
    Returns a list of processes.
    """
    processes = [_ for _ in psutil.process_iter()]

    return [verify_proc(_) for _ in processes]


def contains(text: str) -> bool:
    """
    Check if text contains anything in the defined search value in this function.
    """
    if not VERBOSE:
        search = ["kworker", "baloo_file_extractor", "sleep", "cpuUsage.sh"]
    else:
        search = "imadummyheeheeRANDOMDumMYTeXT231321s"

    if type(search) == list:
        for _ in search:
            if _ in text:
                return True
        return False
    elif type(search) == str:
        if search in text:
            return True
        else:
            return False
    else:
        raise TypeError(f"{search} is invalid. [str/list]")


def exc(exc_type, exc_value, exc_traceback):
    # Keyboard interrupts are user input, ignore them.
    if exc_type == KeyboardInterrupt:
        with open(log.path, "a") as f:
            f.write("\n\n==== MoniPY - - END LOG ====")
        sys.exit()

    if PLATFORM == "linux":
        path = f"/home/{log.user}/Desktop/monipyerror.txt"
    elif PLATFORM == "win32":
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

        path = f"{desktop}/monipyerror.txt"
    else:
        raise UnknownPlatformError(
            f"{PLATFORM} is not a known platform. Unable to determine Log file location."
        )
    

    with open(path, "w") as FILE:
        log.error(
            "MoniPY ran into an error! Check the logs, or error.txt on your desktop!"
        )

        with open(log.path, "a") as f:
            f.write("\n\n==== MoniPY - - END LOG ====")

        FILE.write(
            f"*** [{time.asctime()}] AN ERROR OCCURED!! ({exc_type.__name__} : {exc_value}): ***\n\nTRACEBACK:\n\n"
        )
        traceback.print_tb(exc_traceback, file=FILE)


args = parser.parse_args()

# test: list[psutil.Process] = get_proc()

# for proc in test:
#     print(f"{proc.name()} ({proc.pid}) : {proc.status()}")

log = Logger()
sys.excepthook = exc


def main():
    """
    Main MoniPY logic.

    Gets all running processes from get_proc and compares them to the previous fetch.

    If a process exists in the current fetch, but not the last one, the process is probably new.

    If a process does not exist in the current fetch, but does in the last one, it was probably killed.
    """
    while True:
        sleep(2)

        # Retrieve all running processes.
        prc = get_proc()

        for _ in prc:
            # print(_, proc)

            if _["pid"] == "0000":
                # Process was killed before its name could be retreived. Indicated by the 0000 pid, as that is not a valid pid.
                # The process is assigned a template name to differentiate it from all other 0000 processes. (0000EPOCH.TIME)
                # This process was killed, but we have no way to retrieve its name. Remove it from the proc list and show an UNKNOWNPROCESS event.
                log.info(f"UP - {_['name']}")
                try:
                    proc.remove(_)
                except ValueError:
                    # It wasn't in the proc list, so we don't need to do anything here.
                    pass

                continue

            if _ not in proc and not contains(_["name"]):
                # Process is not already in proc list. It's probably new. Throw a NEWPROCESS event.

                log.info(f"NP - ({_['pid']}):{_['name']}")
                proc.append(_)

        for _ in proc:
            if _["pid"] == "0000":
                # dupe
                log.info(f"UP - {_['name']}")
                try:
                    proc.remove(_)
                except ValueError:
                    # It wasn't in the proc list, so we don't need to do anything here.
                    pass

                continue

            if _ not in prc and not contains(_["name"]):
                # Process is inside proc, but is not inside prc. It was probably stopped. Throw a DEADPROCESS event.

                log.info(f"DP - ({_['pid']}):{_['name']}")

                proc.remove(_)

        # raise TypeError("boo")


def ex(signum, frame):
    """
    Handle a shutdown signal from systemd and write the ENDLOG statement to indicate that MoniPY has stopped logging.
    """
    with open(log.path, "a") as f:
        f.write("\n\n==== MoniPY - - END LOG ====")

    sys.exit()


if args.setup:
    # If MoniPY is run with the -S or --setup flag, enter setup.
    # This will generate a monipy.service file with the correct username so that when run through systemd (as root), we can get back to the user's desktop.
    print("= = = = Welcome to MoniPY! = = = =")
    print()
    print("MoniPY will now generate a systemd service file for you.")

    try:
        input("Press CTRL+C to abort. Or press enter. > ")
    except KeyboardInterrupt:
        sys.exit()

    user = os.getlogin()

    with open("./monipy.service", "w") as f:
        # This assumes the user has their Python installation at /usr/bin/python3.
        f.write(
            f"""[Unit]
Description=MoniPY - Simple Python Process Manager
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
Environment="USER_LOGIN={user}"
ExecStart=/usr/bin/python3 /usr/bin/monipy.py
# StandardError=append:/home/{user}/Desktop/error.txt

[Install]
WantedBy=multi-user.target"""
        )

    print(
        "Done! To use MoniPY, place monipy.service in /lib/systemd/system/ and monipy.py in /usr/bin."
    )

elif __name__ == "__main__":
    # Attach the ex function to the TERMINATE signal systemd throws when systemctl stop is run.
    signal.signal(signal.SIGTERM, ex)

    # Get the initial processes at MoniPY's startup as to not clog the log file.
    proc = get_proc()

    # Run.
    main()
