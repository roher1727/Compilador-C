#!/usr/bin/python

import re, sys, os 
"""
The lexer (also called the scanner or tokenizer) is the phase of the compiler that breaks up a 
string (the source code) into a list of tokens. A token is the smallest unit the parser can understand - if a 
program is like a paragraph, tokens are like individual words. (Many tokens are individual words, separated by whitespace.) 
Variable names, keywords, and constants, and punctuation like braces are all examples of tokens. Here’s a list of all the tokens 
in return_2.c:

    -Open brace {
    -Close brace }
    -Open parenthesis \(
    -Close parenthesis \)
    -Semicolon ;
    -Int keyword int
    -Return keyword return
    -Identifier [a-zA-Z]\w*
    -Integer literal [0-9]+

"""

def lexing(cadena, new_tokens):
    """
        Retorna una lista de tokens predeterminados
        lexing(string, list)
        >>> lexing("int()", []) 
        >>> "int()", ["int", '(', ')']
    """

    palabras_reservadas = {"openBrace" : '{', "closeBrace" : '}', "openParen" : '(', "closeParen" : ')', "semicolon" : ';', "identifier":'main',  "constant" :r'[0-9]+', "negation":'-', "bitwise":'~', "logicalNegation":'!', "addition":'+', "multiplication":'*', "division":'/'}
    patrones = { "intKeyword" : 'int', "returnKeyword":'return'}
    identificacion = {'A' : palabras_reservadas, 'B' : patrones}
    alto = True
    for llave in identificacion:
        
        for tipo, patron in identificacion[llave].items():
            if tipo == "constant": 
                if re.match(r'[0-9]+',cadena):
                    alto = False
                    aux = re.findall(r'[0-9]+',cadena)
                    new_tokens.append((tipo, aux[0]))
                    cadena = cadena.replace(aux[0], '', 1)
            if cadena.startswith(patron):
                alto = False
                new_tokens.append((tipo, patron))
                cadena = cadena.replace(patron, '', 1)
    
    if alto:
        raise Exception("\n Syntax error: Undentified character {}".format(cadena))

    if not cadena:
        return new_tokens

    return lexing(cadena, new_tokens)
