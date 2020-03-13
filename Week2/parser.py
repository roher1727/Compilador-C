#!/usr/bin/python

"""
Write a parse function that accepts a list of tokens and returns an AST, rooted at a Program node. 
The function should build the correct AST for all valid stage 1 examples, and raise an error on all invalid stage 1 examples.
If you want, you can also have your parser fail gracefully if it encounters integers above your system’s INT_MAX.

There are a lot of ways to represent an AST in code - each type of node could be its own class or its own datatype,
depending on what language you’re writing your compiler in. For example, here’s how you might define AST nodes as OCaml 
datatypes.
"""
import AST 

def next(tokens):
    if tokens:
        return tokens.pop(0)
    else:
        return (None, None)

def parsing(tokens, nombre):
    program = parse_program(tokens, nombre)

    ast = AST.AST(program)
    return ast 
    
def parse_program(tokens, nombre):
    if tokens:
        fun = parse_function(tokens)
        if not fun:
            return 0
        #Creates a node program
        program = AST.Node("program", nombre, None)
        program.insertIzq(fun)
    
    return program

def parse_function(tokens):
    nextToken = next(tokens)
    if nextToken[0] != "intKeyword":
        raise Exception("Unknown character: ", nextToken[1])
    nextToken = next(tokens)
    if nextToken[0] != "identifier":
        raise Exception("Unknown character: ", nextToken[1])
    else:
        identifier = nextToken[1]
    nextToken = next(tokens)
    if nextToken[0] != "openParen":
        raise Exception("Función sin parentesis izquierdo \n Unknown character: ", nextToken[1])
    nextToken = next(tokens)
    if nextToken[0] != "closeParen":
        raise Exception("Función sin parentesis derecho \n Unknown character: ", nextToken[1])
    nextToken = next(tokens)
    if nextToken[0] != "openBrace":
        raise Exception("Unknown character: ", nextToken[1])
    stat = parse_statement(tokens)
    if not stat:
        return 0
    #Creates a function node
    function = AST.Node("function", identifier, None)
    function.insertIzq(stat)
    nextToken = next(tokens)
    if nextToken[0] != "closeBrace":
        raise Exception("Unknown character: ", nextToken[1])

    return function

def parse_unaryop(token):
    if token[0] != "negation" and token[0] != "logicalNegation" and token[0] != "bitwise":
        raise Exception("Unknown character: ", token[1])        
    else:
        #Node for unary operators
        unaryOp = AST.Node("unaryop", token[1], None)
        return unaryOp

def parse_statement(tokens):
    nextToken = next(tokens)
    if nextToken[0] != "returnKeyword":
        raise Exception("Unknown character: ", nextToken[1])
    #Validates the expresion
    exp = parse_expression(tokens)
    if not exp:
        return 0
    #Creates a statement node
    statement = AST.Node("return", nextToken[1], None)
    statement.insertIzq(exp)
    nextToken = next(tokens)
    if nextToken[0] != "semicolon":
        raise Exception("Unknown character: ", nextToken[1])
    return statement

def parse_expression(tokens):
    nextToken = next(tokens)
    if nextToken[0] == "constant":
        constant = AST.Node("constant", nextToken[1], None)
    else:
        op = parse_unaryop(nextToken)
        inner_exp = parse_expression(tokens)
        if inner_exp.izquierdo:
            inner_exp.izquierdo.insertIzq(op)
        else:
            inner_exp.insertIzq(op)
        return inner_exp
    return constant