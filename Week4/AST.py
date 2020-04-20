#!/usr/bin/python

# Arbol AST

class Node():
    def __init__(self, tipo, dato, padre):
        self.tipo = tipo
        self.dato = dato
        self.padre = padre
        self.izquierdo = None
        self.derecho = None

    def insertIzq(self, Node):
        Node.padre = self
        self.izquierdo = Node

    def insertDer(self, Node):
        Node.padre = self
        self.derecho = Node

class AST():

    def __init__(self, raiz):
        self.raiz = raiz

    def printTree(self):
        if(self.raiz!=None):
            self.printarbol(self.raiz,0,"")
        print()

    def printarbol(self,Node,count,hoja):
        if count >= 1:
            if Node.izquierdo or Node.derecho:
                print("|--->", end="")
            else:
                print("|--->", end="")

        print(hoja,Node.tipo,": ",str(Node.dato))
        
        if Node.izquierdo or Node.derecho:
            if Node.izquierdo:
                for _ in range(count):
                    print("   ", end="")
                self.printarbol(Node.izquierdo,count+1,"(izquierdo)")
            if Node.derecho:
                for _ in range(count):
                    print("   ", end="")
                self.printarbol(Node.derecho,count+1,"(derecho)")