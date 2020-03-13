#!/usr/bin/python

import sys

def generar(arbol, assembly_file):
    nodos = []
    nodos = postorder(arbol.raiz, nodos)
    f = open(assembly_file, "w")
    for n in nodos:
        generar_ensamblador(n, assembly_file)
    f.close()

def postorder(root, nodos):
    nodos.append(root)
    if root.izquierdo:
        postorder(root.izquierdo, nodos) 
    if root.derecho:
        postorder(root.derecho, nodos) 
    return nodos

def generar_ensamblador(nodo, assembly_file):
    f = open(assembly_file,"a")
    if nodo.tipo == "program":
        #f.write("{}"+"\n")
        f.write("\n")
    elif nodo.tipo == "function":
        f.write("\t.globl _" + nodo.dato + "\n_" + nodo.dato + ":\n")
    elif nodo.tipo == "constant":
        f.write("\tmov\t$" + str(nodo.dato) + ", %eax")
    elif nodo.tipo == "return":
        f.write("\n")
    elif nodo.tipo == "unaryop":
        if nodo.dato == '-':
            f.write("\n\tneg\t%eax")
        elif nodo.dato == '~':
            f.write("\n\tnot\t%eax")
        elif nodo.dato == '!':
            f.write("\n\tcmpl\t$0, %eax")
            f.write("\n\tmovl\t$0, %eax")
            f.write("\n\tsete\t%al")
    else:
        f.close()
        raise Exception("Operacion desconocida ")
    if nodo.izquierdo == None and nodo.derecho == None:
        f.write("\n\tret")
    f.close()


