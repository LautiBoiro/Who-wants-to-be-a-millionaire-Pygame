from funciones_especificas_juego import *
import os
import platform
from colorama import Fore, Style

def mostrar_pregunta (key_pregunta: str):
    """Se encarga de mostrar la pregunta de la key "Pregunta"

    Args:
        key_pregunta (str): Es la cadena que contiene la pregunta
    """
    printear_con_transicion (f"{key_pregunta}\n")

def mostrar_opciones(pregunta_elegida: dict):
    """Se encarga de mostrar las opciones de la key "Opciones"

    Args:
        pregunta_elegida (dict): Es el diccionario de la pregunta
    """
    for opcion in pregunta_elegida["Opciones"]:
        printear_con_transicion (opcion, 0.050)

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

def mostrar_resultado_estadisticas(estado: dict):
    """Muestra las principales estadísticas de la partida (Cantidad de rondas jugadas y preguntas acertadas)

    Args:
        estado (dict): _description_
    """
    texto = (
        f"📊 Estadísticas de la partida:\n- Rondas jugadas: {estado['Rondas']}\n- Preguntas acertadas: {estado['Preguntas_acertadas']}"
    )
    printear_con_transicion(texto)

def mostrar_finalizacion_partida(estado_del_juego: dict):
    """Muestra las estadísticas finales de la partida

    Args:
        estado_del_juego (dict): Diccionario que contiene los datos de la partida actual
    """
    if estado_del_juego["Perdida"]:
        printear_con_transicion("Ha finalizado el juego. Mejor suerte la próxima.")
    elif estado_del_juego["Rondas"] < 7:
        printear_con_transicion(f"Has retirado tu premio de ${estado_del_juego['Puntuacion']} ¡Felicidades!")
    else:
        printear_con_transicion(f"¡Felicidades! ¡Ganaste el premio mayor de ${estado_del_juego['Puntuacion']}!")

def mostrar_estadistica_csv(estadistica: dict):
    linea = (
        f"Usuario: {estadistica['Usuario']}, Rondas: {estadistica['Rondas_jugadas']}, Acertadas: {estadistica['Preguntas_acertadas']}, Promedio tiempo: {estadistica['Tiempo_promedio']}s, Ganadas: {estadistica['Contador_partidas_ganadas']}, "
    )
    if estadistica["Mejor_tiempo"] != float("inf"):
        linea += f"Mejor tiempo: {estadistica['Mejor_tiempo']}s"
    else:
        linea += "Mejor tiempo: --"
    print(linea)

def mostrar_resultado_final(estado: dict):
    """Muestra las estadísticas finales de la partida y el estado final del juego (perdió, se retiró o ganó)

    Args:
        estado (dict): _description_
    """
    clear_console()
    mostrar_finalizacion_partida(estado)
    time.sleep(3)
    mostrar_resultado_estadisticas(estado)

def mostrar_menu_dificultad():
    """Se encarga de mostrar el menú de dificultades al usuario
    """
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.MAGENTA + "🎯 SELECCIÓN DE DIFICULTAD")
    print(Fore.MAGENTA + "===========================")
    print(Fore.YELLOW + "1." + Fore.WHITE + " 😺 Fácil      → 4 fáciles + 3 medias")
    print(Fore.YELLOW + "2." + Fore.WHITE + " 😼 Normal     → 3 fáciles + 2 medias + 2 difíciles")
    print(Fore.YELLOW + "3." + Fore.WHITE + " 😾 Difícil    → 4 medias + 3 difíciles")
    print(Fore.YELLOW + "4." + Fore.WHITE + " 👹 Extremo    → 7 difíciles")
    print(Fore.MAGENTA + "===========================\n")

def printear_con_transicion(texto, delay=0.009):
    """
    Imprime un texto carácter por carácter con una transición visual.

    Args:
        texto (str): Texto a mostrar.
        delay (float): Tiempo entre cada carácter.
    """
    for caracter in texto:
        print(caracter, end='', flush=True)
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

def mostrar_menu_principal():
    print(Fore.BLUE + Style.BRIGHT + "📋 MENÚ PRINCIPAL")
    print(Fore.BLUE + "==================================")
    print(Fore.YELLOW + "1." + Fore.WHITE + " 🎮 Jugar")
    print(Fore.YELLOW + "2." + Fore.WHITE + " ⚙️  Ver configuración")
    print(Fore.YELLOW + "3." + Fore.WHITE + " 📊 Ver estadísticas")
    print(Fore.RED + "4." + Fore.WHITE + " ✖️  Salir")
    print(Fore.BLUE + "==================================")

def mostrar_configuracion_actual(config: dict):
    print(Fore.MAGENTA + "\n⚙️ CONFIGURACIÓN ACTUAL:")
    print(Fore.WHITE + f"- Tiempo por pregunta: {config['tiempo_preguntas']} segundos")
    print(f"- Cantidad de preguntas: {config['cantidad_preguntas']}")
    print(f"- Caracteres máximo para el nombre: {config['caracteres_maximo']}")

def mostrar_submenu_perfil_usuario():
    print(Fore.CYAN + "\n¿Con qué perfil te identificás?")
    print(Fore.YELLOW + "1." + Fore.WHITE + " Neurotípico (tiempo normal por pregunta: 20 segundos)")
    print(Fore.YELLOW + "2." + Fore.WHITE + " Neurodivergente (más tiempo por pregunta: 40 segundos)")
    print(Fore.RED + "3." + Fore.WHITE + " ⬅️  Volver al menú")

def mostrar_dificultad(dificultad: str):
    print(Fore.MAGENTA + f"\n========= {dificultad.capitalize()} =========")
