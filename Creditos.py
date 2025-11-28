# Créditos del Juego de Cartas Alpha

INFORMACION_JUEGO = {
    "nombre": "Juego de Cartas Alpha",
    "version": "1.0.0",
    "descripcion": "Juego de memoria y concentración con dos modos: Parejas e Intruso",
    "tecnologia": "Python 3 + Pygame",
    "año": "2024"
}

INFORMACION_AUTORES = {
    "universidad": "Universidad Abierta Interamericana",
    "año_cursada": "3er año",
    "comision": "Comisión A",
    "turno": "Turno Noche",
    "sede": "Lomas de Zamora",
    "integrantes": [
        "Sassaroli Joaquín",
        "Siffredi Agustín", 
        "San Martín Santiago",
        "Smyth Lautaro"
    ]
}

def mostrar_creditos():
    """Muestra los créditos del juego en consola"""
    print(f"\n{'='*50}")
    print(f"  {INFORMACION_JUEGO['nombre']} v{INFORMACION_JUEGO['version']}")
    print(f"{'='*50}")
    print(f"Descripción: {INFORMACION_JUEGO['descripcion']}")
    print(f"Tecnología: {INFORMACION_JUEGO['tecnologia']}")
    print(f"Año: {INFORMACION_JUEGO['año']}")
    print(f"\n{'='*50}")
    print("  EQUIPO DE DESARROLLO")
    print(f"{'='*50}")
    print(f"Universidad: {INFORMACION_AUTORES['universidad']}")
    print(f"Año: {INFORMACION_AUTORES['año_cursada']}")
    print(f"Comisión: {INFORMACION_AUTORES['comision']}")
    print(f"Turno: {INFORMACION_AUTORES['turno']}")
    print(f"Sede: {INFORMACION_AUTORES['sede']}")
    print(f"\nIntegrantes:")
    for integrante in INFORMACION_AUTORES['integrantes']:
        print(f"  • {integrante}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    mostrar_creditos()