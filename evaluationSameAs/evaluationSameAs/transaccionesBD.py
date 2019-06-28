#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#---------------------------- Documentación General ----------------------------
__author__ = "Fernando Baculima DCC Ucuenca"
__version__ = "0.1"
__status__ = "Beta 0.1"
__copyright__ = "Escuela de Sistemas - Facultad de Ingeniería - Universidad de Cuenca - Fernando Baculima"

#---------------------------- Importa las librerías ----------------------------
import psycopg2, sys
import evaluationSameAs.evaluationSameAs.nltk_similarity
import time
import hashlib
from evaluationSameAs.evaluationSameAs.nltk_similarity import *
from flask import jsonify
#---------------------- Definición de Variables Globales -----------------------
#conexion = psycopg2.connect(database='geolinkeddata',user='ucuenca',password='ucuenca2017', host='172.17.0.2')
#CURSOR = conexion.cursor()
ID_ASIGNATURA1 = '271'
ID_ASIGNATURA2 = '122'
TEXTO1_STEMMING = set()
TEXTO2_STEMMING = set()
NOMBRE_ASIGNATURA1 = ""
NOMBRE_ASIGNATURA2 = ""
CAPITULOS_ASIGNATURA1 = {}
CAPITULOS_ASIGNATURA2 = {}
DESCRIPCION_ASIGNATURA1 = ""
DESCRIPCION_ASIGNATURA2 = ""

#--------------------------- Definición de Funciones ---------------------------
def datos_insertar(escuela,edad,genero):
    persona_id = get_persona_id()
    try:
        connection = psycopg2.connect(user="ucuenca",
                                  password="ucuenca2017",
                                  host="172.17.0.4",
                                  port="5432",
                                  database="geolinkeddata")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO personas (id, escuela, edad, genero) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (persona_id, escuela, edad, genero)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into personas table")
        msg_out = "ok"
    except (Exception, psycopg2.Error) as error :
       if(connection):
           print("Failed to insert record into personas table", error)
           msg_out = "failed"
    finally:
       #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return jsonify({ 'status': msg_out, 'persona_id': str(persona_id)})

def datos_consultar(param):
    try:
        connection = psycopg2.connect(user="ucuenca",
                                  password="ucuenca2017",
                                  host="172.17.0.4",
                                  port="5432",
                                  database="geolinkeddata")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from pares order by RANDOM() limit " + param
        cursor.execute(postgreSQL_select_Query)
        msg_out = "data recovery ok"
        records = cursor.fetchall() 
        print("Print each row and it's columns values")
        group = []
        for row in records:
            pair = {}
            pair['id'] = row[0]
            pair['uri_a'] = row[1]
            pair['uri_b'] = row[2]
            group.append(pair)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
        msg_out = "Error while fetching data from database"
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return jsonify(group)



def datos_insertar_evaluacion(evaluacion, id_persona, id_par):
    try:
        connection = psycopg2.connect(user="ucuenca",
                                  password="ucuenca2017",
                                  host="172.17.0.4",
                                  port="5432",
                                  database="geolinkeddata")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO evaluacion (evaluacion, id_persona, id_par) VALUES (%s,%s,%s)"""
        record_to_insert = (evaluacion, id_persona, id_par)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into evaluacion table")
        msg_out = "ok"
    except (Exception, psycopg2.Error) as error :
       if(connection):
           print("Failed to insert record into evaluacion table", error)
           msg_out = "failed"
    finally:
       #closing database connection.
       if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return jsonify({ 'status': msg_out })



def get_persona_id():
    millis = int(round(time.time()*1000))
    return millis


def suma_digitos(num):
    s = 0
    while num>0:
        s = s + num % 10
        num=num // 10
    return s


def obtener_nombre(id_asignatura):
    """Función para realizar la conexión con PostgreSQL."""
    nombre = ''
    CURSOR.execute("SELECT DISTINCT nombre_asignatura FROM silabo "+
                   "WHERE id_silabo = '" + id_asignatura + "'")
    rows = CURSOR.fetchall()
    nombre = rows[0][0]
    return nombre

def obtener_descripcion(id_asignatura):
    """Función para obtener la descripción de una asignatura."""
    descripcion = ""
    CURSOR.execute("SELECT DISTINCT descripcion_silabo FROM silabo " +
                   "WHERE id_silabo = '" + id_asignatura + "'")
    rows = CURSOR.fetchall()
    descripcion = rows[0][0]
    return descripcion

def obtener_capitulos(id_asignatura):
    """Función para obtener los capítulos de una asignatura."""
    capitulos = {}
    CURSOR.execute("SELECT DISTINCT capitulos FROM contenido WHERE id_silabo = '" +
                   id_asignatura + "'")
    for row in CURSOR:
        capitulos[row[0]] = []
    return capitulos

def obtener_subcapitulos(id_asignatura, capitulo):
    """Función para obtener los subcapítulos de una asignatura."""
    subcapitulos = []
    CURSOR.execute("SELECT DISTINCT subcapitulos FROM contenido WHERE id_silabo = '" +
                   id_asignatura + "' and capitulos = '" + capitulo + "'")
    for row in CURSOR:
        subcapitulos.append(row[0])
    return subcapitulos

def preprocesamiento(texto):
    """Función para realizar el preprocesamiento de un texto."""
    texto_normalize = normalization(texto)
    texto_tokenize = tweet_tokenization(texto_normalize)
    texto_stopping = stopping(texto_tokenize)
    texto_stemming = snowball_stemming(texto_stopping)
    return texto_stemming

def calculo_similitud_capitulos(asignatura1, asignatura2):
    """Función para calcular la similitud entre los capítulos de dos asignaturas."""
    similitud_capitulos = {}
    porcentaje_similitud = 0
    longitud = len(asignatura1)
    for cap_asignatura1 in asignatura1:
        for cap_asignatura2 in asignatura2:
            pro_asignatura1 = preprocesamiento(cap_asignatura1)
            pro_asignatura2 = preprocesamiento(cap_asignatura2)
            similitud = dices_similarity(pro_asignatura1, pro_asignatura2)
            if cap_asignatura1 in similitud_capitulos:
                temp = similitud_capitulos[cap_asignatura1][0]
                if similitud >= temp:
                    similitud_capitulos[cap_asignatura1] = [similitud, \
                                                            cap_asignatura2]
            else:
                similitud_capitulos[cap_asignatura1] = [similitud, \
                                                        cap_asignatura2]
        porcentaje_similitud += similitud_capitulos[cap_asignatura1][0]
    return [porcentaje_similitud / longitud, similitud_capitulos]

def calculo_similitud_subcapitulos(asignatura1, asignatura2):
    """Función para calcular la similitud entre los subcapítulos de dos asignaturas."""
    similitud_subcapitulos = {}
    porcentaje_similitud = 0
    longitud = len(asignatura1)
    for subcap_asignatura1 in asignatura1:
        for subcap_asignatura2 in asignatura2:
            pro_asignatura1 = preprocesamiento(subcap_asignatura1)
            pro_asignatura2 = preprocesamiento(subcap_asignatura2)
            similitud = dices_similarity(pro_asignatura1, pro_asignatura2)
            if subcap_asignatura1 in similitud_subcapitulos:
                temp = similitud_subcapitulos[subcap_asignatura1]
                if similitud >= temp:
                    similitud_subcapitulos[subcap_asignatura1] = similitud
            else:
                similitud_subcapitulos[subcap_asignatura1] = similitud
        porcentaje_similitud += similitud_subcapitulos[subcap_asignatura1]
    return porcentaje_similitud/longitud

def extraccion_textos():
    """Función para extraer los textos de cada asignatura."""
    global NOMBRE_ASIGNATURA1, NOMBRE_ASIGNATURA2
    global DESCRIPCION_ASIGNATURA1, DESCRIPCION_ASIGNATURA2
    global CAPITULOS_ASIGNATURA1, CAPITULOS_ASIGNATURA2

    NOMBRE_ASIGNATURA1 = obtener_nombre(ID_ASIGNATURA1)
    NOMBRE_ASIGNATURA2 = obtener_nombre(ID_ASIGNATURA2)

    DESCRIPCION_ASIGNATURA1 = obtener_descripcion(ID_ASIGNATURA1)
    DESCRIPCION_ASIGNATURA2 = obtener_descripcion(ID_ASIGNATURA2)

    CAPITULOS_ASIGNATURA1 = obtener_capitulos(ID_ASIGNATURA1)
    CAPITULOS_ASIGNATURA2 = obtener_capitulos(ID_ASIGNATURA2)

def preprocesamiento_textos():
    """Función para el preprocesamiento de textos."""
    global TEXTO1_STEMMING, TEXTO2_STEMMING
    TEXTO1_STEMMING = preprocesamiento(DESCRIPCION_ASIGNATURA1)
    TEXTO2_STEMMING = preprocesamiento(DESCRIPCION_ASIGNATURA2)

def main():
    """Función principal del script"""
    contador = 0
    porcentaje_similitud = 0.0
    similitud_subcapitulos = 0.0

    print("\nLa descripción de la Asignatura '" + NOMBRE_ASIGNATURA1 +
          "' es: " + DESCRIPCION_ASIGNATURA1 + "\n")
    print("La descripción de la Asignatura '" + NOMBRE_ASIGNATURA2 + "' es: " +
          DESCRIPCION_ASIGNATURA2 + "\n")
    print("La similitud de las asignaturas se presenta a continuación:")

    similitud_descripciones = dices_similarity(TEXTO1_STEMMING,
                                               TEXTO2_STEMMING)
    print("El porcentaje similitud de las descripciones es: " +
          str(round(similitud_descripciones*100, 2)) + "%")

    for key in CAPITULOS_ASIGNATURA1:
        CAPITULOS_ASIGNATURA1[key] = obtener_subcapitulos(ID_ASIGNATURA1, key)
    for key in CAPITULOS_ASIGNATURA2:
        CAPITULOS_ASIGNATURA2[key] = obtener_subcapitulos(ID_ASIGNATURA2, key)

    [porcentaje_similitud_capitulos, similitud_capitulos] = \
    calculo_similitud_capitulos(CAPITULOS_ASIGNATURA1.keys(), \
                                CAPITULOS_ASIGNATURA2.keys())
    print("El porcentaje similitud de los capítulos es: " +
          str(round(porcentaje_similitud_capitulos * 100, 2)) + "%")

    for key in similitud_capitulos:
        if similitud_capitulos[key][0] > 0.0:
            porcentaje_similitud += \
            calculo_similitud_subcapitulos(CAPITULOS_ASIGNATURA1[key],\
            CAPITULOS_ASIGNATURA2[similitud_capitulos[key][1]])
            contador += 1
    if contador > 0:
        similitud_subcapitulos = porcentaje_similitud/contador
    else:
        similitud_subcapitulos = 0.0
    print("El porcentaje similitud de los temas es: " +
          str(round(similitud_subcapitulos * 100, 2)) + "%")

    porcentaje_similitud_total = (similitud_descripciones) * \
                                  float(1/5) + (porcentaje_similitud_capitulos \
                                  + similitud_subcapitulos) * \
                                  float(2/5)
    print("El porcentaje similitud total de las asignaturas es: " +
          str(round(porcentaje_similitud_total * 100, 2)) + '%\n')
    return str(round(porcentaje_similitud_total * 100, 2))
#--------------------------- Extracción de los Textos --------------------------
#extraccion_textos()

def get_value():
    return main()
#----------------------- Preprocesamiento de los Textos ------------------------
preprocesamiento_textos()

#------------------------- Ejecución de los Algoritmos -------------------------
if __name__ == '__main__':
    main()
