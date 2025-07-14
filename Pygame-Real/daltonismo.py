import pygame

def ajustar_color(color, tipo_daltonismo):
    """
    Ajusta un color RGB para un tipo específico de daltonismo
    @param color: Tuple (R, G, B)
    @param tipo_daltonismo: str ("protanopia", "deuteranopia", "tritanopia")
    @return: Tuple (R, G, B) ajustado
    """
    if not tipo_daltonismo:
        return color
    
    r, g, b = color
    
    # Matrices de transformación para diferentes tipos de daltonismo
    if tipo_daltonismo == "protanopia":
        return (
            int(0.567 * r + 0.433 * g),
            int(0.558 * r + 0.442 * g),
            int(0.242 * g + 0.758 * b)
        )
    elif tipo_daltonismo == "deuteranopia":
        return (
            int(0.625 * r + 0.375 * g),
            int(0.7 * r + 0.3 * g),
            int(0.3 * g + 0.7 * b)
        )
    elif tipo_daltonismo == "tritanopia":
        return (
            int(0.95 * r + 0.05 * g),
            int(0.433 * g + 0.567 * b),
            int(0.475 * g + 0.525 * b)
        )
    return color

def agregar_simbolos(opciones):
    """Agrega símbolos distintivos a las opciones para daltonismo"""
    simbolos = ["■", "▲", "●", "★"]
    opciones_con_simbolos = []

    for i in range(len(opciones)):
        if i < len(simbolos):
            nueva_opcion = f"{simbolos[i]} {opciones[i]}"
        else:
            nueva_opcion = opciones[i]
        opciones_con_simbolos.append(nueva_opcion)

    return opciones_con_simbolos
