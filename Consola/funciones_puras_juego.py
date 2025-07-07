def criterio_dificultad(pregunta: dict, dificultad_actual: str, preguntas_elegidas: set) -> bool:
    """Se encarga de definir un criterio para filtrar preguntas por dificultad que no hayan sido usadas

    Args:
        pregunta (dict): Es el diccionario de la pregunta
        dificultad_actual (str): Cadena que indica la dificultad por la cuál se van a filtrar las preguntas
        preguntas_elegidas (set): Set de preguntas que ya fueron elegidas

    Returns:
        bool: Devuelve False si la pregunta no cumple el criteiro de dificultad, True si lo hace.
    """
    dificultad = pregunta["Categoria/Dificultad"][1]
    cumple_criterio = False
    if dificultad == dificultad_actual and pregunta["Pregunta"] not in preguntas_elegidas:
        cumple_criterio = True
    return cumple_criterio

def determinar_premio_mayor(puntuacion: int) -> str:
    """Determina cuando se gana o no el premio mayor

    Args:
        puntuacion (int): Puntuación actual del jugador

    Returns:
        str: Devuelve si se ganó o no
    """
    premio_mayor = "No"
    if puntuacion == 1000:
        premio_mayor = "Si"
    return premio_mayor

def determinar_tiempo_promedio(tiempo_total: float, cantidad_rondas: int) -> float:
    """Determina el tiempo promedio en responder las preguntas durante la partida

    Args:
        tiempo_total (float): El tiempo total que transcurre durante la partida
        cantidad_rondas (int): Las rondas jugadas por el jugador

    Returns:
        float: Devuelve el tiempo promedio
    """
    tiempo_promedio = 0
    if cantidad_rondas > 0:
        tiempo_promedio = tiempo_total / cantidad_rondas
    return tiempo_promedio

def determinar_mejor_tiempo(puntuacion: int, tiempo_total: float):
    """Determina el mejor tiempo en terminar el juego

    Args:
        puntuacion (int): Puntuación actual del jugador
        tiempo_total (float): Tiempo total que le tomó al jugador ganar

    Returns:
        float: Devuelve el mejor tiempo en terminar el juego
    """
    mejor_tiempo = float("inf")
    if puntuacion == 1000:
        mejor_tiempo = tiempo_total
    return mejor_tiempo

def verificar_respuesta (respuesta: str, pregunta_elegida: dict) -> bool:
    """Se encarga de verificar si la respuesta ingresada es correcta o no

    Args:
        respuesta (str): Es la respuesta ingresada por el usuario
        pregunta_elegida (dict): Es el diccionario de la pregunta

    Returns:
        bool: Devuelve True en caso de que la respuesta sea correcta, devuelve False en caso de que no lo sea
    """
    respuesta_correcta = False
    if respuesta.lower() == pregunta_elegida ["Respuesta"].lower():
        respuesta_correcta = True
    return respuesta_correcta