"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd
import re


def ingest_data():

    #
    # Inserte su código aquí
    #

    with open('clusters_report.txt', 'r') as file:
        df = file.readlines()[4:] #Empieza desde la línea 4 para no tener en cuenta el encabezado

    clusters = []

    # Variables temporales para mantener los datos del cluster actual
    # Diccionario con valores predeterminados (0 para los valores numéricos y una cadena vacía para las palabras clave)
    guardar_cluster = {'cluster': 0, 'cantidad_de_palabras_clave': 0, 'porcentaje_de_palabras_clave': 0, 'principales_palabras_clave': ''}

    for line in df:
            if re.match('^ +[0-9]+ +', line): #Con la lib re y el método match lo que se hace es mirar si la línea empieza con un número para entrar al loop
            # Si la línea comienza con números, es una nueva entrada de cluster
                if guardar_cluster['cluster'] != 0:
                    clusters.append(guardar_cluster.copy())  # Guardamos el cluster actual antes de comenzar uno nuevo
                numero, cantidad, porcentaje, *palabras = line.split() #Cualquier palabra adicional después de percentage será empaquetada en la lista words
                guardar_cluster['cluster'] = int(numero)
                guardar_cluster['cantidad_de_palabras_clave'] = int(cantidad)
                guardar_cluster['porcentaje_de_palabras_clave'] = float(porcentaje.replace(',', '.'))
                if palabras[0].startswith('%'):
                    palabras[0] = palabras[0][1:]  # Eliminar el primer carácter (%)
                guardar_cluster['principales_palabras_clave'] = ' '.join(palabras).strip()
            
            elif re.match('^ +[a-z]', line):
                # Si la línea comienza con letras, es una continuación del cluster actual
                words = line.split()
                guardar_cluster['principales_palabras_clave'] += ' '+' '.join(words).strip()


    # Agregamos el último cluster después del bucle
    if guardar_cluster['cluster'] != 0:
        clusters.append(guardar_cluster)


    # Construir el DataFrame
    df = pd.DataFrame(clusters, columns=['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'])

    return df