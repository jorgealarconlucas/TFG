import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers) #lanzo la peticion
r1 = conn.getresponse() #Acepto la respuesta recibida desde openfda
print(r1.status, r1.reason) #Compruebo si con el recurso lanzado me ha respondido bien
label_raw = r1.read().decode("utf-8") #lee el contenido de la respuesta en json. Ademas poniendo
#.decode, consigo interpretar simbolos anormales.
conn.close()

label_normal = json.loads(label_raw)  #con el loads consigo transformar el contenido a una forma mas
# estructurada
informacion_medicamento=label_normal['results'][0]

print ('ID: ',informacion_medicamento['id'])
print ('Proposito: ',informacion_medicamento['purpose'][0])
print ('Fabricante: ',informacion_medicamento['openfda']['manufacturer_name'][0])
