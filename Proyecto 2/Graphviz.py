from graphviz import Digraph
from graphviz import render
from reportes import Automata_Equivalente as AE
from reportes import Recorrido_Cadena

class Graphviz:

    # Recibe el objeto gramatica
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.listaTerminales = gramatica.listaTerminales
        self.listaNoTerminales = gramatica.lista_NoTerminales
        self.transisiones = []
        self.transisiones_automata = []
        self.pila_original = []
        self.count = 0


    # GENERA LAS TRANSICIONES QUE ESTARAN EN LAS ARISTAS DE CADA ESTADO
    def generar_funciones(self):    
        producciones = self.gramatica.listaProducciones
        lista_terminales = self.gramatica.listaTerminales
        lista_no_terminales = self.gramatica.lista_NoTerminales
        
        posiciones = []                                                         # Donde se guardaran las posiciones que ya fueron obtenidas

        for i in range(len(producciones)):
            produccion = producciones[i]
            lista = produccion.split("->")
            izquierda_produccion = lista[0].strip()
            derecha_produccion = lista[1].strip()

            cadena = ""
            estado = 0
            pos = 0
            
            lista = ["q,λ," + izquierda_produccion, "q," + derecha_produccion]
            self.transisiones.append(lista)
        
        for j in range(len(lista_terminales)):
            terminal = lista_terminales[j]
            lista = ["q," + terminal + "," + terminal, "q,λ"]
            self.transisiones.append(lista)
            
        print(self.transisiones)


    # GENERARA UN GRAFO EN UN HTML
    def generar_grafo(self, imprimir):

        nombre_grafo = "AP_" + self.gramatica.nombre + ".dot"
        f = Digraph('grafo', filename=nombre_grafo, node_attr={'height': '1.1', 'fontsize':"18"}, format='png')
        #s.attr(bgcolor='white', fontcolor='white')
        f.attr(rankdir="LR", diredgeconstraints="True")

        no_terminal_inicial = self.gramatica.NoTerminalInicial

        f.attr('node', shape="none", fontcolor='black')
        f.node('')
        f.attr('node', shape='circle')
        f.node('i', fontsize='30')
        f.node('p', fontsize='30')
        f.attr('node', shape='doublecircle')
        f.node('f', fontsize='30')
        f.attr('node', shape='circle')
        #f.edge("estado actual", "estado al que va", label="caracter en lectura, pop pila; push pila")
        f.edge('', 'i', label="")
        f.edge('i', 'p', label='λ , λ; #')
        f.edge('p', 'q', label='λ , λ; '+ "S")

        etiqueta_NT = ""
        etiqueta_T = ""

        for i in range(len(self.transisiones)):

            transicion = self.transisiones[i]
            info_estado_actual = transicion[0].split(",")
            info_estado_siguiente = transicion[1].split(",")
            caracter_lectura = info_estado_actual[1].strip()
            pop_pila = info_estado_actual[2].strip()
            push_pila = info_estado_siguiente[1].strip()

            if caracter_lectura in self.listaTerminales and pop_pila in self.listaTerminales:   # Para ponerlo arriba del estado 
                etiqueta_T += caracter_lectura + ", " + pop_pila + "; " + push_pila + "\n"
                #print("terminal " + caracter_lectura)
            else:                                                                               # Para ponerlo abajo del estado
                etiqueta_NT += caracter_lectura + ", " + pop_pila + "; " + push_pila + "\n" # Etiqueta para los no terminales
                #print("No terminal " + caracter_lectura)
                
            lista = [caracter_lectura, pop_pila, push_pila]
            self.transisiones_automata.append(lista)
            print(caracter_lectura + ", " + pop_pila + "; " + push_pila)
        
        print()
        #print("Los no terminales son ", etiqueta_NT)
        f.edge('q', 'q', label=etiqueta_NT)
        #print("Terminales son ", etiqueta_T)
        f.edge('q', 'q:s', label=etiqueta_T)
        f.edge('q', 'f', label='λ , #; λ')
        ruta = "../img/" + nombre_grafo
        ruta_imagen = f.render(ruta)

        # nombre, alfabeto_pila, lista_terminales, lista_no_Terminales, estado_inicial, ruta_imagen

        terminales = self.convertir_a_str(self.listaTerminales, 0)
        no_terminales = self.convertir_a_str(self.listaNoTerminales, 0)
        alfabeto_pila = terminales + no_terminales + "#"

        terminales = self.convertir_a_str(self.listaTerminales, 1)

        if imprimir == True:
            AE.generar_reporte(self.gramatica.nombre, alfabeto_pila, terminales, ruta_imagen)  

    
    def realizarRecorrido(self, estado, entrada, pila, transicionn):

        nombre_grafo = "AP_" + self.gramatica.nombre + str(self.count) + ".dot"
        self.count += 1
        f = Digraph('grafo', filename=nombre_grafo, node_attr={'height': '1.1', 'fontsize':"18"}, format='png')
        #s.attr(bgcolor='white', fontcolor='white')
        f.attr(rankdir="LR", diredgeconstraints="True")

        no_terminal_inicial = self.gramatica.NoTerminalInicial

        f.attr('node', shape="none", fontcolor='black')
        f.node('')

        if estado == "i":
            print("EL ESTADO QUE ESTA ES i")
            f.attr('node', shape='circle', fillcolor='green1', style='filled')
            f.node('i', fontsize='30')
            f.attr('node', shape='circle', fillcolor='white', style='filled')
            f.node('p', fontsize='30')
            f.node('q', fontsize='30')
            f.attr('node', shape='doublecircle', fillcolor="white", style='filled')
            f.node('f', fontsize='30')
            f.edge('', 'i', label="")
            f.edge('i', 'p', label='>>> λ , λ; # <<<')
            f.edge('p', 'q', label='λ , λ; '+ no_terminal_inicial)
            f.edge('q', 'f', label='λ , #; λ')
        
        elif estado == "p":
            print("EL ESTADO QUE ESTA ES p")
            f.attr('node', shape='circle', fillcolor='white', style='filled')
            f.node('i', fontsize='30')
            f.attr('node', fillcolor="green1", style='filled')
            f.node('p', fontsize='30')
            f.attr('node', shape='circle', fillcolor='white', style='filled')
            f.node('q', fontsize='30')
            f.attr('node', shape='doublecircle')
            f.node('f', fontsize='30')
            f.edge('', 'i', label="")
            f.edge('i', 'p', label='λ , λ; #')
            f.edge('p', 'q', label='>>> λ , λ; '+ no_terminal_inicial + " <<<")
            f.edge('q', 'f', label='λ , #; λ')
        
        elif estado == "q":
            f.attr('node', shape='circle', fillcolor='white', style='filled')
            f.node('i', fontsize='30')
            f.node('p', fontsize='30')
            f.attr('node', shape='circle', fillcolor='green1', style='filled')
            f.node('q', fontsize='30')
            f.attr('node', shape='doublecircle', fillcolor='white', style='filled')
            f.node('f', fontsize='30')
            f.edge('', 'i', label="")
            f.edge('i', 'p', label='λ , λ; #')
            f.edge('p', 'q', label='λ , λ; '+ no_terminal_inicial)
            f.edge('q', 'f', label='λ , #; λ')
        
        elif estado == "f":
            f.attr('node', shape='circle', fillcolor='white', style='filled')
            f.node('i', fontsize='30')
            f.node('p', fontsize='30')
            f.attr('node', shape='circle', fillcolor='white', style='filled')
            f.node('q', fontsize='30')
            f.attr('node', shape='doublecircle', fillcolor='green1', style='filled')
            f.node('f', fontsize='30')
            f.edge('', 'i', label="")
            f.edge('i', 'p', label='λ , λ; #')
            f.edge('p', 'q', label='λ , λ; '+ no_terminal_inicial)
            f.edge('q', 'f', label=transicionn)

        #f.edge("estado actual", "estado al que va", label="caracter en lectura, pop pila; push pila")
        
        etiqueta_NT = ""
        etiqueta_T = ""
        etiqueta = ""

        for i in range(len(self.transisiones)):

            transicion = self.transisiones[i]
            info_estado_actual = transicion[0].split(",")
            info_estado_siguiente = transicion[1].split(",")
            caracter_lectura = info_estado_actual[1].strip()
            pop_pila = info_estado_actual[2].strip()
            push_pila = info_estado_siguiente[1].strip()

            agregado = False
            es_terminal = False

            if caracter_lectura in self.listaTerminales and pop_pila in self.listaTerminales:   # Para ponerlo arriba del estado 
                etiqueta = caracter_lectura + ", " + pop_pila + "; " + push_pila
                #print("La etiqueta formada fue (" + etiqueta + ") == " + "(",transicionn,")")
                if etiqueta == transicionn.strip():
                    etiqueta_T += " >>> " + caracter_lectura + ", " + pop_pila + "; " + push_pila + " <<< " + "\n"
                    agregado = True
                else:
                    etiqueta_T += caracter_lectura + ", " + pop_pila + "; " + push_pila + "\n"
                es_terminal = True
                #print("terminal " + caracter_lectura)
            
            if agregado == False and es_terminal == False:                                                                               # Para ponerlo abajo del estado
                etiqueta = caracter_lectura + ", " + pop_pila + "; " + push_pila # Etiqueta para los no terminales
                if etiqueta == transicionn.strip():
                    #print("SE GENERO UN NUEVA ETIQUETA")
                    etiqueta_NT += " >>> " + caracter_lectura + ", " + pop_pila + "; " + push_pila + " <<< " + "\n"
                else:
                    etiqueta_NT += caracter_lectura + ", " + pop_pila + "; " + push_pila + "\n"
                #print("No terminal " + caracter_lectura)
                
            lista = [caracter_lectura, pop_pila, push_pila]
            print(caracter_lectura + ", " + pop_pila + "; " + push_pila)
        
        print()
        #print("Los no terminales son ", etiqueta_NT)
        f.edge('q', 'q', label=etiqueta_NT)
        f.edge('q', 'q:s', label=etiqueta_T)        

        # nombre, alfabeto_pila, lista_terminales, lista_no_Terminales, estado_inicial, ruta_imagen

        terminales = self.convertir_a_str(self.listaTerminales, 0)
        no_terminales = self.convertir_a_str(self.listaNoTerminales, 0)
        alfabeto_pila = terminales + no_terminales + "#"

        terminales = self.convertir_a_str(self.listaTerminales, 1)

        ruta = "img/" + nombre_grafo
        ruta_imagen = f.render(ruta)
        Recorrido_Cadena.realizar_iteracion(ruta_imagen, pila, entrada)

        # if imprimir == True:
        #     AE.generar_reporte("Recorrido", alfabeto_pila, terminales, ruta_imagen)  


    
    def getTransiciones(self):
        return self.transisiones_automata
    
    def getNoTerminalInicial(self):
        return self.gramatica.NoTerminalInicial

    def getTerminales(self):
        return self.listaTerminales
    
    def getNoterminales(self):
        return self.listaNoTerminales
    
                        
    # Convierte una lista a una cadena con ','. Si recibe opcion = 0, se le concatena una ',' al final de la cadena
    # si recibe opcion = 1, no se le concatena una ',' al final de la cadena
    def convertir_a_str(self, lista, opcion):
        cadena = ""
        for i in range(len(lista)):
            if i == len(lista) - 1 and opcion == 1:
                cadena += lista[i]
            else:
                cadena += lista[i] + ", "
        return cadena


                                
                


















                # if pila[0] in self.listaNoTerminales:
                #     posiciones = []
                #     cad = ""
                #     for i in range(len(transiciones)):
                #         cad = transiciones[i][2]

                #         if transiciones[i][1] == pila[0] and cad[0] == caracter:
                #             posiciones.append(i)

                #     cade = ""

                #     for j in range(len(posiciones)):
                #         for k in range(pos, len_cadena):
                #             cade += cadena[k]
                #         pila.pop(0)
                        
                #         cadena1 = transiciones[j][2]
                #         cadena2 = ""
                        
                #         print("La cadena1 es " + cade)
                #         for l in range(len(cadena1)):
                #             if cadena1[l + 1] == " " or cadena1[l +1] == None or cadena1[l + 1] == "\t" and l != 0:
                #                 print("La cadena2 es (" + cadena2 + ")")
                #                 pila.insert(0, cadena2)
                #                 cadena2 = ""
                #             else:
                #                 cadena2 += cadena1[l]
                        
                #         op = self.automata_de_pila(cadena=cade, state="q", pos=pos, Pila=pila)
                #         if op == True:
                #             return
                #         pila = self.pila_original
                
                # elif pila[0] in self.listaTerminales:
                #     pos = pos + 1










                    



    