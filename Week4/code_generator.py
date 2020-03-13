#!/usr/bin/python

import sys

def generar(arbol, assembly_file):
    nodos = []
    nodos = postorder(arbol.raiz, nodos)
    binario = False
    for nodo in nodos:
        if nodo.tipo == "binaryop":
            binario = True
    if binario: 
        indice = [n.tipo for n in nodos].index("binaryop")
        f = open(assembly_file, "w")
        for n in nodos[:indice]:
            generar_ensamblador(n, assembly_file)

        ensamblador_binario(nodos[indice:][0], assembly_file)
        f.close()
    else: 
        f = open(assembly_file, "w")
        for n in nodos:
            generar_ensamblador(n, assembly_file)
        f.close()
    f = open(assembly_file,"a")
    f.write("\n\tret")
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
        f.write("\t.globl _" + nodo.dato + "\n_" + nodo.dato + ":")
    elif nodo.tipo == "constant":
        f.write("\n\tmov\t$" + str(nodo.dato) + ", %eax")
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
    f.close()

def ensamblar_unario(nodo, assembly_file):
    if nodo.tipo == "unaryop":
        generar_ensamblador(nodo, assembly_file)
        ensamblador_binario(nodo.izquierdo, assembly_file)
    elif nodo.tipo == "constant":
        generar_ensamblador(nodo, assembly_file)

def ensamblador_binario(nodo, assembly_file):
    
    if nodo.izquierdo:
        if nodo.izquierdo.tipo == "binaryop":
            ensamblador_binario(nodo.izquierdo, assembly_file)
    elif nodo.derecho:
        if nodo.derecho.tipo == "binaryop": 
            ensamblador_binario(nodo.derecho, assembly_file)

    if nodo.izquierdo:
        ensamblar_unario(nodo.izquierdo, assembly_file)
        f = open(assembly_file,"a")
        if nodo.dato=="||":
            f.write("\n\tcmpl\t$0, %eax")
            f.write("\n\tje\t_clause2")
            f.write("\n\tmovl\t$1, %eax")
            f.write("\n\tjmp\t_end")
            f.write("\n_clause2:")
        elif nodo.dato=="&&":
            f.write("\n\tcmpl\t$0, %eax")
            f.write("\n\tje\t_clause2")
            f.write("\n\tjmp\t_end")
            f.write("\n_clause2:")
        else:
            f.write("\n\tpush\t%eax")
        f.close()
    if nodo.derecho:
        ensamblar_unario(nodo.derecho, assembly_file)
        f = open(assembly_file,"a")
        if nodo.dato=="||":
            f.write("\n\tcmpl\t$0, %eax")
            f.write("\n\tmovl\t$0, %eax")
            f.write("\n\tsetne\t%al")
            f.write("\n_end:")
        elif nodo.dato=="&&":
            f.write("\n\tcmpl\t$0, %eax")
            f.write("\n\tmovl\t$0, %eax")
            f.write("\n\tsetne\t%al")
            f.write("\n_end:")
        else:
            f.write("\n\tpop\t%ecx")
        f.close()

    f = open(assembly_file,"a")
    if nodo.dato == '+':
        f.write("\n\taddl\t%ecx, %eax")
    elif nodo.dato == '*':
        f.write("\n\timul\t%ecx, %eax")
    elif nodo.dato == '/':
        f.write("\n\tidivl\t%ecx, %eax")
    elif nodo.dato == '-':
        f.write("\n\tsubl\t%ecx, %eax")
    elif nodo.dato == '==':
        f.write("\n\tcmpl\t%eax, %ecx")
        f.write("\n\tmovl\t$0, %eax")
        f.write("\n\tsete\t%al")
    elif nodo.dato == '!=':
        f.write("\n\tcmpl\t%eax, %ecx")
        f.write("\n\tmovl\t$0, %eax")
        f.write("\n\tsetne\t%al")
    elif nodo.dato == '>=':
        f.write("\n\tcmpl\t%eax, %ecx")
        f.write("\n\tmovl\t$0, %eax")
        f.write("\n\tsetge\t%al")
    elif nodo.dato == '<=':
        f.write("\n\tcmpl\t%eax, %ecx")
        f.write("\n\tmovl\t$0, %eax")
        f.write("\n\tsetle\t%al")
    elif nodo.dato == '<':
        f.write("\n\tcmpl\t%eax, %ecx")
        f.write("\n\tmovl\t$0, %eax")
        f.write("\n\tsetl\t%al")
    elif nodo.dato == '>':
        f.write("\n\tcmpl\t%eax, %ecx")
        f.write("\n\tmovl\t$0, %eax")
        f.write("\n\tsetg\t%al")
    f.close()