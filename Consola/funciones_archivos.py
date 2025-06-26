from funciones_juego import *
import re
import json

def escribir_preguntas(lista_preguntas: list, path: str):
    with open(path, "w", encoding = "utf-8") as archivo_preguntas:
        for pregunta in lista_preguntas:
            opciones_str = "|".join(pregunta["Opciones"]) #Paso la lista a un solo string
            categoria = pregunta["Categoria/Dificultad"] [0] #La categoría se separa de la tupla
            dificultad = pregunta["Categoria/Dificultad"] [1] #La dificultad se separa de la tupla
            linea = (
            f"{pregunta["Pregunta"]};"
            f"{opciones_str};"
            f"{pregunta["Respuesta"]};"
            f"{categoria}|{dificultad};"
            f"{pregunta["Descripcion"]}\n"
            )
            archivo_preguntas.write(linea)

def cargar_preguntas(path: str):
    lista_preguntas = []
    with open(path, "r", encoding = "utf-8",) as archivo_preguntas:
        for linea in archivo_preguntas:
            registro = re.split(";|\n", linea.strip()) #Le saco los espacios para que no tome \n de ["Descripción"]
            opciones = registro[1].split("|") #Vuelvo a convertirlo en una lista
            categoria, dificultad = registro[3].split("|") #Las separamos para despues convertirlo a tupla
            pregunta = {
                "Pregunta": registro[0],
                "Opciones": opciones,
                "Respuesta": registro[2],
                "Categoria/Dificultad": (categoria, dificultad),
                "Descripcion": registro[4]
            }
            lista_preguntas.append(pregunta)
    return lista_preguntas

def escribir_configuracion(config: dict, path: str):
    with open(path, "w", encoding = "utf-8") as archivo_configuracion:
        json.dump(config, archivo_configuracion, indent = 4, ensure_ascii = False)

def cargar_configuracion(path: str) -> dict:
    with open(path,"r", encoding = "utf-8") as archivo_configuracion:
        archivo_cargado = json.load(archivo_configuracion)
        return archivo_cargado
