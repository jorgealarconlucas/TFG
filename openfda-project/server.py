import http.server
import http.client
import json
import socketserver

#estos import son utiles ya que me voy a comportar como servidor, cuando me pidan informacion. Como
#servidor para pedir informacion a OpenFDA. Ademas el import json me servira para tratar la respuesta
#recibida de OpenFDA. Y el import socketserver sirve para reservar la IP y el puerto donde mi servidor va a escuchar.

PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):#esta clase define como se comporta nuestra practica ante una peticion http

    OPENFDA_API_URL="api.fda.gov"       #esto son constantes que yo me he definido
    OPENFDA_API_EVENT="/drug/label.json"
    OPENFDA_API_DRUG='&search=active_ingredient:'
    OPENFDA_API_COMPANY='&search=openfda.manufacturer_name:'


    def get_main_page(self):# con esta funcion consigo la pagina donde el usuario puede consultar. Se trata de formularios
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body>
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html
    def web (self, lista): #esta funcion da la pagina web cuando pulsas una de las opciones del formulario
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return list_html

    def resultados_genericos (self, limit=10):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+str(limit))
        print (self.OPENFDA_API_EVENT + "?limit="+str(limit))
        r1 = conn.getresponse()
        label_raw = r1.read().decode("utf8")
        data = json.loads(label_raw)
        resultados = data['results']
        return resultados

    def do_GET(self): #utilizo el metodo GET para pedir una peticion por http
        recurso_list = self.path.split("?")  #aquí vemos si hay parámetros o no, ya que los parámetros empiezan con una ?,
        if len(recurso_list) > 1:   #si len es mayor que 1, hay parámetros.
            params = recurso_list[1]
        else:
            params = "" # en este caso si len (longitud) es 1 es que no hay parámetros.

        limit = 1 #el limite por defecto es 1

        if params:
            parse_limit = params.split("=")
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("No existen parametros")


        if self.path=='/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html=self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))

        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            medicamentos = []
            resultados = self.resultados_genericos(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    medicamentos.append (resultado['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Desconocido')
            resultado_html = self.web (medicamentos)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listCompanies' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []
            resultados = self.resultados_genericos (limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocido')
            resultado_html = self.web(companies)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listWarnings' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []
            resultados = self.resultados_genericos (limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    warnings.append (resultado['warnings'][0])
                else:
                    warnings.append('Desconocido')
            resultado_html = self.web(warnings)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10   #en este caso el limite por defecto es 10
            drug=self.path.split('=')[1]

            drugs = []
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+str(limit) + self.OPENFDA_API_DRUG + drug)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            events_search_drug = biblioteca_data['results']
            for resultado in events_search_drug:
                if ('generic_name' in resultado['openfda']):
                    drugs.append(resultado['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')

            resultado_html = self.web(drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            company=self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + str(limit) + self.OPENFDA_API_COMPANY + company)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            events_search_company = biblioteca_data['results']

            for event in events_search_company:
                companies.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.web(companies)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'redirect' in self.path:
            self.send_response(301)  #esta respuesta redirige a la pagina
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_error(401)  #significa que la pagina esta restringida
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return

#Este es el programa principal

socketserver.TCPServer.allow_reuse_address= True

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever() #el servidor comienza a atender peticiones para siempre
