#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def Suma(pila,linea):
    if len(linea):
        a = float(linea)
        b = float(pila.pop())
    else:
        a = float(pila.pop())
        b = float(pila.pop())
    valor = str(a+b)
    return valor

def Insercion(linea,pulsacion):
    if pulsacion == '.' and pulsacion not in linea or pulsacion != '.':
        linea += pulsacion
    return linea

def FormatElementoPila(elemento):
    return
