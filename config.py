   
import random

def mostrar_menu_clases() -> tuple[str, str]:
    """
    Muestra la bienvenida y el menú de selección de clases en la consola, solicita el nombre 
    del jugador (asignando uno por defecto si está vacío) y valida que la opción elegida sea correcta.
    """
    print("BIENVENIDO AL JUEGO! \n")
    nombre_jugador = input("Ingrese su nombre: ").strip() or "Jugador"

    print(f"\n¡Hola {nombre_jugador}! Seleccioná qué tipo de personaje querés ser:")
    print("-----------------------------------------------")
    print("1 - 🤺 GUERRERO")
    print("2 - 🏹 ARQUERO")
    print("3 - 🧙 MAGO")

    opcion_clase = input("\nElija el número de su clase (1, 2 o 3): ").strip()

    while opcion_clase not in ["1", "2", "3"]:
        print("❌ Opción inválida.")
        opcion_clase = input("Ingrese nuevamente una opción: ").strip()

    return nombre_jugador, opcion_clase

def obtener_atributos_clase(opcion_clase: str) -> dict:
    """
    Asigna y estructura en un diccionario el nombre, los multiplicadores de estadísticas 
    y la descripción de la habilidad especial correspondientes a la clase elegida por el jugador.

    Args:
        opcion_clase: El string numérico ("1", "2" o "3") que representa la opción de clase seleccionada.

    Returns:
        Un diccionario con los datos específicos de la clase (nombre, multiplicadores y habilidad).
    """
    clases = {
        "1": {
            "nombre": "Guerrero",
            "multiplicador_vida": 1.2,
            "multiplicador_danio": 1.0,
            "multiplicador_defensa": 1.2,
            "habilidad": "Cada 3er ronda protege 2 zonas"
        },
        "2": {
            "nombre": "Arquero",
            "multiplicador_vida": 0.9,
            "multiplicador_danio": 1.3,
            "multiplicador_defensa": 0.9,
            "habilidad": "Primeros 2 ataques a distancia"
        },
        "3": {
            "nombre": "Mago",
            "multiplicador_vida": 0.8,
            "multiplicador_danio": 1.1,
            "multiplicador_defensa": 0.8,
            "habilidad": "Ataques ignoran la defensa"
        }
    }
    
    return clases[opcion_clase]

def calcular_estadisticas_personaje(nombre_jugador: str, personaje_base: dict, datos_clase: dict) -> dict:
    """
    Crea el diccionario definitivo del personaje aplicando los multiplicadores numéricos de la clase 
    sobre las estadísticas base e inicializando los valores de posición y estados actuales.

    Args:
        nombre_jugador: El nombre elegido por el usuario para su personaje.
        personaje_base: Diccionario con los atributos iniciales de partida (vida, danio, defensa, fila, columna).
        datos_clase: Diccionario con la información y multiplicadores de la clase seleccionada.

    Returns:
        El diccionario completo del personaje configurado y listo con todas sus estadísticas calculadas.
    """
    vida_maxima = int(personaje_base["vida"] * datos_clase["multiplicador_vida"])

    return {
        "nombre": nombre_jugador,
        "clase": datos_clase["nombre"],
        "vida_max": vida_maxima,
        "vida_actual": vida_maxima,
        "danio": int(personaje_base["danio"] * datos_clase["multiplicador_danio"]),
        "defensa": int(personaje_base["defensa"] * datos_clase["multiplicador_defensa"]),
        "habilidad": datos_clase["habilidad"],
        "fila": personaje_base["fila"],
        "columna": personaje_base["columna"],
        "efectos": []
    }

def gestionar_creacion_personaje() -> dict:
    """
    Coordina el proceso completo de configuración del personaje, invocando los menús de entrada, 
    estableciendo los valores base del juego y aplicando los cálculos de estadísticas finales.
    """
    nombre_jugador, opcion_clase = mostrar_menu_clases()

    personaje_base = {
        "vida": 100,
        "danio": 25,
        "defensa": 10,
        "fila": 5,
        "columna": 4
    }

    datos_clase = obtener_atributos_clase(opcion_clase)
    personaje_final = calcular_estadisticas_personaje(nombre_jugador, personaje_base, datos_clase)

    print(f"\n» ¡Listo! Tu personaje es {personaje_final['nombre']} y ha elegido la senda del {personaje_final['clase']}.")
    return personaje_final

def crear_enemigo_aleatorio() -> dict:
    """
    Genera un nuevo enemigo seleccionando un tipo al azar de un listado predefinido 
    y mapea sus estadísticas para inicializar su estructura de combate.
    """
    enemigos_base = [
        {"nombre": "Orco", "vida": 60, "danio": 15, "defensa": 5},
        {"nombre": "Esqueleto", "vida": 40, "danio": 12, "defensa": 2},
        {"nombre": "Goblín", "vida": 30, "danio": 10, "defensa": 1}
    ]
          
    seleccionado = random.choice(enemigos_base)
    
    return {
        "nombre": seleccionado["nombre"],
        "vida_max": seleccionado["vida"],
        "vida_actual": seleccionado["vida"],
        "danio": seleccionado["danio"],
        "defensa": seleccionado["defensa"]
    }

