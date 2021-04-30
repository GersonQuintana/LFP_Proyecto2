import Graphviz
import reportes.Reporte_en_Tabla as RT

""" 
Las cadenas que no acepta el siguiente automata de pila son aquellas en donde un no terminal aparece como primer elemento de la expresion en el lado derecho de la produccion 
para un solo no terminal; es decir, solo reconoce gramaticas en donde sus producciones sean de la forma: 
S -> a B
S -> a C

y no cadenas en donde sus producciones sean de la forma:
S -> a B
S -> a C
S -> a

Tampoco reconoce gramaticas de la forma:
S -> A
S -> B
A -> C a
B -> C b
"""

from time import sleep

transiciones_i = []
no_terminales_ing = []
objeto_grafo = None



# Transiciones de la forma: [['λ', 'S', 'z M N z'], ['λ', 'M', 'a M a'], ['b', 'b', 'λ'], ['z', 'z', 'λ']]
def analizar_Cadena(obj_grafo, cadena, transiciones, terminales, no_terminales, no_terminal_inicial):

    global transiciones_i
    global no_terminales_ing
    global objeto_grafo
    print()
    print(transiciones)
    print()
    print("Se recibio la gramatica con exito ", obj_grafo.gramatica.nombre)


    transiciones_i = transiciones
    no_terminales_ing = no_terminales
    objeto_grafo = obj_grafo

    estado = "i"
    n = 0
    pila = []
    respaldo = ""
    transicion = ""
    

    while n < len(cadena):

        char = cadena[n]
        print("--------------------------------------")
        print()
        print("El contenido de la pila es: ", pila)

        print("Lo que se esta leyendo de la cadena es: ")
        cadena_i = ""

        for i in range(n, len(cadena)):
            cadena_i += cadena[i]
        print(cadena_i)
        sleep(0.5)

        if estado == "i":
            transicion = "(i, λ, λ; p)"
            objeto_grafo.realizarRecorrido("i", " ", " ", transicion, 0)
            pila.insert(0, "#")
            estado = "p"

        elif estado == "p":
            transicion = "λ, λ; S"
            objeto_grafo.realizarRecorrido("p", " ", " ", transicion, 1)
            pila.insert(0, no_terminal_inicial)
            estado = "q"

        elif estado == "q":
            
            # Si lo que esta en cima de la pila es un no terminal
            if pila[0] in no_terminales:

                producciones = buscar_producciones(pila[0])  # Obteniendo todas las producciones de el no terminal que se encuentra en la cima de la pila
                pos_x = []   # Guardara las posiciones de las producciones en donde expresiones del lado derecho de la produccion empiezan con el con el caracter que estoy leyendo de la cadena
                pos_y = []   # Guardara las posiciones de las producciones en donde el lado derecho de la produccion unicamente tienen un no terminal
                epsilon = 0  # Si cambia de valor, significa que hay una produccion para ese no terminal con cadena vacia


                # Recorriendo la lista de todas las producciones encontradas del no terminal que esta en la cima
                for i in range(len(producciones)):

                    produccion = producciones[i]    # Obtendiendo la produccion que esta en esa posicion
                    lista_expresion = str_a_lista(produccion)   # Conviertiendo la expresion al lado derecho de la produccion a lista

                    # Si la expresion al lado derecho de la expresion comienza con el caracter que se esta leyendo
                    if lista_expresion[0] == char:  # Si el lado derecho de la expresion comienza con el caracter que se esta leyendo, que agrege las posiciones
                        pos_x.append(i)

                    # Si la expresion al lado derecho de la expresion comienza con un no terminal
                    if lista_expresion[0] in no_terminales: # Si el lado derecho de la expresion comienza con un no terminal
                        pos_y.append(i)
                    
                    # Si la expresion al lado derecho de la expresion es una cadena vacia
                    if lista_expresion[0] == "λ":
                        epsilon = epsilon + 1
                

                # Significa que si hay expresiones del lado derecho de la produccion que si empiezan con el caracter que estoy leyendo de la cadena
                if len(pos_x) != 0:
                    
                    # CASO 1: La pila esta vacia (tiene #) pero son se ha llegado al final de la cadena
                    if pila[1] == "#" and n + 1 != len(cadena):    # Si se cumple deberia de reemplazar por la expresion mas 'grande' o con el que tenga un no terminal despues del terminal de su izquierda
                        count = 0
                        
                        # Recorriendo todas las posiciones guardadas en la lista 'pos_x'
                        for posicion in pos_x:  # Recorriendo todas las posiciones en que hay producciones que empiezan con el caracter que se esta leyendo
                            
                            # Convieriendo a lista la expresion que esta en la esa posicion
                            produccion = producciones[posicion]
                            lista_expresion = str_a_lista(produccion)

                            # Va a acceder solo cuando hayan dos o mas terminales o no terminales en la expresion del lado derecho (si es asi, se asume que en la posicion 1 hay no terminal)
                            # Esto porque hay que elegir la expresion que sea más 'grande' o que contenga por lo menos un no terminal, para seguir generando producciones
                            if len(lista_expresion) != 1:

                                #if lista_expresion[1] in no_terminales: 
                                transicion = "λ, " + pila[0] + "; " + produccion
                                objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                            
                                
                            
                            # if count == len(pos_x):
                            #     print("1. La cadena no es aceptada")
                            # count = count + 1

                    
                    # CASO 2: La pila esta vacia (tiene en la posicion 0 a 'S' y en la 1 a '#') y estoy en el ultimo caracter de la cadena
                    elif pila[1] == "#" and n + 1 >= len(cadena):

                        # Recorriendo todas las posiciones guardadas en la lista 'pos_x'
                        for posicion in pos_x:

                            # Convieriendo a lista la expresion que esta en la esa posicion
                            produccion = producciones[posicion] # Obteniendo la expresion del lado derecho de la produccion
                            lista_expresion = str_a_lista(produccion)
                            
                            
                            # Debido a que solo falta leer un caracter, lo debo reemplazar por la expresion que tenga longitud 1, es decir, ya que solo se encontraron
                            # las expresiones que iniciaban con el caracter que estoy leyendo, entonces en este caso la lista solo va a tener el caracter que se esta leyendo
                            if len(lista_expresion) == 1:   # Solo tiene un elemeto de la lista
                                transicion = "λ, " + pila[0] + "; " + produccion
                                objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break

                    
                    # Si el elemento posterior a la cima de pila no es un '#' y no estoy leyendo el ultimo caracter de la cadena
                    elif pila[1] != "#" and n + 1 != len(cadena):

                        contador = 0

                        # Recorriendo todas las posiciones guardadas en la lista 'pos_x'
                        for posicion in pos_x:  # Recorriendo todas las posiciones de las producciones que tiene al inicio de la produccion el caracter que estoy leyendo (Ej. A -> z B ó C -> z C)

                            contador = contador + 1

                            # Convieriendo a lista la expresion que esta en la esa posicion
                            produccion = producciones[posicion]
                            lista_expresion = str_a_lista(produccion)

                            # Los siguientes casos se aplican cuando se encuentran dos o mas producciones que inician con el caracter que estoy leyendo
                            if len(pila) - 1 == len(cadena) - n:    # Si en la pila tengo la misma cantidad de elementos (sin contar el '#') que el tamaño del resto de la cadena que estoy leyendo. Ej. pila = {#,a,B}; cadena que falta leer = {a, b}

                                # Cuando se presenta este caso, solamente se reemplaza el no terminal con la produccion que tenga como expresion solo cadena que estoy leyendo, es decir, cuando la lista de longitud 1
                                # Ya que ya esta implicito que sea el caracte que se esta leyendo
                                if len(lista_expresion) == 1:   # Si la lista de expresiones unicamento tienen el elemento que estoy leyendo, lo debo de insertar
                                    transicion = "λ, " + pila[0] + "; " + produccion
                                    objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                    pila.pop(0)
                                    pila = lista_expresion + pila
                                    break
                            
                            # Si lo que lo que la cima tiene justo abajo es igual al siguiente caracter de la cadena, 
                            # entonces cuando encuentre la produccion que tenga como inicial de la expresion el caracter que se esta leyendo y como siguinete de la pila y cadena un mismo caracter,
                            # entonces se puede remplazar el no terminal con el la produccion que genera la expresion que solo tiene el caracter que se esta leyendo
                            elif pila[1] == cadena[n+1]:

                                bandera = False # Si toma el valor de True, significa que dentro de la pila si hay un no terminal, sino, no hay no no terminal
                                for i in range(1, len(pila)):   # Buscando si hay no terminal dentro de la pila
                                    if pila[i] in no_terminales:
                                        bandera = True
                                        break
                                    
                                # Si en el lado derecho de la produccion solo esta el caracter que estoy buscando y ademas dentro de la pila hay un no terminal,
                                # eso me da la confianza de poder reemplazarlo por un terminal para asegurarme de que la cadena se siga leyendo, ya que ese no terminal generara mas producciones
                                if len(lista_expresion) == 1 and bandera == True:
                                    transicion = "λ, " + pila[0] + "; " + produccion
                                    objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                    pila.pop(0)
                                    pila = lista_expresion + pila
                                    break
                                
                                # Si en el lado derecho de la produccion es de longitud 2 o mas y no hay ningun terminal dentro de la lista, 
                                # Entonces hay que insertar esa produccion a la pila (suponiendo que esa produccion tiene por lo menos un simbolo no terminal y asi poder seguir generando producciones)
                                elif len(lista_expresion) >= 2 and bandera == False:
                                    transicion = "λ, " + pila[0] + "; " + produccion
                                    objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                    pila.pop(0)
                                    pila = lista_expresion + pila
                                    break
                            
                            elif len(lista_expresion) > 1:  # Sino se cumple lo anterior, entonces si lo que produce el no terminal es de longitud mayor a 1 (esta el caracter que estoy leyendo mas otro terminal o no terminal)
                                transicion = "λ, " + pila[0] + "; " + produccion
                                objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                            
                            # Si no se cumple lo anterior, y solo esta el caracter que se esta leyendo, solo lo inserto. En este caso solo se guarda por si ya terminó el ciclo y no se encontro
                            # una produccion que tuviera dos o mas terminales o no terminales
                            elif len(lista_expresion) == 1: 
                        
                                respaldo = lista_expresion[0]
                            
                            # Si ya se termino de recorrer la lista de posiciones que tienen las expresiones que comienzan con el caracter que estoy leyendo y no entro a ninguno de los anteriores, 
                            # entonces que inserte a la lista la produccion que solo tenia como expresion el caracter que esoy leyendo (ej. A --> z)
                            if contador == len(pos_x):
                                transicion = "λ, " + pila[0] + "; " + produccion
                                objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                                
                            # El siguiente caso aplica solo cuando se encuentra una produccion que inicia con el caracter que estoy leyendo. Se debe de insertar si o si, ya que no hay mas opciones
                            if len(producciones) == 1 and len(lista_expresion) == 1:   # Solo tiene un elemeto de la lista
                                transicion = "λ, " + pila[0] + "; " + produccion
                                objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                    

                # Si se encontraron producciones que tiene como inicio y no terminal
                elif len(pos_y) != 0:   # Si entra aqui significa que no hay expresiones del lado derecho de las producciones que empiecen con el caracter que estoy leyendo

                    # Si el no terminal solo tiene una expresion del lado derecho que empieza con un no terminal (Ej. S -> A)
                    if len(pos_y) == 1:
                        # transicion = "λ, " + pila[0] + "; " + produccion
                        # objeto_grafo.realizarRecorrido("q", char, pila, transicion)
                        derecha_produccion = producciones[pos_y[0]] # Obteniendo el lado derecho de la produccion
                        no_terminal = derecha_produccion[0] # Obtendiedo el primer caracter que sea terminal/no terminal 
                        transicion = "λ, " + pila[0] + "; " + derecha_produccion
                        objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                        pila.pop(0)
                        lista_expresion = str_a_lista(derecha_produccion)
                        pila = lista_expresion + pila
                    
                    # Si hay mas de una, entoces que busque cual de todos los no terminales del lado derecho producen una expresion que inicie con el caracter que se esta leyendo
                    else:

                        lista_expresion = []

                        for posicion in pos_y:
                            
                            print("Se busca acceder a la posicion "+ str(posicion) + " en ", producciones)

                            derecha_produccion = producciones[posicion] # Obteniendo el lado derecho de la produccion
                            no_terminal = derecha_produccion[0] # Obtendiedo el primer caracter que sea terminal/no terminal 

                            print("ENVIARA EL NO TERMINAL ", no_terminal)
                            productions = buscar_producciones_con_caracter(no_terminal, char)

                            if len(productions) != 0:  # Significa que con ese no terminal si se puede reemplazar ya que si tiene producciones que inicial con el caracter que se esta leyendo
                                transicion = "λ, " + pila[0] + "; " + derecha_produccion
                                objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                pila.pop(0)
                                lista_expresion = str_a_lista(derecha_produccion)
                                pila = lista_expresion + pila
                                break
                        
                        print("lista_expresiones == ", lista_expresion)

                        if len(lista_expresion) == 0:
                            print("NO HAY PRODUCCIONES QUE GENEREN")
                            productions = ""
                            for posicion in pos_y:

                                derecha_produccion = producciones[posicion]
                                no_terminal = derecha_produccion[0]
                                productions = buscar_producciones_con_no_terminal(no_terminal, char)

                                if len(productions) != 0:
                                    transicion = "λ, " + pila[0] + "; " + derecha_produccion
                                    objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                                    pila.pop(0)
                                    pila = productions + pila
                                    break


                # Si no hay producciones que tiene en su expresion ni un termina ni un no terminal, entonces pueden haber dos opciones: O ese no terminal generaba una cadena vacia o 
                # la cadena no puede ser aceptada al no tener ninguna produccion que tenga al inicio el caracter que se esta leyendo
                elif len(pos_y) == 0 and len(pos_x) == 0:   # Si entra aqui significa que no hay producciones que cumplan con lo que se esta leyendo, por lo que no de debe aceptar la cadena
                    if epsilon != 0:
                        transicion = "λ, " + pila[0] + "; " + " λ"
                        objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                        pila.pop(0)
                    else:
                        print("LA CADENA NO ES ACEPTADA")
                        return
            
            # Si lo que esta en la cima de la pila es un no terminal
            elif pila[0] in terminales:

                # Si lo que esta en la cima de la pila es igual al caracter en lectura
                if pila[0] == char:
                    transicion = pila[0] + ", " + pila[0] + "; λ"
                    objeto_grafo.realizarRecorrido("q", char, pila, transicion, 1)
                    print("Se consumio " + pila[0])
                    pila.pop(0)
                    n = n + 1

                    # ESTADO DE ACEPTACION
                    if pila[0] == "#" and n == len(cadena):
                        transicion = ">>> λ, #; λ <<<"
                        objeto_grafo.realizarRecorrido("f", " ", "#", transicion, 1)
                        transicion = "λ, #; λ"
                        objeto_grafo.realizarRecorrido("f", " ", " ", transicion, 1)
                        print("El contenido de la pila es ", pila)
                        print("N == ", n)
                        print("LA CADENA ES ACEPTADA")
                        return True
            
                
        # CAMBIAR LAS CONDICIONES 

        # Si la pila esta vacia, aun no se ha leido la cadena y por lo menos ya se leyo un caracter de la cadena
        if pila[0] == "#" and n != len(cadena) and n != 0:
            print("LA CADENA NO ES ACEPTADA")
            return
        
        # Si ya se termino de leer la cadena y la pila todavia no esta vacia
        elif n == len(cadena) and pila[0] != "#":
            print("LA CADENA NO ES ACEPTADA")
            return
        print("Ultimo")

        print("n llego hasta ", n)







# Transiciones de la forma: [['λ', 'S', 'z M N z'], ['λ', 'M', 'a M a'], ['b', 'b', 'λ'], ['z', 'z', 'λ']]
def analizar_Cadena_con_tabla(obj_grafo, cadena, transiciones, terminales, no_terminales, no_terminal_inicial):

    global transiciones_i
    global no_terminales_ing
    global objeto_grafo

    reporte_tabla = RT.Reporte_en_Tabla()

    print("Se recibio la gramatica con exito ", obj_grafo.gramatica.nombre)


    transiciones_i = transiciones
    no_terminales_ing = no_terminales
    objeto_grafo = obj_grafo

    estado = "i"
    n = 0
    pila = []
    respaldo = ""
    transicion = ""
    

    while n < len(cadena):

        char = cadena[n]
        print("--------------------------------------")
        print()
        print("El contenido de la pila es: ", pila)

        print("Lo que se esta leyendo de la cadena es: ")
        cadena_i = ""

        for i in range(n, len(cadena)):
            cadena_i += cadena[i]
        print(cadena_i)
        sleep(0.5)

        # (q,λ,B;q,bBb)
        if estado == "i":
            transicion = "(i, λ, λ; p, #)"
            reporte_tabla.realizar_fila("λ", char, transicion, cadena_i)
            pila.insert(0, "#")
            estado = "p"

        elif estado == "p":
            transicion = "(p, λ, λ; q, " + no_terminal_inicial + ")"
            reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
            pila.insert(0, no_terminal_inicial)
            estado = "q"

        elif estado == "q":
            
            # Si lo que esta en cima de la pila es un no terminal
            if pila[0] in no_terminales:

                producciones = buscar_producciones(pila[0])  # Obteniendo todas las producciones de el no terminal que se encuentra en la cima de la pila
                pos_x = []   # Guardara las posiciones de las producciones en donde expresiones del lado derecho de la produccion empiezan con el con el caracter que estoy leyendo de la cadena
                pos_y = []   # Guardara las posiciones de las producciones en donde el lado derecho de la produccion unicamente tienen un no terminal
                epsilon = 0  # Si cambia de valor, significa que hay una produccion para ese no terminal con cadena vacia


                # Recorriendo la lista de todas las producciones encontradas del no terminal que esta en la cima
                for i in range(len(producciones)):

                    produccion = producciones[i]    # Obtendiendo la produccion que esta en esa posicion
                    lista_expresion = str_a_lista(produccion)   # Conviertiendo la expresion al lado derecho de la produccion a lista

                    # Si la expresion al lado derecho de la expresion comienza con el caracter que se esta leyendo
                    if lista_expresion[0] == char:  # Si el lado derecho de la expresion comienza con el caracter que se esta leyendo, que agrege las posiciones
                        pos_x.append(i)

                    # Si la expresion al lado derecho de la expresion comienza con un no terminal
                    if lista_expresion[0] in no_terminales: # Si el lado derecho de la expresion comienza con un no terminal
                        pos_y.append(i)
                    
                    # Si la expresion al lado derecho de la expresion es una cadena vacia
                    if lista_expresion[0] == "λ":
                        epsilon = epsilon + 1
                

                # Significa que si hay expresiones del lado derecho de la produccion que si empiezan con el caracter que estoy leyendo de la cadena
                if len(pos_x) != 0:
                    
                    # CASO 1: La pila esta vacia (tiene #) pero son se ha llegado al final de la cadena
                    if pila[1] == "#" and n + 1 != len(cadena):    # Si se cumple deberia de reemplazar por la expresion mas 'grande' o con el que tenga un no terminal despues del terminal de su izquierda
                        count = 0
                        
                        # Recorriendo todas las posiciones guardadas en la lista 'pos_x'
                        for posicion in pos_x:  # Recorriendo todas las posiciones en que hay producciones que empiezan con el caracter que se esta leyendo
                            
                            # Convieriendo a lista la expresion que esta en la esa posicion
                            produccion = producciones[posicion]
                            lista_expresion = str_a_lista(produccion)

                            # Va a acceder solo cuando hayan dos o mas terminales o no terminales en la expresion del lado derecho (si es asi, se asume que en la posicion 1 hay no terminal)
                            # Esto porque hay que elegir la expresion que sea más 'grande' o que contenga por lo menos un no terminal, para seguir generando producciones
                            if len(lista_expresion) != 1:

                                #if lista_expresion[1] in no_terminales: 
                                transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                            
                                
                            
                            # if count == len(pos_x):
                            #     print("1. La cadena no es aceptada")
                            # count = count + 1

                    
                    # CASO 2: La pila esta vacia (tiene en la posicion 0 a 'S' y en la 1 a '#') y estoy en el ultimo caracter de la cadena
                    elif pila[1] == "#" and n + 1 >= len(cadena):

                        # Recorriendo todas las posiciones guardadas en la lista 'pos_x'
                        for posicion in pos_x:

                            # Convieriendo a lista la expresion que esta en la esa posicion
                            produccion = producciones[posicion] # Obteniendo la expresion del lado derecho de la produccion
                            lista_expresion = str_a_lista(produccion)
                            
                            
                            # Debido a que solo falta leer un caracter, lo debo reemplazar por la expresion que tenga longitud 1, es decir, ya que solo se encontraron
                            # las expresiones que iniciaban con el caracter que estoy leyendo, entonces en este caso la lista solo va a tener el caracter que se esta leyendo
                            if len(lista_expresion) == 1:   # Solo tiene un elemeto de la lista
                                transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break

                    
                    # Si el elemento posterior a la cima de pila no es un '#' y no estoy leyendo el ultimo caracter de la cadena
                    elif pila[1] != "#" and n + 1 != len(cadena):

                        contador = 0

                        # Recorriendo todas las posiciones guardadas en la lista 'pos_x'
                        for posicion in pos_x:  # Recorriendo todas las posiciones de las producciones que tiene al inicio de la produccion el caracter que estoy leyendo (Ej. A -> z B ó C -> z C)

                            contador = contador + 1

                            # Convieriendo a lista la expresion que esta en la esa posicion
                            produccion = producciones[posicion]
                            lista_expresion = str_a_lista(produccion)

                            # Los siguientes casos se aplican cuando se encuentran dos o mas producciones que inician con el caracter que estoy leyendo
                            if len(pila) - 1 == len(cadena) - n:    # Si en la pila tengo la misma cantidad de elementos (sin contar el '#') que el tamaño del resto de la cadena que estoy leyendo. Ej. pila = {#,a,B}; cadena que falta leer = {a, b}

                                # Cuando se presenta este caso, solamente se reemplaza el no terminal con la produccion que tenga como expresion solo cadena que estoy leyendo, es decir, cuando la lista de longitud 1
                                # Ya que ya esta implicito que sea el caracte que se esta leyendo
                                if len(lista_expresion) == 1:   # Si la lista de expresiones unicamento tienen el elemento que estoy leyendo, lo debo de insertar
                                    transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                    reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                    pila.pop(0)
                                    pila = lista_expresion + pila
                                    break
                            
                            # Si lo que lo que la cima tiene justo abajo es igual al siguiente caracter de la cadena, 
                            # entonces cuando encuentre la produccion que tenga como inicial de la expresion el caracter que se esta leyendo y como siguinete de la pila y cadena un mismo caracter,
                            # entonces se puede remplazar el no terminal con el la produccion que genera la expresion que solo tiene el caracter que se esta leyendo
                            elif pila[1] == cadena[n+1]:

                                bandera = False # Si toma el valor de True, significa que dentro de la pila si hay un no terminal, sino, no hay no no terminal
                                for i in range(1, len(pila)):   # Buscando si hay no terminal dentro de la pila
                                    if pila[i] in no_terminales:
                                        bandera = True
                                        break
                                    
                                # Si en el lado derecho de la produccion solo esta el caracter que estoy buscando y ademas dentro de la pila hay un no terminal,
                                # eso me da la confianza de poder reemplazarlo por un terminal para asegurarme de que la cadena se siga leyendo, ya que ese no terminal generara mas producciones
                                if len(lista_expresion) == 1 and bandera == True:
                                    transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                    reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                    pila.pop(0)
                                    pila = lista_expresion + pila
                                    break
                                
                                # Si en el lado derecho de la produccion es de longitud 2 o mas y no hay ningun terminal dentro de la lista, 
                                # Entonces hay que insertar esa produccion a la pila (suponiendo que esa produccion tiene por lo menos un simbolo no terminal y asi poder seguir generando producciones)
                                elif len(lista_expresion) >= 2 and bandera == False:
                                    transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                    reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                    pila.pop(0)
                                    pila = lista_expresion + pila
                                    break
                            
                            elif len(lista_expresion) > 1:  # Sino se cumple lo anterior, entonces si lo que produce el no terminal es de longitud mayor a 1 (esta el caracter que estoy leyendo mas otro terminal o no terminal)
                                transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                            
                            # Si no se cumple lo anterior, y solo esta el caracter que se esta leyendo, solo lo inserto. En este caso solo se guarda por si ya terminó el ciclo y no se encontro
                            # una produccion que tuviera dos o mas terminales o no terminales
                            elif len(lista_expresion) == 1: 
                        
                                respaldo = lista_expresion[0]
                            
                            # Si ya se termino de recorrer la lista de posiciones que tienen las expresiones que comienzan con el caracter que estoy leyendo y no entro a ninguno de los anteriores, 
                            # entonces que inserte a la lista la produccion que solo tenia como expresion el caracter que esoy leyendo (ej. A --> z)
                            if contador == len(pos_x):
                                transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                                
                            # El siguiente caso aplica solo cuando se encuentra una produccion que inicia con el caracter que estoy leyendo. Se debe de insertar si o si, ya que no hay mas opciones
                            if len(producciones) == 1 and len(lista_expresion) == 1:   # Solo tiene un elemeto de la lista
                                transicion = "(q, λ, " + pila[0] + "; q, " + produccion + ")"
                                reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                pila.pop(0)
                                pila = lista_expresion + pila
                                break
                    

                # Si se encontraron producciones que tiene como inicio y no terminal
                elif len(pos_y) != 0:   # Si entra aqui significa que no hay expresiones del lado derecho de las producciones que empiecen con el caracter que estoy leyendo

                    # Si el no terminal solo tiene una expresion del lado derecho que empieza con un no terminal (Ej. S -> A)
                    if len(pos_y) == 1:
                        # transicion = "λ, " + pila[0] + "; " + produccion
                        # objeto_grafo.realizarRecorrido("q", char, pila, transicion)
                        derecha_produccion = producciones[pos_y[0]] # Obteniendo el lado derecho de la produccion
                        no_terminal = derecha_produccion[0] # Obtendiedo el primer caracter que sea terminal/no terminal 
                        transicion = "(q, λ, " + pila[0] + "; q, " + derecha_produccion + ")"
                        reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                        pila.pop(0)

                        lista_expresion = str_a_lista(derecha_produccion)
                        pila = lista_expresion + pila
                    
                    # Si hay mas de una, entoces que busque cual de todos los no terminales del lado derecho producen una expresion que inicie con el caracter que se esta leyendo
                    else:

                        lista_expresion = []

                        for posicion in pos_y:
                            
                            print("Se busca acceder a la posicion "+ str(posicion) + " en ", producciones)

                            derecha_produccion = producciones[posicion] # Obteniendo el lado derecho de la produccion
                            no_terminal = derecha_produccion[0] # Obtendiedo el primer caracter que sea terminal/no terminal 

                            print("ENVIARA EL NO TERMINAL ", no_terminal)
                            productions = buscar_producciones_con_caracter(no_terminal, char)

                            if len(productions) != 0:  # Significa que con ese no terminal si se puede reemplazar ya que si tiene producciones que inicial con el caracter que se esta leyendo
                                transicion = "(q, λ, " + pila[0] + "; q, " + derecha_produccion + ")"
                                reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                pila.pop(0)
                                lista_expresion = str_a_lista(derecha_produccion)
                                pila = lista_expresion + pila
                                break
                        
                        print("lista_expresiones == ", lista_expresion)

                        if len(lista_expresion) == 0:
                            print("NO HAY PRODUCCIONES QUE GENEREN")
                            productions = ""
                            for posicion in pos_y:

                                derecha_produccion = producciones[posicion]
                                no_terminal = derecha_produccion[0]
                                productions = buscar_producciones_con_no_terminal(no_terminal, char)

                                if len(productions) != 0:
                                    transicion = "(q, λ, " + pila[0] + "; q, " + derecha_produccion + ")"
                                    reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                                    pila.pop(0)
                                    pila = productions + pila
                                    break


                # Si no hay producciones que tiene en su expresion ni un termina ni un no terminal, entonces pueden haber dos opciones: O ese no terminal generaba una cadena vacia o 
                # la cadena no puede ser aceptada al no tener ninguna produccion que tenga al inicio el caracter que se esta leyendo
                elif len(pos_y) == 0 and len(pos_x) == 0:   # Si entra aqui significa que no hay producciones que cumplan con lo que se esta leyendo, por lo que no de debe aceptar la cadena
                    if epsilon != 0:
                        transicion = "(q, λ, λ; q, λ)"
                        reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                        pila.pop(0)
                    else:
                        print("LA CADENA NO ES ACEPTADA")
                        return
            
            # Si lo que esta en la cima de la pila es un no terminal
            elif pila[0] in terminales:

                # Si lo que esta en la cima de la pila es igual al caracter en lectura
                if pila[0] == char:
                    transicion = "(q, " + pila[0] + ", " + pila[0] + "; q, λ)"
                    reporte_tabla.realizar_fila(pila, char, transicion, cadena_i)
                    print("Se consumio " + pila[0])
                    pila.pop(0)
                    n = n + 1

                    # ESTADO DE ACEPTACION
                    if pila[0] == "#" and n == len(cadena):
                        transicion = "(q, λ, #; f, λ)"
                        reporte_tabla.realizar_fila(pila, char, transicion, "λ")
                        reporte_tabla.realizar_fila("λ", "λ", "f", "λ")
                        print("El contenido de la pila es ", pila)
                        print("N == ", n)
                        print("LA CADENA ES ACEPTADA")
                        return True
            
                
        # CAMBIAR LAS CONDICIONES 

        # Si la pila esta vacia, aun no se ha leido la cadena y por lo menos ya se leyo un caracter de la cadena
        if pila[0] == "#" and n != len(cadena) and n != 0:
            print("LA CADENA NO ES ACEPTADA")
            return
        
        # Si ya se termino de leer la cadena y la pila todavia no esta vacia
        elif n == len(cadena) and pila[0] != "#":
            print("LA CADENA NO ES ACEPTADA")
            return
        print("Ultimo")

        print("n llego hasta ", n)








# [['λ', 'S', 'z M N z'], ['λ', 'M', 'a M a'], ['b', 'b', 'λ'], ['z', 'z', 'λ']]


# Buscara todas las producciones en donde el caracter al prinicipio de la expresion sea igual al caracter que se esta leyendo
# Ejemplo: caracter en lectura: a; S -> a B ó  S -> a M a
def buscar_producciones_con_caracter(no_terminal, caracter):

    global transiciones_i
    producciones = []

    for i in range(len(transiciones_i)):

        if transiciones_i[i][1] == no_terminal:
            print("SON IGUALES " + transiciones_i[i][1] + " == " + no_terminal)

            expresion = transiciones_i[i][2]

            if expresion[0] == caracter:
                print("LA EXPRESION ES ", expresion)
                print("Lo que tiene la expresion en 0: " + expresion[0])
                producciones.append(transiciones_i[i][2])

    return producciones

def buscar_transicion(no_terminal, produccion):
    global transiciones_i

    for i in range(len(transiciones_i)):
        
        if transiciones_i[i][1] == no_terminal and transiciones_i[i][2] == produccion:
            return transiciones_i[i]


def buscar_producciones_con_no_terminal(no_terminal, caracter):

    print("Entro con ", no_terminal)

    global transiciones_i, no_terminales_ing
    reemplazar_por = []
    producciones = []

    for i in range(len(transiciones_i)):

        if transiciones_i[i][1] == no_terminal:

            expresion = transiciones_i[i][2]

            if expresion[0] in no_terminales_ing:

                producciones = buscar_producciones_con_caracter(no_terminal, caracter)

                if len(producciones) != 0:
                    reemplazar_por.append(n)
                    break

    if len(producciones) != 0:
        return reemplazar_por
    else:
        return reemplazar_por
                    
                



def buscar_producciones(no_terminal):

    global transiciones_i
    producciones = []

    for i in range(len(transiciones_i)):

        if transiciones_i[i][1] == no_terminal:
            producciones.append(transiciones_i[i][2])

    return producciones


def str_a_lista(cadena):

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
