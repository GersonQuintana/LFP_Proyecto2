import os

def generar_reporte(nombre, alfabeto_pila, terminales, ruta_imagen):
    nombre = "AP_" + nombre
    terminales = "{ " + terminales + " }"
    alfabeto_pila = "{ " + alfabeto_pila + " }"
    estados = "{ i, p, q, f }"
    estado_inicial = "{ i }"
    estado_final = "{ f }"

    inicio_html = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Autómata de pila</title>
                        <link rel="stylesheet" href="css/estilos_Automata.css">
                    </head>
                    <body>"""
    
    fin_html = """</body>
                  </html>"""

    contenido = f"""<div class="container">
                        <h1>AUTÓMATA DE PILA EQUIVALENTE</h1>
                        <div class="contenedor">
                            <div class="info-grafo">
                                <p><b>Nombre del grafo = </b>{nombre}</p>
                                <p><b>Terminales = </b>{terminales} </p>
                                <p><b>Alfabeto de pila =</b> {alfabeto_pila}</p>
                                <p><b>Símbolo inicial de la pila =</b> λ</p>
                                <p><b>Estados =</b> {estados}</p>
                                <p><b>Estado inicial =</b> {estado_inicial}</p>
                                <p><b>Estado de aceptación =</b> {estado_final}</p>
                            </div>
                            <img src="../{ruta_imagen}" alt="">
                        </div>
                    </div>"""
    
    
    archivo = open("reportes/Automata_Equivalente.html", "w", encoding="UTF-8")
    documento = inicio_html + contenido + fin_html
    archivo.write(documento)
    archivo.close()

    os.system("reportes\\Automata_Equivalente.html")