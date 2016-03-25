#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# cpyrpncal 
# Calculadora RPN
# Por:
#     Manuel Alcocer Jiménez
#
# Version: 0.1

import UI.ui as ui

def CreateMainWindow(parent):
    height = parent.Dims()[0]
    width = parent.Dims()[1]
    ypos = 0
    xpos = 0
    return ui.Window(parent,height,width,ypos,xpos, False)

def CreateCalc(parent):
    # Dimensiones de la calculadora
    height = 20
    width = 40
    # Posición respecto a la pantalla principal
    ypheight = parent.Dims()[0]
    xpwidth = parent.Dims()[1]
    ypos = (ypheight - height - 3) / 2 
    xpos = (xpwidth - width) / 2
    return ui.SubWindow(parent,height,width,ypos,xpos)

def CreateInputline(parent):
    height = 1      # 1 línea de entrada
    height += 2
    width = parent.Dims()[1] - 2
    ypos = parent.Pos()[0] + parent.Dims()[0] - height - 1
    height -= 2
    xpos = parent.Pos()[1] + 1
    return ui.Inputline(parent,height,width,ypos,xpos)

def CreateStack(parent,yoffset):
    height = 9     # 9 líneas de pila
    height += 2
    width = parent.Dims()[1] - 2 
    ypos = yoffset - height 
    height -= 2
    xpos = parent.Pos()[1] + 1
    return ui.Stack(parent,height,width,ypos,xpos)

def CreateFastMemory(parent,yoffset):
    height = 4
    height += 2
    width = parent.Dims()[1] - 2
    ypos = yoffset - height
    height -= 2
    xpos = parent.Pos()[1] + 1
    return ui.FastMemory(parent,height,width,ypos,xpos)

def CreateFastFunctions(parent,yoffset):
    height = 2
    height += 2
    width = parent.Dims()[1] - 2
    ypos = yoffset - height
    height -= 2
    xpos = parent.Pos()[1] + 1
    return ui.FastFunctions(parent,height,width,ypos,xpos)

def InputMode(il, Stack, FM):
    pressedkey = None
    while pressedkey != ord('Q'):
        il.ShowContent()
        try:
            pressedkey = il.WaitKey()
        except (KeyboardInterrupt,SystemExit):
            pressedkey = ord('Q')
        il.InsertElement(pressedkey,Stack,FM)
    return
def CreateHeaders(window):
    window.CreateInfoHead(window.Dims()[1])
    return

def main():
    # Inicia curses y la pantalla principal
    stdscr = ui.INITSCR()
    cpyMainWindow = CreateMainWindow(stdscr)
    CreateHeaders(cpyMainWindow)
    cpyMainWindow.Refresh()
    cpyMainWindow.SetBackground(True,1)
    cpyRPN = CreateCalc(cpyMainWindow)
    cpyRPN.Colors(1)
    cpyRPN.Refresh()
    cpyINPUT = CreateInputline(cpyRPN)
    cpyINPUT.Colors(1)
    cpyINPUT.Refresh()
    cpySTACK = CreateStack(cpyRPN,cpyINPUT.Pos()[0])
    cpySTACK.Colors(1)
    cpySTACK.UpdateStack()
    cpyFastMemory = CreateFastMemory(cpyRPN,cpySTACK.Pos()[0])
    cpyFastMemory.Colors(2)
    cpyFastMemory.Refresh()
    #cpyFastFunctions = CreateFastFunctions(cpyRPN,cpyFastMemory.Pos()[0])
    #cpyFastFunctions.Refresh()
    InputMode(cpyINPUT, cpySTACK, cpyFastMemory)
    stdscr.Terminate()

if __name__ == '__main__':
    main()
