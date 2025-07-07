import random
import time
from funciones_genericas_archivos import *
from funciones_puras_juego import *
from funciones_genericas_juego import pedir_confirmacion, pedir_nombre, filtrar_preguntas
from interfaz import mostrar_turno, mostrar_resultado_final, mostrar_menu_dificultad, printear_con_transicion, clear_console


respuestas_validas_si_o_no = {"si", "sí", "no"}
respuestas_validas_opciones = {"a", "b", "c", "d"}

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
            printear_con_transicion ("Alcanzaste los $500")
            retirar =  pedir_confirmacion ("Te gustaría retirarte con tu premio acumulado? Si/No: ", "Respuesta inválida. Ingrese Si o No", respuestas_validas_si_o_no)
        case 5:
            puntuacion = 750
            printear_con_transicion ("Alcanzaste los $750")
            retirar =  pedir_confirmacion ("Te gustaría retirarte con tu premio acumulado? Si/No: ", "Respuesta inválida. Ingrese Si o No", respuestas_validas_si_o_no)
        case 7:
            puntuacion = 1000

    return puntuacion, retirar

def verificar_perdida (respuesta_correcta_o_no: bool, tiempo_agotado: bool) -> bool:
    """Verifica si la respuesta es correcta o no. Si no lo es, le pregunta al usuario si quiere reintentar.

    Args:
        respuesta_correcta_o_no (bool): Es True si la respuesta correcta, False en caso contrario.
        tiempo_agotado (bool): Es true si el usuario no respondió a tiempo, False en caso de que haya respondido.

    Returns:
        bool: Devuelve dos booleanos. Para perdida corresponde True solo si el usuario no quiere reiniciar, en caso contrario reiniciar será True. 
            Ambos son False si no se cumplen las condiciones
    """
    perdida = False
    reiniciar = False

    if respuesta_correcta_o_no == False:
        if not tiempo_agotado:
            printear_con_transicion("Respuesta incorrecta, has perdido")
        reintentar = pedir_confirmacion("¿Desea reintentar? Si/No: ", "Respuesta inválida. Ingrese Si o No", respuestas_validas_si_o_no)
        if reintentar == "no":
            perdida = True
        elif reintentar == "si" or reintentar == "sí":
            printear_con_transicion("El juego se reiniciará...")
            reiniciar = True
    return perdida, reiniciar


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
    dificultad_actual = estado_juego["Dificultades"][estado_juego["Rondas"]]

    preguntas_filtradas = filtrar_preguntas(lista_preguntas, criterio_dificultad, dificultad_actual, estado_juego["Preguntas_elegidas"])

    pregunta = elegir_pregunta_filtrada(estado_juego, preguntas_filtradas)
    return pregunta

def preguntar_y_responder(estado_juego: dict, lista_preguntas: list, tiempo_limite: int = None) -> bool | dict:
    """
    Ejecuta el proceso completo de mostrar la pregunta, pedir respuesta y verificarla.

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego.
        lista_preguntas (list): Lista con todas las preguntas disponibles.
        tiempo_limite (int, opcional): Tiempo límite para responder la pregunta.

    Returns:
        bool | dict: Booleano que indica si la respuesta fue correcta, y el diccionario de la pregunta.
    """
    pregunta = crear_y_verificar_nueva_pregunta(estado_juego, lista_preguntas)
    mostrar_turno(pregunta, estado_juego["Rondas"])
    
    respuesta_jugador = pedir_confirmacion(
        "¿Cuál es su respuesta?: ",
        "Respuesta inválida. Ingrese A, B, C, o D",
        respuestas_validas_opciones,
        tiempo_limite
    )
    
    if respuesta_jugador == "Sin tiempo":
        printear_con_transicion("⏰ Tiempo agotado, perdiste")
        estado_juego["Perdida"] = True
        estado_juego["Tiempo_agotado"] = True
        respuesta_correcta_o_no = False
    else:
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
    printear_con_transicion("¡Respuesta correcta!")
    printear_con_transicion(pregunta["Descripcion"])
    estado_juego["Preguntas_acertadas"] += 1
    time.sleep(2)
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
    if estado_juego["Rondas"] == estado_juego["Maximo_rondas"]:
        bandera_continuar = False
    return bandera_continuar

def guardar_estadistica_jugador(estado_juego: dict, path: str):
    lista_estadisticas = leer_estadisticas(path)
    nueva_estadistica = crear_estadistica_final(estado_juego, estado_juego["Usuario"])

    jugador_existente = False
    for estadistica in lista_estadisticas:
        if estadistica["Usuario"] == nueva_estadistica["Usuario"]:
            jugador_existente = True
            actualizar_estadistica_existente(estadistica, nueva_estadistica)
            break

    if not jugador_existente:
        agregar_nuevo_jugador(lista_estadisticas, nueva_estadistica)

    escribir_estadisticas(lista_estadisticas, path)

def actualizar_estadistica_existente(estadistica: dict, nueva: dict):
    """
    Actualiza una estadística existente con una nueva.

    Args:
        estadistica (dict): Estadística ya registrada.
        nueva (dict): Nueva estadística para actualizar los valores.
    """
    estadistica["Rondas_jugadas"] += nueva["Rondas_jugadas"]
    estadistica["Preguntas_acertadas"] += nueva["Preguntas_acertadas"]
    estadistica["Contador_partidas_ganadas"] += nueva["Contador_partidas_ganadas"]

    rondas_anteriores = estadistica["Rondas_jugadas"] - nueva["Rondas_jugadas"]
    tiempo_total_anterior = estadistica["Tiempo_promedio"] * rondas_anteriores
    tiempo_total_nuevo = nueva["Tiempo_promedio"] * nueva["Rondas_jugadas"]
    total_rondas = estadistica["Rondas_jugadas"]

    estadistica["Tiempo_promedio"] = round((tiempo_total_anterior + tiempo_total_nuevo) / total_rondas, 2)

    if nueva["Mejor_tiempo"] < estadistica["Mejor_tiempo"] and nueva["Mejor_tiempo"] > 0:
        estadistica["Mejor_tiempo"] = nueva["Mejor_tiempo"]


def agregar_nuevo_jugador(lista_estadisticas: list, nueva: dict):
    """
    Agrega una nueva estadística de jugador a la lista.

    Args:
        lista_estadisticas (list): Lista actual de estadísticas.
        nueva (dict): Nueva estadística a agregar.
    """
    lista_estadisticas.append(nueva)



def crear_estadistica_final(estado_juego: dict, nombre_jugador: str) -> dict:
    """Crea la estadistica final y devuelve estadistica

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        nombre_jugador (str): Nombre de usuario del jugador

    Returns:
        dict: Devuelve la estadistica
    """
    tiempo_total = estado_juego["Fin_tiempo_partida"] - estado_juego["Inicio_tiempo_partida"]
    tiempo_promedio = determinar_tiempo_promedio(tiempo_total, estado_juego["Rondas"])
    mejor_tiempo = determinar_mejor_tiempo(estado_juego["Puntuacion"], tiempo_total)
    premio_mayor = determinar_premio_mayor(estado_juego["Puntuacion"])

    estadistica = {
        "Usuario": nombre_jugador,
        "Rondas_jugadas": estado_juego["Rondas"],
        "Preguntas_acertadas": estado_juego["Preguntas_acertadas"],
        "Tiempo_promedio": round(tiempo_promedio, 2),
        "Contador_partidas_ganadas": int(premio_mayor == "Si"),
        "Mejor_tiempo": round(mejor_tiempo, 2)
    }
    return estadistica

def interpretar_opcion_dificultad(opcion: str) -> tuple[list[str], str]:
    """Interpreta la respuesta del usuario cuando se pide la dificultad

    Args:
        opcion (str): Respuesta elegida por el usuario

    Returns:
        tuple[list[str], str: Devuelve una tupla, el primer elemento es la lista que contiene la dificultad de cada ronda 
    """
    if opcion == "1":
        dificultad_preguntas_de_la_partida = ["Facil"] * 4 + ["Medio"] * 3
        modo = "facil"
    elif opcion == "2":
        dificultad_preguntas_de_la_partida = ["Facil"] * 3 + ["Medio"] * 2 + ["Dificil"] * 2
        modo = "normal"
    elif opcion == "3":
        dificultad_preguntas_de_la_partida = ["Medio"] * 4 + ["Dificil"] * 3
        modo = "dificil"
    elif opcion == "4":
        dificultad_preguntas_de_la_partida = ["Dificil"] * 7
        modo = "extremo"
    return dificultad_preguntas_de_la_partida, modo

def pedir_dificultad() -> list | str:
    """Se encarga de mostrar el menú de dificultades, toma la respuesta del usuario y la valida

    Returns:
        list: Devuelve la lista que contiene la dificultad de cada pregunta
        str: Modo de dificultad elegido por el jugador
    """
    mostrar_menu_dificultad()
    opcion = pedir_confirmacion(
        "Elija una dificultad (1-4): ",
        "❌ Opción inválida. Ingrese un número del 1 al 4.",
        set_respuestas_validas = {"1", "2", "3", "4"}
    )
    dificultad_preguntas_de_la_partida, modo = interpretar_opcion_dificultad(opcion)
    return dificultad_preguntas_de_la_partida, modo


def inicializar_juego (cantidad_preguntas: int) -> dict:
    """Inicializa el juego creando un diccionario con los datos principales

    Returns:
        dict: Se retorna el diccionario creado con sus keys correspondientes
    """
    estado_juego = {
        "Rondas": 0,
        "Puntuacion": 0,
        "Preguntas_elegidas": set(),
        "Perdida": False,
        "Maximo_rondas": cantidad_preguntas,
        "Preguntas_acertadas": 0,
        "Tiempo_total": 0.0,
        "Tiempo_promedio": 0.0,
        "Mejor_tiempo": float("inf"), #Se marca como infinito ya que debe ser un número mayor al tiempo del jugador
        "Reiniciar": False
    }
    return estado_juego

def jugar_ronda (estado_juego: dict, lista_preguntas: list, tiempo_limite: int) -> bool:
    """Controla el juego normal de una ronda

    Args:
        estado_juego (dict): Diccionario que contiene los datos actuales del juego
        lista_preguntas (list): Lista que contiene los diccionarios de preguntas

    Returns:
        bool: Devuelve dos booleanos. La bandera para continuar jugando y la key "Reiniciar" del dicicionario que contiene los datos del juego
    """
    bandera_continuar_jugando = True
    estado_juego["Tiempo_agotado"] = False
    respuesta_correcta_o_no, pregunta = preguntar_y_responder(estado_juego, lista_preguntas, tiempo_limite)

    if respuesta_correcta_o_no:
        bandera_continuar_jugando = procesar_respuesta_correcta(bandera_continuar_jugando, estado_juego, pregunta)

    estado_juego["Perdida"], estado_juego["Reiniciar"] = verificar_perdida(respuesta_correcta_o_no, estado_juego["Tiempo_agotado"])
    
    bandera_continuar_jugando = procesar_respuesta_incorrecta(bandera_continuar_jugando, estado_juego)

    bandera_continuar_jugando = verificar_cantidad_rondas(bandera_continuar_jugando, estado_juego)

    return bandera_continuar_jugando, estado_juego["Reiniciar"]

def inicializar_bucle_del_juego(estado_juego: dict, lista_preguntas: list, tiempo_limite: int) -> bool:
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
        clear_console()
        seguir, reiniciar = jugar_ronda(estado_juego, lista_preguntas, tiempo_limite)
        if reiniciar:
            break
        time.sleep(2)
    return reiniciar


def obtener_nombre_jugador(config: dict) -> str:
    """Se encarga de obtener el nombre del usuario

    Args:
        config (dict): Diccionario que contiene la configuración principal del juego

    Returns:
        str: Nombre de usuario validado
    """
    nombre = pedir_nombre(
        config["caracteres_maximo"],
        "Ingrese su nombre de usuario (máximo 14 carácteres): ",
        "Error detectado. Reingrese su nombre de usuario (máximo 14 carácteres): "
    )
    return nombre

def desarrollar_partida(nombre_jugador: str, dificultades_rondas: list, lista_preguntas: list, config: dict) -> dict | bool:
    """Función que controla el desarrollo de una partida

    Args:
        nombre_jugador (str): Nombre de usuario del jugador
        dificultades_rondas (list): Lista de dificultades que va a tener por ronda la partida
        lista_preguntas (list): Es la lista que contiene los diccionarios de cada pregunta 
        config (dict): Diccionario que contiene la configuración principal del juego

    Returns:
        dict: Devuelve el diccionario que controla el estado del juego
        bool: Devuelve reiniciar cuando finalice el bucle del juego
    """
    estado_del_juego = preparar_nueva_partida(nombre_jugador, dificultades_rondas)
    reiniciar = inicializar_bucle_del_juego(estado_del_juego, lista_preguntas, config["tiempo_preguntas"])
    estado_del_juego["Fin_tiempo_partida"] = time.time()
    return estado_del_juego, reiniciar

def finalizar_partida(estado_del_juego: dict, modo: str):
    """Función que finaliza definitivamente la partida

    Args:
        estado_del_juego (dict): Diccionario que contiene los datos actuales del juego
        modo (str): Modo de dificultad elegido por el jugador
    """
    mostrar_resultado_final(estado_del_juego)
    guardar_estadistica_jugador(estado_del_juego, f"estadisticas_{modo}.csv")

def preparar_nueva_partida(nombre_jugador: str, dificultades_rondas: list) -> dict:
    """Se encarga de preparar los datos para iniciar una nueva partida

    Args:
        nombre_jugador (str): Nombre del usuario
        dificultades_rondas (list): Lista de dificultad por ronda a jugar

    Returns:
        dict: Retorna el diccionario que contiene los datos del juego
    """
    clear_console()
    printear_con_transicion("¡Bienvenido a Quien quiere ser Millonario!\n", delay=0.01)
    time.sleep(2)

    estado_del_juego = inicializar_juego(len(dificultades_rondas))
    estado_del_juego["Usuario"] = nombre_jugador
    estado_del_juego["Inicio_tiempo_partida"] = time.time()
    estado_del_juego["Dificultades"] = dificultades_rondas
    return estado_del_juego


def jugar(lista_preguntas: list, config: dict, modo: str, dificultades_rondas: list):
    """Función principal del juego. Controla inicio, desarrollo y final.

    Args:
        lista_preguntas (list): Lista que contiene los diccionarios de preguntas
        config (dict): Diccionario que contiene la configuración principal del juego
        modo (str): Modo de dificultad elegido por el jugador
        dificultades_rondas (list): Lista de dificultades que va a tener por ronda la partida
    """
    clear_console()
    nombre_jugador = obtener_nombre_jugador(config)
    reiniciar = True

    while reiniciar:
        estado_del_juego, reiniciar = desarrollar_partida(nombre_jugador, dificultades_rondas, lista_preguntas, config)

    if not reiniciar:
        finalizar_partida(estado_del_juego, modo)