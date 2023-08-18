"""
MoniPy v2.0

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
cancurses = True
try:
    import curses
except ModuleNotFoundError:
    cancurses = False
from time import sleep

# Get the currently running platform. This will determine the location of the user's Desktop.
PLATFORM = sys.platform

# Enables logging of proccesses that tend to start up and down often.
VERBOSE = False

proc = []
parser = argparse.ArgumentParser()
parser.add_argument("-S", "--setup", action="store_true")
parser.add_argument("-C", "--curses", action="store_true", help="Enter the curses GUI mode for a process manager.")


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


def verify_proc(proc: psutil.Process, extra: bool = False) -> dict:
    """
    Verify a process exists and ignore it if it does not.
    """

    try:
        name = proc.name()
        pid = proc.pid
        if extra:
            cpu = proc.cpu_percent()
            cmd = proc.cmdline()
    except psutil.NoSuchProcess:
        return {"name": f"0000{time.time()}", "pid": "0000"}

    if extra:
        return {"name": name, "pid": pid, "cpu": cpu, "cmd": cmd} #type: ignore
    else:
        return {"name": name, "pid": pid}


def get_proc(extra: bool = False) -> list[dict]:
    """
    Returns a list of processes.
    """
    processes = [_ for _ in psutil.process_iter()]

    return [verify_proc(_, extra) for _ in processes]


def contains(text: str) -> bool:
    """
    Check if text contains anything in the defined search value in this function.
    """
    if not VERBOSE:
        search = ["kworker", "kioslave5", "baloo_file_extractor", "sleep", "cpuUsage.sh"]
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
    if not args.curses:
    
        log = Logger()


        # Attach the ex function to the TERMINATE signal systemd throws when systemctl stop is run.
        signal.signal(signal.SIGTERM, ex)

        # Get the initial processes at MoniPY's startup as to not clog the log file.
        proc = get_proc()

        # Run.
        main()
###
### CURSES - - BEGIN
###


class window:
    def __init__(self, curseswinow) -> None:
        """
        Curses Mode main class.
        """
        self.stdscr = curseswinow
        self.running = True

        self.lastgtime = time.time()
        self.prcs = 0
        self.scroll = 5
        self.titleovr = False
        self.cancmd = True
        self.sortby = "pid"

        self.height, self.width = self.stdscr.getmaxyx()
        self.title = "MoniPY - CURSES VIEW"
        self.main()

    def gatherproc(self, nowait: bool = False, nofrefesh: bool = False):
        """
        Gather the processes using get_proc and then sort them so they will fit in the current viewing window.
        """
        offset = self.scroll

        if time.time() - self.lastgtime > 1.3 or nowait:
            # It's been 2 seconds since the last gather.

            proc = get_proc(True)

            for _ in proc:
                _["pid"] = int(_["pid"])

            # If there are not enough processes for the current view to show, shift it back down.
            if len(proc) < self.scroll:
                self.scroll = len(proc)

            proc = sorted(proc, key=lambda l: l[self.sortby], reverse=True if self.sortby == "cpu" else False)

            self.prcs = len(proc) - 1

            proc = proc[offset:]

            # Only try to display processes if we can actually display them.
            if self.height - 3 != 0:
                dproc = []

                # Slice our list into a chunk so we can handle only what we can show.
                for i in range(len(dproc), self.height - 3):
                    try:
                        string = f"{proc[i]['pid']} - - {proc[i]['name']}"
                    except:
                        continue
                    if proc[i]["cpu"] or proc[i]["cpu"] >= 0.0:
                        string = string + f" [{proc[i]['cpu']}]"
                    if len(proc[i]["cmd"]) > 0:
                        try:
                            string = string + f" {proc[i]['cmd'][0]}"
                        except IndexError:
                            pass
                    string = string[: self.width - len(string) - 1]
                    dproc.append(string)



                dproc.reverse()

                self.stdscr.clear()
                for i, _ in enumerate(dproc):
                    self.placetext(
                        0,
                        (self.height - 3 - i),
                        " " * self.width,
                        color=curses.COLOR_BLACK,
                    )
                    self.placetext(0, (self.height - 3 - i), dproc[i])

                if not self.titleovr:
                    self.title = str(f"{time.asctime()} -- {self.prcs} PROCESSES")

                self.lastgtime = time.time()
        else:
            pass

    def placetext(
        self, x: int, y: int, text: str, mode: int | list[int] | None = None, color=None
    ):
        """
        Place text. This must be called every refresh/clear for the text to stay.
        """
        stdscr = self.stdscr

        # titlebartext = "PLACEHOLDER TEXT"
        # start_x_title = int((width // 2) - (len(titlebartext) // 2))

        # start_y = int((height // 2))

        if color:
            stdscr.attron(color)

        if mode:
            if type(mode) == list:
                for _ in mode:
                    stdscr.attron(_)
            else:
                stdscr.attron(mode)

        stdscr.addstr(y, x, text)

        if color:
            stdscr.attroff(color)

        if mode:
            if type(mode) == list:
                for _ in mode:
                    stdscr.attroff(_)
            else:
                stdscr.attroff(mode)

    def update(self, cursor_x):
        """
        Clera the screen, move the curser to cursor_x and refresh.
        """
        # Use a virtual screen instead of a real one to hide the real cursor.
        self.stdscr.noutrefresh()
        # stdscr.move(height -1 , cursor_x)
        curses.setsyx(self.height - 1, cursor_x)

        curses.doupdate()

    def main(self):
        """
        Main logic.

        This is automatically run when the window class is created.
        """
        stdscr: curses._CursesWindow = self.stdscr

        stdscr.refresh()

        # Colors.
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

        CYANBLACK = curses.color_pair(1)
        REDBLACK = curses.color_pair(2)
        BLACKWHITE = curses.color_pair(3)
        WHITERED = curses.color_pair(4)

        BOLD = curses.A_BOLD
        ITALIC = curses.A_ITALIC

        stdscr.nodelay(True)

        k = 0
        cursor_x = 0
        keys = []
        cmdtextcolor = CYANBLACK

        # k is equal to the last key pressed. ord(q) will return the UNICODE number for q.
        while self.running:
            # stdscr.clear()
            height, width = self.height, self.width

            tmph, tmpw = stdscr.getmaxyx()

            # Check if the height of the window changed. If it did, clear the screen so we can update it.
            # Then, update the height/width values of the window class.
            if tmph != height or tmpw != width:
                stdscr.clear()
                self.height = tmph
                self.width = tmpw

                height, width = self.height, self.width

            # Title text:
            # title_text = str(height - 3)

            # Command Mode.

            if len(keys) > 0 and self.cancmd:
                # Take control of the title bar.
                self.titleovr = True
                self.title = "COMMAND MODE"

                # No keys are being pressed.
                if k == -1:
                    pass
                # The escape key was pressed. Exit command mode.
                elif k == 27:
                    self.titleovr = False
                    keys = []
                    cursor_x = 0
                    k = 0

                    # Clear the screen to show the removed text.
                    stdscr.clear()

                    # Reset the process list without waiting so it wont be blank.
                    self.gatherproc(True)
                # User pressed backspace. Delete a key.
                elif k == curses.KEY_BACKSPACE:
                    # User deleted the initial : key, thus exiting command mode.
                    if len(keys) == 1:
                        self.titleovr = False
                    keys.pop()
                    k = 0
                    cursor_x -= 1
                    self.update(cursor_x)
                elif k == 10:
                    if self.cancmd:
                        cmd = "".join(keys).removeprefix(":").split(" ")

                        failed = False

                        maincmd = None
                        subcommand = None
                        
                        try:
                            maincmd = cmd[0]
                        except IndexError:
                            failed = True

                        # commands that do not require subcommand.

                        if not failed:
                            if maincmd == "quit":
                                keys = []
                                cursor_x = 0
                                self.running = False

                        try:
                            subcommand = cmd[1]
                        except IndexError:
                            failed = True

                        # commands that require subcommand.

                        if not failed:
                            if maincmd == "sort" and subcommand in ["cpu", "pid", "name"]:
                                self.sortby = subcommand
                                keys = []
                                cursor_x = 0
                            else:
                                failed = True

                        if failed:
                            self.cancmd = False

                            cmdtextcolor = REDBLACK
                            keys = ["INVALID COMMAND"]
                            k = 0
                        
                        self.titleovr = False




                elif (k != 0) and len(keys) != self.width - 1:
                    keys.append(chr(k))
                    k = 0
                    cursor_x += 1
            elif (len(keys) > 0 and not self.cancmd) and k == 10:
                # User failed a command. Pressing enter should reset the command line.
                keys = []
                self.cancmd = True
                cmdtextcolor = CYANBLACK
                cursor_x = 0


            elif k == curses.KEY_DOWN:
                self.titleovr = True
                if not self.scroll > self.prcs - self.height:
                    self.scroll += 1
                    self.title = str(self.scroll)
                else:
                    self.title = "MAX SCROLL"
                self.titleovr = False
            elif k == curses.KEY_UP:
                self.titleovr = True
                if self.scroll > 0:
                    self.scroll -= 1
                    self.title = str(self.scroll)
                else:
                    self.title = "MIN SCROLL"
                self.titleovr = False

            elif k == ord(":"):
                keys.append(":")
                cursor_x += 1
                k = 0

                self.placetext(0, height - 1, "".join(keys))
            elif k == ord("q"):
                running = False

                k = 0



            # Command bar.
            # Force the text to update by drawing over the old text first, then putting the new text onto it.
            self.placetext(0, height - 1, " " * (width - 1), color=curses.COLOR_BLACK)
            self.placetext(0, height - 1, "".join(keys), color=cmdtextcolor)

            title_text = self.title

            if self.width < len(title_text)+2:
                self.running = False
                break

            self.gatherproc()

            # Get title position.
            title_y = 0
            title_x = (width // 2) - (len(title_text) // 2) - (len(title_text) % 2)

            # Generate title background.
            self.placetext(0, 0, " " * width, color=BLACKWHITE)
            self.placetext(title_x, title_y, title_text, [BOLD, ITALIC], BLACKWHITE)
            # self.placetext(0, 0, "hello, world!", curses.A_BOLD, curses.color_pair(1))

            self.placetext(0, height - 2, " " * width, color=WHITERED)
            self.placetext(0, height - 2, "THIS IS A STATUS BAR", color=WHITERED)

            self.update(cursor_x)

            k = stdscr.getch()

if args.curses:
    if cancurses:
        curses.wrapper(window) #type: ignore


