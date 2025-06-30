from funciones_juego import *
from funciones_archivos import cargar_preguntas, cargar_configuracion

lista_preguntas = cargar_preguntas("preguntas.csv")
config = cargar_configuracion("config.json")
jugar(lista_preguntas, config, "estadisticas.csv")