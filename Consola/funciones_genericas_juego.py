from inputimeout import inputimeout, TimeoutOccurred

def pedir_nombre(caracteres_maximos, mensaje, mensaje_error) -> str:
    """
    Solicita al usuario un nombre y valida su longitud.

    Args:
        caracteres_maximos (int): Cantidad máxima de caracteres permitidos.
        mensaje (str): Mensaje inicial a mostrar.
        mensaje_error (str): Mensaje a mostrar si el nombre supera el límite.

    Returns:
        str: Nombre validado del usuario.
    """
    nombre_usuario = input(mensaje).strip()
    while len(nombre_usuario) > caracteres_maximos:
        nombre_usuario = input(mensaje_error).strip()

    return nombre_usuario

def pedir_confirmacion(mensaje: str, mensaje_error: str, set_respuestas_validas: set, tiempo_limite: int = None) -> str:
    """
    Solicita confirmación al usuario validando su respuesta con o sin límite de tiempo.

    Args:
        mensaje (str): Mensaje que se le muestra al usuario.
        mensaje_error (str): Mensaje de error si la entrada no es válida.
        set_respuestas_validas (set): Conjunto de respuestas válidas.
        tiempo_limite (int, opcional): Tiempo límite para responder.

    Returns:
        str: Respuesta validada o "Sin tiempo" si el tiempo terminó.
    """
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

def filtrar_preguntas(lista_preguntas: list, criterio_funcion, *args) -> list:
    """Se encarga de filtrar preguntas según un criterio

    Args:
        lista_preguntas (list): Es la lista que contiene los diccionarios de cada pregunta
        criterio_funcion: Función que determina el criterio por el cuál se van a filtrar las preguntas

    Returns:
        list: Lista de preguntas filtradas (coinciden con el criterio)
    """
    preguntas_filtradas = []
    for pregunta in lista_preguntas:
        if criterio_funcion(pregunta, *args):
            preguntas_filtradas.append(pregunta)
    return preguntas_filtradas