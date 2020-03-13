#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexer
import parser
import argparse
from code_generator import generar
import re, sys, os 

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Compilador de C hecho en Python3.7.6")
    argparser.add_argument('source_file', type=str, help='Archivo a compilar con extensión .c') 
    argparser.add_argument('-t','--tree', action='store_true', help='Desplegar del Arbol de Sintanxis Abstracto')
    argparser.add_argument('-a','--assembly', action='store_true', help='Desplegar codigo ensamblador')
    argparser.add_argument('-l','--ltokens', action='store_true', help='Desplegar lista de tokens')
    argparser.add_argument('-n','--name', type=str, help='Definir el nombre del ejecutable')
    args = argparser.parse_args()
    # source_file = sys.argv[1]
    assembly_file = os.path.splitext(args.source_file)[0] + ".s"

    with open(args.source_file, 'r') as infile, open(assembly_file, 'w') as outfile:
        source = infile.read().replace('\n', '').strip().replace(" ", "")
        new_tokens = []
        vacio = []
        lexado = lexer.lexing(source, new_tokens)
        if args.ltokens:
            print("Tokens lexados: ")
            print(lexado)
        arbol = parser.parsing(new_tokens, args.source_file)
        if args.tree:
            arbol.printTree()    
        generar(arbol, assembly_file)
        if args.assembly:
            print("Código Ensamblador")
            print(open(assembly_file).read())
        if args.name:
            os.system("gcc -m32 {} -o {}".format(assembly_file, args.name))
        else:
            os.system("gcc -m32 {} -o {}".format(assembly_file, args.source_file.split("/")[-1][:-2]))

# -O optimizador
# -t Impirmir Arbol AST
# -a asm 
# -h ayuda
# -l lista de tokens
# -n define el nombre   