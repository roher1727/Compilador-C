import unittest
import logging
import lexer
import parser
import argparse
import AST
import os
from code_generator import generar

def postorder(root, nodos):
    nodos.append(root.dato)
    if root.izquierdo:
        postorder(root.izquierdo, nodos) 
    if root.derecho:
        postorder(root.derecho, nodos) 
    return nodos

class test_compilador(unittest.TestCase):

    def test_lexing_and_true(self):
        with open("valid/and_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace','{'), ('returnKeyword', 'return'), ('constant', '1'), ('AND', '&&'), ('negation', '-'),('constant', '1'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_and_false(self):    
        with open("valid/and_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('AND', '&&'), ('constant', '0'), ('semicolon', ';'), ('closeBrace', '}')])
    
    def test_lexing_eq_false(self):    
        with open("valid/eq_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('equal', '=='), ('constant', '2'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_eq_true(self):    
        with open("valid/eq_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('equal', '=='), ('constant', '1'), ('semicolon', ';'), ('closeBrace', '}')])
    
    def test_lexing_ge_true(self):
        with open("valid/ge_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('greaterthanequal', '>='), ('constant', '1'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_ge_false(self):    
        with open("valid/ge_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('greaterthanequal', '>='), ('constant', '2'), ('semicolon', ';'), ('closeBrace', '}')])
    
    def test_lexing_le_false(self):     
        with open("valid/le_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('lessthanequal', '<='), ('negation', '-'), ('constant', '1'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_le_true(self):     
        with open("valid/le_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '0'), ('lessthanequal', '<='), ('constant', '2'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_lt_false(self):
        with open("valid/lt_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '2'), ('lessthan', '<'), ('constant', '1'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_lt_true(self):
        with open("valid/lt_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('lessthan', '<'), ('constant', '2'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_ne_true(self):
        with open("valid/ne_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('negation', '-'), ('constant', '1'), ('notequal', '!='), ('negation', '-'), ('constant', '2'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_ne_false(self):
        with open("valid/ne_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '0'), ('notequal', '!='), ('constant', '0'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_or_false(self):
        with open("valid/or_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '0'), ('OR', '||'), ('constant', '0'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_or_true(self):
        with open("valid/or_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('OR', '||'), ('constant', '0'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_precedence(self):
        with open("valid/precedence.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '1'), ('OR', '||'), ('constant', '0'), ('AND', '&&'), ('constant', '2'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_precedence2(self):
        with open("valid/precedence_2.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('openParen', '('), ('constant', '1'), ('OR', '||'), ('constant', '0'), ('closeParen', ')'), ('AND', '&&'), ('constant', '0'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_precedence3(self):
        with open("valid/precedence_3.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '2'), ('equal', '=='), ('constant', '2'), ('greaterthan', '>'), ('constant', '0'), ('semicolon', ';'), ('closeBrace', '}')])

    def test_lexing_precedence4(self):
        with open("valid/precedence_4.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            self.assertEqual(lexer.lexing(archivo, []), [('intKeyword', 'int'), ('identifier', 'main'), ('openParen', '('), ('closeParen', ')'), ('openBrace', '{'), ('returnKeyword', 'return'), ('constant', '2'), ('equal', '=='), ('constant', '2'), ('OR', '||'), ('constant', '0'), ('semicolon', ';'), ('closeBrace', '}')])


    def test_parsing_and_true(self):
        with open("valid/and_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/and_true.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '&&', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            operador_un_n = AST.Node('unaryop', '-', None)
            operador_bi_n.insertDer(operador_un_n)
            constante_der = AST.Node('constant', '1', None)
            operador_un_n.insertIzq(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/and_true.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))
    
    def test_parsing_and_false(self):
        with open("valid/and_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/and_false.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '&&', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '0', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/and_false.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_eq_false(self):
        with open("valid/eq_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/eq_false.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '==', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '2', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/eq_false.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_eq_true(self):
        with open("valid/eq_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/eq_true.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '==', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '1', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/eq_true.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_ge_true(self):
        with open("valid/ge_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/ge_true.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '>=', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '1', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/ge_true.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_ge_false(self):
        with open("valid/ge_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/ge_false.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '>=', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '2', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/ge_false.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_le_false(self):
        with open("valid/le_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/le_false.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '<=', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            operador_un_n = AST.Node('unaryop', '-', None)
            operador_bi_n.insertDer(operador_un_n)
            constante_der = AST.Node('constant', '1', None)
            operador_un_n.insertIzq(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/le_false.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_le_true(self):
        with open("valid/le_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/le_true.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '<=', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '0', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '2', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/le_true.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_lt_false(self):
        with open("valid/lt_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/lt_false.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '<', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '2', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '1', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/lt_false.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_lt_true(self):
        with open("valid/lt_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/lt_true.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '<', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '2', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/lt_true.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_ne_false(self):
        with open("valid/ne_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/ne_false.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '!=', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '0', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '0', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/ne_false.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_ne_true(self):
        with open("valid/ne_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/ne_true.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '!=', None)
            return_n.insertIzq(operador_bi_n)
            operador_un = AST.Node('unaryop', '-', None)
            operador_bi_n.insertIzq(operador_un)
            constante_izq = AST.Node('constant', '1', None)
            operador_un.insertIzq(constante_izq)
            operador_un_n = AST.Node('unaryop', '-', None)
            operador_bi_n.insertDer(operador_un_n)
            constante_der = AST.Node('constant', '2', None)
            operador_un_n.insertIzq(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/ne_true.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_or_false(self):
        with open("valid/or_false.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/or_false.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '||', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '0', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '0', None)
            operador_bi_n.insertDer(constante_der)
        
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/or_false.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_or_true(self):
        with open("valid/or_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/or_true.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '||', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '0', None)
            operador_bi_n.insertDer(constante_der)
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/or_true.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_precedence(self):
        with open("valid/precedence.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/precedence.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '||', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_n.insertIzq(constante_izq)
            operador_bi_der = AST.Node('binaryop', '&&', None)
            operador_bi_n.insertDer(operador_bi_der)
            constante_izq = AST.Node('constant', '0', None)
            operador_bi_der.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '2', None)
            operador_bi_der.insertDer(constante_der)
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/precedence.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_precedence_2(self):
        with open("valid/precedence_2.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/precedence_2.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '&&', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '0', None)
            operador_bi_n.insertDer(constante_izq)
            operador_bi_der = AST.Node('binaryop', '||', None)
            operador_bi_n.insertIzq(operador_bi_der)
            constante_izq = AST.Node('constant', '1', None)
            operador_bi_der.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '0', None)
            operador_bi_der.insertDer(constante_der)
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/precedence_2.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_precedence_3(self):
        with open("valid/precedence_3.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/precedence_3.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '==', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '2', None)
            operador_bi_n.insertIzq(constante_izq)
            operador_bi_der = AST.Node('binaryop', '>', None)
            operador_bi_n.insertDer(operador_bi_der)
            constante_izq = AST.Node('constant', '2', None)
            operador_bi_der.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '0', None)
            operador_bi_der.insertDer(constante_der)
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/precedence_3.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))

    def test_parsing_precedence_4(self):
        with open("valid/precedence_4.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")
            raiz = AST.Node('program', 'valid/precedence_4.c', None)
            funcion_n = AST.Node('identifier', 'main', None)
            raiz.insertIzq(funcion_n)
            return_n = AST.Node('return', 'return', None)
            funcion_n.insertIzq(return_n)
            operador_bi_n = AST.Node('binaryop', '||', None)
            return_n.insertIzq(operador_bi_n)
            constante_izq = AST.Node('constant', '0', None)
            operador_bi_n.insertDer(constante_izq)
            operador_bi_der = AST.Node('binaryop', '==', None)
            operador_bi_n.insertIzq(operador_bi_der)
            constante_izq = AST.Node('constant', '2', None)
            operador_bi_der.insertIzq(constante_izq)
            constante_der = AST.Node('constant', '2', None)
            operador_bi_der.insertDer(constante_der)
            arbol = AST.AST(raiz)
            
            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/precedence_4.c")
            l_arbol = []
            l_arbol_prueba = []
            print()
            self.assertEqual(postorder(arbol.raiz, l_arbol), postorder(arbol_prueba.raiz, l_arbol_prueba))
   
    def test_missing_first_op(self):
        with open("invalid/missing_first_op.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            
            try:
                tokens = lexer.lexing(archivo, [])
                parser.parsing(tokens, "valid/missing_first_op.c")
            except Exception:
                print("Error por: ")

    def test_missing_second_op(self):
        with open("invalid/missing_second_op.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            try:
                tokens = lexer.lexing(archivo, [])
                parser.parsing(tokens, "valid/missing_second_op.c")
            except Exception:
                print("Error por: ")
    
    def test_missing_mid_op(self):
        with open("invalid/missing_mid_op.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            try:
                tokens = lexer.lexing(archivo, [])
                parser.parsing(tokens, "valid/missing_mid_op.c")
            except Exception:
                print("Error por: ")
    
    def test_missing_semicolon(self):
        with open("invalid/missing_semicolon.c", 'r') as infile:
            archivo = infile.read().replace('\n','').strip().replace(" ", "")
            try:
                tokens = lexer.lexing(archivo, [])
                parser.parsing(tokens, "valid/missing_semicolon.c")
            except Exception:
                print("Error por: ")

    def test_salida(self):
        assembly_file = os.path.splitext("valid/and_true.c")[0] + ".s"
        with open("valid/and_true.c", 'r') as infile:
            archivo = infile.read().replace('\n', '').strip().replace(" ", "")

            tokens = lexer.lexing(archivo, [])
            arbol_prueba = parser.parsing(tokens, "valid/and_true.c")
            generar(arbol_prueba, assembly_file)
            os.system("gcc -m32 {} -o {}".format(assembly_file, "and_true"))
            os.system("gcc -w valid/and_true.c")
            prueba = os.popen("./and_true;echo $?").read()
            verdadero = os.popen("./a.out;echo $?").read()
            print(prueba, verdadero)
            self.assertEqual(prueba, verdadero)
            
if __name__ == '__main__':
    unittest.main()