import random
import time

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

pregunta_8 = {
    "Pregunta": "¿Cuál es la capital de Australia?",
    "Opciones": ["A. Sydney", "B. Melbourne", "C. Canberra", "D. Brisbane"],
    "Respuesta": "C",
    "Descripcion": "Canberra es la capital de Australia desde 1913.",
    "Categoria/Dificultad": ("Geografía", "Medio")
}

pregunta_9 = {
    "Pregunta": "¿Quién escribió 'Cien años de soledad'?",
    "Opciones": ["A. Mario Vargas Llosa", "B. Gabriel García Márquez", "C. Pablo Neruda", "D. Isabel Allende"],
    "Respuesta": "B",
    "Descripcion": "Gabriel García Márquez, escritor colombiano, autor de esta famosa novela.",
    "Categoria/Dificultad": ("Literatura", "Facil")
}

pregunta_10 = {
    "Pregunta": "¿Qué velocidad tiene la luz en el vacío?",
    "Opciones": ["A. 300,000 km/s", "B. 150,000 km/s", "C. 3,000 km/s", "D. 30,000 km/s"],
    "Respuesta": "A",
    "Descripcion": "La velocidad de la luz en el vacío es aproximadamente 300,000 kilómetros por segundo.",
    "Categoria/Dificultad": ("Ciencia", "Dificil")
}

pregunta_11 = {
    "Pregunta": "¿Cuál es el metal más ligero?",
    "Opciones": ["A. Aluminio", "B. Litio", "C. Magnesio", "D. Titanio"],
    "Respuesta": "B",
    "Descripcion": "El litio es el metal más ligero y es usado en baterías recargables.",
    "Categoria/Dificultad": ("Ciencia", "Medio")
}

pregunta_12 = {
    "Pregunta": "¿En qué año comenzó la Primera Guerra Mundial?",
    "Opciones": ["A. 1912", "B. 1914", "C. 1918", "D. 1939"],
    "Respuesta": "B",
    "Descripcion": "La Primera Guerra Mundial comenzó en 1914 y terminó en 1918.",
    "Categoria/Dificultad": ("Historia", "Facil")
}

pregunta_13 = {
    "Pregunta": "¿Cuál es el país con mayor número de idiomas oficiales?",
    "Opciones": ["A. Sudáfrica", "B. India", "C. Bolivia", "D. Suiza"],
    "Respuesta": "A",
    "Descripcion": "Sudáfrica tiene 11 idiomas oficiales reconocidos.",
    "Categoria/Dificultad": ("General", "Medio")
}

pregunta_14 = {
    "Pregunta": "¿Qué instrumento mide la presión atmosférica?",
    "Opciones": ["A. Barómetro", "B. Termómetro", "C. Anemómetro", "D. Higrómetro"],
    "Respuesta": "A",
    "Descripcion": "El barómetro es el instrumento utilizado para medir la presión atmosférica.",
    "Categoria/Dificultad": ("Ciencia", "Facil")
}

respuestas_validas_si_o_no = ["si", "sí", "no"]
respuestas_validas_opciones = ["a", "b", "c", "d"]

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
    if respuesta.lower() == pregunta_elegida ["Respuesta"].lower():
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
        reintentar = pedir_confirmacion("¿Desea reintentar? Si/No: ", "Respuesta inválida. Ingrese Si o No", respuestas_validas_si_o_no)
        if reintentar == "no":
            perdida = True
        elif reintentar == "si" or reintentar == "sí":
            print ("El juego se reiniciará...")
            reiniciar = True
    return perdida, reiniciar

def pedir_retirarse () -> str:
    """La función le pregunta al usuario si quiere retirarse con su premio acumulado

    Returns:
        str: Respuesta del usuario (Si/No)
    """
    retirar = pedir_confirmacion ("Te gustaría retirarte con tu premio acumulado? Si/No: ", "Respuesta inválida. Ingrese Si o No", respuestas_validas_si_o_no)
    return retirar

def pedir_confirmacion(mensaje: str, mensaje_error: str, lista_respuestas_validas: list, tiempo_limite: int = None) -> str | None:
    """Valida la respuesta del usuario. Opcionalmente puede usar un tiempo límite.

    Args:
        mensaje (str): Mensaje que se va a mostrar al usuario al pedir la respuesta

        mensaje_error (str): Mensaje que se muestra en caso de que el usuario ingrese una respuesta inválida

        lista_respuestas_validas (str): Es la lista que contiene las respuestas válidas que debe ingreesar el usuario

    Returns:
        str: Devuelve la respuesta validada
        None: Si se terminó el tiempo
    """
    bandera_while = True
    respuesta = None
    tiempo_inicio = time.time()

    while bandera_while:
        if tiempo_limite is not None and time.time() - tiempo_inicio > tiempo_limite:
            print("¡Se acabó el tiempo!")
            respuesta = None #Siempre que se termine el tiempo retorna None
            bandera_while = False

        else:
            respuesta = input(mensaje).strip().lower()
            for i in range(len(lista_respuestas_validas)):
                if respuesta == lista_respuestas_validas[i]:
                    bandera_while = False
                    break
            if bandera_while:
                print(mensaje_error)
    return respuesta

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
    respuesta_jugador = pedir_confirmacion("¿Cuál es su respuesta?: ", "Respuesta inválida. Ingrese A, B, C, o D", respuestas_validas_opciones)
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
    if retirar == "si" or retirar == "sí":
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

def inicializar_juego (cantidad_preguntas: int) -> dict:
    """Inicializa el juego creando un diccionario con los datos principales

    Returns:
        dict: Se retorna el diccionario creado con sus keys correspondientes
    """
    estado_juego = {
        "Rondas" : 0,
        "Puntuacion" : 0,
        "Preguntas_elegidas" : set(),
        "Perdida" : False,
        "Maximo_rondas" : cantidad_preguntas
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


def jugar (lista_preguntas: list, config: dict):
    """Función principal que controla el juego
    """
    reiniciar = True
    while reiniciar:
        estado_del_juego = inicializar_juego(config["cantidad_preguntas"])
        reiniciar = inicializar_bucle_del_juego(estado_del_juego, lista_preguntas)
        if not reiniciar:
            finalizar_juego(estado_del_juego)