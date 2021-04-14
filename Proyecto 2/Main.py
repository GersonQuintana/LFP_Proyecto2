from time import sleep
import Analizar_Archivo


print("\n\n------------------------- Proyecto 2 - LFP -------------------------") # Sustituir por el nombre del programa
print("Lenguajes Formales y de Programación,  sección B+\n"
      "Gerson Sebastian Quintana Berganza, 201908686")
print("--------------------------------------------------------------------")


# cuenta = ""
# i = 5
# while i >= 0:
#     # Si ya es la ultima vez que entra al ciclo que no imprima una ',' sino '...'
#     if i == 0:                      
#         cuenta += str(i)
#         print(cuenta + " ", end="...")
#         sleep(0.5)
#     else:
#         cuenta += str(i)
#         # Se hace un retorno al carro para que quite lo que estaba anteriormente y ponga lo que la variable 'cuenta' lleva concatenado
#         print(cuenta + "\r", end=" ")
#         cuenta += ", "
#     sleep(1)
#     i -= 1



opcion = 0      # Donde se guardara la opcion ingresada
ruta = ""    # Donde se guardara la ruta del archivo
analizar_archivo = None

# Mostrando menu principal
while opcion != 6:
    try:

        print("\n\n################### Menú Principal #####################\n"
                "#      1. Cargar archivo                               #\n"
                "#      2. Mostrar información general de la gramática  #\n"
                "#      3. Generar autómata de pila equivalenete        #\n"
                "#      4. Reporte de recorrido                         #\n"
                "#      5. Reporte en tabal                             #\n"
                "#      6. Salir                                        #\n"
                "########################################################\n")

        opcion = int(input("Ingrese una opción: "))
        print("\n")

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

    
    # OPCIONES 
    if opcion == 1:
        ruta = "entrada.txt"
    
    elif opcion == 2:
        # Enviando la ruta del archivo
        analizar_archivo = Analizar_Archivo.Analizar_Archivo(ruta)  
        # Analizando el archiv
        analizar_archivo.analizar_file()    
        # Obteniendo la lista que tiene el nombre de todas las gramaticas que estan en el archivo de entrada
        nombres_gramaticas = analizar_archivo.nombres_gramaticas
        # Tamaño de la lista de nombres
        len_nombres_gramaticas = len(nombres_gramaticas)

        posiciones = []
        expresion = ""  # Guardara lo que esta al lado derecho de cada produccion
        caracter_referencia = ""    # Guardara lo que esta al lado izquierdo de la produccion

        for i in range(len_nombres_gramaticas):
            print(str(i+1) + ". " + nombres_gramaticas[i])

        opcion_gramatica = int(input("Ingrese el número correspondiente a la gramática: "))
        nombre_gramatica = nombres_gramaticas[opcion_gramatica-1]                                     # Donde se guardaran las posiciones que ya fueron obtenidas

        print("\n---------- " + nombre_gramatica + " -------------\n")
        
        gramatica = analizar_archivo.imprimir_gramaticas(nombre_gramatica)    # Buscando el nodo de la lista circular con el nombre de la gramatica
        producciones = gramatica.listaProducciones                  # Obteniendo todas las producciones de la gramatica que se acaba de buscar (devuelve una lista)
        posiciones = []                                             # Donde se guardaran las posiciones que ya fueron obtenidas

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
                        expresion +="\n   | " + lista[1].strip()
                        posiciones.append(k)
            
            # Si hay algo en la variable expresion
            if len(expresion) != 0:    
                print(noTerminal_referencia + " -> " + expresion)
            # Que limpie lo que hay en la variable para la siguiente corrida
            expresion = ""
                    







            # for j in range(len(producciones)):
            #     produccion = producciones[j]
            #     lista = produccion.split("->")
            #     #print("&&" + lista[1])
            #     if j == 0:
            #         noTerminal = lista[0]
            #         caracter_referencia = noTerminal[0]
            #         expresion = lista[1]
            #     else:
            #         noTerminal = lista[0]
            #         caracter = noTerminal[0]
            #         if caracter == caracter_referencia:
            #             expresion +="\n   | " + str(lista[1])
            #         else:
            #             print(caracter_referencia + " -> " + expresion)
            #             caracter_referencia = caracter
            #             expresion = lista[1]

            #     if j == len(producciones)-1:
            #         print(caracter_referencia + " -> " + expresion)


            

