import pygame
import random
import time
import os
from .Core import Carta, Cronometro, Puntuacion
from .config import DATOS_MATERIAS, CONFIG_PAREJAS
from .Color import *
from .Var import *
from .sonidos import sistema_audio

class ModoParejas:
    def __init__(self, pantalla, ancho, alto, materias_seleccionadas=None):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        
        # Materias a usar en el juego
        if materias_seleccionadas is None:
            self.materias_seleccionadas = ["Matemáticas"]  # Por defecto
        else:
            self.materias_seleccionadas = materias_seleccionadas
        
        # Estado del juego
        self.nivel_actual = 1
        self.parejas_encontradas = 0
        self.cartas_seleccionadas = []
        self.tiempo_mostrar_cartas = 0
        self.mostrando_cartas_inicial = True
        self.esperando_volteo = False
        self.tiempo_espera_volteo = 0
        self.esperando_siguiente_nivel = False
        self.tiempo_espera_nivel = 0
        
        # Tiempo total acumulado
        self.tiempo_total_acumulado = 0
        self.tiempo_inicio_juego = time.time()
        
        # Cargar imagen de fondo con mejor calidad
        try:
            self.fondo_partida = pygame.image.load(os.path.join("Sprite", "Fondo", "fondominijuego.png")).convert_alpha()
            # Usar smoothscale para mejor calidad de escalado
            self.fondo_partida = pygame.transform.smoothscale(self.fondo_partida, (ancho, alto))
        except:
            self.fondo_partida = None
        
        # Componentes - Posiciones ajustadas para los componentes integrados en la imagen
        # Cronómetro en la esquina superior derecha
        self.cronometro = Cronometro(814, 160, PAREJAS_TIEMPO_CRONOMETRO)
        # Puntuación en la esquina superior izquierda
        self.puntuacion = Puntuacion(30, 160)
        
        # Crear tablero
        self.crear_tablero()
        self.iniciar_visualizacion_inicial()
    
    def crear_tablero(self):
        # Obtener datos de las materias seleccionadas
        materia_idx = random.randint(0, len(self.materias_seleccionadas) - 1)
        self.materia_actual = self.materias_seleccionadas[materia_idx]  # Almacenar la materia seleccionada
        datos_materia = DATOS_MATERIAS[self.materia_actual]
        
        # Seleccionar 3 pares aleatorios
        pares_disponibles = list(datos_materia.items())
        pares_seleccionados = random.sample(pares_disponibles, 3)
        
        # Crear lista de cartas (2 de cada par) - Total: 6 cartas
        cartas_datos = []
        for pregunta, respuestas in pares_seleccionados:
            # Si respuestas es una lista, seleccionar una respuesta aleatoria
            if isinstance(respuestas, list):
                respuesta_seleccionada = random.choice(respuestas)
            else:
                respuesta_seleccionada = respuestas
            
            cartas_datos.append(("pregunta", pregunta))
            cartas_datos.append(("respuesta", respuesta_seleccionada))
        
        # Mezclar las cartas
        random.shuffle(cartas_datos)
        
        # Crear tablero 2x3 (2 filas, 3 columnas) - Total: 6 posiciones
        self.tablero = []
        self.cartas = []
        
        # Calcular posiciones
        margen_x = (self.ancho - (PAREJAS_COLUMNAS * CARTA_ANCHO + (PAREJAS_COLUMNAS - 1) * CARTA_ESPACIADO)) // 2
        margen_y = (self.alto - (PAREJAS_FILAS * CARTA_ALTO + (PAREJAS_FILAS - 1) * CARTA_ESPACIADO)) // 2 + 50
        
        for fila in range(PAREJAS_FILAS):
            fila_cartas = []
            for col in range(PAREJAS_COLUMNAS):
                idx = fila * PAREJAS_COLUMNAS + col
                tipo, contenido = cartas_datos[idx]
                
                x = margen_x + col * (CARTA_ANCHO + CARTA_ESPACIADO)
                y = margen_y + fila * (CARTA_ALTO + CARTA_ESPACIADO)
                
                carta = Carta(x, y, CARTA_ANCHO, CARTA_ALTO, contenido, tipo)
                fila_cartas.append(carta)
                self.cartas.append(carta)
            
            self.tablero.append(fila_cartas)
    
    def iniciar_visualizacion_inicial(self):
        # Mostrar todas las cartas por 3 segundos
        for carta in self.cartas:
            carta.mostrar()
        self.tiempo_mostrar_cartas = pygame.time.get_ticks()
        self.mostrando_cartas_inicial = True
    
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and not self.mostrando_cartas_inicial and not self.esperando_volteo and not self.esperando_siguiente_nivel:
            pos = pygame.mouse.get_pos()
            
            # Verificar clic en cartas
            for carta in self.cartas:
                if carta.rect.collidepoint(pos) and not carta.volteada and not carta.encontrada:
                    self.seleccionar_carta(carta)
                    break
        
        return None
    
    def seleccionar_carta(self, carta):
        # Voltear carta
        carta.voltear()
        self.cartas_seleccionadas.append(carta)
        
        # Si hay 2 cartas seleccionadas
        if len(self.cartas_seleccionadas) == 2:
            carta1, carta2 = self.cartas_seleccionadas
            
            if self.es_pareja(carta1, carta2):
                # Es pareja - marcar como encontradas
                carta1.encontrada = True
                carta2.encontrada = True
                self.parejas_encontradas += 1
                self.puntuacion.sumar_puntos(CONFIG_PAREJAS["puntos_acierto"])
                
                # Reproducir sonido de acierto
                sistema_audio.reproducir_correcto()
                
                # Verificar si se completó el nivel
                if self.parejas_encontradas == 3:
                    if self.nivel_actual < PAREJAS_NIVELES_MAX:
                        # Iniciar delay de 2 segundos antes del siguiente nivel
                        self.esperando_siguiente_nivel = True
                        self.tiempo_espera_nivel = pygame.time.get_ticks()
                    else:
                        # Último nivel completado - ir directo a game over
                        self.completar_nivel()
                
                self.cartas_seleccionadas = []
            else:
                # No es pareja - esperar antes de voltear
                # Restar puntos por error
                self.puntuacion.restar_puntos(abs(CONFIG_PAREJAS["puntos_error"]))
                # Reproducir sonido de error
                sistema_audio.reproducir_incorrecto()
                self.esperando_volteo = True
                self.tiempo_espera_volteo = pygame.time.get_ticks()
    
    def es_pareja(self, carta1, carta2):
        # Verificar si las cartas forman una pareja
        if carta1.categoria == carta2.categoria:
            return False
        
        # Buscar solo en los datos de la materia actual
        materia_datos = DATOS_MATERIAS[self.materia_actual]
        for pregunta, respuestas in materia_datos.items():
            # Si respuestas es una lista, verificar contra todos los elementos
            if isinstance(respuestas, list):
                for respuesta in respuestas:
                    if ((carta1.contenido == pregunta and carta2.contenido == respuesta) or
                        (carta1.contenido == respuesta and carta2.contenido == pregunta)):
                        return True
            else:
                # Si respuestas es un string simple
                if ((carta1.contenido == pregunta and carta2.contenido == respuestas) or
                    (carta1.contenido == respuestas and carta2.contenido == pregunta)):
                    return True
        return False
    
    def completar_nivel(self):
        # Sumar tiempo del nivel actual al acumulado
        tiempo_nivel = self.cronometro.obtener_tiempo_transcurrido()
        self.tiempo_total_acumulado += tiempo_nivel
        
        if self.nivel_actual < PAREJAS_NIVELES_MAX:
            # Avanzar al siguiente nivel
            self.nivel_actual += 1
            self.parejas_encontradas = 0
            self.cartas_seleccionadas = []
            self.esperando_siguiente_nivel = False
            self.cronometro.reiniciar(PAREJAS_TIEMPO_CRONOMETRO)
            self.crear_tablero()
            self.iniciar_visualizacion_inicial()
        else:
            # Juego completado
            return {
                "estado": "game_over",
                "victoria": True,
                "puntuacion": self.puntuacion.puntos,
                "tiempo": self.tiempo_total_acumulado
            }
    
    def actualizar(self):
        # Actualizar cronómetro
        self.cronometro.actualizar()
        
        # Verificar tiempo agotado
        if self.cronometro.tiempo_agotado():
            # Sumar tiempo del nivel actual al acumulado
            tiempo_nivel = self.cronometro.obtener_tiempo_transcurrido()
            self.tiempo_total_acumulado += tiempo_nivel
            
            return {
                "estado": "game_over",
                "victoria": False,
                "puntuacion": self.puntuacion.puntos,
                "tiempo": self.tiempo_total_acumulado
            }
        
        # Verificar si se completó el nivel (esto puede retornar game_over)
        resultado_nivel = None
        if self.parejas_encontradas == 3 and self.nivel_actual == PAREJAS_NIVELES_MAX:
            resultado_nivel = self.completar_nivel()
            if resultado_nivel:
                return resultado_nivel
        
        # Manejar visualización inicial
        if self.mostrando_cartas_inicial:
            if pygame.time.get_ticks() - self.tiempo_mostrar_cartas > 3000:
                # Ocultar todas las cartas
                for carta in self.cartas:
                    carta.ocultar()
                self.mostrando_cartas_inicial = False
        
        # Manejar espera de volteo
        if self.esperando_volteo:
            if pygame.time.get_ticks() - self.tiempo_espera_volteo > 1000:
                # Voltear cartas no encontradas
                for carta in self.cartas_seleccionadas:
                    if not carta.encontrada:
                        carta.voltear()
                self.cartas_seleccionadas = []
                self.esperando_volteo = False
        
        # Manejar espera entre niveles (delay de 3 segundos)
        if self.esperando_siguiente_nivel:
            if pygame.time.get_ticks() - self.tiempo_espera_nivel > 3000:
                self.completar_nivel()
        
        return None
    
    def dibujar(self):
        # Fondo
        if self.fondo_partida:
            self.pantalla.blit(self.fondo_partida, (0, 0))
        else:
            self.pantalla.fill(CREMA)
        
        # Dibujar componentes
        self.cronometro.dibujar(self.pantalla)
        self.puntuacion.dibujar(self.pantalla)
        
        # Información del nivel
        fuente = pygame.font.Font(None, 36)
        texto_nivel = fuente.render(f"Nivel: {self.nivel_actual}", True, GRIS_CLARO)
        self.pantalla.blit(texto_nivel, (self.ancho // 2 - 50, 20))
        
        # Dibujar tablero
        for fila in self.tablero:
            for carta in fila:
                carta.dibujar(self.pantalla)
        
        # Mensaje durante visualización inicial
        if self.mostrando_cartas_inicial:
            fuente_mensaje = pygame.font.Font(None, 48)
            texto_mensaje = fuente_mensaje.render("¡Memoriza las cartas!", True, ROJO_PRINCIPAL)
            texto_rect = texto_mensaje.get_rect(center=(self.ancho // 2, self.alto - 50))
            self.pantalla.blit(texto_mensaje, texto_rect)
        
        # Contador visual para siguiente nivel (solo si no es el último nivel)
        if self.esperando_siguiente_nivel and self.nivel_actual < PAREJAS_NIVELES_MAX:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_espera_nivel
            segundos_restantes = max(0, 3 - (tiempo_transcurrido // 1000))
            
            fuente_contador = pygame.font.Font(None, 36)
            texto_contador = fuente_contador.render(f"Siguiente nivel en {segundos_restantes} segundos", True, VERDE_EXITO)
            contador_rect = texto_contador.get_rect(center=(self.ancho // 2, self.alto - 80))
            self.pantalla.blit(texto_contador, contador_rect)