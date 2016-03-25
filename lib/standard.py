# -*- coding: utf-8 -*-

from sys import maxint,float_info
import trig

class Operators:
    def __init__(self):
        operators = [ '+', '-', '*', '/', '^', '%', 'v', 'V' ]
        self.BasicOperators = [ ord(operator) for operator in operators ]
        return

##############################################
# Element types: int,float,matrix,complex,... #
###############################################

class Element:
    def __init__(self,enumber,algtype):
        self.element = {}
        self.type = algtype
        self.DefType(enumber)
        return
    
    def DefType(self,enumber):
        if self.type == int:
            self.value = int(enumber)
        elif self.type == float:
            self.value = float(enumber)
        elif self.type == complex:
            self.value == complex(enumber)
        return

    def __str__(self):
        value = '%s' %self.value
        return value

    def __add__(self, otro):
        try:
            return self.value + otro.value
        except:
            return self.value

    def __sub__(self, otro):
        try:
            return self.value - otro.value
        except:
            return self.value

    def __mod__(self, otro):
        try:
            return self.value % otro.value
        except ZeroDivisionError:
            return float_info.min

    def __mul__(self, otro):
        try:
            return self.value * otro.value
        except:
            return self.value

    def __div__(self, otro):
        try:
            return self.value / otro.value
        except ZeroDivisionError:
            return maxint

    def __pow__(self, otro):
        try:
            return self.value ** otro.value
        except:
            return self.value

#####################
# END Element Types #
#####################

def CreateElement(enumber, algtype):
    if algtype == int:
        # int number
        element = Element(enumber,algtype)
    elif algtype == float:
        # float number
        element = Element(enumber,algtype)
    elif algtype == complex:
        # complex number
        pass
    elif algtype == 'matrix':
        # matrix number
        pass
    elif algtype == list:
        # list number
        pass
    return element

##############
# OPERATIONS #
##############
def Operation(Stack,Line,operator):
    operator = chr(operator)
    Run(Stack,Line,operator)
    return 

def Calc(x,y,op):
    if op == '+':
        return x + y
    elif op == '*':
        return x * y
    elif op == '/':
        return x / y
    elif op == '%':
        return x % y
    elif op == '^':
        return x ** y
    elif op == 'v':
        return y ** x
    return

def Run(Stack,Line,operator):
    if len(Line.linecontent):
        y = CreateElement(Line.linecontent,Line.algtype)
        Line.CleanLineContent()
    elif len(Stack.StackLines) > 1:
        y = Stack.POP()
    else:
        y = Stack.StackLast()
    if operator not in ['v', 'V']:
        x = Stack.POP()
    elif operator == 'v':
        x = CreateElement('0.5',float)
    value = Calc(x, y, operator)
    newtype = type(value)
    Stack.PUSH(str(value),newtype)
    return
