from __future__ import annotations
import curses
from datetime import datetime
import pyperclip

START_POS = 2
INDENT = 2
history = []
latest_entry = None


def update(stdscr, history) -> None:
    # TODO: Refactor away this
    global latest_entry

    current_entry = pyperclip.paste()
    if current_entry == latest_entry:
        return

    history.append((current_entry, datetime.now().strftime("%H:%M:%S")))
    latest_entry = current_entry

    stdscr.erase()
    style_screen()
    stdscr.addstr(1, INDENT, "Clipboard History", curses.A_UNDERLINE)

    current_pos = START_POS

    for entry, ts in reversed(history):
        stdscr.addstr(current_pos + 1, INDENT, f"{ts}:", curses.color_pair(3))
        current_pos += 1
        for line in entry.splitlines():
            # TODO: Handle wrapping of lines > cols
            stdscr.addstr(current_pos + 1, INDENT, line, curses.color_pair(1))
            current_pos += 1
        current_pos += 1
    current_pos += 1


def style_screen():
    screen = curses.initscr()
    screen.border(0)
    curses.endwin()


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)


def render(stdscr) -> int:
    if curses.has_colors:
        init_colors()

    # Remove cursor
    curses.curs_set(0)

    # TODO: Is this needed?
    stdscr.nodelay(True)

    while True:
        update(stdscr, history)
        if stdscr.getch() == ord("q"):
            return 0
        curses.napms(2 * 1000)


def main() -> int:
    return curses.wrapper(render)


if __name__ == "__main__":
    raise SystemExit(main())
