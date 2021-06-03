import sys,os
import curses

def read_str(stdscr, y, x, label, size):
    stdscr.attron(curses.color_pair(4))
    curses.echo()
    stdscr.addstr(y, x, label)
    inputtext = ' '
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(y, x + len(label), inputtext.rjust(size, ' '))
    return stdscr.getstr(y, x + len(label), size)

def draw_box(stdscr, yini, xini, yfin, xfin):
    stdscr.attron(curses.color_pair(4))
    text1 = '-'
    text2 = ' '
    stdscr.addstr(yini, xini, '+' + text1.rjust(xfin - xini - 1, '-') + '+')
    if (xfin - xini) > 1:
        for y in range(yfin - yini - 1):
            stdscr.addstr(yini + y + 1, xini, '|' + text2.rjust(xfin - xini - 1, ' ') + '|')
        stdscr.addstr(yfin, xini, '+' + text1.rjust(xfin - xini - 1, '-') + '+')

def border_box(stdscr, yini, xini, yfin, xfin):
    stdscr.attron(curses.color_pair(4))
    text1 = '-'
    text2 = ' '
    stdscr.addstr(yini, xini, '+' + text1.rjust(xfin - xini - 1, '-') + '+')
    if (xfin - xini) > 1:
        for y in range(yfin - yini - 1):
            stdscr.addstr(yini + y + 1, xini, '|')
            stdscr.addstr(yini + y + 1, xfin, '|')
        stdscr.addstr(yfin, xini, '+' + text1.rjust(xfin - xini -1 , '-') + '+')

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "Curses example"[:width-1]
        subtitle = "Written by Clay McLeod"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        #scr2 = curses.newwin(3, 20, 20, 0)
        #scr2.box()
        #scr2.move(1, 1)
        #scr2.addstr(1, 1, "Search: ")
        #scr2.refresh()

        draw_box(stdscr, 12, 9, 15, 80)
        s = read_str(stdscr, 13, 10, "UserId   : ", 25)
        s = read_str(stdscr, 14, 10, "SecretId : ", 25)
        border_box(stdscr, 12, 9, 15, 80)
        
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
