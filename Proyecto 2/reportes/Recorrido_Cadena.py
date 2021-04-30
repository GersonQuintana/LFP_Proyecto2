contador = 0

def realizar_iteracion(ruta_imagen, contenido_pila, entrada):
    global contador
    inicio_HTML = ""
    fin_HTML = ""
    inicio_body = ""
    fin_body = ""

    ruta_imagen = ruta_imagen.replace("\\", "/")
    print("La ruta ahora es ", ruta_imagen)

    print(">> La ruta de la imagen es <<", ruta_imagen)
    
    if contador == 0:
        inicio_HTML = """<!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="css/estilos_recorrido.css">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="css/bootstrap.min.css">
    </head>\n"""
        
        fin_HTML = "</html>\n"
        inicio_body = "<body>\n"
        fin_body = "</body>\n"
        file = open("reportes/Recorrido_Cadena.html", "w", encoding="UTF-8")
        file.write(" ")
        file.close()

    print("LA RUTA DE LA IMAGEN ES ", ruta_imagen)
    contenido = f"""<div class="titulo">
        <h2>Iteracion #{str(contador)}</h2>
    </div>
    <div class="container">
        <img src="../{ruta_imagen}" alt="">
        <div class="info">
            <table class="table">
                <thead class="table-light">
                    <tr>
                        <th>Pila</th>
                        <td>{"".join(contenido_pila)}</td>
                    </tr>
                </thead>
            </table>
            <table class="table">
                <thead class="table-light">
                    <tr>
                        <th style="background-color: rgb(87, 81, 241);">Entrada</th>
                        <td>{entrada}</td>
                    </tr>
                </thead>
            </table>
        </div>
    </div>\n"""

    HTML = inicio_HTML + inicio_body + contenido

    file = open("reportes/Recorrido_Cadena.html", "a", encoding="UTF-8")
    file.write(HTML)
    file.close()
    contador = contador + 1