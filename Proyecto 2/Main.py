from time import sleep
import os
import Analizar_Archivo
import Graphviz
import Automata_de_Pila


def mostrar_Informacion():
    print("\n\n------------------------- Proyecto 2 - LFP -------------------------") # Sustituir por el nombre del programa
    print("Lenguajes Formales y de Programación,  sección B+")
    print("Gerson Sebastian Quintana Berganza, 201908686")
    print("--------------------------------------------------------------------\n\n")


def cuenta_Regresiva():
    cuenta = ""
    i = 5
    while i >= 0:
        # Si ya es la ultima vez que entra al ciclo que no imprima una ',' sino '...'
        if i == 0:                      
            cuenta += str(i)
            print(cuenta + " ", end="...")
            sleep(0.5)
        else:
            cuenta += str(i)
            # Se hace un retorno al carro para que quite lo que estaba anteriormente y ponga lo que la variable 'cuenta' lleva concatenado
            print(cuenta + "\r", end=" ")
            cuenta += ", "
        sleep(1)
        i -= 1
    print(" ¡Bienvenido!")
    sleep(1)


# Va a separar cada 'terminal' por comas
def estructurar_Lista_Terminales(lista_Terminales):
    terminales = ""
    for i in range(len(lista_terminales)):
        if i == len(lista_terminales) - 1:
            terminales += lista_terminales[i].strip()
        else:
            terminales += lista_terminales[i].strip() + ", "
    return terminales


# Va a separar cada 'no terminale' por comas
def estructurar_Lista_No_Terminales(lista_No_Terminales):
    no_terminales = ""
    for j in range(len(lista_no_terminales)):
        if j == len(lista_no_terminales) - 1:
            no_terminales += lista_no_terminales[j].strip()
        else:
            no_terminales += lista_no_terminales[j].strip() + ", "
    return no_terminales


opcion = 0      # Donde se guardara la opcion ingresada
ruta = ""    # Donde se guardara la ruta del archivo
analizar_archivo = None
grafo = None
contador = 0


while opcion != 6:
    # if contador == 0:
    #     mostrar_Informacion()
    #     cuenta_Regresiva()
    #     contador = 1

    try:
        print("\n\n\n################### Menú Principal #####################\n"
                "#      1. Cargar archivo                               #\n"
                "#      2. Mostrar información general de la gramática  #\n"
                "#      3. Generar autómata de pila equivalenete        #\n"
                "#      4. Reporte de recorrido                         #\n"
                "#      5. Reporte en tabal                             #\n"
                "#      6. Salir                                        #\n"
                "########################################################\n")

        opcion = int(input("Ingrese una opción: "))
        print()

        if (opcion < 0 or opcion > 6):                                          # En caso ingrese un numero pero no este en las opciones genero una excepción
            opción = 7/0

    except ZeroDivisionError:
        print("\n----------------------------------------------------------\n"
              "La opción ingresada no está disponible. Vuelve a intentar.\n"
              "------------------------------------------------------------\n")
        opcion = 0

    except ValueError:
        print("\n----------------------------------------------------------\n"
              "Debe ingresar el número que corresponda a la opción.\n"
              "------------------------------------------------------------\n")
        opcion = 0

    if opcion == 1:
        ruta = "entrada.txt"

        if ruta != "":

            print("> Archivo cargado con éxito...")
            analizar_archivo = Analizar_Archivo.Analizar_Archivo(ruta)              # Enviando la ruta del archivo  
            analizar_archivo.analizar_file()                                        # Analizando el archivo
            gramaticas_no_cargadas = analizar_archivo.getGramaticas_no_cargadas()

            # if gramaticas_no_cargadas != 0:
            #     opcion = input("> Algunas gramáticas no se cargaron.¿Desea ver el reporte? (s/n): ")
            #     if opcion.lower() == "s":
            #         os.system("reportes\\Reporte.html")
        
        else:
            print("\n---------------------------------------------------------------")
            print("No se ingresó ruta de archivo.")
            print("---------------------------------------------------------------\n")
    
    elif opcion == 2:

        nombres_gramaticas = analizar_archivo.getNombres_Gramaticas()           # Obteniendo la lista que tiene el nombre de todas las gramaticas que estan en el archivo de entrada
        len_nombres_gramaticas = len(nombres_gramaticas)                        # Tamaño de la lista de nombres
        expresion = ""                                                          # Guardara lo que esta al lado derecho de cada produccion

        print("\n---------- Gramáticas Cargadas -------------\n")
        for i in range(len_nombres_gramaticas):
            print("  " + str(i+1) + ". " + nombres_gramaticas[i])
        print()

        try:

            opcion_gramatica = int(input("Ingrese el número correspondiente a la gramática: "))

            if opcion_gramatica > 0 and opcion_gramatica <= len_nombres_gramaticas:

                nombre_gramatica = nombres_gramaticas[opcion_gramatica-1]                                     # Donde se guardaran las posiciones que ya fueron obtenidas
                
                gramatica = analizar_archivo.obtener_objeto_gramatica(nombre_gramatica)      # Buscando el nodo de la lista circular con el nombre de la gramatica
                producciones = gramatica.listaProducciones                              # Obteniendo todas las producciones de la gramatica que se acaba de buscar (devuelve una lista)
                nombre_gramatica = gramatica.nombre
                lista_no_terminales = gramatica.lista_NoTerminales
                lista_terminales = gramatica.listaTerminales
                no_terminal_inicial = gramatica.NoTerminalInicial
                terminales = ""
                no_terminales = ""

                terminales = estructurar_Lista_Terminales(lista_terminales)
                no_terminales = estructurar_Lista_No_Terminales(lista_no_terminales)
                
                print("\n\nNombre de la gramática = " + nombre_gramatica)
                print("No terminales = " + "{" + no_terminales + "}")
                print("Terminales = " + "{" + terminales + "}")
                print("No terminal inicial = " + no_terminal_inicial)
                print("Producciones: \n")

                posiciones = []                                                         # Donde se guardaran las posiciones que ya fueron obtenidas

                # Este for obtendra lo que esta al lado izquierdo de la produccion y lo compara con todas las partes
                # izquierdas de las producciones de todas las gramaticas para ver cuales son iguales
                for j in range(len(producciones)):
                    produccion = producciones[j]
                    lista = produccion.split("->")                                      # Separando cada produccion
                    noTerminal_referencia = lista[0].strip()

                    # Recorriendo nuevamente las producciones de la gramatica para obtener las que son iguales
                    # a al no terminal del lado izquierdo de cada produccion que se acaba de obtenern en 'caracter_referencia'
                    for k in range(len(producciones)):
                        produccion = producciones[k]
                        lista = produccion.split("->")
                        noTerminal = lista[0].strip()

                        if noTerminal == noTerminal_referencia and len(posiciones) == 0:
                            expresion += lista[1].strip()                                   # Obtenidendo el lado derecho de la produccion
                            posiciones.append(k)                                            # Guardando la posicion (para que ya no vuelva a leer esta posicion de la gramatica)

                        elif noTerminal == noTerminal_referencia:
                            # Si k se encuentra en la lista de posiciones guardadas. Es decir, ya se leyo la produccion en esa posicion
                            # que no haga nada
                            if k in posiciones:
                                print("", end="")

                            # Si no hay todavia posiciones guardadas, que guarde lo que hay al lado derecho de la produccion   
                            elif len(expresion) == 0:
                                expresion += lista[1].strip()
                                posiciones.append(k)
                                
                            # Sino, que guarde lo que esta del lado derecho de la produccion pero con una estructura definida
                            else:
                                expresion +="\n   | " + lista[1].strip()
                                posiciones.append(k)
                    
                    # Si hay algo en la variable expresion
                    if len(expresion) != 0:    
                        print(noTerminal_referencia + " -> " + expresion)
                    expresion = ""                                          # Que limpie lo que hay en la variable para la siguiente corrida
                
                input("\nPresione 'Enter' para limpiar la consola ")
                os.system("cls")
                
            else:
                print("\n--------------------------------------------------------") 
                print("Únicamente puede eligir entre las opciones disponibles.")
                print("--------------------------------------------------------") 

        except ValueError:
            print("\n--------------------------------------------------------") 
            print("Debe ingresar el número que corresponde a la gramática.")
            print("--------------------------------------------------------") 

    
    elif opcion == 3:

        nombres_gramaticas = analizar_archivo.getNombres_Gramaticas()
        len_nombres_gramaticas = len(nombres_gramaticas)
        
        for i in range(len_nombres_gramaticas):
            print(str(i+1) + ". " + nombres_gramaticas[i])
        print()

        try:
            opcion_gramatica = int(input("Ingrese el número correspondiente a la gramática: "))
            
            if opcion_gramatica > 0 and opcion_gramatica <= len_nombres_gramaticas:
                nombre_gramatica = nombres_gramaticas[opcion_gramatica-1]
                gramatica = analizar_archivo.obtener_objeto_gramatica(nombre_gramatica)
                grafo = Graphviz.Graphviz(gramatica)
                grafo.generar_funciones()
                grafo.generar_grafo(True)
            else:
                print("\n--------------------------------------------------------") 
                print("Únicamente puede eligir entre las opciones disponibles.")
                print("--------------------------------------------------------") 

        except ValueError:
            print("\n--------------------------------------------------------") 
            print("Debe ingresar el número que corresponde a la gramática.")
            print("--------------------------------------------------------") 

    
    elif opcion == 4:
        #cadena = input("Ingrese una cadena: ")
        cadena = "baaa"
        gramatica = analizar_archivo.obtener_objeto_gramatica("Gramatica14")  # Retorna el objeto 'gramatica'
        grafo = Graphviz.Graphviz(gramatica)    
        grafo.generar_funciones()
        grafo.generar_grafo(False)
        transiciones = grafo.getTransiciones()
        no_terminal_inicial = grafo.getNoTerminalInicial()
        terminales = grafo.getTerminales()
        no_terminales = grafo.getNoterminales()

        print("Transisiones: ", transiciones)
        print("No terminal inicial: ", no_terminal_inicial)
        print("Terminales: ", terminales)
        print("No terminales: ", no_terminales)

        Automata_de_Pila.analizar_Cadena(cadena, transiciones, terminales, no_terminales, no_terminal_inicial)



""" 
zazabzbz con Gramatica5
abbbaa con Gramatica7
abbbab con Gramatica12
0001000 con Gramatica11
zaazaabbzbbz con Gramatica11
abzba con Grm1
aabbcccccccc con Gramatica13
baaaba con Gramatica14 -> No aceptada
bcabacaa -> Gramatica4
""" 