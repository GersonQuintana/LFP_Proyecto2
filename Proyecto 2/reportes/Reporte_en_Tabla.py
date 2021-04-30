class Reporte_en_Tabla():

    def __init__(self):
        self.contador = 0

    def realizar_fila(self, contenido_pila, entrada, transicion, cadena):
        inicio_HTML = ""
        fin_HTML = ""
        inicio_body = ""
        fin_body = ""
        inicio_tabla = ""
        titulo = ""
        
        if self.contador == 0:
            inicio_HTML = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte en tabla</title>
        <link rel="stylesheet" href="css/bootstrap.min.css">
        <link rel="stylesheet" href="css/estilos_reporte_tabla.css">
    </head>\n"""
            titulo = """<div class="title">
    <h1>REPORTE EN TABLA</h1>
</div>"""
            
            fin_HTML = "</html>\n"
            inicio_body = "<body>\n"
            fin_body = "</body>\n"
            inicio_tabla = """<div class="contenido">
            <table class="table table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Iteración</th>
                        <th>Resto de la cadena</th>
                        <th>Pila</th>
                        <th>Entrada</th>
                        <th>Transiciones</th>
                    </tr>
                    <tbody>"""
            
            file = open("reportes/Reporte_Tabla.html", "w", encoding="UTF-8")
            file.write(" ")
            file.close()
        

        contenido = f"""
                        <tr>
                            <td class="centrar">{str(self.contador)}</td>
                            <td class="centrar">{cadena}</td>
                            <td class="derecha">{"".join(contenido_pila)}</td>
                            <td class="centrar">{entrada}</td>
                            <td class="izquierda">{transicion}</td>
                        </tr>
                    """

        HTML = inicio_HTML + inicio_body + titulo + inicio_tabla + contenido

        file = open("reportes/Reporte_Tabla.html", "a", encoding="UTF-8")
        file.write(HTML)
        file.close()
        self.contador = self.contador + 1

        # NOTA: Aqui no se cierra el body no el html, este se cierra en el 'Main.py' ya que no se sabe cuando sera la ultima imagen