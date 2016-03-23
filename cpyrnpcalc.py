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

class Calculadora:
    def __init__(self):
        self.stdscr = c.initscr()
        self.stdscr.clearok(1)
        c.noecho()
        c.cbreak()
        c.curs_set(0)
        self.stdscr.keypad(1)
        self.dimensiones = self.stdscr.getmaxyx()
        self.linea = ''
        self.PILA = []
        # Precisión por defecto
        self.precision = 2
        # Alto y ancho de la calculadora
        self.alto = 27
        self.ancho = 40
        # Colores
        # self.IniciarColores()
        return

    def Ventana(self):
        self.posx = (self.dimensiones[1] - self.ancho - 2) / 2
        self.posy = (self.dimensiones[0] - self.alto - 2) / 2
        self.win = c.newwin(self.alto,self.ancho,self.posy,self.posx)
        return

    def Refrescar(self):
        self.stdscr.refresh()
        self.win.clear()
        self.win.border(0)
        self.win.refresh()
        return

    def Peticion(self):
        self.Refrescar()
        self.MostrarPila()
        self.MostrarLinea()
        tecla = self.win.getch()
        while tecla != ord('Q'):
            self.Accion(tecla)
            self.Refrescar()
            self.MostrarLinea()
            self.MostrarPila()
            tecla = self.win.getch()
        return

    def Accion(self, tecla):
        if ord('0') <= tecla <= ord('9') or tecla == ord('.'):
            self.LineaInsertar(chr(tecla))
        elif tecla == c.KEY_ENTER or tecla == 10:
            self.PUSHPILA(tecla)
        elif tecla == c.KEY_RESIZE:
            self.Refrescar()
        else:
            self.Comando(self.PILA,self.linea,tecla)
        return

    def LineaInsertar(self,tecla):
        self.linea = libbasic.Insercion(self.linea,tecla)
        return

    def MostrarLinea(self):
        posy = self.alto - 2
        longitud = len(self.linea)-1
        posx = self.ancho - 2 - longitud
        self.win.addstr(posy,posx,self.linea)
        return
    
    def MostrarPila(self):
        # posición del primer elemento
        posy = self.alto - 3
        # tamaño máximo de pila
        tammax = 9
        cont = 0
        while cont < tammax:
            if cont < len(self.PILA):
                valor = self.PILA[len(self.PILA)-cont-1]
                valor = self.Formatear(valor)
                resto = ' ' * (34 - len(str(valor)))
                cadena = '%s: %s%s' % (cont+1,valor,resto)
            else:
                cadena = '%s:%s' %(cont+1,' '*32)
            self.win.addstr(posy-cont,2,cadena)
            cont += 1
        return

    def PUSHPILA(self,elemento):
        if len(self.linea):
            self.PILA.append(self.linea)
            self.linea = ''
            self.Refrescar()
        return
    
#### OPERACIONES
    def Suma(self):
        self.PILA.append(basic.Suma(self.PILA, self.linea))
        return

    def Resta(self):
        if len(self.linea):
            # Si linea tiene decimales
            if '.' in self.linea:
                numero = float(self.linea)
                numero = numero * -1
                self.linea = str(numero)
            else:
                self.linea = str(int(self.linea) * -1)
        else:
            if len(self.PILA) > 1:
                a = float(self.PILA.pop())
                b = float(self.PILA.pop())
                self.PILA.append(b-a)
                self.BorrarLinea()
        return

    def Multiplica(self):
        if len(self.linea):
            a = float(self.linea)
            self.BorrarLinea()
            b = float(self.PILA.pop())
            self.PILA.append(b*a)
        else:
            if len(self.PILA) > 1:
                a = float(self.PILA.pop())
                b = float(self.PILA.pop())
                self.PILA.append(b*a)
                self.BorrarLinea()
        return

#### FIN OPERACIONES

    def Formatear(self, valor):
        precision = self.precision
        valor = round(float(valor),precision)
        if '.' in str(valor):
            if int(str(valor).split('.')[1]) == 0:
                return int(valor)
            else:
                return round(float(valor),precision)
        else:
            return valor

    def Terminar(self):
        c.nocbreak()
        self.stdscr.keypad(0)
        c.echo()
        c.endwin()
        exit(0)

def main():
    Principal = Calculadora()
    Principal.Ventana()
    Principal.Refrescar()
    Principal.Peticion()
    Principal.Terminar()

if __name__ == '__main__':
    main()
