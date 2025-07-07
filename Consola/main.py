from colorama import Fore, Style
from funciones_genericas_archivos import cargar_preguntas, cargar_configuracion, leer_estadisticas, escribir_configuracion
from funciones_especificas_juego import jugar, pedir_dificultad
from interfaz import *

PATH_CONFIG = "config.json"

def inicio():
    seguir = True
    while seguir:
        mostrar_menu_principal()

        opcion = input(Fore.GREEN + "🫴 Elija una opción (1-4): ").strip()
        print(Style.RESET_ALL, end="") #Resetea para que no se vea todo el juego en verde
        if opcion == "1":
            lista_preguntas = cargar_preguntas("preguntas.csv")
            config = cargar_configuracion(PATH_CONFIG)
            dificultades, modo = pedir_dificultad()
            jugar(lista_preguntas, config, modo, dificultades)


        elif opcion == "2":
            config = cargar_configuracion(PATH_CONFIG)
            mostrar_configuracion_actual(config)

            mostrar_submenu_perfil_usuario()
    
            opcion_perfil = input(Fore.GREEN + "Elegí una opción (1, 2 o 3): ").strip()

            if opcion_perfil == "1":
                config["tiempo_preguntas"] = 20
                print(Fore.BLUE + "✅ Tiempo ajustado a 20 segundos para perfil neurotípico.")
            elif opcion_perfil == "2":
                config["tiempo_preguntas"] = 40
                print(Fore.BLUE + "✅ Tiempo ajustado a 40 segundos para perfil neurodivergente.")
            elif opcion_perfil == "3":
                print(Fore.CYAN + "🔙 Volviendo al menú principal sin cambios.")
            else:
                print(Fore.RED + "❌ Opción inválida. No se modificó la configuración.")

            escribir_configuracion(config, PATH_CONFIG)

        elif opcion == "3":
            dificultades = ["facil", "normal", "dificil", "extremo"]
            for dificultad in dificultades:
                path = f"estadisticas_{dificultad}.csv"
                mostrar_dificultad(dificultad)
                estadisticas = leer_estadisticas(path)

                if estadisticas:
                    for est in estadisticas:
                        mostrar_estadistica_csv(est)
                else:
                    print(Fore.RED + "❌ No hay estadísticas registradas.")

        elif opcion == "4":
            print(Fore.RED + "👋 Saliendo del juego... ¡Hasta luego!")
            seguir = False
        else:
            print(Fore.RED + "❌ Opción inválida. Ingrese un número entre 1 y 4.")

        if seguir:
            input(Fore.CYAN + "\nPresione ENTER para volver al menú...")
            clear_console()


# Llamar al menú
if __name__ == "__main__":
    inicio()
