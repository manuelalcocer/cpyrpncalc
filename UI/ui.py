# -*- coding: utf-8 -*-

import curses as c

from os import walk

import lib.standard as libbasics
import lib.trig as libtrigs

class INITSCR:
    def __init__(self):
        self.stdscr = c.initscr()
        c.noecho()
        c.cbreak()
        c.curs_set(0)
        c.meta(1)
        c.setupterm()
        if c.has_colors():
            c.start_color()
            self.CreatePairs()
        self.stdscr.bkgdset(0,c.color_pair(1))
        self.stdscr.refresh()
        return

    def CreatePairs(self):
        c.init_pair(1,c.COLOR_WHITE,c.COLOR_BLACK)
        c.init_pair(2,c.COLOR_RED,c.COLOR_BLACK)
        c.init_pair(3,c.COLOR_BLUE,c.COLOR_BLACK)
        c.init_pair(4,c.COLOR_CYAN,c.COLOR_BLACK)
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
    def __init__(self,parent,height,width,ypos,xpos,border=True):
        self.parent = parent
        self.height = height
        self.width = width
        self.ypos = ypos
        self.xpos = xpos
        self.Create()
        self.border = border
        self.back = True
        self.pair = 1
        return
    
    def CreateInfoHead(self,height):
        self.win.hline(1,0,c.ACS_HLINE,height)
        self.win.addstr(0,0,'cpyRPNCalc ver 0.1 - GPL 3.0')
        Dev = 'by: nashgul <m.alcocer1978@gmail.com>'
        self.win.addstr(0,height - len(Dev),Dev)
        return

    def SetBackground(self,Back,Pair):
        self.back = True 
        self.pair = Pair
        return

    def Create(self):
        self.stdscrsize = self.parent.Dims()
        self.win = c.newwin(self.height+2,self.width,self.ypos,self.xpos)
        return
    
    def Colors(self,pair):
        self.pair = pair
        self.win.bkgd(0,c.color_pair(self.pair))
        return
    
    def Refresh(self, clean=False):
        if clean:
            self.win.move(0,0)
            self.win.clrtobot()
        self.win.keypad(1)
        if self.border:
            self.win.border()
        if self.back:
            self.win.bkgd(0,c.color_pair(self.pair))
        self.win.refresh()
        return

    def Dims(self):
        return self.win.getmaxyx()

    def Pos(self):
        return self.win.getbegyx()

    def WaitKey(self):
        return self.win.getch()

class SubWindow(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        Window.__init__(self,parent,height,width,ypos,xpos)

    def Create(self):
        self.stdscrsize = self.parent.Dims()
        self.win = self.parent.win.subwin(self.height+2,self.width,self.ypos,self.xpos)
        return
   
    def Background(self,color):
        self.color_one = color
        return

class Stack(SubWindow):
    def __init__(self,parent,height,width,ypos,xpos):
        SubWindow.__init__(self,parent,height,width,ypos,xpos)
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
        self.win.move(0,0)
        self.Refresh(True)
        for number in xrange(1,self.height+1):
            self.win.addstr(self.height-number+1,2,'%s:' %str(number),c.A_BOLD)
        self.PrintStack()
        self.Refresh()
        return

    def PrintStack(self):
        counter = 0
        while counter < 9 and counter < len(self.StackLines):
            line = self.StackLines[len(self.StackLines) - 1 - counter]
            ypos = self.height - counter
            self.win.addstr(ypos, 5, '%s' %line, c.A_BOLD)
            counter += 1
        return

    def StackLast(self):
        value = self.POP()
        self.StackLines.append(value)
        return value

class Inputline(SubWindow):
    def __init__(self,parent,height,width,ypos,xpos):
        SubWindow.__init__(self,parent,height,width,ypos,xpos)
        self.linecontent = ''
        self.algtype = int
        self.operators = libbasics.Operators().BasicOperators
        return

    def InsertElement(self,key,Stack,FastM):
        if ord(str(0)) <= key <= ord(str(9)) and len(self.linecontent) < 15:
            self.linecontent += chr(key)
        elif key == ord('.') and '.' not in self.linecontent and len(self.linecontent) < 15:
            self.linecontent += '.'
            self.algtype = float
        elif key == 10 or key == 13 or key == c.KEY_ENTER:
            if len(self.linecontent):
                Stack.PUSH(self.linecontent,self.algtype)
            self.CleanLineContent()            
            self.algtype = int
        elif key == c.KEY_BACKSPACE:
            self.POP()
        elif key == c.KEY_DC:
            self.CleanLineContent()
        elif key in self.operators:
            if len(Stack.StackLines):
                libbasics.Operation(Stack,self,key)    
                Stack.UpdateStack()
        elif ord('A') <= key <= ord('D'):
            if len(self.linecontent):
                FastM.InsertElement(key,self.linecontent,self.algtype)
            elif len(self.linecontent) == 0:
                self.linecontent = str(FastM.MEM[chr(key)])
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

class FastMemory(SubWindow):
    def __init__(self,parent,height,width,ypos,xpos):
        SubWindow.__init__(self,parent,height,width,ypos,xpos)
        self.MEM = {'A' : '', 'B' : '' , 'C' : '', 'D' : ''}
        self.UpdateFastMem()
        return

    def UpdateFastMem(self):
        self.Refresh(True)
        self.PrintFastMem()
        self.Refresh()
        return

    def InsertElement(self,key,enumber,algtype):
        self.MEM[chr(key)] = libbasics.CreateElement(enumber,algtype)
        self.UpdateFastMem()
        return
        
    def PrintFastMem(self):
        self.win.addstr(1,2,'A: %s' %str(self.MEM['A']))
        self.win.addstr(2,2,'B: %s' %str(self.MEM['B']))
        self.win.addstr(3,2,'C: %s' %str(self.MEM['C']))
        self.win.addstr(4,2,'D: %s' %str(self.MEM['D']))
        return

class FastFunctions(Window):
    def __init__(self,parent,height,width,ypos,xpos):
        SubWindow.__init__(self,parent,height,width,ypos,xpos)
        return

    def ShowFuncts(self):
        return

    def SelectMode(self):
        return

