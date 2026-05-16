from salas import menu_salas
from clientes import menu_clientes
from empleados import menu_empleados
from reservas import menu_reservas
from records import registrar_resultado, ver_ranking
from estadisticas import ver_estadisticas


def menu_principal():
    """Menú principal del gestor. Se repite hasta que el admin elige salir."""

    while True:
        print("\n==============================")
        print("   GESTOR DE ESCAPE ROOM")
        print("==============================")
        print("1. Gestión de salas")
        print("2. Gestión de clientes")
        print("3. Gestión de empleados")
        print("4. Gestión de reservas")
        print("5. Registrar resultado de sesión")
        print("6. Ver ranking de récords")
        print("7. Ver estadísticas")
        print("8. Salir")
        print("------------------------------")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_salas()
        elif opcion == "2":
            menu_clientes()
        elif opcion == "3":
            menu_empleados()
        elif opcion == "4":
            menu_reservas()
        elif opcion == "5":
            registrar_resultado()
        elif opcion == "6":
            ver_ranking()
        elif opcion == "7":
            ver_estadisticas()
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Elige un número del 1 al 8.")