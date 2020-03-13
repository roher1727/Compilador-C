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

def peek(tokens):
    if tokens:
        return tokens[0]
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
    log_and = parse_logical_and(tokens)
    siguiente = peek(tokens)
    while siguiente[0] == "OR":
        token = next(tokens)
        logy = parse_logical_and(tokens)
        if not log_and or not logy:
            raise Exception("No hay segundo termino")
        
        binaryop = AST.Node("binaryop", token[1], None)
        binaryop.insertIzq(log_and)
        binaryop.insertDer(logy)
        log_and = binaryop
        siguiente = peek(tokens)
    return log_and


def parse_logical_and(tokens):
    equality = parse_equality(tokens)
    siguiente = peek(tokens)
    while siguiente[0] == "AND":
        token = next(tokens)
        equidad = parse_equality(tokens)
        if not equality or not equidad:
            raise Exception("No hay segundo termino")
        
        binaryop = AST.Node("binaryop", token[1], None)
        binaryop.insertIzq(equality)
        binaryop.insertDer(equidad)
        equality = binaryop
        siguiente = peek(tokens)
    return equality

def parse_equality(tokens):
    relation = parse_relational(tokens)
    siguiente = peek(tokens)
    while siguiente[0] == "equal" or  siguiente[0] == "notequal":
        token = next(tokens)
        relacion = parse_relational(tokens)
        if not relation or not relacion:
            raise Exception("No hay segundo termino")
        
        binaryop = AST.Node("binaryop", token[1], None)
        binaryop.insertIzq(relation)
        binaryop.insertDer(relacion)
        relation = binaryop
        siguiente = peek(tokens)
    return relation


def parse_relational(tokens):
    addition = parse_addition(tokens)
    siguiente = peek(tokens)
    while siguiente[0] == "lessthan" or  siguiente[0] == "lessthanequal" or  siguiente[0] == "greaterthan" or  siguiente[0] == "greaterthanequal":
        token = next(tokens)
        adicion = parse_addition(tokens)
        if not addition or not adicion:
            raise Exception("No hay segundo termino")
        
        binaryop = AST.Node("binaryop", token[1], None)
        binaryop.insertIzq(addition)
        binaryop.insertDer(adicion)
        addition = binaryop
        siguiente = peek(tokens)
    return addition

def parse_addition(tokens):
    term = parse_term(tokens)
    siguiente = peek(tokens)
    while siguiente[0] == "addition" or siguiente[0] == "negation":
        token = next(tokens)
        termy = parse_term(tokens)

        if not term or not termy:
            raise Exception("No hay segundo termino")
        
        binaryop = AST.Node("binaryop", token[1], None)
        binaryop.insertIzq(term)
        binaryop.insertDer(termy)
        term = binaryop
        siguiente = peek(tokens)
    return term

def parse_term(tokens):
    factor = parse_factor(tokens)
    siguiente = peek(tokens)
    #print(siguiente)
    while siguiente[0] == "multiplication" or siguiente[0] == "division":
        token = next(tokens)
        factor_2 = parse_factor(tokens)
        if not factor or not factor_2:
            raise Exception("No hay segundo termino")

        binaryop = AST.Node("binaryop", token[1], None)
        binaryop.insertIzq(factor)
        binaryop.insertDer(factor_2)
        factor = binaryop
        siguiente = peek(tokens)
        if siguiente[1] == '0':
            raise Exception("Not possible division by zero")
    return factor

def parse_factor(tokens):
    nextToken = next(tokens)
    if nextToken[0] == "openParen":
        exp = parse_expression(tokens)
        nextToken = next(tokens)
        if nextToken[0] != "closeParen":
            raise Exception("El par de parentesis del factor esta incompleto")
        return exp
    elif nextToken[0] == "constant":
        constant = AST.Node("constant", nextToken[1], None)
        return constant
    elif parse_unaryop(nextToken):
        unaryop = parse_unaryop(nextToken)
        factor = parse_factor(tokens)
        if not factor:
            raise Exception("No hay constante")
        unaryop.insertIzq(factor)
        return unaryop
    else:
        raise Exception("Ultimo termino no son paréntesis, constantes u operadores unarios")

def parse_unaryop(token):
    if token[0] != "negation" and token[0] != "logicalNegation" and token[0] != "bitwise":
        raise Exception("Unknown character: ", token[1])        
    else:
        unaryOp = AST.Node("unaryop", token[1], None)
        return unaryOp