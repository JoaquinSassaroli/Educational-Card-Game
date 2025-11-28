"""
Archivo de configuración del juego
Contiene los datos de las materias, cartas y configuraciones del juego
"""

from .preguntas_parejas import DATOS_MATERIAS

# Configuración para el modo Parejas
CONFIG_PAREJAS = {
    "puntos_acierto": 50,
    "puntos_error": -25,
    "tiempo_cronometro": 120,
    "cartas_por_nivel": 6
}

# Configuración del juego Intruso
CONFIG_INTRUSO = {
    "cartas_por_nivel": 6,
    "tiempo_cronometro": {
        1: 30,  # Nivel 1: 30 segundos
        2: 25,  # Nivel 2: 25 segundos
        3: 20,  # Nivel 3: 20 segundos
        4: 15,  # Nivel 4: 15 segundos
        5: 10   # Nivel 5: 10 segundos
    },
    "tiempo_espera_nivel": 5,           # Tiempo de espera entre niveles (5 segundos)
    "puntos_acierto": 75,              # Puntos por encontrar el intruso
    "puntos_error": -30,                # Puntos que se restan por error
    "puntos_tiempo_bonus": 10,          # Puntos bonus por segundo restante
    "niveles_maximos": 5
}

# Configuración de la ventana
CONFIG_VENTANA = {
    "ancho": 1024,
    "alto": 768,
    "fps": 60,
    "titulo": "Cartas en Juego"
}

# Configuración de colores
COLORES = {
    "fondo": (50, 100, 150),
    "carta_frente": (255, 255, 255),
    "carta_atras": (70, 130, 180),
    "texto": (0, 0, 0),
    "texto_blanco": (255, 255, 255),
    "boton": (70, 130, 180),
    "boton_hover": (100, 149, 237),
    "boton_seleccionado": (255, 215, 0),
    "cronometro_normal": (255, 255, 255),
    "cronometro_alerta": (255, 0, 0)
}

# Configuración de dimensiones
DIMENSIONES = {
    "carta_ancho": 120,
    "carta_alto": 160,
    "margen_cartas": 20,
    "cronometro_ancho": 200,
    "cronometro_alto": 80,
    "puntuacion_ancho": 200,
    "puntuacion_alto": 80
}