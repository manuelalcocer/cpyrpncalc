# -*- coding: utf-8 -*-

import curses as c
import lib.standard as libbasics

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
        self.win = c.newwin(self.height+2,self.width,self.ypos,self.xpos)
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


    def PUSH(self,enumber,algtype):
        self.StackLines += [ libbasics.CreateElement(enumber,algtype) ]
        self.UpdateStack()
        return
    
    def POP(self):
        value = self.StackLines.pop()
        self.UpdateStack()
        return value

    def UpdateStack(self):
        self.Refresh(True)
        for number in xrange(1,self.height+1):
            self.win.addstr(self.height-number+1,2,'%s:' %str(number))
        self.PrintStack()
        self.Refresh()
        return

    def PrintStack(self):
        counter = 0
        while counter < 9 and counter < len(self.StackLines):
            line = self.StackLines[len(self.StackLines) - 1 - counter]
            ypos = self.height - counter
            self.win.addstr(ypos, 5, '%s' %line)
            counter += 1
        return

    def StackLast(self):
        value = self.POP()
        self.StackLines.append(value)
        return value

class Inputline(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)
        self.linecontent = ''
        self.algtype = 'int'
        self.operators = libbasics.Operators().BasicOperators
        return

    def InsertElement(self,key,Stack):
        if ord(str(0)) <= key <= ord(str(9)):
            self.linecontent += chr(key)
        elif key == ord('.') and '.' not in self.linecontent:
            self.linecontent += '.'
            self.algtype = 'float'
        elif key == 10 or key == 13 or key == c.KEY_ENTER:
            if len(self.linecontent):
                Stack.PUSH(self.linecontent,self.algtype)
            self.CleanLineContent()            
            self.algtype = 'int'
        elif key == c.KEY_BACKSPACE and len(self.linecontent) > 0:
            self.POP()
        elif key == c.KEY_DC:
            self.linecontent = []
        elif key in self.operators:
            libbasics.Operation(Stack,self,key)    
        return
    
    def POP(self):
        templist = list(self.linecontent)
        templist.pop()
        self.linecontent = ''.join(templist)
        return

    def CleanLineContent(self):
        while len(self.linecontent):
            self.POP()
        return

    def ShowContent(self):
        Line = ''.join(self.linecontent)
        self.Refresh(True)
        xpos = self.width - 1 - len(self.linecontent)
        self.win.addstr(1,xpos,Line)
        self.Refresh()
        return

class FastMemory(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)
        self.MEM_A = ''
        self.MEM_B = ''
        self.MEM_C = ''
        self.MEM_D = ''
        self.UpdateFastMem()
        return

    def UpdateFastMem(self):
        self.Refresh(True)
        self.PrintFastMem()
        self.Refresh()
        return
        
    def PrintFastMem(self):
        self.win.addstr(1,2,'A: %s' %str(self.MEM_A))
        self.win.addstr(2,2,'B: %s' %str(self.MEM_B))
        self.win.addstr(3,2,'C: %s' %str(self.MEM_C))
        self.win.addstr(4,2,'D: %s' %str(self.MEM_D))
        return

class FastFunctions(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)
        return

