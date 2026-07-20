
def imprimir_mapa_en_consola(matriz: list[list[str]]) -> None:
    """
    Imprime la matriz en consola con formato visual de cuadrícula, agregando bordes superiores, 
    inferiores y laterales para simular el marco de un escenario de juego.

    Args:
        matriz: La matriz bidimensional de strings que representa el estado actual del mapa.
    """
    
    ancho_contenido = len(matriz[0]) * 2
    borde_horizontal = f"+{'-' * ancho_contenido}-+"

    print(borde_horizontal)
    
    for fila in matriz:
        
        contenido_fila = " ".join(fila)
        print(f"| {contenido_fila} |")

    print(borde_horizontal)

def mostrar_resultado_tiramonedas(puntaje_anterior: int, puntaje_actual: int, monto_apuesta: int, tirada: list[str]) -> None:
    """
    Muestra los 3 símbolos obtenidos y el veredicto final en la consola.
    """
    print(f"\n🎰 [ {' | '.join(tirada)} ] 🎰")
    
    if puntaje_actual == 0 and puntaje_anterior >= monto_apuesta:
        print("💥 ¡Combinación maldita! Perdiste todos tus fondos acumulados.")
    elif puntaje_actual > puntaje_anterior:
        premio = puntaje_actual - (puntaje_anterior - monto_apuesta)
        print(f"🎉 ¡Ganaste premio! Sumás {premio} puntos.")
    else:
        print("😢 No hubo suerte en este tiro.")