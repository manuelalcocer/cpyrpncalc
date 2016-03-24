# -*- coding: utf-8 -*-

class Operators:
    def __init__(self):
        operators = [ '+', '-', '*', '/', '^', '%', 'v', 'V' ]
        self.BasicOperators = [ ord(operator) for operator in operators ]
        return

##############################################
# Element types: int,float,matrix,complex,... #
###############################################

class IntElement:
    def __init__(self,enumber):
        self.element = {}
        self.element['value'] = int(enumber)
        self.type = 'int' 
        return

    def __str__(self):
        value = '%s' %self.element['value']
        return value

class FloatElement:
    def __init__(self,enumber):
        self.element = {}
        self.element['value'] = float(enumber)
        self.element['int'] = int(str(self.element['value']).split('.')[0])
        self.element['dec'] = int(str(self.element['value']).split('.')[1])
        self.precission = len(str(self.element['dec']))
        self.type = 'float'
        return

    def __str__(self):
        value = '%s' %self.element['value']
        return value

class Element(object):
    def __init__(self,enumber,algtype):

        pass

    def __getattr__(self,name):
        return self[name]

    def __setattr__(self,value):
        self[name] = value

#####################
# END Element Types #
#####################

def CreateElement(enumber, algtype):
    if algtype == 'int':
        # int number
        element = IntElement(enumber)
    elif algtype == 'float':
        # float number
        element = FloatElement(enumber)
    elif algtype == 'complex':
        # complex number
        pass
    elif algtype == 'matrix':
        # matrix number
        pass
    elif algtype == 'list':
        # list number
        pass
    return element


##############
# OPERATIONS #
##############

def Operation(Stack,Line,operator):
    operator = chr(operator)
    if operator == '+':
        # Add operation
        Run(Stack,Line,operator)
    elif operator == '-' and len(Line.linecontent) != 0:
        # substract
        Run(Stack,Line,operator)
        pass
    elif operator == '*':
        # multiply operation
        Run(Stack,Line,operator)
        pass
    elif operator == '/':
        Run(Stack,Line,operator)
        # divide operation
        pass
    elif operator == '%':
        # module operation
        Run(Stack,Line,operator)
        pass
    elif operator == 'v':
        # sqr operation
        Run(Stack,Line,operator)
        pass
    elif operator == '^':
        # power operation
        Run(Stack,Line,operator)
        pass
    elif operator == '-' and len(Line.linecontent):
        # line * -1
        value = CreateElement(Line.linecontent,Line.algtype)
        pass
    return 

def Calc(x,y,op):
    if op == '+':
        return x + y
    elif op == '*':
        return x * y
    elif op == '/':
        if y == 0:
            return 0
        else:
            return y / x
    elif op == '%':
        if y == 0:
            return 0
        else:
            return y % x
    return

def Run(Stack,Line,operator):
    if len(Line.linecontent):
        y = CreateElement(Line.linecontent,Line.algtype)
        Line.CleanLineContent()
    elif len(Stack.StackLines) > 1:
        y = Stack.POP()
    else:
        y = Stack.StackLast()
    x = Stack.POP()
    if y.type == 'float' or x.type == 'float':
        newtype = y.type
    elif y.type == x.type and y.type == 'int':
        newtype = y.type
    value = Calc(y.element['value'], x.element['value'], operator)
    Stack.PUSH(str(value),newtype)
    return
