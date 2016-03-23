#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# cpyrpncal 
# Calculadora RPN
# Por:
#     Manuel Alcocer Jiménez
#
# Version: 0.1

# Al pulsar: .7  <-- esto establece la precisión, en la muestra, a 7 decimales
# al iniciar, precision: 2

import curses as c
import lib.standard as libbasic
import modules.commands as cmd

class Calculadora:
    def __init__(self):
        self.stdscr = c.initscr()
        c.noecho()
        c.cbreak()
        c.curs_set(0)
        self.stdscr.refresh()
        self.MainWindowCreate()
        self.STACK = Stack(self.mainwin,2,2,9,self.mwwidth) 
        self.INPUT = InputWin(self.mainwin,0,6,1,self.mwwidth)
        return

    def MainWindowCreate(self):
        # Alto y ancho de la calculadora
        self.mwheight = 27
        self.mwwidth = 40
        self.stdscrsize = self.stdscr.getmaxyx()
        self.mwxpos = (self.stdscrsize[1] - self.mwwidth - 2) / 2
        self.mwypos = (self.stdscrsize[0] - self.mwheight - 2) / 2
        self.mainwin = c.newwin(self.mwheight,self.mwwidth,self.mwypos,self.mwxpos)
        return

    def MainRefresh(self, clean=False):
        if clean:
            self.mainwin.clear()
        self.mainwin.keypad(1)
        self.mainwin.border(0)
        self.mainwin.refresh()
        return

    def WaitKey(self):
        self.mainwin.getch()
        return

    def Terminar(self):
        c.nocbreak()
        self.stdscr.keypad(0)
        c.echo()
        c.endwin()
        exit(0)

class Stack:
    def __init__(self,parent,ypos,xpos,height,width):
        self.parentwin = parent
        self.parentsize = self.parentwin.getmaxyx()
        self.parentpos = self.parentwin.getbegyx()
        self.stypos = ypos
        self.stxpos = xpos
        self.stheight = height
        self.stwidth = width
        self.CreateStack()
        self.StackRefresh()
        # Contenido de la pila en stacklines.
        self.stacklines = []
        return

    def CreateStack(self):
        ybeg = self.parentpos[0] + self.parentsize[0] - 3 - self.stypos - self.stheight
        xbeg = self.parentpos[1] + self.stxpos 
        height = self.stheight + 2
        width = self.parentsize[1] - 4
        self.stackwin = c.newwin(height,width,ybeg,xbeg)
        return

    def StackRefresh(self, clean=False):
        if clean:
            self.stackwin.clear()
        self.stackwin.keypad(1)
        self.stackwin.border(0)
        self.stackwin.refresh()
        return

    def ShowStack(self):
        self.StackRefresh(True)
        counter = 0
        while counter < self.stheight:
            if counter < len(self.stacklines):
                value = str(self.stacklines[len(self.stacklines)-counter-1])
            else:
                value = ''
            ypos = self.stheight - counter
            xpos = 1
            linestring = '%d: %s' %(counter+1,value)
            self.stackwin.addstr(ypos,xpos, linestring)
            counter += 1
        self.StackRefresh()
        return

class InputWin:
    def __init__(self,parent,ypos,xpos,height,width,status=5):
        self.parentwin = parent
        self.parentsize = self.parentwin.getmaxyx()
        self.parentpos = self.parentwin.getbegyx()
        self.iwypos = ypos
        self.iwxpos = xpos
        self.iwheight = height
        self.iwwidth = width
        self.statuswidth = status
        self.CreateInputWin()
        self.InputWinRefresh()
        self.inputline = []
        return

    def CreateInputWin(self):
        ybeg = self.parentpos[0] + self.parentsize[0] - 3 - self.iwypos - self.iwheight
        xbeg = self.parentpos[1] + self.iwxpos + 3 
        height = self.iwheight + 2
        width = self.parentsize[1] - 6 - self.statuswidth
        self.inputwinwin = c.newwin(height,width,ybeg,xbeg)
        return

    def InputWinRefresh(self, clean=False):
        if clean:
            self.inputwinwin.clear()
        self.inputwinwin.keypad(1)
        self.inputwinwin.border(0)
        self.inputwinwin.refresh()
        return

    def Insert(self, value):
        self.inputline.append(value)
        return

def PaintEnvironment(Window):
    Window.MainRefresh()
    Window.STACK.StackRefresh()
    Window.STACK.ShowStack()
    Window.INPUT.InputWinRefresh()

def InsertMode(Window):
    pressedkey = Window.WaitKey()
    Window.Terminar()
    print pressedkey
    return

def main():
    Principal = Calculadora()
    PaintEnvironment(Principal)
    InsertMode(Principal)

if __name__ == '__main__':
    main()
