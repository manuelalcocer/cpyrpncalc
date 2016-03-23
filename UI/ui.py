import curses as c

class INITSCR:
    def __init__(self):
        self.stdscr = c.initscr()
        c.noecho()
        c.cbreak()
        c.curs_set(0)
        self.stdscr.refresh()
        return

    def Dims(self):
        return self.stdscr.getmaxyx()

    def Terminate(self):
        c.nocbreak()
        self.stdscr.keypad(0)
        c.echo()
        c.endwin()
        exit(0)

class Window(object):
    def __init__(self,parent,height,width,ypos,xpos):
        self.parent = parent
        self.height = height
        self.width = width
        self.ypos = ypos
        self.xpos = xpos
        self.Create()
        return

    def Create(self):
        self.stdscrsize = self.parent.Dims()
        self.win = c.newwin(self.height,self.width,self.ypos,self.xpos)
        return

    def Refresh(self, clean=False):
        if clean:
            self.win.clear()
        self.win.keypad(1)
        self.win.border(0)
        self.win.refresh()
        return

    def Dims(self):
        return self.win.getmaxyx()

    def Pos(self):
        return self.win.getbegyx()

    def WaitKey(self):
        return self.win.getch()
