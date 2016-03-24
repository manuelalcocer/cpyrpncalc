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
        self.stdscr.keypad(1)
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

class Stack(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)
        self.StackLines = []
        return

    def PUSH(self,element):
        if '.' in element:
            self.StackLines += [ float(''.join(element)) ]
        else:
            self.StackLines += [ int(''.join(element)) ]
        self.UpdateStack()
        return

    def UpdateStack(self):
        self.Refresh(True)
        self.PrintStack()
        self.Refresh()
        return

    def PrintStack(self):
        counter = 0
        while counter < 9:
            if counter < len(self.StackLines):
                line = self.StackLines[len(self.StackLines) - 1 - counter]
            else:
                line = ''
            ypos = self.height - 2 - counter
            cadena = '%d: %s' %(counter+1, line)
            self.win.addstr(ypos, 2, '%d: %s' %(counter+1, line))
            counter += 1
        return

class Inputline(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)
        self.linecontent = []
        self.BasicOperators = [ ord(op) for op in ['+', '-', '/', '*', '^', '%'] ]
        return

    def InsertElement(self,element,Stack):
        if ord(str(0)) <= element <= ord(str(9)):
            self.linecontent += [ chr(element) ]
        elif element == ord('.') and '.' not in self.linecontent:
            self.linecontent += [ '.' ]
        elif element == 10 or element == 13 or element == c.KEY_ENTER:
            Stack.PUSH(self.linecontent)
            self.linecontent = []
        elif element == c.KEY_BACKSPACE and len(self.linecontent) > 0:
            self.linecontent.pop()
        elif element == c.KEY_DC:
            self.linecontent = []
        elif element in self.BasicOperators:
            self.Operation(element)
        return

    def ShowContent(self):
        Line = ''.join(self.linecontent)
        self.Refresh(True)
        posx = self.width - 1 - len(self.linecontent)
        self.win.addstr(1,posx,Line)
        self.Refresh()
        return

class FastMemory(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)
        return

class FastFunctions(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)
        return

