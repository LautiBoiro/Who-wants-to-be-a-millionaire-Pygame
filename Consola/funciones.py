import random

pregunta_1 = {
    "Pregunta": "¿Cuántos dedos en total tiene un ser humano?",
    "Opciones": ["A. 2", "B. 8", "C. 20", "D. 25"],
    "Respuesta": "C",
    "Descripcion": "Un ser humano normalmente tiene 20 dedos en total: 10 en las manos y 10 en los pies.",
    "Categoria/Dificultad": ("General", "Facil")
}

pregunta_2 = {
    "Pregunta": "¿Quién fue el ganador de la Copa Libertadores 2020?",
    "Opciones": ["A. Flamengo", "B. Botafogo", "C. San Lorenzo", "D. Palmeiras"],
    "Respuesta": "D",
    "Descripcion": "Palmeiras ganó la Copa Libertadores 2020 tras vencer a Santos en la final.",
    "Categoria/Dificultad": ("Deportes", "Dificil")
}

pregunta_3 = {
    "Pregunta": "¿Cuál es el río más largo del mundo?",
    "Opciones": ["A. Amazonas", "B. Nilo", "C. Yangtsé", "D. Misisipi"],
    "Respuesta": "A",
    "Descripcion": "El Amazonas es considerado el río más largo del mundo, ubicado en América del Sur.",
    "Categoria/Dificultad": ("Geografía", "Facil")
}

pregunta_4 = {
    "Pregunta": "¿Qué elemento químico tiene el símbolo 'O'?",
    "Opciones": ["A. Oro", "B. Osmio", "C. Oxígeno", "D. Óxido"],
    "Respuesta": "C",
    "Descripcion": "El símbolo 'O' corresponde al oxígeno, un elemento esencial para la respiración.",
    "Categoria/Dificultad": ("Ciencia", "Medio")
}

pregunta_5 = {
    "Pregunta": "¿En qué país se encuentra la Torre Eiffel?",
    "Opciones": ["A. Italia", "B. Francia", "C. España", "D. Alemania"],
    "Respuesta": "B",
    "Descripcion": "La Torre Eiffel es un ícono de Francia, ubicada en su capital, París.",
    "Categoria/Dificultad": ("Geografía", "Medio")
}

pregunta_6 = {
    "Pregunta": "¿Qué planeta es conocido como el planeta rojo?",
    "Opciones": ["A. Venus", "B. Júpiter", "C. Marte", "D. Saturno"],
    "Respuesta": "C",
    "Descripcion": "Marte es conocido como el planeta rojo por el óxido de hierro en su superficie.",
    "Categoria/Dificultad": ("Ciencia", "Dificil")
}

pregunta_7 = {
    "Pregunta": "¿Cuántos minutos tiene una hora?",
    "Opciones": ["A. 60", "B. 100", "C. 30", "D. 120"],
    "Respuesta": "A",
    "Descripcion": "Una hora tiene 60 minutos, según el sistema de medición del tiempo estándar.",
    "Categoria/Dificultad": ("General", "Facil")
}


lista_preguntas = [pregunta_1, pregunta_2, pregunta_3, pregunta_4, 
                   pregunta_5, pregunta_6, pregunta_7]

def elegir_pregunta (lista_preguntas: list) -> dict | str:
    """Se encarga de elegir aleatoriamente una pregunta en la lista de diccionarios

    Args:
        lista_preguntas (list): Es la lista que contiene los diccionarios de cada pregunta

    Returns:
        dict | str: Devuelve el diccionario de la pregunta elegida y la key "Pregunta".
    """
    pregunta_elegida = random.choice(lista_preguntas)
    key_pregunta = pregunta_elegida["Pregunta"]
    return pregunta_elegida, key_pregunta

def mostrar_pregunta (key_pregunta: str):
    """Se encarga de mostrar la pregunta de la key "Pregunta"

    Args:
        key_pregunta (str): Es la cadena que contiene la pregunta
    """
    print (f"{key_pregunta}\n")

def mostrar_turno (pregunta_elegida: dict, ronda: int):
    """Se encarga de mostrar la ronda actual, categoría de la pregunta, dificultad y sus opciones

    Args:
        pregunta_elegida (dict): Es el diccionario de la pregunta elegida
        ronda (int): Ronda actual
    """
    categoria, dificultad = pregunta_elegida["Categoria/Dificultad"]
    print (f"Ronda: {ronda}")
    print (f"Categoría: {categoria} | Dificultad: {dificultad}")
    mostrar_pregunta(pregunta_elegida["Pregunta"])
    mostrar_opciones(pregunta_elegida)

def mostrar_opciones(pregunta_elegida: dict):
    """Se encarga de mostrar las opciones de la key "Opciones"

    Args:
        pregunta_elegida (dict): Es el diccionario de la pregunta
    """
    for opcion in pregunta_elegida["Opciones"]:
        print (opcion)
   
def verificar_respuesta (respuesta: str, pregunta_elegida: dict) -> bool:
    """Se encarga de verificar si la respuesta ingresada es correcta o no

    Args:
        respuesta (str): Es la respuesta ingresada por el usuario
        pregunta_elegida (dict): Es el diccionario de la pregunta

    Returns:
        bool: Devuelve True en caso de que la respuesta sea correcta, devuelve False en caso de que no lo sea
    """
    respuesta_correcta = False
    if respuesta == pregunta_elegida ["Respuesta"]:
        respuesta_correcta = True
    return respuesta_correcta

def verificar_puntuacion (ronda: int, puntuacion: int) -> int | str | None:
    """Se encarga de verificar cuánto puntaje corresponde y, en los casos correspondientes, le pregunta al usuario si quiere retirarse

    Args:
        ronda (int): Ronda actual del bucle
        puntuacion (int): Puntuación actual del jugador

    Returns:
        int | bool | None: Devuelve la puntuación actualizada. Si el usuario decidió retirarse devuelve un string, devuelve None si la función no pide retirarse.
    """
    retirar = None
    match ronda:
        case 3:
            puntuacion = 500
            print ("Alcanzaste los $500")
            retirar = pedir_retirarse()
        case 5:
            puntuacion = 750
            print ("Alcanzaste los $750")
            retirar = pedir_retirarse()
        case 7:
            puntuacion = 1000

    return puntuacion, retirar

def verificar_perdida (respuesta_correcta_o_no: bool) -> bool:
    """Verifica si la respuesta es correcta o no. Si no lo es, le pregunta al usuario si quiere reintentar.

    Args:
        respuesta_correcta_o_no (bool): Es True si la respuesta correcta, False en caso contrario.

    Returns:
        bool: Devuelve dos booleanos. Para perdida corresponde True solo si el usuario no quiere reiniciar, en caso contrario reiniciar será True. 
              Ambos son False si no se cumplen las condiciones
    """
    perdida = False
    reiniciar = False

    if respuesta_correcta_o_no == False:
        reintentar = input ("¿Desea reintentar? Si/No: ")
        if reintentar == "No":
            perdida = True
        elif reintentar == "Si":
            print ("El juego se reiniciará...")
            reiniciar = True
    return perdida, reiniciar

def pedir_retirarse () -> str:
    """La función le pregunta al usuario si quiere retirarse con su premio acumulado

    Returns:
        str: Respuesta del usuario (Si/No)
    """
    retirar = input ("Te gustaría retirarte con tu premio acumulado? Si/No: ")
    return retirar

def filtrar_pregunta_dificultad (dificultad_actual: str, estado_juego: dict, lista_preguntas: list) -> list:
    """Filtra las preguntas por dificultad específica, creando una lista

    Args:
        dificultad_actual (str): Dificultad que va a tener cada pregunta
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        lista_preguntas (list): Lista que contiene los diccionarios

    Returns:
        list: Retorna la lista de preguntas filtrada por dificultad
    """
    preguntas_filtradas = [
        pregunta for pregunta in lista_preguntas
        if pregunta["Categoria/Dificultad"][1] == dificultad_actual and
        pregunta["Pregunta"] not in estado_juego["Preguntas_elegidas"]
    ]
    return preguntas_filtradas

def elegir_pregunta_filtrada (estado_juego: dict, preguntas_filtradas: list) -> dict:
    """Se encarga de elegir una pregunta previamente filtrada

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        preguntas_filtradas (list): Es una lista filtrada previamente

    Returns:
        dict: Es el diccionario de la pregunta seleccionada
    """
    pregunta = random.choice(preguntas_filtradas)
    estado_juego["Preguntas_elegidas"].add(pregunta["Pregunta"])
    estado_juego["Rondas"] += 1
    return pregunta


def crear_y_verificar_nueva_pregunta(estado_juego: dict, lista_preguntas: list) -> dict:
    """Elige una pregunta y la verifica. Si es correcta se retorna.

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        lista_preguntas (list): Lista que contiene los diccionarios

    Returns:
        dict: Es el diccionario de la pregunta seleccionada
    """
    dificultad_actual = obtener_dificultad_por_ronda(estado_juego["Rondas"] + 1)

    preguntas_filtradas = filtrar_pregunta_dificultad (dificultad_actual, estado_juego, lista_preguntas)

    pregunta = elegir_pregunta_filtrada(estado_juego, preguntas_filtradas)
    return pregunta

def preguntar_y_responder (estado_juego: dict, lista_preguntas: list) -> bool | dict:
    """Maneja la secuencia de pregunta y respuesta del juego

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        lista_preguntas (list): Lista que contiene los diccionarios de preguntas

    Returns:
        bool | dict: Devuelve un booleano y un diccionario. La respuesta correcta es True o False dependiendo la verificación. El diccionario corresponde a la pregunta elegida.
    """
    pregunta = crear_y_verificar_nueva_pregunta (estado_juego, lista_preguntas)
    mostrar_turno(pregunta, estado_juego["Rondas"])
    respuesta_jugador = input ("¿Cuál es su respuesta?: ")
    respuesta_correcta_o_no = verificar_respuesta(respuesta_jugador, pregunta)
    return respuesta_correcta_o_no, pregunta

def procesar_respuesta_correcta (bandera_continuar: bool, estado_juego: dict, pregunta: dict) -> bool:
    """Se encarga de procesar y mostrar los datos si la respuesta es correcta

    Args:
        bandera_continuar (bool): Es la bandera que determina si el bucle debe seguir o cortarse
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        pregunta (dict): Es el diccionario de la pregunta seleccionada

    Returns:
        bool: Retorna la bandera continuar previamente parametrizada. Se devuelve como False si el usuario decidió retirarse.
    """
    print ("¡Respuesta correcta!")
    print (pregunta["Descripcion"])
    estado_juego ["Puntuacion"], retirar = verificar_puntuacion(estado_juego["Rondas"], estado_juego["Puntuacion"])
    if retirar == "Si":
        bandera_continuar = False
    return bandera_continuar

def procesar_respuesta_incorrecta(bandera_continuar: bool, estado_juego: dict) -> bool:
    """Se encarga de procesar los datos si la respuesta es incorrecta

    Args:
        bandera_continuar (bool): Es la bandera que determina si el ciclo debe seguir o cortarse
        estado_juego (dict): Diccionario que contiene los datos actuales del juego

    Returns:
        bool:  Retorna la bandera continuar previamente parametrizada. Se devuelve como False si la key "Perdida" es True.
    """
    if estado_juego["Perdida"]:
        bandera_continuar = False
    return bandera_continuar

def verificar_cantidad_rondas (bandera_continuar: bool, estado_juego: dict) -> bool:
    """Se encarga de verificar si se llegó a la ronda máxima

    Args:
        bandera_continuar (bool): Es la bandera que determina si el ciclo debe seguir o cortarse
        estado_juego (dict): Diccionario que contiene los datos actuales del juego

    Returns:
        bool: Retorna la bandera continuar previamente parametrizada. Se devuelve como False si se llegó a la ronda máxima.
    """
    if estado_juego["Rondas"] == 7:
        bandera_continuar = False
    return bandera_continuar

def obtener_dificultad_por_ronda(ronda: int) -> str:
    """Se encarga de obtener la dificultad de la ronda actual

    Args:
        ronda (int): Ronda actual

    Returns:
        str: Retorna la dificultad de la ronda correspondiente ("Facil", "Medio" o "Dificil")
    """
    dificultad = None
    if ronda <= 3:
        dificultad = "Facil"
    elif ronda <= 5:
        dificultad = "Medio"
    else:
        dificultad = "Dificil"
    return dificultad

def inicializar_juego () -> dict:
    """Inicializa el juego creando un diccionario con los datos principales

    Returns:
        dict: Se retorna el diccionario creado con sus keys correspondientes
    """
    estado_juego = {
        "Rondas" : 0,
        "Puntuacion" : 0,
        "Preguntas_elegidas" : set(),
        "Perdida" : False
    }
    return estado_juego

def jugar_ronda (estado_juego: dict, lista_preguntas: list) -> bool:
    """Controla el juego normal de una ronda

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        lista_preguntas (list): Lista que contiene los diccionarios de preguntas

    Returns:
        bool: Devuelve dos booleanos. La bandera para continuar jugando y la key "Reiniciar" del dicicionario que contiene los datos del juego
    """
    bandera_continuar_jugando = True
    respuesta_correcta_o_no, pregunta = preguntar_y_responder(estado_juego, lista_preguntas)
    if respuesta_correcta_o_no:
        bandera_continuar_jugando = procesar_respuesta_correcta(bandera_continuar_jugando, estado_juego, pregunta)

    estado_juego["Perdida"], estado_juego["Reiniciar"] = verificar_perdida(respuesta_correcta_o_no)
    bandera_continuar_jugando = procesar_respuesta_incorrecta(bandera_continuar_jugando, estado_juego)

    bandera_continuar_jugando = verificar_cantidad_rondas(bandera_continuar_jugando, estado_juego)

    return bandera_continuar_jugando, estado_juego["Reiniciar"]


def inicializar_bucle_del_juego(estado_juego: dict, lista_preguntas: list) -> bool:
    """Inicializa y controla el bucle principal del juego

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        lista_preguntas (list): Lista que contiene los diccionarios de preguntas

    Returns:
        bool: Se retorna la variable reiniciar
    """
    seguir = True
    reiniciar = False
    while seguir:
        seguir, reiniciar = jugar_ronda(estado_juego, lista_preguntas)
        if reiniciar:
            break
    return reiniciar

def finalizar_juego(estado: dict):
    """Muestra los datos al finalizar el juego

    Args:
        estado (dict): Diccionario que contiene los datos actuales del juego
    """
    if estado["Perdida"]:
        print("Ha finalizado el juego. Mejor suerte la próxima.")

    elif estado["Rondas"] < 7:
        print (f"Has retirado tu premio de ${estado["Puntuacion"]} ¡Felicidades!")
    
    else:
        print (f"¡Felicidades!¡Ganaste el premio mayor de ${estado["Puntuacion"]}!")


def jugar ():
    """Función principal que controla el juego
    """
    reiniciar = True
    while reiniciar:
        estado_del_juego = inicializar_juego()
        reiniciar = inicializar_bucle_del_juego(estado_del_juego, lista_preguntas)
        if not reiniciar:
            finalizar_juego(estado_del_juego)