import sys

def generar(arbol, assembly_file):
    nodos = []
    nodos = postorder(arbol.raiz, nodos)
    f = open(assembly_file, "w")
    for n in nodos:
        #f.write(n.dato)
        #f.write(n.tipo)
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
        # f.write("\tret")
        f.write("\n")
    else:
        f.close()
        raise Exception("Operacion desconocida ")
    if nodo.izquierdo == None and nodo.derecho == None:
        f.write("\n\tret")
    f.close()


