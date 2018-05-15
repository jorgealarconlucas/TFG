import http.server
import socketserver
import http.client
import json

PORT = 2018 #  Puerto donde lanzar el servidor
#el puerto puede ser cualquiera, siempre por encima del 1024


def lista_medicamentos():
    lista = []
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=11", None, headers)

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    label_raw = r1.read().decode("utf-8")
    conn.close()

    label = json.loads(label_raw)
    for i in range(len(label['results'])):
        medicamento_info = label['results'][i]
        if (medicamento_info['openfda']):
            lista.append(medicamento_info['openfda']['generic_name'][0])

    return lista

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): #esta clase hereda todos los
    #metodos de la clase principal BaseHTTPRequestHandler.

    def do_GET(self): #utilizo el metodo GET para pedir una peticion por http
        self.send_response(200)
        # pongo las cabezeras para que el cliente sepa
        # que el contenido que le voy a enviar es html
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content="<html><body>"
        lista=lista_medicamentos () #funcion en la que el servidor pide los 10 medicamentos a OpenFDA
        # y te los devuelve en json
        for e in lista:
            content += e+"<br>"  #br significa saltar de linea
        content+="</body></html>"

        self.wfile.write(bytes(content, "utf8")) #Sirve para  enviar el mensaje completo
        return


# El servidor comienza  aqui
# estableciendo como manejador nuestra propia clase
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler) # esperamos conexiones del cliente
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")
