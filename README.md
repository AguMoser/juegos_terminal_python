# Casino y RPG en Consola (Python)

Aplicacion de consola que combina minijuegos de casino (Tragamonedas y Blackjack) y uno interactivo de exploración y combate (RPG)Guarda las partidas del RPG en un archivo local.

El desarrollo está estructurado de forma modular.

---
## Estructura del Código

```text
juegos-terminal-python/
├── main.py          # Punto de entrada, menú principal.
├── motor_rpg.py     # Lógica del mapa, movimientos y combates.
├── minijuegos.py    # Cálculos de Blackjack y Tragamonedas.
├── configuracion.py # Creación de personajes, estadísticas y enemigos.
├── interfaz.py      # Prints por pantalla, renderizado del mapa y tableros.
└── archivos.py      # Lectura y escritura del historial en formato CSV.

## Ejecucion

python main.py
