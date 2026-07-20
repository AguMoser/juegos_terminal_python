import random
def obtener_carta_aleatoria(mazo_cartas: list[str]) -> str:
    """
    Devuelve una sola carta al azar del mazo.

    Args:
        mazo_cartas: Lista de strings que contiene las cartas disponibles en el juego.

    Returns:
        Un string que representa la carta seleccionada de forma aleatoria.
    """
    return random.choice(mazo_cartas)

def obtener_valor_carta_blackjack(carta: str) -> int:
    """
    Traduce el valor de una carta en formato string a su valor numérico real.

    Args:
        carta: El string que representa la carta (ej: "2", "10", "J", "Q", "K", "A").

    Returns:
        El valor numérico correspondiente según las reglas tradicionales del Blackjack.
    """
    if carta in ["J", "Q", "K"]:
        return 10
    if carta == "A":
        return 11
    return int(carta)

def repartir_banca_inicial(mazo_cartas: list[str]) -> int:
    """
    Reparte las dos primeras cartas de la banca y muestra solo la primera.

    Args:
        mazo_cartas: Lista de strings con las cartas disponibles para repartir.

    Returns:
        La suma acumulada del valor numérico de las dos cartas iniciales de la banca.
    """
    carta_visible = obtener_carta_aleatoria(mazo_cartas)
    carta_oculta = obtener_carta_aleatoria(mazo_cartas)
    
    print(f"🃏 La carta de la banca es: {carta_visible}")
    return obtener_valor_carta_blackjack(carta_visible) + obtener_valor_carta_blackjack(carta_oculta)

def ejecutar_turno_jugador(puntos_iniciales_jugador: int, mazo_cartas: list[str]) -> int:
    """
    Maneja el bucle de decisiones del jugador para pedir cartas.

    Args:
        puntos_iniciales_jugador: Puntaje acumulado por el jugador con sus dos primeras cartas.
        mazo_cartas: Lista de strings de donde se obtendrán las nuevas cartas si decide pedir.

    Returns:
        El puntaje total final obtenido por el jugador al terminar su turno.
    """
    puntos_totales_jugador = puntos_iniciales_jugador
    
    while puntos_totales_jugador < 21:
        print(f"💲 Tus puntos actuales son: {puntos_totales_jugador}\n")
        decision_usuario = input("¿Desea otra tirada más? (s/n): ")
        
        if not validar_entrada_blackjack(decision_usuario):
            print("❌ Opción inválida. Por favor, escriba la letra correcta nuevamente\n")
            continue
            
        if decision_usuario.lower() == "n":
            break
            
        nueva_carta = obtener_carta_aleatoria(mazo_cartas)
        print(f"🃏 Tu carta es: {nueva_carta}")
        puntos_totales_jugador += obtener_valor_carta_blackjack(nueva_carta)
            
    print(f"Tu puntaje es: {puntos_totales_jugador}\n")
    return puntos_totales_jugador

def ejecutar_turno_banca(mazo_cartas: list[str], puntos_iniciales_banca: int) -> int:
    """
    Ejecuta la estrategia automática de la banca pidiendo cartas hasta llegar a 17 o más.

    Args:
        mazo_cartas: Lista de strings de donde la banca tomará cartas adicionales.
        puntos_iniciales_banca: Puntaje total inicial que la banca sumó en el reparto.

    Returns:
        El puntaje definitivo acumulado por la banca tras finalizar de pedir cartas.
    """
    puntos_totales_banca = puntos_iniciales_banca

    print(f"🔸 Puntaje inicial de la banca: {puntos_totales_banca}\n")
    
    while puntos_totales_banca < 17:            
        nueva_carta_banca = obtener_carta_aleatoria(mazo_cartas)
        puntos_totales_banca += obtener_valor_carta_blackjack(nueva_carta_banca)
        print(f"🃏 La banca saca: {nueva_carta_banca}. Total banca: {puntos_totales_banca}\n")        
        
    return puntos_totales_banca

def determinar_ganador_blackjack(puntos_jugador: int, puntos_banca: int) -> str:
    """
    Compara los puntajes finales de Blackjack y define el resultado del juego.

    Args:
        puntos_jugador: Puntaje total definitivo obtenido por el usuario.
        puntos_banca: Puntaje total definitivo obtenido por la IA de la banca.

    Returns:
        Un string con el estado del veredicto final ("GANO_JUGADOR", "GANO_BANCA" o "EMPATE").
    """
    if puntos_jugador > 21:
        print(f"💸 Perdiste la ronda. Te pasaste con {puntos_jugador} puntos.\n")
        return "GANO_BANCA"
        
    if puntos_banca > 21:
        print(f"🏆 Ganaste! La banca se pasó con {puntos_banca} puntos.\n")
        return "GANO_JUGADOR"
        
    if puntos_jugador > puntos_banca:
        print(f"🏆 Ganaste!. Puntos jugador: {puntos_jugador} vs Banca: {puntos_banca}\n")
        return "GANO_JUGADOR"
        
    if puntos_jugador < puntos_banca:
        print(f"💸 Perdiste la ronda. Puntos jugador: {puntos_jugador} vs Banca: {puntos_banca}\n")
        return "GANO_BANCA"
        
    print(f"🤝 Empate en {puntos_jugador} puntos. Se devuelve la apuesta. 💰\n")
    return "EMPATE"

def calcular_actualizacion_puntaje(estado_ronda: str, monto_apuesta: int) -> int:
    """
    Calcular cuántos puntos se le deben otorgar al jugador según el resultado final.

    Args:
        estado_ronda: El string identificador del veredicto ("GANO_JUGADOR", "EMPATE", etc).
        monto_apuesta: Cantidad de dinero/puntos que el jugador puso en riesgo en la ronda.

    Returns:
        El monto numérico neto a transferir de regreso a la billetera del jugador.
    """
    if estado_ronda == "GANO_JUGADOR":
        return monto_apuesta * 2
    if estado_ronda == "EMPATE":
        return monto_apuesta
    return 0

def procesar_jugada_blackjack(billetera_jugador: int, monto_apuesta: int, mazo_cartas: list[str]) -> int:
    """
    Ejecuta una ronda completa de Blackjack coordinando las funciones.

    Args:
        billetera_jugador: Cantidad de dinero/fichas actuales del usuario antes de la jugada.
        monto_apuesta: Monto seleccionado para apostar en esta mano.
        mazo_cartas: El mazo completo en forma de lista de strings.

    Returns:
        El balance final neto de la billetera del jugador tras resolver la jugada.
    """
    billetera_actualizada = billetera_jugador - monto_apuesta    
    puntos_banca = repartir_banca_inicial(mazo_cartas)    
   
    carta_uno_jugador = obtener_carta_aleatoria(mazo_cartas)
    carta_dos_jugador = obtener_carta_aleatoria(mazo_cartas)
    puntos_jugador = obtener_valor_carta_blackjack(carta_uno_jugador) + obtener_valor_carta_blackjack(carta_dos_jugador)
    
    print(f"🃏 Tus cartas iniciales son: {carta_uno_jugador} y {carta_dos_jugador}\n")
 
    puntos_jugador = ejecutar_turno_jugador(puntos_jugador, mazo_cartas)
  
    if puntos_jugador <= 21:
        puntos_banca = ejecutar_turno_banca(mazo_cartas, puntos_banca)
        
    estado_ronda = determinar_ganador_blackjack(puntos_jugador, puntos_banca)
    return billetera_actualizada + calcular_actualizacion_puntaje(estado_ronda, monto_apuesta)

def validar_entrada_blackjack(entrada_usuario: str) -> bool:
    """
    Valida si el usuario ingresó una opción correcta (S o N).

    Args:
        entrada_usuario: Texto ingresado por el usuario en consola.

    Returns:
        True si coincide con "s" o "n" (ignorando mayúsculas), False en caso contrario.
    """
    return entrada_usuario.lower() in ['s', 'n']

def generar_tirada_de_monedas(opciones_monedas: list[str]) -> list[str]:
    """
    Selecciona al azar 3 caras de las monedas de la lista de opciones.

    Args:
        opciones_monedas: Lista de strings con los caracteres posibles que pueden salir (ej: "7", "0", etc.).

    Returns:
        Una lista de 3 strings que representan el resultado del giro de las monedas.
    """
    cantidad_monedas = 3
    return random.choices(opciones_monedas, k=cantidad_monedas)

def calcular_premio_tiramonedas(resultado_tirada: list[str], monto_apuesta: int) -> int:
    """
    Calcula el premio obtenido según la combinación de monedas.

    Args:
        resultado_tirada: Lista de strings con las 3 caras resultantes del tiro.
        monto_apuesta: Cantidad de puntos o dinero que el jugador puso en riesgo.

    Returns:
        El valor numérico del premio total ganado. Devuelve -1 si sale la combinación 
        especial de pérdida total ("0", "0", "0") y 0 si no se logró ninguna combinación.
    """
    if resultado_tirada.count("0") == 3:
        return -1

    cantidad_caras_unicas = len(set(resultado_tirada))

    if cantidad_caras_unicas == 1:
        if resultado_tirada[0] == "7":
            return monto_apuesta * 10
        return monto_apuesta * 5

    if cantidad_caras_unicas == 2:
        return monto_apuesta * 2

    return 0

def procesar_jugada_tiramonedas(puntaje_actual: int, monto_apuesta: int, opciones_monedas: list[str]) -> int:
    """
    Ejecuta una ronda, calcula el premio obtenido y actualiza el saldo del jugador.

    Args:
        puntaje_actual: Saldo o billetera disponible del jugador antes del tiro.
        monto_apuesta: Puntos destinados a apostar en esta jugada.
        opciones_monedas: Caracteres disponibles para la generación aleatoria de la tirada.

    Returns:
        El nuevo saldo neto del jugador tras resolver el tiro. Devuelve 0 de forma directa 
        si se activa la condición de pérdida total (-1).
    """
    tirada_obtenida = generar_tirada_de_monedas(opciones_monedas)
    premio_ganado = calcular_premio_tiramonedas(tirada_obtenida, monto_apuesta)

    if premio_ganado == -1:
        return 0, tirada_obtenida

    puntaje_restante = puntaje_actual - monto_apuesta
    saldo_final = puntaje_restante + premio_ganado

    return saldo_final, tirada_obtenida

def validar_respuesta_si_no(texto_ingresado: str) -> bool:
    """
    Valida si el usuario ingresó una opción afirmativa o negativa válida (S o N).

    Args:
        texto_ingresado: Cadena de texto escrita por el usuario en consola.

    Returns:
        True si coincide con "s" o "n" (ignorando mayúsculas), False en caso contrario.
    """
    entrada_limpia = texto_ingresado.lower()
    opciones_validas = ['s', 'n']
    
    return entrada_limpia in opciones_validas

def validar_monto_apuesta(monto_apuesta: int, puntaje_actual: int) -> bool:
    """
    Verifica si la apuesta se encuentra dentro del rango de saldo permitido.

    Args:
        monto_apuesta: El valor numérico de la apuesta que se intenta realizar.
        puntaje_actual: Fondos totales que posee el jugador en ese momento.

    Returns:
        True si la apuesta es mayor o igual a 1 y no supera el saldo actual, False de lo contrario.
    """
    apuesta_minima = 1
    return apuesta_minima <= monto_apuesta <= puntaje_actual

def validar_es_numero(texto_ingresado: str) -> bool:
    """
    Verifica si la cadena ingresada contiene únicamente dígitos numéricos.

    Args:
        texto_ingresado: Texto que se quiere validar.

    Returns:
        True si el string está compuesto solo por números enteros positivos, False en caso contrario.
    """
    return texto_ingresado.isdigit()