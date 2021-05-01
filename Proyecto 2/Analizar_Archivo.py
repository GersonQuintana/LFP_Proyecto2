import Lista_Circular
from reportes import Reporte_Gramaticas

class Analizar_Archivo:

    def __init__(self, ruta):
        self.ruta = ruta    # Ruta del archivo  
        self.lista_circular = Lista_Circular.Lista_Circular()
        self.nombre = ""    # Nombre de la gramatica
        self.noTerminales = []  # Guarda todos los no terminales de la gramatica
        self.terminales = []    # Guardara todos los terminales de la gramatica
        self.no_terminal_inicial = ""   # Guardara el no terminal inicial de la gramatica
        self.producciones = []  # Se guardaran las producciones de una gramatica
        self.nombres_gramaticas = []    # Guardar todos los nombre de las gramaticas
        self.estado = 0               # Para guiar que linea de la gramatica estoy 
        self.libre_del_contexto = False  # Para validar que la gramatica sea libre del contexto
        self.gramaticas_no_cargadas = []    # Se guardara el nombre de las gramaticas que no sean libres del contexto
        self.cont_gramaticas_no_cargadas = 0    # Llevara el numero de gramaticas no cargadas
        
    
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
                        self.lista_circular.insertar_gramatica(nombre_gramatica=self.nombre, lista_NoTerminales=self.noTerminales, lista_Terminales=self.terminales, NoTerminalInicial=self.no_terminal_inicial, listaProducciones=self.producciones)
                        self.nombres_gramaticas.append(self.nombre)     # Agregando el nombre de la gramatica a la lista de nombres de las gramaticas
                    
                    else:
                        Reporte_Gramaticas.agregar_al_reporte(self.nombre)
                        self.gramaticas_no_cargadas.append(self.nombre)
                        self.cont_gramaticas_no_cargadas += 1


                    # Resetendo todas las variables para podera agregar una nueva gramatica
                    self.nombre = []
                    self.noTerminales = []
                    self.terminales = []
                    self.no_terminal_inicial = ""
                    self.producciones = []
                    self.estado = 0
                    self.libre_del_contexto = False

                else:
                    self.estructurar_gramatica(linea)
        Reporte_Gramaticas.generar_reporte()
    

    # Va a ir guardando las listas necesarias para guardar una gramatica
    def estructurar_gramatica(self, linea):
        if self.estado == 0:              # Estoy leyendo la primera linea de la estructura de la gramatica: LEER EL NOMBRE DE LA GRAMATICA
            self.nombre = linea.strip()
            self.estado = 1
        
        elif self.estado == 1:            # Estoy leyendo la segunda linea de la estructura de la gramatica: LEER 'NO TERMINALES', 'TERMINALES' Y 'NO TERMINAL INICIAL'
            
            lista = linea.split(";")        # Separandolos por el ';'
            # Se creara un lista con 3 posiciones
            lista[0] = self.limpiar_Cadena(lista[0])
            self.noTerminales = lista[0].split(",")
            lista[1] = self.limpiar_Cadena(lista[1])
            self.terminales = lista[1].split(",")
            self.no_terminal_inicial = lista[2].strip()
            self.estado = 2
        
        elif self.estado == 2:                               # Estoy leyendo las lineas que siguen: LEER PRODUCCIONES
            self.producciones.append(linea.strip())

            lista = linea.strip().split("->")
            # En la segunda posicion de 'lista' contendra las expresiones que se producen

            # Aqui sera de validar que la produccion sea de una gramatica libre de contexto      
            contador_terminales = 0
            contador_no_terminales = 0
            derecha_produccion = lista[1]
            
            for i in range(len(derecha_produccion)):
                caracter = derecha_produccion[i]
                if caracter != " " and caracter != "\t":
                    if caracter in self.terminales:
                        contador_terminales += 1
                    elif caracter in self.noTerminales:
                        contador_no_terminales += 1
            
            # Los siguientes 'if' solo son de las dos formas en que puede el lado derecho de una
            # produccion de una gramatica regular, por lo que simplemente no se hace nada, ya que solo se cambiara
            # cuando encuentre una estructura de una gramatica libre del contexto
            if contador_terminales == 1 and contador_no_terminales == 1:    # Significa que esta produccion no pertenece a una gramatica regular
                print("", end="")                              
            elif contador_terminales == 1 and contador_no_terminales == 0:  # Significa que esta produccion no pertenece a una gramatica regular
                print("", end="")
            elif contador_terminales == 0 and contador_no_terminales == 0:  # Significa que no se reconocio ningun terminal o no terminal definido al principio de la gramatica
                print("", end="")
            else:
                self.libre_del_contexto = True                              # Significa que es una gramatica libre del contexoto
    
    def getNombres_Gramaticas(self):
        return self.nombres_gramaticas
    
    def obtener_objeto_gramatica(self, nombre_gramatica):
        gramatica = self.lista_circular.buscar_gramatica(nombre_gramatica)
        return gramatica

    # Limpia la cadena enviada para que quede sin espacios o tabulaciones
    def limpiar_Cadena(self, cadena):
        cadenaLimpia = ""
        for i in range(len(cadena)):
            if cadena[i] != " " and cadena[i] != "\t":
                cadenaLimpia += cadena[i]
        return cadenaLimpia
    
    # Si hay gramaticas que no se cargaron, entonces de retornará la lista de los nombres de esas gramaticas, sino solo un 0
    def getGramaticas_no_cargadas(self):
        if self.cont_gramaticas_no_cargadas != 0:
            return self.gramaticas_no_cargadas
        return 0
