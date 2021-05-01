from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog as FileDialog
from time import sleep
import os
from os import path
from os import remove
import Analizar_Archivo
import Graphviz
import Automata_de_Pila


def mostrar_Informacion():
    print("\n\n------------------------- Proyecto 2 - LFP -------------------------")
    print("Lenguajes Formales y de Programación,  sección B+")
    print("Gerson Sebastian Quintana Berganza, 201908686")
    print("--------------------------------------------------------------------\n\n")


def cuenta_Regresiva():
    cuenta = ""
    i = 5
    while i >= 0:
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
def estructurar_Lista_Terminales(lista_terminales):
    terminales = ""
    for i in range(len(lista_terminales)):
        if i == len(lista_terminales) - 1:
            terminales += lista_terminales[i].strip()
        else:
            terminales += lista_terminales[i].strip() + ", "
    return terminales


# Va a separar cada 'no terminale' por comas
def estructurar_Lista_No_Terminales(lista_no_terminales):
    no_terminales = ""
    for j in range(len(lista_no_terminales)):
        if j == len(lista_no_terminales) - 1:
            no_terminales += lista_no_terminales[j].strip()
        else:
            no_terminales += lista_no_terminales[j].strip() + ", "
    return no_terminales



def mostrar_informacion_gramaticas():

    global analizar_archivo

    # Obteniendo la lista que tiene el nombre de todas las gramaticas que estan en el archivo de entrada
    nombres_gramaticas = analizar_archivo.getNombres_Gramaticas()
    # Tamaño de la lista de nombres
    len_nombres_gramaticas = len(nombres_gramaticas)
    # Guardara lo que esta al lado derecho de cada produccion
    expresion = ""

    print("\n---------- Gramáticas Cargadas -------------\n")
    for i in range(len_nombres_gramaticas):
        print("  " + str(i+1) + ". " + nombres_gramaticas[i])
    print()

    try:

        opcion_gramatica = int(input("Ingrese el número correspondiente a la gramática: "))

        if opcion_gramatica > 0 and opcion_gramatica <= len_nombres_gramaticas:

            # Donde se guardaran las posiciones que ya fueron obtenidas
            nombre_gramatica = nombres_gramaticas[opcion_gramatica-1]

            # Buscando el nodo de la lista circular con el nombre de la gramatica
            gramatica = analizar_archivo.obtener_objeto_gramatica(nombre_gramatica)

            # Obteniendo todas las producciones de la gramatica que se acaba de buscar (devuelve una lista)
            producciones = gramatica.listaProducciones
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

            # Donde se guardaran las posiciones que ya fueron obtenidas
            posiciones = []

            # Este for obtendra lo que esta al lado izquierdo de la produccion y lo compara con todas las partes
            # izquierdas de las producciones de todas las gramaticas para ver cuales son iguales
            for j in range(len(producciones)):

                produccion = producciones[j]
                # Separando cada produccion
                lista = produccion.split("->")
                noTerminal_referencia = lista[0].strip()

                # Recorriendo nuevamente las producciones de la gramatica para obtener las que son iguales
                # a al no terminal del lado izquierdo de cada produccion que se acaba de obtenern en 'caracter_referencia'
                for k in range(len(producciones)):
                    produccion = producciones[k]
                    lista = produccion.split("->")
                    noTerminal = lista[0].strip()

                    if noTerminal == noTerminal_referencia and len(posiciones) == 0:
                        # Obtenidendo el lado derecho de la produccion
                        expresion += lista[1].strip()
                        # Guardando la posicion (para que ya no vuelva a leer esta posicion de la gramatica)
                        posiciones.append(k)

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
                            expresion += "\n   | " + lista[1].strip()
                            posiciones.append(k)

                # Si hay algo en la variable expresion
                if len(expresion) != 0:
                    print(noTerminal_referencia + " -> " + expresion)
                # Que limpie lo que hay en la variable para la siguiente corrida
                expresion = ""

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




opcion = 0      # Donde se guardara la opcion ingresada
ruta = ""    # Donde se guardara la ruta del archivo
analizar_archivo = None
grafo = None
contador = 0
automatas_de_pila = []


while opcion != 6:
    if contador == 0:
        mostrar_Informacion()
        cuenta_Regresiva()
        contador = 1

    try:
        print("\n\n\n################### Menú Principal #####################\n"
              "#      1. Cargar archivo                               #\n"
              "#      2. Mostrar información general de la gramática  #\n"
              "#      3. Generar autómata de pila equivalente         #\n"
              "#      4. Reporte de recorrido                         #\n"
              "#      5. Reporte en tabla                             #\n"
              "#      6. Salir                                        #\n"
              "########################################################\n")

        opcion = int(input("Ingrese una opción: "))
        print()

        # En caso ingrese un numero pero no este en las opciones genero una excepción
        if (opcion < 0 or opcion > 6):
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
        root = Tk()
        print("> Cargando archivo de menú...")
        ruta = FileDialog.askopenfilename(title="Abrir fichero", filetypes=(("txt files","*.glc"),("todos los archivos","*.*")))
        root.destroy()

        if ruta != "":

            print("> Archivo cargado con éxito...")
            analizar_archivo = Analizar_Archivo.Analizar_Archivo(ruta)              # Enviando la ruta del archivo
            # Analizando el archivo
            analizar_archivo.analizar_file()
            gramaticas_no_cargadas = analizar_archivo.getGramaticas_no_cargadas()

            if gramaticas_no_cargadas != 0:
                opcion = input("> Algunas gramáticas no se cargaron.¿Desea ver el reporte? (s/n): ")
                if opcion.lower() == "s":
                    os.system("reportes\\Reporte_Gramaticas.html")

        else:
            print("\n---------------------------------------------------------------")
            print("No se ingresó ruta de archivo.")
            print("---------------------------------------------------------------\n")

    elif opcion == 2:
        mostrar_informacion_gramaticas()
        
    elif opcion == 3:

        nombres_gramaticas = analizar_archivo.getNombres_Gramaticas()
        len_nombres_gramaticas = len(nombres_gramaticas)

        for i in range(len_nombres_gramaticas):
            print(str(i+1) + ". " + nombres_gramaticas[i])
        print()

        try:
            opcion_gramatica = int(
                input("Ingrese el número correspondiente a la gramática: "))

            if opcion_gramatica > 0 and opcion_gramatica <= len_nombres_gramaticas:
                nombre_gramatica = nombres_gramaticas[opcion_gramatica-1]
                automatas_de_pila.append(nombre_gramatica)
                gramatica = analizar_archivo.obtener_objeto_gramatica(
                    nombre_gramatica)
                grafo = Graphviz.Graphviz(gramatica)
                grafo.generar_funciones()
                grafo.generar_grafo(True)

                print("\n--------------------------------------------------------")
                print("> Autómata de pila equivalente generado con éxito.")
                print("--------------------------------------------------------")

            else:
                print("\n--------------------------------------------------------")
                print("Únicamente puede eligir entre las opciones disponibles.")
                print("--------------------------------------------------------")

        except ValueError:
            print("\n--------------------------------------------------------")
            print("Debe ingresar el número que corresponde a la gramática.")
            print("--------------------------------------------------------")

    elif opcion == 4:

        len_automatas_de_pila = len(automatas_de_pila)
        expresion = ""

        print("\n---------- Gramáticas Cargadas -------------\n")
        for i in range(len_automatas_de_pila):
            print("  " + str(i+1) + ". AP_" + automatas_de_pila[i])
        print()

        try:
            if len(automatas_de_pila) != 0:
                opcion_automata = int(input("Ingrese el número correspondiente a la gramática: "))
                cadena = input("Ingrese una cadena: ")

                if opcion_gramatica > 0 and opcion_automata <= len_automatas_de_pila:

                    # Donde se guardaran las posiciones que ya fueron obtenidas
                    nombre_gramatica = automatas_de_pila[opcion_automata-1]
                    gramatica = analizar_archivo.obtener_objeto_gramatica(nombre_gramatica)
                    grafo = Graphviz.Graphviz(gramatica)
                    grafo.generar_funciones()
                    grafo.generar_grafo(False)
                    transiciones = grafo.getTransiciones()
                    no_terminal_inicial = grafo.getNoTerminalInicial()
                    terminales = grafo.getTerminales()
                    no_terminales = grafo.getNoterminales()


                    recorrido, razon = Automata_de_Pila.analizar_Cadena(grafo, cadena, transiciones, terminales, no_terminales, no_terminal_inicial)

                    if recorrido == True:   # La cadena fue valida
                        file = open("reportes/Recorrido_Cadena.html","a", encoding="UTF-8")
                        file.write("\n\t<div class=\"estado\">¡La cadena ingresada es válida!</div>\n\t</body>\n</html>\n")
                    else:   # La cadena no fue valida
                        file = open("reportes/Recorrido_Cadena.html","a", encoding="UTF-8")
                        file.write("\n\t<div class=\"estado\">CADENA NO VÁLIDA.\n" + razon + "</div>\n\t</body>\n</html>\n")
                    file.close()
                    os.system("reportes\\Recorrido_Cadena.html")

                else:
                    print("\n--------------------------------------------------------")
                    print("Únicamente puede eligir entre las opciones disponibles.")
                    print("--------------------------------------------------------")
            else:
                print("\n--------------------------------------------------------")
                print("Debe generar antes un autómata de pila equivalente.")
                print("--------------------------------------------------------")

        except ValueError:
            print("\n--------------------------------------------------------")
            print("Debe ingresar el número que corresponde a la gramática.")
            print("--------------------------------------------------------")

        

    elif opcion == 5:
        
        # Tamaño de la lista de nombres
        len_automatas_de_pila = len(automatas_de_pila)
        # Guardara lo que esta al lado derecho de cada produccion
        expresion = ""

        print("\n---------- Gramáticas Cargadas -------------\n")
        for i in range(len_automatas_de_pila):
            print("  " + str(i+1) + ". " + automatas_de_pila[i])
        print()

        try:
            if len(automatas_de_pila) != 0:
                opcion_automata = int(input("Ingrese el número correspondiente al autómata: "))
                cadena = input("Ingrese una cadena: ")

                if opcion_gramatica > 0 and opcion_automata <= len_automatas_de_pila:

                    # Donde se guardaran las posiciones que ya fueron obtenidas
                    nombre_gramatica = automatas_de_pila[opcion_automata-1]
                    gramatica = analizar_archivo.obtener_objeto_gramatica(nombre_gramatica)  # Retorna el objeto 'gramatica'
                    grafo = Graphviz.Graphviz(gramatica)
                    grafo.generar_funciones()
                    grafo.generar_grafo(False)
                    transiciones = grafo.getTransiciones()
                    no_terminal_inicial = grafo.getNoTerminalInicial()
                    terminales = grafo.getTerminales()
                    no_terminales = grafo.getNoterminales()

                    recorrido, razon = Automata_de_Pila.analizar_Cadena_con_tabla(grafo, cadena, transiciones, terminales, no_terminales, no_terminal_inicial)

                    if recorrido == True:
                        file = open("reportes/Reporte_Tabla.html", "a", encoding="UTF-8")
                        fin_HTML = """</tbody>\n</thead>\n</table>\n</div>\n\t<div class=\"estado\">¡La cadena ingresada es válida!</div>\n\t"""
                        file.write(fin_HTML)
                    else:
                        file = open("reportes/Reporte_Tabla.html", "a", encoding="UTF-8")
                        fin_HTML = "</tbody>\n</thead>\n</table>\n</div>\n\t<div class=\"estado\">CADENA NO VÁLIDA.\n" + razon + "</div>\n\t"
                        file.write(fin_HTML)
                    file.close()

                    os.system("reportes\\Reporte_Tabla.html")

                else:
                    print("\n--------------------------------------------------------")
                    print("Únicamente puede eligir entre las opciones disponibles.")
                    print("--------------------------------------------------------")
            else:
                print("\n--------------------------------------------------------")
                print("Debe generar antes un autómata de pila equivalente.")
                print("--------------------------------------------------------")

        except ValueError:
            print("\n--------------------------------------------------------")
            print("Debe ingresar el número que corresponde a la gramática.")
            print("--------------------------------------------------------")


""" 
zazabzbz con Gramatica5
abbbaa con Gramatica7
abbbab con Gramatica12
0001000 con Gramatica11
zaazaabbzbbz con Gramatica9
abzba con Grm1
aabbcccccccc con Gramatica13
baaa con Gramatica14
bcabacaa -> Gramatica4
caaebeaebedgggddbh -> Gramatica17
aaaba -> Gramatica18
"""
