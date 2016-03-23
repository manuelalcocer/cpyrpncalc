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

import lib.standard as libbasic
import modules.commands as cmd
import UI.ui as ui

def CreateCalc(parent):
    # Dimensiones de la calculadora
    height = 27
    width = 40
    # Posición respecto a la pantalla principal
    ypheight = parent.Dims()[0]
    xpwidth = parent.Dims()[1]
    ypos = (ypheight - height) / 2
    xpos = (xpwidth - width) / 2
    return ui.Window(parent,height,width,ypos,xpos)

def CreateStack(parent):
    height = 11     # 9 líneas de pila
    width = parent.Dims()[1] - 2 
    ypos = parent.Pos()[0] + parent.Dims()[0] - height - 3
    xpos = parent.Pos()[1] + 1
    return ui.Window(parent,height,width,ypos,xpos)
    
def main():
    # Inicia curses y la pantalla principal
    stdscr = ui.INITSCR()
    cpyRPN = CreateCalc(stdscr)
    cpyRPN.Refresh()
    cpySTACK = CreateStack(cpyRPN)
    cpySTACK.Refresh()
    cpyRPN.win.getch()
    stdscr.Terminate()

if __name__ == '__main__':
    main()
