from minijuegos import (
    procesar_jugada_tiramonedas, 
    procesar_jugada_blackjack, 
    validar_es_numero, 
    validar_monto_apuesta
)
from interfaz import mostrar_resultado_tiramonedas
from motor_rpg import iniciar_modulo_rpg

puntaje = 100
apuesta = 10

opciones_apuesta = ["A", "B", "C", "D", "E", "0", "7"]
mazo_de_cartas = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

menu = """
------- MENU DE JUEGO --------
1- Jugar Tragamonedas
2- Jugar Blackjack
3- Modificar apuesta
4- Jugar RPG
5- Salir
Seleccione una opción: 
------------------------------
"""

while True:
    
    if puntaje <= 0:
        print("\n[ Casino ] Te quedaste sin fondos! Gracias por jugar.")
        break

    print(f"\n[ SALDO ACTUAL: {puntaje} | APUESTA: {apuesta} ]")
    opcion_elegida = input(menu)

    match opcion_elegida:
        
        case "1":
            if puntaje >= apuesta:                
                puntaje_anterior = puntaje 
                puntaje, tirada = procesar_jugada_tiramonedas(puntaje, apuesta, opciones_apuesta)
                mostrar_resultado_tiramonedas(puntaje_anterior, puntaje, apuesta, tirada)
            else:
                print("❌ Saldo insuficiente para la apuesta actual.")

        case "2":
            if puntaje >= apuesta:                
                puntaje = procesar_jugada_blackjack(puntaje, apuesta, mazo_de_cartas)
            else:
                print("❌ Saldo insuficiente para jugar Blackjack.")

        case "3":
            entrada_apuesta = input("Ingrese nueva apuesta: ")           
           
            if validar_es_numero(entrada_apuesta) == True:
                nueva_apuesta = int(entrada_apuesta)             
                if validar_monto_apuesta(nueva_apuesta, puntaje):
                    apuesta = nueva_apuesta
                    print(f"✅ Apuesta actualizada a: {apuesta}!")
                else:
                    print(f"\n ❌ Apuesta inválida. Debe ser entre 1 y tu saldo actual ({puntaje}).")
            else:
                print("❌ Error: Por favor, ingrese un número entero válido.")
        case "4":
            
            iniciar_modulo_rpg()
        case "5":
            print("Gracias por jugar. Hasta la próxima!😊")
            break
            
        case _:
            print("❌ Opción inválida. Por favor, seleccione una opción del 1 al 4.")