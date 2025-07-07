import re

def formatear_pregunta_csv(pregunta: dict) -> str:
    """Formatea una linea un diccionario de pregunta a una línea de csv

    Args:
        pregunta (dict): Diccionario que contiene los datos de la pregunta

    Returns:
        str: Línea ya formateada que se escribirá en el csv
    """
    opciones_str = "|".join(pregunta["Opciones"]) #Paso la lista a un solo string
    categoria, dificultad = pregunta["Categoria/Dificultad"] #Se separa categoría y dificultad de la tupla
    linea = (#usar un solo f string, implementar try except
    f"{pregunta["Pregunta"]};{opciones_str};{pregunta["Respuesta"]};{categoria}|{dificultad};{pregunta["Descripcion"]}\n"
     )
    return linea

def formatear_estadistica_csv(estadistica: dict) -> str:
    """Formatea un diccionario de estadística a una línea de csv

    Args:
        estadistica (dict): Diccionario que contiene los datos de la estadística

    Returns:
        str: Línea ya formateada que se escribirá en el csv
    """
    mejor_tiempo = estadistica["Mejor_tiempo"]
    if mejor_tiempo == float("inf"):
        mejor_tiempo = "--"
    linea = (
        f"{estadistica['Usuario']};{estadistica['Rondas_jugadas']};{estadistica['Preguntas_acertadas']};{estadistica['Tiempo_promedio']};{estadistica['Contador_partidas_ganadas']};{mejor_tiempo}\n"
    )
    return linea

def leer_linea_pregunta(linea: str) -> dict | None:
    """Lee una línea de pregunta formateada en csv y la transforma a un diccionario

    Args:
        linea (str): Linea previamente formateada a csv

    Returns:
        dict: Diccionario con los datos de la pregunta
        None: Se encontró un error al momento de leer y transformar los datos
    """
    try: 
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
    except (IndexError, ValueError):
        pregunta = None
    return pregunta

def leer_linea_estadisticas(linea: str) -> dict | None:
    """Lee una línea de estadística formateada en csv y la transforma a un diccionario

    Args:
        linea (str): Linea previamente formateada a csv

    Returns:
        dict: Diccionario con los datos de la estadística
        None: Se encontró un error al momento de leer y transformar los datos
    """
    try:
        llave = linea.split(";")
        if llave[5] == "--":
            mejor_tiempo = float("inf")
        else:
            mejor_tiempo = float(llave[5])
        estadistica = {
            "Usuario": llave[0],
            "Rondas_jugadas": int(llave[1]),
            "Preguntas_acertadas": int(llave[2]),
            "Tiempo_promedio": float(llave[3]),
            "Contador_partidas_ganadas": int(llave[4]),
            "Mejor_tiempo": mejor_tiempo
            }
    except (IndexError, ValueError):
        estadistica = None
    return estadistica