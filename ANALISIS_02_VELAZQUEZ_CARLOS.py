#Primero importaremos los modulos necesarios, en este caso csv para el archivo
#y la funcion counter del modulo collections para facilitar el conteo.
import csv
from collections import Counter

#Debido a que trabajaremos con numeros grandes haremos una funcion que agregue
#comas a numeros enteros.
def numero_con_comas(number):
    return ("{:,}".format(number))

#Despues crearemos una funcion que de una lista de lineas obtenidas del archivo
#csv(ya sea lista de importaciones o exportaciones) obtenga los medios de
#transporte mas utilizados y cuanta ganancia genero cada medio de transporte.
def mejores_medios_transporte(lista):
    lista_de_ganancias = {}
    lista_de_transportes = []
    for line in lista:
        tipo_de_transporte = line['transport_mode']
        lista_de_transportes.append(tipo_de_transporte)
        #Este condicional if nos permite ir sumando las ganancias obtenidas de
        #cada linea y lo agrega a un diccionario en su respectivo medio de
        #transporte
        if tipo_de_transporte not in lista_de_ganancias:
            lista_de_ganancias[tipo_de_transporte] = int(line['total_value'])
        else:
            sumatoria =  int(lista_de_ganancias.get(tipo_de_transporte))+ int(line['total_value'])
            lista_de_ganancias[tipo_de_transporte] = sumatoria

    #Despues, ya que tenemos en la lista_de_transportes cada vez que se utilizo
    #cada medio de transporte, ya podemos contar con la funcion Counter y
    #ademas tenemos la ganancia de cada medio, por lo que podemos imprimir las
    #veces que se utilizo cada medio de transporte y la ganancia de cada una
    #ordenadas de mayor a menor
    print("Las veces que se utilizaron los diferentes metodos de transporte son los siguientes:")
    conteo_lista_transportes = Counter(lista_de_transportes)
    sort_lista_de_transportes = sorted(conteo_lista_transportes.items(), key=lambda x: x[1], reverse=True)
    for transporte in sort_lista_de_transportes:
        print(transporte[0], ":", numero_con_comas(transporte[1]))
    print("\n")
    print("La suma de dinero ganada por los distintos metodos de transporte es la siguiente:")
    sort_lista_de_ganancias = sorted(lista_de_ganancias.items(), key=lambda x: x[1], reverse=True)
    for transporte in sort_lista_de_ganancias:
        print(transporte[0], ":", numero_con_comas(transporte[1]))

#Posteriormente, crearemos una funcion que identifique todas las rutas que se
#efectuaron, para una lista de lineas del archivo csv(ya sea de importaciones
#o exportaciones), despues las cuenta las veces que se efectuo cada ruta, las
#ordena y ademas calcula la ganancia generada de cada ruta, para finalmente
#imprimir los 10 primeros resultados de mayor demanda a menor demanda
def rutas_mas_demandadas(lista):
    lista_de_rutas = []
    ganancia_de_ruta = {}
    for line in lista:
        #Definiremos una variable que contenga la ruta con el formato (ORIGEN-
        #DESTINO) y lo agregamos a lista_de_rutas para despues contarlo, ademas
        #vamos sumando la ganancia de la ruta y la vamos agregando a un
        #diccionario
        ruta = line['origin'] + "-" + line['destination']
        lista_de_rutas.append(ruta)
        if ruta not in ganancia_de_ruta:
            ganancia_de_ruta[ruta] = line['total_value']
        else:
            sumatoria_de_ganancias_de_ruta =  int(line['total_value']) + int(ganancia_de_ruta[ruta])
            ganancia_de_ruta[ruta] = sumatoria_de_ganancias_de_ruta
    #Despues crearemos un diccionario para agregar la cuenta de las veces que
    #se utilizo cada ruta
    lista_de_rutas_contadas = {}
    for ruta in lista_de_rutas:
        conteo = lista_de_rutas.count(ruta)
        lista_de_rutas_contadas[ruta] = conteo
    #por ultimo imprimiremos las top 10 rutas que tuvieron mas demanda junto
    #con la ganancia de cada una
    i = 1
    for key, value in sorted(lista_de_rutas_contadas.items(), key= lambda x:x[1], reverse=True):
        if i < 11:
            print(i,". Ruta: ",key, '   Demanda: ', value,"    Ganancia de ruta: ", numero_con_comas(ganancia_de_ruta[key]))
            i += 1
        else:
            break
#Tambien, definiremos una funcion que obtenga el valor total de ganancias para
#cada pais que se encuentre en la lista (ya sea lista de importacion
#o exportacion) y despues imprimiermos el total neto obtenido, para despues
#imprimir la ganancia de los paises que formen el 80% de las ganancias, de mayor
#a menor
def valor_total(lista):
    #En lista de ganancias iremos actualizando la ganancia de cada pais para
    #despues de que lea cada linea ya tengamos la ganancia total de cada pais
    lista_de_ganancias = {}
    #cada ganancia obtenida la agregaremos a suma_total_de_ganancias para
    #despues usar la funcion sum y obtener el total de las ganancias netas
    suma_total_de_ganancias = []
    for line in lista:
        if line['origin'] not in lista_de_ganancias:
            lista_de_ganancias[line['origin']] = line['total_value']
            suma_total_de_ganancias.append(int(line['total_value']))
        else:
            sumatoria_de_ganancias = int(line['total_value']) + int(lista_de_ganancias[line['origin']])
            lista_de_ganancias[line['origin']] = sumatoria_de_ganancias
            suma_total_de_ganancias.append(int(line['total_value']))

    #imprimimos las ganancias totales y luego las ganancias de los paises que
    #forman el 80% de las ganancias
    print(f"En total se obtuvo {numero_con_comas(sum(suma_total_de_ganancias))} de ganancias")
    i = 0

    for value, key in sorted(lista_de_ganancias.items(), key= lambda x: x[1], reverse= True):
        if i <= 80:
            porcentaje_de_ganancias = (key * 100) / sum(suma_total_de_ganancias)
            print(value," : ", numero_con_comas(key), "esto es el", round(porcentaje_de_ganancias, 2), "% del total")
            i += round(porcentaje_de_ganancias, 2)

#agregamos introduccion al programa para informar al usuario que se esta
#analizando la base de datos(el archivo csv)
print("\n")
print("**" * 20)
print("Synergy Logistics")
print("**" * 20)
print("Analizando base de datos...")
print("NOTA: Tarda 5 segundos en cargar")

#abrimos el archivo y separamos las importaciones y las exportaciones
#en diferentes lisitas
with open('synergy_logistics_database.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    lista_de_importaciones = []
    lista_de_exportaciones = []
    lista_de_ganancias = {}
    for line in csv_reader:
        if line['direction'] == 'Imports':
            lista_de_importaciones.append(line)
        else:
            lista_de_exportaciones.append(line)

#Imprimimos el titulo de la seccion y despues corremos la funcion con la lista
#que deseamos analizar (ya sea de importaciones o exportaiones) y agregamos
# \n despues de cada bloque para que se pueda ver mejor
print("\n")
print("**" * 20)
print("10 Rutas mas demandadas[EXPORTACIONES] (Origen-Destino)")
print("**" * 20)
rutas_mas_demandadas(lista_de_exportaciones)

print("\n")
print("**" * 20)
print("10 Rutas mas demandadas[IMPORTACIONES] (Origen-Destino)")
print("**" * 20)
rutas_mas_demandadas(lista_de_importaciones)

print("\n")
print("**" * 20)
print("MEJORES MEDIOS DE TRANSPORTE PARA IMPORTACIONES")
print("**" * 20)
mejores_medios_transporte(lista_de_importaciones)

print("\n")
print("**" *20)
print("MEJORES MEDIOS DE TRANSPORTE PARA EXPORTACIONES")
print("**" * 20)
mejores_medios_transporte(lista_de_exportaciones)
# PENDIENTE AGREGAR EL %
print("\n")
print("**" *20)
print("Paises que generan el 80% del valor total de las importaciones:")
print("**" * 20)
valor_total(lista_de_importaciones)

print("\n")
print("**" *20)
print("Paises que generan el 80% del valor total de las exportaciones:")
print("**" *20)
valor_total(lista_de_exportaciones)
