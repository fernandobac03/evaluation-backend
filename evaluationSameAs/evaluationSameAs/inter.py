
import json
from flask import jsonify
from evaluationSameAs.evaluationSameAs.transaccionesBD import datos_insertar, datos_consultar, datos_insertar_evaluacion
#from comparingtext.comparingtext.calculo_similitud_asignatura import get_value


def insert_person(jsondata):
    return datos_insertar(get_escuela(jsondata), get_edad(jsondata), get_genero(jsondata))


def get_pairs_data(param):
    return datos_consultar(param)

def insert_evaluation(jsondata):
    return datos_insertar_evaluacion(str(jsondata['evaluacion']), str(jsondata['id_persona']), str(jsondata['id_par']))


#recuperarndo escuela
def get_escuela(jsondata):
    escuela = str(jsondata['escuela'])
    return escuela

#recuperando edad
def get_edad(jsondata):
    edad = str(jsondata['edad'])
    return edad

#recuperando género de la persona
def get_genero(jsondata):
    genero = str(jsondata['genero'])
    return genero





#recuperando descripcion del titulo
def get_description(jsondata, silabo_id):
    description = str(jsondata[silabo_id]['description'])
    return description


def get_direct_results():
    return jsonify({'similarity': "No hay resultado, bloqueado el código en get_direct_results() en inter.py, servicio: comparingtext"})


def get_full_similarity(jsondata):
 #   return jsonify({'key': 'similarity', 'value': detecting_similarity(get_title(jsondata, 0), get_description(jsondata, 0), get_academic_unit(jsondata, 0), get_results(jsondata, 0), get_objectives(jsondata, 0), get_title(jsondata, 1),  get_description(jsondata, 1), get_chapters(jsondata, 0), get_chapters(jsondata, 1))})
    
    if len(jsondata)>2:
        if jsondata[2]: #viene json de pesos, 
            #verificar que cumpla 100%
            return null
    else:
        
        return jsonify({'key': 'similarity', 'value': detecting_similarity(jsondata[0], jsondata[1], get_default_weight())})


def get_default_weight():
    return {"name": "5", "description": "20", "content": "50", "objectives": "15", "results": "10", "unit": "0"}


#recuperando titulo del silabo
def get_title(jsondata, silabo_id):
    title = str(jsondata[silabo_id]['title'])
    return title 

#recuperando descripcion del titulo
def get_description(jsondata, silabo_id):
    description = str(jsondata[silabo_id]['description'])
    return description


#recuperando Unidad Academica como lista
def get_academic_unit(jsondata, silabo_id):
    unidad_academica = str(jsondata[silabo_id]['unit'])
    return unidad_academica 
  


#recuperando resultados como lista
def get_results(jsondata, silabo_id):
    results = []  
    for result in jsondata[silabo_id]['results']:
        results.append(result) 
    return results
  


#recuperando objetivos como lista
def get_objectives(jsondata, silabo_id):
    objectives = []  
    for obj in jsondata[silabo_id]['objectives']:
        objectives.append(obj) 
    return objectives
  

#recuperando capitulos y subcapitulos como lista
def get_chapters(jsondata, silabo_id):
    chapters = []  
    for chapter in jsondata[silabo_id]['content']:
        chapters.append(chapter) 
    return chapters

