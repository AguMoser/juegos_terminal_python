import csv

def leer_historial_partidas(nombre_archivo: str) -> list[list[str]]:
    """
    Abre el archivo de historial en modo lectura y parsea el contenido CSV de forma segura.

    Args:
        nombre_archivo: La ruta o nombre del archivo CSV que contiene los registros.

    Returns:
        Una lista de listas, donde cada sublista representa una fila válida con los datos de una partida. 
        Devuelve una lista vacía si el archivo no existe o si ocurre un error de lectura.     
    """
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            
            lector_csv = csv.reader(archivo)
            return [fila for fila in lector_csv if fila]
                    
    except FileNotFoundError:
        print("Aviso: El archivo de historial no existe todavía.")
    except OSError:
        print("❌ Error al intentar leer el archivo de historial.")
        
    return []

def registrar_partida_csv(nombre_jugador: str, clase: str, resultado: str, turnos_jugados: int) -> None:
    """
    Registra los datos estadísticos finales de una partida en un archivo CSV usando el escritor nativo.

    Args:
        nombre_jugador: El nombre que el usuario le dio a su personaje.
        clase: La clase seleccionada para jugar (Guerrero, Arquero o Mago).
        resultado: El estado final de la partida ("Victoria", "Derrota" o "Abandono").
        turnos_jugados: La cantidad total de movimientos realizados durante la partida.
    """
    ruta_historial = "historial_partidas.csv"

    try:
        with open(ruta_historial, "a", newline="", encoding="utf-8") as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow([nombre_jugador, clase, resultado, turnos_jugados])
            
        print("💾 Partida guardada correctamente.")

    except OSError:
        print("❌ Error de escritura: No se pudo guardar la partida.")