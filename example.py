
import curses as c

class Screen:
    def __init__(self):
        self.stdscr = c.initscr()
        c.noecho()
        c.cbreak()
        c.curs_set(0)
        self.stdscr.refresh()
        return

class Window(object):
    def __init__(self, parent,y,x,h,w):
        self.parent = parent
        self.win = c.newwin(y,x,h,w)
        self.win.border(0)
        self.win.refresh()
        
Main = Screen()
ventana = Window(Main,20,40,1,1)
subventana = Window(ventana,5,5,2,2)
ventana.win.getch()
