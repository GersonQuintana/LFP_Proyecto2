import Lista_Circular

class Analizar_Archivo:

    def __init__(self, ruta):
        self.ruta = ruta
        self.lista_circular = Lista_Circular.Lista_Circular()
        self.nombre = ""
        self.noTerminales = []
        self.terminales = []
        self.terminal_inicial = []
        self.producciones = []
        self.nombres_gramaticas = []    # Guardar todos los nombre de las gramaticas
        self.contador = 0               # Para guiar que linea de la gramatica estoy 
        self.libre_del_contexto = False  # Para validar que la gramatica sea libre del contexto
        
    
    # Enviara las lineas del archivo para que sea analizado
    def analizar_file(self):
        archivo = open(self.ruta, "r", encoding="UTF-8")

        for linea in archivo.readlines():

            if linea != "\n":
                # Cuando encuentre un '*' significa que es el fin de una gramatica
                if linea.strip() == "*":
                    
                    # Por lo menos se encontro en la parte derecha de una produccion
                    # la estructura de una gramatica libre del contexto, es decir, si la 
                    # variable self.libre_del_contexto cambio su valor a True
                    if self.libre_del_contexto == True:
                        self.lista_circular.insertar_gramatica(nombre_gramatica=self.nombre, lista_NoTerminales=self.noTerminales, lista_Terminales=self.terminales, listaProducciones=self.producciones)
                        self.nombres_gramaticas.append(self.nombre)     # Agregando el nombre de la gramatica a la lista de nombres de las gramaticas

                    # Resetendo todas las variables para podera agregar una nueva gramatica
                    self.nombre = []
                    self.noTerminales = []
                    self.terminales = []
                    self.terminal_inicial = []
                    self.producciones = []
                    self.contador = 0
                    self.libre_del_contexto = False

                else:
                    self.estructurar_gramatica(linea)
    

    # Va a ir guardando las listas necesarias para guardar una gramatica
    def estructurar_gramatica(self, linea):
        if self.contador == 0:              # Estoy leyendo la primera linea de la estructura de la gramatica: LEER EL NOMBRE DE LA GRAMATICA
            self.nombre = linea.strip()
            self.contador += 1
        
        elif self.contador == 1:            # Estoy leyendo la segunda linea de la estructura de la gramatica: LEER 'NO TERMINALES', 'TERMINALES' Y 'NO TERMINAL INICIAL'
            lista = linea.split(";")        # Separandolos por el ';'
            # Se creara un lista con 3 posiciones
            self.noTerminales = lista[0].split(",")
            self.terminales = lista[1].split(",")
            self.terminal_inicial.append(lista[2].strip())
            self.contador += 1
        
        else:                               # Estoy leyendo las lineas que siguen: LEER PRODUCCIONES
            self.producciones.append(linea.strip())

            lista = linea.strip().split("->")
            # En la segunda posicion de 'lista' contendra las expresiones que se producen
            #cadena = lista[1].replace(" ","")   # Con esto se obtiene una cadena sin espacios

            # Aqui sera de validar que la produccion sea de una gramatica libre de contexto      
            contador_terminales = 0
            contador_no_terminales = 0
            derecha_produccion = lista[1]
            #print("(" + derecha_produccion + ")")

            for i in range(len(derecha_produccion)):
                caracter = derecha_produccion[i]
                if caracter != " " and caracter != "\t":
                    if caracter in self.terminales:
                        contador_terminales += 1
                    elif caracter in self.noTerminales:
                        contador_no_terminales += 1
            
            # print("ContadorTerminales == ", contador_terminales)
            # print("ContadorNoTerminales == ", contador_no_terminales)
            # print("------")
            
            # Los siguientes 'if' solo son de las dos formas en que puede el lado derecho de una
            # produccion de una gramatica regular, por lo que simplemente no se hace nada, ya que solo se cambiara
            # cuando encuentre una estructura de una gramatica libre del contexto
            if contador_terminales == 1 and contador_no_terminales == 1:    # Significa que esta produccion no pertenece a una gramatica regular
                print("", end="")                              
            elif contador_terminales == 1 and contador_no_terminales == 0:  # Significa que esta produccion no pertenece a una gramatica regular
                print("", end="")
            elif contador_terminales == 0 and contador_no_terminales == 0:  # Significa que no se reconocio ningun terminal o no terminal definido al principio de la gramatica
                print("Los caracteres no forman parte del alfabeto")
            else:
                self.libre_del_contexto = True                              # Significa que es una gramatica libre del contexoto
            
    
    def imprimir_gramaticas(self, nombre_gramatica):
        gramatica = self.lista_circular.buscar_gramatica(nombre_gramatica)
        return gramatica


