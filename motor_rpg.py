import random
from config import  gestionar_creacion_personaje, crear_enemigo_aleatorio
from interfaz import imprimir_mapa_en_consola
from archivos import registrar_partida_csv

def iniciar_modulo_rpg() -> None:
    """
    Controla el bucle principal y el flujo general de la partida del juego RPG.
    """
    jugador = gestionar_creacion_personaje()
    if not jugador:
        print("❌ Creación de personaje cancelada. Volviendo al menú.")
        return

    mapa_juego = inicializar_escenario_rpg()
    turnos_totales = 0
    resultado = "Abandono"

    while True:

        fila_jugador = jugador["fila"]
        columna_jugador = jugador["columna"]

        mapa_juego[fila_jugador][columna_jugador] = "P"
        imprimir_mapa_en_consola(mapa_juego)
        mapa_juego[fila_jugador][columna_jugador] = "."

        entrada_control = input("Controles: W(arriba) | A(izquierda) | S(abajo) | D(derecha) [0 para salir]: ").strip().upper()
        if entrada_control == "0":
            break

        turnos_totales += 1

        movimiento_valido = mover_jugador_en_mapa(jugador, mapa_juego, entrada_control)
        if not movimiento_valido:
            resultado = "Derrota"
            break

        if not verificar_enemigo_activo(mapa_juego):
            print("🏆 ¡Ganaste la partida!")
            resultado = "Victoria"
            break       
   
    registrar_partida_csv(jugador["nombre"], jugador["clase"], resultado, turnos_totales)

def crear_mapa_base(cantidad_filas: int, cantidad_columnas: int) -> list[list[str]]:
    """
    Crea una matriz bidimensional llena de puntos que sirve como estructura inicial del mapa.

    Args:
        cantidad_filas: El número total de filas del escenario.
        cantidad_columnas: El número total de columnas del escenario.

    Returns:
        Matriz inicializada con caracteres ".".
    """    
    return [["." for _ in range(cantidad_columnas)] for _ in range(cantidad_filas)]

def dibujar_bordes_mapa(matriz: list[list[str]]) -> None:
    """
    Dibuja los bordes externos del mapa utilizando el carácter "#".

    Args:
        matriz: Escenario actual donde se sobreescribirán los límites gráficos.
    """
    cantidad_filas = len(matriz)
    cantidad_columnas = len(matriz[0])

    for indice_columna in range(cantidad_columnas):
        matriz[0][indice_columna] = "#"
        matriz[cantidad_filas - 1][indice_columna] = "#"

    for indice_fila in range(cantidad_filas):
        matriz[indice_fila][0] = "#"
        matriz[indice_fila][cantidad_columnas - 1] = "#"

def colocar_muros_internos(matriz: list[list[str]], lista_muros: list[dict]) -> None:
    """
    Ubica los muros interiores dentro del mapa según una lista de coordenadas.

    Args:
        matriz: Escenario en donde se colocarán los obstáculos.
        lista_muros: Lista de diccionarios con las coordenadas "fila" y "columna".
    """
    for muro in lista_muros:
        matriz[muro["fila"]][muro["columna"]] = "#"

def ubicar_objetos_interactivos_mapa(matriz: list[list[str]], lista_objetos: list[dict]) -> None:
    """
    Ubica los objetos interactivos (enemigos o fogatas) usando el carácter que los representa.

    Args:
        matriz: Escenario donde se posicionarán las entidades.
        lista_objetos: Lista de diccionarios con la posición y el "tipo" ("E" o "F").
    """
    for objeto in lista_objetos:
        matriz[objeto["fila"]][objeto["columna"]] = objeto["tipo"]

def ubicar_elementos_mapa(matriz: list[list[str]], lista_muros: list[dict], lista_objects: list[dict]) -> list[list[str]]:
    """
    Ubica los bordes, los muros interiores y los objetos interactivos dentro del mapa.

    Args:
        matriz: Escenario base vacío.
        lista_muros: Lista con las posiciones de los obstáculos.
        lista_objects: Lista con las posiciones de las entidades.

    Returns:
        La matriz del mapa completamente configurada y lista para jugar.
    """
    dibujar_bordes_mapa(matriz)
    colocar_muros_internos(matriz, lista_muros)
    ubicar_objetos_interactivos_mapa(matriz, lista_objects)
    return matriz

def calcular_proxima_coordenada(fila_actual: int, columna_actual: int, direccion: str) -> tuple[int, int]:
    """
    Calcula la nueva posición del personaje según la dirección de movimiento ingresada.

    Args:
        fila_actual: Índice de fila actual del jugador.
        columna_actual: Índice de columna actual del jugador.
        direccion: Tecla de dirección presionada ("W", "A", "S", "D").

    Returns:
        Tupla con los nuevos índices calculados (nueva_fila, nueva_columna).
    """
    desplazamientos = {
        "W": (-1, 0),
        "S": (1, 0),
        "A": (0, -1),
        "D": (0, 1)
    }
    movimiento = desplazamientos.get(direccion.upper(), (0, 0))
    return fila_actual + movimiento[0], columna_actual + movimiento[1]

def coordenada_dentro_del_mapa(fila: int, columna: int, matriz: list[list[str]]) -> bool:
    """
    Verifica si una coordenada específica pertenece a los límites de la matriz del mapa.

    Args:
        fila: Índice de la fila a comprobar.
        columna: Índice de la columna a comprobar.
        matriz: Mapa contra el cual se contrastan los límites.

    Returns:
        True si la coordenada está dentro de la matriz, False en caso contrario.
    """
    return 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0])

def validar_limites_y_obstaculos(posicion: tuple[int, int], matriz: list[list[str]]) -> bool:
    """
    Verifica que el destino esté dentro de los límites y que la casilla no sea un muro.

    Args:
        posicion: Tupla (fila, columna) a validar.
        matriz: Mapa actual del juego.

    Returns:
        True si el paso es válido y transitable, False si es un borde o un muro.
    """
    fila, columna = posicion
    if coordenada_dentro_del_mapa(fila, columna, matriz):
        return matriz[fila][columna] != "#"
    return False

def actualizar_posicion_personaje(personaje: dict, nueva_posicion: tuple[int, int]) -> None:
    """
    Actualiza el diccionario del personaje guardando sus nuevas coordenadas.

    Args:
        personaje: El diccionario de datos del jugador.
        nueva_posicion: Tupla conteniendo la (nueva_fila, nueva_columna).
    """
    personaje["fila"], personaje["columna"] = nueva_posicion

def aplicar_curacion_fogata(personaje: dict) -> None:
    """
    Recupera un 30% de la vida máxima del personaje sin superar su tope.

    Args:
        personaje: El diccionario del jugador a sanar.
    """
    puntos_curacion = int(personaje["vida_max"] * 0.3)
    personaje["vida_actual"] = min(personaje["vida_actual"] + puntos_curacion, personaje["vida_max"])

def procesar_beneficio_fogata(personaje: dict) -> None:
    """
    Otorga un beneficio estadístico aleatorio al personaje al interactuar con una fogata.

    Args:
        personaje: El diccionario del jugador que recibe el efecto.
    """
    print("🔥 Te sentás a descansar junto a la fogata...")
    beneficio = random.randint(1, 4)

    if beneficio == 1:
        aplicar_curacion_fogata(personaje)
        print("❤️ Recuperaste parte de tu vida.")
    elif beneficio == 2:
        personaje["efectos"].append("danio_duplicado")
        print("⚔️ Tu próximo ataque hará el doble de daño.")
    elif beneficio == 3:
        personaje["efectos"].append("esquive_automatico")
        print("💨 Esquivarás automáticamente el próximo ataque.")
    elif beneficio == 4:
        personaje["efectos"].append("defensa_potenciada")
        personaje["defensa"] += 5
        print("🛡️ Tu defensa aumentó temporalmente.")

def solicitar_zona(tipo_accion: str) -> str:
    """
    Solicita al usuario que elija una zona para atacar o defenderse, validando la opción.

    Args:
        tipo_accion: El contexto de la entrada para el prompt ("ATACAR", "DEFENDERSE", etc).

    Returns:
        Nombre de la zona seleccionada ("Cabeza", "Torso", "Piernas").
    """
    mapeo = {"1": "Cabeza", "2": "Torso", "3": "Piernas"}
    while True:
        opcion = input(f"Elija zona para {tipo_accion} ([1] Cabeza, [2] Torso, [3] Piernas): ").strip()
        if opcion in mapeo:
            return mapeo[opcion]
        print("⚠️ Opción inválida. Elija 1, 2 o 3.")

def procesar_efecto_personaje(personaje: dict, efecto_a_buscar: str) -> bool:
    """
    Busca un efecto específico en los efectos activos y, si lo encuentra, lo elimina.

    Args:
        personaje: El diccionario del jugador.
        efecto_a_buscar: El nombre del string del buff/debuff a procesar.

    Returns:
        True si el efecto estaba activo y fue consumido, False de lo contrario.
    """
    if efecto_a_buscar in personaje["efectos"]:
        personaje["efectos"].remove(efecto_a_buscar)
        return True
    return False

def obtener_danio_jugador(personaje: dict) -> int:
    """
    Calcula el daño total que realizará el jugador evaluando el efecto de daño duplicado.

    Args:
        personaje: El diccionario del jugador atacante.

    Returns:
        El valor numérico final del daño calculado.
    """
    danio_calculado = personaje["danio"]
    if procesar_efecto_personaje(personaje, "danio_duplicado"):
        danio_calculado *= 2
    return danio_calculado

def obtener_modificadores_clase(personaje: dict, ronda_actual: int) -> tuple[bool, bool]:
    """
    Determina si la clase del personaje posee habilidades especiales activas en la ronda actual.

    Args:
        personaje: El diccionario del jugador.
        ronda_actual: El número de la ronda de combate en curso.

    Returns:
        Una tupla de booleanos indicando (ignora_bloqueo, ignora_defensa).
    """  
    ignora_bloqueo = (personaje["clase"] == "Arquero" and ronda_actual <= 2)
    ignora_defensa = (personaje["clase"] == "Mago")
    return ignora_bloqueo, ignora_defensa

def calcular_danio_impacto(zona_ataque: str, zona_defensa_rival: str, danio_atacante: int, defensa_rival: int,
                           ignora_bloqueo: bool, ignora_defensa: bool) -> int:
    """
    Calcula el daño final de un ataque considerando zonas, defensa y modificadores.

    Args:
        zona_ataque: Zona elegida por el atacante.
        zona_defensa_rival: Zona elegida para cubrirse por el defensor.
        danio_atacante: Daño bruto del atacante.
        defensa_rival: Puntos de armadura del objetivo.
        ignora_bloqueo: Booleano que define si se salta la coincidencia de zonas.
        ignora_defensa: Booleano que define si se salta el descuento por armadura.

    Returns:
        El valor numérico del daño final neto resultante.
    """
    if zona_ataque == zona_defensa_rival and not ignora_bloqueo:
        print("🛡️ ATAQUE BLOQUEADO!")
        return 0

    if ignora_defensa:
        print("✨ Ignora defensa")
        return danio_atacante

    return max(0, danio_atacante - defensa_rival)

def aplicar_danio_enemigo(enemigo: dict, danio: int) -> None:
    """
    Resta los puntos de daño calculados de la salud del enemigo.

    Args:
        enemigo: El diccionario del enemigo objetivo.
        danio: Puntos netos a infligir.
    """
    enemigo["vida_actual"] -= danio
    print(f"💥 Daño al enemigo: {danio}")

def aplicar_danio_personaje(personaje: dict, danio: int) -> None:
    """
    Resta los puntos de daño recibidos de la salud del jugador.

    Args:
        personaje: El diccionario del jugador afectado.
        danio: Puntos netos de daño que entran.
    """   
    personaje["vida_actual"] -= danio
    print(f"🩸 Recibiste {danio} puntos de daño.")

def ejecutar_ataque_jugador(personaje: dict, enemigo: dict, ronda_actual: int,
                           zona_ataque: str, zona_defensa_enemigo: str) -> None:
    """
    Gestiona el turno de ataque del jugador, aplicando el impacto al enemigo.

    Args:
        personaje: El atacante.
        enemigo: El objetivo.
        ronda_actual: Ronda en curso para validar habilidades pasivas.
        zona_ataque: Zona seleccionada por el usuario.
        zona_defensa_enemigo: Zona elegida de forma aleatoria por la IA enemiga.
    """                    
    danio_jugador = obtener_danio_jugador(personaje)
    ignora_bloqueo, ignora_defensa = obtener_modificadores_clase(personaje, ronda_actual)
    danio_final = calcular_danio_impacto(zona_ataque, zona_defensa_enemigo, danio_jugador, enemigo["defensa"], ignora_bloqueo, ignora_defensa)
    
    if danio_final > 0:
        aplicar_danio_enemigo(enemigo, danio_final)
    elif zona_ataque != zona_defensa_enemigo:
        aplicar_danio_enemigo(enemigo, 5)

def ejecutar_ataque_enemigo(personaje: dict, enemigo: dict, zona_ataque_enemigo: str, 
                            zona_defensa_jugador: str, segunda_zona_defensa_jugador: str | None) -> None:
    """
    Gestiona el turno de ataque del enemigo evaluando bloqueos o efectos de esquive.

    Args:
        personaje: El jugador defendiéndose.
        enemigo: El enemigo que arremete.
        zona_ataque_enemigo: Zona elegida por la IA enemiga.
        zona_defensa_jugador: Primera zona de cobertura elegida por el usuario.
        segunda_zona_defensa_jugador: Segunda zona opcional (para Guerrero activo) o None si no aplica.
    """
    if procesar_efecto_personaje(personaje, "esquive_automatico"):
        print("✨ Esquivaste automáticamente el ataque.")
        return

    bloqueado = (zona_ataque_enemigo == zona_defensa_jugador) or (segunda_zona_defensa_jugador and zona_ataque_enemigo == segunda_zona_defensa_jugador)

    if bloqueado:
        print("🛡️ Bloqueaste el ataque enemigo.")
    else:
        danio_recibido = max(0, enemigo["danio"] - personaje["defensa"])
        if danio_recibido > 0:
            aplicar_danio_personaje(personaje, danio_recibido)

def mostrar_inicio_combate(enemigo: dict) -> None:
    """
    Muestra la interfaz estética del comienzo de un enfrentamiento.

    Args:
        enemigo: Diccionario de la entidad hostil que apareció.
    """
    print(f"\n⚔️ ¡UN {enemigo['nombre'].upper()} APARECIÓ!")
    print(f"Vida: {enemigo['vida_actual']}")

def mostrar_estado_combate(personaje: dict, enemigo: dict, ronda_actual: int) -> None:
    """
    Imprime los datos de salud de ambos combatientes en la ronda actual.

    Args:
        personaje: Datos actuales del jugador.
        enemigo: Datos actuales del enemigo.
        ronda_actual: Número secuencial del asalto de pelea.
    """
    print(f"\n----------------------------\nRONDA {ronda_actual}")
    print(f"❤️ Vida: {personaje['vida_actual']} || {personaje['vida_max']}")
    print(f"🖤 Vida enemigo: {enemigo['vida_actual']} || {enemigo['vida_max']}")

def solicitar_acciones_jugador(personaje: dict, ronda_actual: int) -> tuple[str, str, str | None]:
    """
    Solicita las zonas de ataque y defensa del jugador, gestionando la habilidad del Guerrero.

    Args:
        personaje: Diccionario del jugador para verificar su clase.
        ronda_actual: El número de la ronda de combate en curso.

    Returns:
        Tupla con (zona_ataque, zona_defensa, segunda_zona_defensa).
    """
    zona_ataque = solicitar_zona("ATACAR")
    zona_defensa = solicitar_zona("DEFENDERSE")
    segunda_zona_defensa = solicitar_zona("DEFENSA EXTRA") if (personaje["clase"] == "Guerrero" and ronda_actual % 3 == 0) else None

    return zona_ataque, zona_defensa, segunda_zona_defensa

def obtener_zona_aleatoria() -> str:
    """
    Genera de forma aleatoria una de las tres zonas de combate posibles.

    Returns:
        Un string aleatorio de las zonas del juego.
    """
    return random.choice(["Cabeza", "Torso", "Piernas"])

def obtener_acciones_enemigo() -> tuple[str, str]:
    """
    Establece aleatoriamente la zona de ataque y de defensa del enemigo.

    Returns:
        Tupla de strings representando (zona_ataque_enemigo, zona_defensa_enemigo).
    """
    return obtener_zona_aleatoria(), obtener_zona_aleatoria()

def finalizar_efectos_temporales(personaje: dict) -> None:
    """
    Remueve las alteraciones estadísticas temporales al terminar el combate.

    Args:
        personaje: Diccionario del jugador para limpiar buffs de escena.
    """
    if procesar_efecto_personaje(personaje, "defensa_potenciada"):
        personaje["defensa"] -= 5

def desarrollar_combate(personaje: dict) -> bool:
    """
    Controla el bucle principal de un combate por turnos.

    Args:
        personaje: El jugador que entabla la pelea.

    Returns:
        True si el jugador sobrevive al encuentro, False si cae derrotado.
    """
    enemigo = crear_enemigo_aleatorio() 
    mostrar_inicio_combate(enemigo)
    ronda_actual = 1

    while personaje["vida_actual"] > 0 and enemigo["vida_actual"] > 0:
        mostrar_estado_combate(personaje, enemigo, ronda_actual)
        zona_ataque, zona_defensa, segunda_defensa = solicitar_acciones_jugador(personaje, ronda_actual)
        ataque_enemigo, defensa_enemigo = obtener_acciones_enemigo()

        ejecutar_ataque_jugador(personaje, enemigo, ronda_actual, zona_ataque, defensa_enemigo)

        if enemigo["vida_actual"] > 0:
            ejecutar_ataque_enemigo(personaje, enemigo, ataque_enemigo, zona_defensa, segunda_defensa)

        ronda_actual += 1

    finalizar_efectos_temporales(personaje)
    return personaje["vida_actual"] > 0

def inicializar_escenario_rpg() -> list[list[str]]:
    """
    Configura las dimensiones del mapa y ubica los elementos físicos iniciales.

    Returns:
        Matriz bidimensional con bordes, muros y coleccionables cargados.
    """   
    mapa = crear_mapa_base(10, 10)
    muros = [
        {"fila": 2, "columna": 2}, {"fila": 2, "columna": 3}, {"fila": 2, "columna": 4},
        {"fila": 6, "columna": 7}, {"fila": 6, "columna": 8}
    ]
    elementos = [
        {"fila": 3, "columna": 5, "tipo": "E"}, {"fila": 7, "columna": 2, "tipo": "E"},
        {"fila": 4, "columna": 2, "tipo": "F"}, {"fila": 6, "columna": 3, "tipo": "F"}
    ]
    return ubicar_elementos_mapa(mapa, muros, elementos)

def verificar_enemigo_activo(mapa: list[list[str]]) -> bool:
    """
    Verifica si todavía quedan enemigos ("E") en el escenario.

    Args:
        mapa: Estado de la matriz actual en memoria.

    Returns:
        True si al menos un casillero contains una "E", False si fue limpiado.
    """
    return any("E" in fila for fila in mapa)

def procesar_casilla(casilla: str, jugador: dict, mapa: list[list[str]], fila: int, columna: int) -> bool:
    """
    Evalúa el contenido de la casilla pisada por el jugador y activa eventos.

    Args:
        casilla: El carácter del casillero destino antes de pisar.
        jugador: Los datos estadísticos de tu héroe.
        mapa: La matriz del juego para limpiar los marcadores resueltos.
        fila: Índice de la fila de colisión.
        columna: Índice de la columna de colisión.

    Returns:
        True si el evento no mató al jugador, False si el combate resultó en derrota.
    """
    if casilla == "E":                    
        if not desarrollar_combate(jugador):
            return False
        mapa[fila][columna] = "."
    elif casilla == "F":
        procesar_beneficio_fogata(jugador)
        mapa[fila][columna] = "."
    return True

def mover_jugador_en_mapa(jugador: dict, mapa: list[list[str]], entrada: str) -> bool:
    """
    Mueve al jugador dentro del mapa y procesa el contenido de la casilla de destino.

    Args:
        jugador: Diccionario del personaje.
        mapa: Matriz del escenario del juego.
        entrada: La tecla ingresada por el usuario ya parseada.

    Returns:
        True si el movimiento es válido y mantiene con vida al jugador, False si muere.
    """
    fila_actual, columna_actual = jugador["fila"], jugador["columna"]
    nueva_fila, nueva_columna = calcular_proxima_coordenada(fila_actual, columna_actual, entrada)

    if validar_limites_y_obstaculos((nueva_fila, nueva_columna), mapa):
        casilla = mapa[nueva_fila][nueva_columna]
        if procesar_casilla(casilla, jugador, mapa, nueva_fila, nueva_columna):
            actualizar_posicion_personaje(jugador, (nueva_fila, nueva_columna))
            return True
        return False
    return True

