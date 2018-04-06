import http.client
import json

headers = {'User-Agent': 'http-client'}

skip_number=0
while True:
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=100&skip="+str(skip_number)+'&search=substance_name:"ASPIRIN"', None, headers) # porcentaje y 22 son comillas

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    label_raw = r1.read().decode("utf-8") #lee la respuesta en json
    conn.close()

    label_normal = json.loads(label_raw)
    for i in range (len (label_normal['results'])):
        informacion_medicamento=label_normal['results'][i]
        if (informacion_medicamento['openfda']):
            print('Fabricante: ', informacion_medicamento['openfda']['manufacturer_name'][0])

    if (len (label_normal['results'])<100): #en el momento en el que hay menos de 100 medicamentos
        #con aspirina, el bucle se cierra.
        break
    skip_number=skip_number+100 #de esta manera consigo que el programa vaya saltandose los 100
    #medicamentos que ya ha imprimido.