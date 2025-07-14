def cargar_preguntas(path):
    with open(path, encoding='utf-8') as archivo:
        lineas = archivo.readlines()[1:]
        preguntas = []
        for linea in lineas:
            partes = linea.strip().split(";")
            if len(partes) == 5:
                pregunta, opciones, respuesta, cat_dif, descripcion = partes
                opciones = opciones.split("|")
                categoria, dificultad = cat_dif.split("|")
                preguntas.append({
                    "pregunta": pregunta,
                    "opciones": opciones,
                    "respuesta": respuesta,
                    "categoria": categoria,
                    "dificultad": dificultad.lower(),
                    "descripcion": descripcion
                })
        return preguntas