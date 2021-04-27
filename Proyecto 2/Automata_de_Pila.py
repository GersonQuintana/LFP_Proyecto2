from time import sleep

cadena_i = "" # i = ingresados
transiciones_i = []
terminales_i = []
no_terminales_i = []
no_terminal_inicial_i = ""

cadena_lectura = ""
contenido_pila_bueno = []
cont = 0
n = 0
pila = []
estado = "i"
bandera = True
num = 0
estados_buenos = []
b = ""



# [['λ', 'S', 'z M N z'], ['λ', 'M', 'a M a'], ['b', 'b', 'λ'], ['z', 'z', 'λ']]
def analizar_Cadena(indice, cadena, transiciones, terminales, no_terminales, no_terminal_inicial):
    global cadena_i, transiciones_i, terminales_i, no_terminales_i, no_terminal_inicial_i, cont, n, pila, estado, contenido_pila_bueno, bandera, num, estados_buenos, b
    cadena_i = ""
    for i in range(indice, len(cadena)):
        cadena_i += cadena[i]


    print("-------------------------------------------")
    print("Se leera: " + cadena_i)
    sleep(1)
    cadena_i = cadena
    transiciones_i = transiciones
    terminales_i = terminales
    no_terminales_i = no_terminales
    no_terminal_inicial_i = no_terminal_inicial

    # Transisiones:  [['λ', 'S', 'z M N z'], ['λ', 'M', 'a M a'], ['λ', 'M', 'z'], ['λ', 'N', 'b N b'], ['λ', 'N', 'z'], ['a', 'a', 'λ'], ['b', 'b', 'λ'], ['z', 'z', 'λ']]
    # No terminal inicial:  S
    # Terminales:  ['a', 'b', 'z']
    # No terminales:  ['S', 'M', 'N']
    # La cadena ingresada es zazabzbz
    if cont == 0:
        n = 0
        pila = []
        cont = cont + 1
        bandera = True


    while n < len(cadena) and bandera == True:
        caracter = cadena_i[n]

        if estado == 'i':
            pila.insert(0, '#')
            estado = 'p'

        elif estado == 'p':
            pila.insert(0, no_terminal_inicial)
            contenido_pila_bueno = pila
            estado = 'q'

        elif estado == 'q':


            if pila[0] in no_terminales:
                contenido_pila_bueno = pila

                #print("SE AGREGO LA PILA BUENO ", contenido_pila_bueno)
                producciones, noterminal = buscar_producciones(pila[0])
                
                for i in range(len(producciones)):
                    print("Buscando " + pila[0])
                    produccion = producciones[i]
                    lista = str_a_lista(produccion)
                    pila.pop(0)
                    num = num + 1
                    print("Se inserto ", lista)
                    pila = lista + pila
                    b = analizar_Cadena(n, cadena, transiciones, terminales, no_terminales, no_terminal_inicial)
                    


                    if b == True:
                        print(b)
                        bandera = False
                        return
                    else:
                       
                        print("La pila estaba como ", pila)
                        contenido_pila_bueno.insert(0, noterminal)
                        pila = contenido_pila_bueno

                        print("La pila regreso a ", pila)
                        print()
                        # pila = contenido_pila_bueno



            elif pila[0] in terminales:

                if pila[0] == cadena_i[n]:
                    # pa = ""
                    # for h in range(indice, len(cadena)):
                    #     pa += cadena[h]
                    # estados_buenos.append(pa)
                    respaldo = pila[0]
                    n = n + 1
                    pila.pop(0)
                    print("EL ACTUAL CONTENIDO ACTUAL ES ", pila)

                    if pila[0] == "#" and n < len(cadena):
                        print()
                        print("------------------------------------")
                        print()
                        print(">>>>>>>> CANDENA NO ACEPTADA <<<<<<<<<")
                        print()
                        print("------------------------------------")
                        print()
                        bandera = False
                        return True
                    
                    if pila[0] == "#" and n == len(cadena):
                        print()
                        print("------------------------------------")
                        print()
                        print(">>>>>>>> CANDENA ACEPTADA <<<<<<<<<")
                        print()
                        print("------------------------------------")
                        print()
                        bandera = False
                        return True

                    if pila[0] == "#" and n != len(cadena):
                        pila.insert(0, respaldo)
                        n = n - 1
                        return False

                    

                else:
                    return False


                # n = n + 1
                # pila.pop(0)
                # print("EL CONTENIDO DE LA PILA ES ", pila)
                # return True



def buscar_producciones(no_terminal):
    global transiciones_i
    producciones = []
    for i in range(len(transiciones_i)):
        if transiciones_i[i][1] == no_terminal:
            producciones.append(transiciones_i[i][2])
    return producciones, no_terminal

def str_a_lista(cadena):
    # print("La cadena es ", cadena)
    cad = ""
    lista = []
    for i in range(len(cadena)):
        if cadena[i] == " " or cadena[i] == "\t":
            if cad != "":
                lista.append(cad)
                cad = ""
        else:
            cad += cadena[i]

        if i == len(cadena) - 1 and cad != "":
            lista.append(cad)
    return lista






    # estado = 0
    # len_cadena = len(cadena)
    # n = 0
    # pila = []

    # while n < len_cadena:

    #     caracter = cadena[n]

    #     if estado == "i":
    #         pila.insert(0, '#')
    #         estado = "p"

    #     elif estado == "p":
    #         pila.insert(0, no_terminal_inicial)
    #         estado = "q"

    #     elif estado == "q":

    #         if pila[0] in no_terminales:
    #             posiciones = []
    #             for i in range(len(transiciones)):
    #                 cad = transiciones[i][2]
    #                 if transiciones[i][1] == pila[0]:
    #                     posiciones.append(i)

    #             posicionesExtra = []

    #             for i in posiciones:
    #                 cad = transiciones[i][2]
    #                 if cad[0] == caracter:
    #                     posicionesExtra.append(i)

    #             if len(posiciones) == 1:    # Significa que no habian transiciones que tuvieran una produccion que iniciara con el caracter que esta leyendo
    #                 no_terminal = transiciones[0][1]
    #                 pila.pop(0)
    #                 pila.insert(no_terminal)




