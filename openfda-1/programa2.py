import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers) #gracias a lo leido en el API REST
# de OpenFDA he conseguido saber que escribiendo ?limit=10 consigo la informacion de 10 medicamentos.
# Ademas es importante saber que la funcion 'request', necesita 4 parametros.
r1 = conn.getresponse()
print(r1.status, r1.reason)
label_raw = r1.read().decode("utf-8")
conn.close()

label_normal = json.loads(label_raw)
for i in range (len (label_normal['results'])): #Creo un bucle haciendo que la i valga desde 0 hasta 9.
    informacion_medicamento=label_normal['results'][i]

    print ('ID: ',informacion_medicamento['id']) #En este programa solo imrpimo el id.