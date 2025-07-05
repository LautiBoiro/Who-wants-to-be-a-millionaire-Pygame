from colorama import Fore, Style
from funciones_archivos import cargar_preguntas, cargar_configuracion, leer_estadisticas, escribir_configuracion
from funciones_juego import jugar
import os

def inicio():
    seguir = True
    while seguir:
        os.system("cls" if os.name == "nt" else "clear")
        print(Fore.BLUE + Style.BRIGHT + "📋 MENÚ PRINCIPAL")
        print(Fore.BLUE + "==================================")
        print(Fore.YELLOW + "1." + Fore.WHITE + " 🎮 Jugar")
        print(Fore.YELLOW + "2." + Fore.WHITE + " ⚙️  Ver configuración")
        print(Fore.YELLOW + "3." + Fore.WHITE + " 📊 Ver estadísticas")
        print(Fore.RED + "4." + Fore.WHITE + " ✖️  Salir")
        print(Fore.BLUE + "==================================")

        opcion = int(input(Fore.GREEN + "🫴 Elija una opción (1-4): "))
        print(Style.RESET_ALL, end="") #Resetea para que no se vea todo el juego en verde
        if opcion == 1:
            if opcion == 1:
                lista_preguntas = cargar_preguntas("preguntas.csv")
                config = cargar_configuracion("config.json")
                dificultades, modo = pedir_dificultad()
                jugar(lista_preguntas, config, modo, dificultades)


        elif opcion == 2:
            config = cargar_configuracion("config.json")
            print(Fore.MAGENTA + "\n⚙️ CONFIGURACIÓN ACTUAL:")
            print(Fore.WHITE + f"- Tiempo por pregunta: {config['tiempo_preguntas']} segundos")
            print(f"- Cantidad de preguntas: {config['cantidad_preguntas']}")
            print(f"- Caracteres máximo para el nombre: {config['caracteres_maximo']}")

            print(Fore.CYAN + "\n¿Con qué perfil te identificás?")
            print(Fore.YELLOW + "1." + Fore.WHITE + " Neurotípico (tiempo normal por pregunta: 20 segundos)")
            print(Fore.YELLOW + "2." + Fore.WHITE + " Neurodivergente (más tiempo por pregunta: 40 segundos)")
            print(Fore.RED + "3." + Fore.WHITE + " ⬅️ Volver al menu")
    
            opcion_perfil = input(Fore.GREEN + "Elegí una opción (1 o 2): ").strip()

            if opcion_perfil == "1":
                config["tiempo_preguntas"] = 20
                print(Fore.BLUE + "✅ Tiempo ajustado a 20 segundos para perfil neurotípico.")
            elif opcion_perfil == "2":
                config["tiempo_preguntas"] = 40
                print(Fore.BLUE + "✅ Tiempo ajustado a 40 segundos para perfil neurodivergente.")
            elif opcion_perfil == "3":
                print(Fore.CYAN + "🔙 Volviendo al menú principal sin cambios.")
                break
            else:
                print(Fore.RED + "❌ Opción inválida. No se modificó la configuración.")

            escribir_configuracion(config, "config.json")

        elif opcion == 3:
            dificultades = ["facil", "normal", "dificil", "extremo"]
            for dificultad in dificultades:
                path = f"estadisticas_{dificultad}.csv"
                print(Fore.MAGENTA + f"\n========= {dificultad.capitalize()} =========")
                estadisticas = leer_estadisticas(path)

                if estadisticas:
                    for est in estadisticas:
                        print(Fore.WHITE + f"Usuario: {est['Usuario']}, "
                        f"Rondas: {est['Rondas_jugadas']}, "
                        f"Acertadas: {est['Preguntas_acertadas']}, "
                        f"Promedio tiempo: {est['Tiempo_promedio']}s, "
                        f"Ganadas: {est['Contador_partidas_ganadas']}, ", end="")
                        if est['Mejor_tiempo'] != float('inf'):
                            print(f"Mejor tiempo: {est['Mejor_tiempo']}s")
                        else:
                            print("Mejor tiempo: --")
                else:
                    print(Fore.RED + "❌ No hay estadísticas registradas.")

        elif opcion == 4:
            print(Fore.RED + "👋 Saliendo del juego... ¡Hasta luego!")
            seguir = False
        else:
            print(Fore.RED + "❌ Opción inválida. Ingrese un número entre 1 y 4.")

        if seguir:
            input(Fore.CYAN + "\nPresione ENTER para volver al menú...")

def pedir_dificultad() -> list:
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.MAGENTA + "🎯 SELECCIÓN DE DIFICULTAD")
    print(Fore.MAGENTA + "===========================")
    print(Fore.YELLOW + "1." + Fore.WHITE + " 😺 Fácil      → 4 fáciles + 3 medias")
    print(Fore.YELLOW + "2." + Fore.WHITE + " 😼 Normal     → 3 fáciles + 2 medias + 2 difíciles")
    print(Fore.YELLOW + "3." + Fore.WHITE + " 😾 Difícil    → 4 medias + 3 difíciles")
    print(Fore.YELLOW + "4." + Fore.WHITE + " 👹 Extremo    → 7 difíciles")
    print(Fore.MAGENTA + "===========================\n")

    while True:
        opcion = input(Fore.GREEN + "Elija una dificultad (1-4): ").strip()
        if opcion == "1":
            preguntas_de_la_partida = ["Facil"] * 4 + ["Medio"] * 3
            modo = "facil"
        elif opcion == "2":
            preguntas_de_la_partida = ["Facil"] * 3 + ["Medio"] * 2 + ["Dificil"] * 2
            modo = "normal"
        elif opcion == "3":
            preguntas_de_la_partida = ["Medio"] * 4 + ["Dificil"] * 3
            modo = "dificil"
        elif opcion == "4":
            preguntas_de_la_partida = ["Dificil"] * 7
            modo = "extremo"
        else:
            print(Fore.RED + "❌ Opción inválida. Ingrese un número del 1 al 4.")
            continue
        
        return preguntas_de_la_partida, modo


# Llamar al menú
if __name__ == "__main__":
    inicio()
