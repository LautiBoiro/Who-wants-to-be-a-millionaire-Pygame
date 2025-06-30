import random
import time
import os
import platform
from funciones_archivos import *
from inputimeout import inputimeout, TimeoutOccurred

respuestas_validas_si_o_no = {"si", "sí", "no"}
respuestas_validas_opciones = {"a", "b", "c", "d"}

def pedir_nombre(caracteres_maximos, mensaje, mensaje_error) -> str:
    
    nombre_usuario = input(mensaje).strip()
    while len(nombre_usuario) > caracteres_maximos:
        nombre_usuario = input(mensaje_error).strip()

    return nombre_usuario

def comprobar_nombre (nombre_usuario: str):
    if nombre_usuario:
        pass

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
    printear_con_transicion(f"Ronda: {ronda}")
    printear_con_transicion(f"Categoría: {categoria} | Dificultad: {dificultad}")
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
            retirar =  pedir_confirmacion ("Te gustaría retirarte con tu premio acumulado? Si/No: ", "Respuesta inválida. Ingrese Si o No", respuestas_validas_si_o_no)
        case 5:
            puntuacion = 750
            print ("Alcanzaste los $750")
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

def pedir_confirmacion(mensaje: str, mensaje_error: str, set_respuestas_validas: set, tiempo_limite: int = None) -> str:
    respuesta = "Sin tiempo"
    while True:
        try:
            if tiempo_limite is not None:
                entrada = inputimeout(prompt=mensaje, timeout=tiempo_limite).strip().lower()
            else:
                entrada = input(mensaje).strip().lower()
        except TimeoutOccurred:
            break

        if entrada in set_respuestas_validas:
            respuesta = entrada
            break
        else:
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
    preguntas_filtradas = []

    for pregunta in lista_preguntas:
        pregunta_usada = False
        dificultad = pregunta["Categoria/Dificultad"][1]
        if pregunta["Pregunta"] in estado_juego["Preguntas_elegidas"]:
            pregunta_usada = True

        if dificultad == dificultad_actual and not pregunta_usada:
            preguntas_filtradas.append(pregunta)

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

def preguntar_y_responder(estado_juego: dict, lista_preguntas: list, tiempo_limite: int = None) -> bool | dict:
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

def guardar_estadistica_jugador(estado_juego: dict, path: str):
    lista_estadisticas = leer_estadisticas(path)
    nueva_estadistica = crear_estadistica_final(estado_juego, estado_juego["Usuario"])

    jugador_encontrado = False

    for estadistica in lista_estadisticas:
        if estadistica["Usuario"] == nueva_estadistica["Usuario"]:
            jugador_encontrado = True #El jugador está en la lista
            estadistica["Rondas_jugadas"] += nueva_estadistica["Rondas_jugadas"]
            estadistica["Preguntas_acertadas"] += nueva_estadistica["Preguntas_acertadas"]
            estadistica["Contador_partidas_ganadas"] += int(nueva_estadistica["Premio_mayor"] == "Si")

            rondas_totales = estadistica["Rondas_jugadas"]
            rondas_nuevas = nueva_estadistica["Rondas_jugadas"]
            tiempo_total_nuevo = nueva_estadistica["Tiempo_total"]
            tiempo_promedio_anterior = estadistica["Tiempo_promedio"]

            rondas_anteriores = rondas_totales - rondas_nuevas
            tiempo_total_anterior = tiempo_promedio_anterior * rondas_anteriores

            total_tiempo = tiempo_total_anterior + tiempo_total_nuevo
            estadistica["Tiempo_promedio"] = round(total_tiempo / rondas_totales, 2)

            if nueva_estadistica["Mejor_tiempo"] < estadistica["Mejor_tiempo"]:
                estadistica["Mejor_tiempo"] = nueva_estadistica["Mejor_tiempo"]
            break

    if not jugador_encontrado:
        estadistica_a_guardar = {
            "Usuario": nueva_estadistica["Usuario"],
            "Rondas_jugadas": nueva_estadistica["Rondas_jugadas"],
            "Preguntas_acertadas": nueva_estadistica["Preguntas_acertadas"],
            "Tiempo_promedio": nueva_estadistica["Tiempo_promedio"],
            "Contador_partidas_ganadas": int(nueva_estadistica["Premio_mayor"] == "Si"),
            "Mejor_tiempo": nueva_estadistica["Mejor_tiempo"]
        }
        lista_estadisticas.append(estadistica_a_guardar)

    escribir_estadisticas(lista_estadisticas, path)


def determinar_premio_mayor(puntuacion:dict):
    premio_mayor = "No"
    if puntuacion == 1000:
        premio_mayor = "Si"
    return premio_mayor

def determinar_tiempo_promedio(tiempo_total, cantidad_rondas):
    tiempo_promedio = 0
    if cantidad_rondas > 0:
        tiempo_promedio = tiempo_total / cantidad_rondas
    return tiempo_promedio

def determinar_mejor_tiempo(cantidad_rondas, tiempo_total):
    mejor_tiempo = 0 #Se inicializa en cero en caso de que el usuario no haya ganado. Al comparar se va a hacer un condicional > 0.
    if cantidad_rondas == 7:   
        mejor_tiempo = tiempo_total

    return mejor_tiempo

def crear_estadistica_final(estado_juego: dict, nombre_jugador: str) -> dict:
    tiempo_total = estado_juego["Fin_tiempo_partida"] - estado_juego["Inicio_tiempo_partida"]
    tiempo_promedio = determinar_tiempo_promedio(tiempo_total, estado_juego["Rondas"])
    mejor_tiempo = determinar_mejor_tiempo(estado_juego["Rondas"], tiempo_total)

    estadistica = {
        "Usuario": nombre_jugador,
        "Rondas_jugadas": estado_juego["Rondas"],
        "Preguntas_acertadas": estado_juego["Preguntas_acertadas"],
        "Tiempo_total": round(tiempo_total, 2), #Round redondea con 2 decimales
        "Tiempo_promedio": round(tiempo_promedio, 2),
        "Premio_mayor" : determinar_premio_mayor(estado_juego["Puntuacion"]),
        "Mejor_tiempo": round(mejor_tiempo, 2)
    }
    return estadistica

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

def finalizar_juego(estado: dict):
    """Muestra los datos al finalizar el juego

    Args:
        estado (dict): Diccionario que contiene los datos actuales del juego
    """
    clear_console()
    if estado["Perdida"]:
        printear_con_transicion("Ha finalizado el juego. Mejor suerte la próxima.")

    elif estado["Rondas"] < 7:
        printear_con_transicion(f"Has retirado tu premio de ${estado["Puntuacion"]} ¡Felicidades!")
    
    else:
        printear_con_transicion(f"¡Felicidades!¡Ganaste el premio mayor de ${estado["Puntuacion"]}!")
    
    time.sleep(3)


def jugar (lista_preguntas: list, config: dict, path_estadisticas: str):
    """Función principal que controla el juego
    """
    clear_console()
    nombre_jugador = pedir_nombre(config["caracteres_maximo"], "Ingrese su nombre de usuario (máximo 14 carácteres): ", "Error detectado. Reingrese su nombre de usuario (máximo 14 carácteres): ")
    reiniciar = True
    while reiniciar:
        clear_console()
        printear_con_transicion("¡Bienvenido a Quien quiere ser Millonario!\n", delay=0.01)
        time.sleep(2)
        estado_del_juego = inicializar_juego(config["cantidad_preguntas"])
        estado_del_juego["Usuario"] = nombre_jugador
        estado_del_juego["Inicio_tiempo_partida"] = time.time()

        reiniciar = inicializar_bucle_del_juego(estado_del_juego, lista_preguntas, config["tiempo_preguntas"])
        estado_del_juego["Fin_tiempo_partida"] = time.time()

        if not reiniciar:
            finalizar_juego(estado_del_juego)
            printear_con_transicion(f"Estadísticas de la partida:\n- Rondas jugadas: {estado_del_juego['Rondas']}\n- Preguntas acertadas: {estado_del_juego['Preguntas_acertadas']}")
            guardar_estadistica_jugador(estado_del_juego, path_estadisticas)

def printear_con_transicion(text, delay=0.009):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def clear_console():
    """
    Limpia la consola dependiendo del sistema operativo.
    """
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    elif system == 'Linux':
        os.system('clear')