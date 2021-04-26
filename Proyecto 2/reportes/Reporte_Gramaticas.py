row = ""

def agregar_al_reporte(nombre_gramatica):
    global row
    razon = "No posee ninguna producción que la convierta exclusivamente en libre del contexto."
    row += f"""<tr>
                    <td>{nombre_gramatica}</td>
                    <td>{razon}</td>
                </tr>\n"""

def generar_reporte():
    global row
    i_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <title>Document</title>
    <link rel="stylesheet" href="css/estilos.css">
</head>
<body>\n"""

    f_html = """</body>
</html>\n"""

    tabla = f"""<div class="container">
        <h1>Reporte de Gramáticas No Aceptadas</h1>
        <table class="table table-hover">
            <thead class="table-dark">
                <th width="400">Nombre de la gramática</th>
                <th>Razón</th>
            </thead>
            <tbody>
                {row}
            </tbody>
            </table>
        </div>\n"""
    
    HTML = i_html + tabla + f_html
    file = open("reportes/Reporte_Gramaticas.html", "w", encoding='UTF-8')
    file.write(HTML)
    file.close()
    row = ""