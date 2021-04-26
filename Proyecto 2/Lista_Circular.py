class Gramatica:
    def __init__(self, nombre=None, lista_NoTerminales=None, lista_Terminales=None, NoTerminalInicial=None, listaProducciones=None):
        self.nombre = nombre
        self.lista_NoTerminales = lista_NoTerminales
        self.listaTerminales = lista_Terminales
        self.NoTerminalInicial = NoTerminalInicial
        self.listaProducciones = listaProducciones


class Nodo:
    def __init__(self, gramatica=None, siguiente=None):
        self.gramatica = gramatica
        self.siguiente = siguiente
    

class Lista_Circular:
    def __init__(self, head=None):
        self.head = head
        self.tamano = 0
    
    def insertar_gramatica(self, nombre_gramatica=None, lista_NoTerminales=None, lista_Terminales=None, NoTerminalInicial=None, listaProducciones=None):
        if self.tamano == 0:
            gramatica = Gramatica(nombre=nombre_gramatica, lista_NoTerminales=lista_NoTerminales, lista_Terminales=lista_Terminales, NoTerminalInicial=NoTerminalInicial, listaProducciones=listaProducciones)
            self.head = Nodo(gramatica=gramatica)
            self.head.siguiente = self.head
        else:
            gramatica = Gramatica(nombre=nombre_gramatica, lista_NoTerminales=lista_NoTerminales, lista_Terminales=lista_Terminales, NoTerminalInicial=NoTerminalInicial, listaProducciones=listaProducciones)
            nuevo_nodo = Nodo(gramatica=gramatica, siguiente=self.head.siguiente)
            self.head.siguiente = nuevo_nodo
        self.tamano += 1

    def buscar_gramatica(self, nombre_gramatica):
        if self.tamano == 0:
            return False
        
        nodo = self.head
        for i in range(self.tamano):
            if nodo.gramatica.nombre == nombre_gramatica:
                return nodo.gramatica
            nodo = nodo.siguiente