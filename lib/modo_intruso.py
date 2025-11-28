import pygame
import random
import time
import os
from .Core import Carta, Cronometro, Puntuacion
from .config import DATOS_MATERIAS, CONFIG_INTRUSO
from .preguntas_intruso import PREGUNTAS_INTRUSO
from .Color import *
from .Var import *
from .sonidos import sistema_audio

class ModoIntruso:
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
        self.intruso_encontrado = False
        self.esperando_siguiente_nivel = False
        self.tiempo_espera_nivel = 0
        
        # Cargar imagen de fondo con mejor calidad
        try:
            self.fondo_partida = pygame.image.load(os.path.join("Sprite", "Fondo", "fondominijuego.png")).convert_alpha()
            # Usar smoothscale para mejor calidad de escalado
            self.fondo_partida = pygame.transform.smoothscale(self.fondo_partida, (ancho, alto))
        except:
            self.fondo_partida = None
        
        # Componentes - Posiciones ajustadas para los componentes integrados en la imagen
        # Cronómetro en la esquina superior derecha
        self.cronometro = Cronometro(814, 160, INTRUSO_TIEMPO_CRONOMETRO[1])  # Usar tiempo del nivel 1
        # Puntuación en la esquina superior izquierda
        self.puntuacion = Puntuacion(30, 160)
        
        # Crear nivel
        self.crear_nivel()
    
    def crear_nivel(self):
        # Obtener la materia seleccionada (solo una)
        materia_principal = self.materias_seleccionadas[0]
        
        # Generar contenido temático según la materia
        if materia_principal == "Matemáticas":
            contenidos, indice_intruso, categoria_mayoria = self.generar_matematicas_intruso()
        elif materia_principal == "Historia":
            contenidos, indice_intruso, categoria_mayoria = self.generar_historia_intruso()
        elif materia_principal == "Química":
            contenidos, indice_intruso, categoria_mayoria = self.generar_quimica_intruso()
        elif materia_principal == "Geografía":
            contenidos, indice_intruso, categoria_mayoria = self.generar_geografia_intruso()
        else:
            # Fallback al método anterior si no hay implementación específica
            contenidos, indice_intruso = self.generar_intruso_generico(materia_principal)
            categoria_mayoria = "elementos"
        
        # Guardar índice del intruso y categoría
        self.indice_intruso = indice_intruso
        self.categoria_mayoria = categoria_mayoria
        
        # Crear cartas
        self.cartas = []
        
        # Calcular posiciones (2 filas x 3 columnas)
        margen_x = (self.ancho - (3 * CARTA_ANCHO + 2 * CARTA_ESPACIADO)) // 2
        margen_y = (self.alto - (2 * CARTA_ALTO + CARTA_ESPACIADO)) // 2 + 50
        
        for i, contenido in enumerate(contenidos):
            fila = i // 3
            col = i % 3
            
            x = margen_x + col * (CARTA_ANCHO + CARTA_ESPACIADO)
            y = margen_y + fila * (CARTA_ALTO + CARTA_ESPACIADO)
            
            # Determinar tipo
            tipo = "intruso" if i == self.indice_intruso else "normal"
            carta = Carta(x, y, CARTA_ANCHO, CARTA_ALTO, contenido, tipo)
            carta.mostrar()  # Las cartas están siempre visibles
            self.cartas.append(carta)
    
    def generar_matematicas_intruso(self):
        """Genera contenido matemático con un intruso sutil"""
        opciones = PREGUNTAS_INTRUSO["Matemáticas"]
        
        # Seleccionar una opción aleatoria
        normales, intruso, categoria = random.choice(opciones)
        
        # Crear lista final mezclada
        contenidos = normales + [intruso]
        random.shuffle(contenidos)
        
        # Encontrar índice del intruso
        indice_intruso = contenidos.index(intruso)
        
        return contenidos, indice_intruso, categoria
    
    def generar_historia_intruso(self):
        """Genera contenido histórico con un intruso sutil"""
        opciones = PREGUNTAS_INTRUSO["Historia"]
        
        normales, intruso, categoria = random.choice(opciones)
        contenidos = normales + [intruso]
        random.shuffle(contenidos)
        indice_intruso = contenidos.index(intruso)
        
        return contenidos, indice_intruso, categoria
    
    def generar_quimica_intruso(self):
        """Genera contenido químico con un intruso sutil"""
        opciones = PREGUNTAS_INTRUSO["Química"]
        
        normales, intruso, categoria = random.choice(opciones)
        contenidos = normales + [intruso]
        random.shuffle(contenidos)
        indice_intruso = contenidos.index(intruso)
        
        return contenidos, indice_intruso, categoria
    
    def generar_geografia_intruso(self):
        """Genera contenido geográfico con un intruso sutil"""
        opciones = PREGUNTAS_INTRUSO["Geografía"]
        
        normales, intruso, categoria = random.choice(opciones)
        contenidos = normales + [intruso]
        random.shuffle(contenidos)
        indice_intruso = contenidos.index(intruso)
        
        return contenidos, indice_intruso, categoria
    
    def generar_intruso_generico(self, materia_principal):
        """Método de fallback usando el sistema anterior"""
        # Usar todas las materias disponibles para seleccionar una diferente como intrusa
        todas_materias = list(DATOS_MATERIAS.keys())
        materias_restantes = [m for m in todas_materias if m != materia_principal]
        materia_intrusa = random.choice(materias_restantes)
        
        # Obtener datos
        datos_principal = DATOS_MATERIAS[materia_principal]
        datos_intruso = DATOS_MATERIAS[materia_intrusa]
        
        # Seleccionar 5 elementos de la materia principal
        elementos_principales = random.sample(list(datos_principal.keys()), 5)
        
        # Seleccionar 1 elemento intruso
        elemento_intruso = random.choice(list(datos_intruso.keys()))
        
        # Crear lista de contenidos
        contenidos = elementos_principales + [elemento_intruso]
        random.shuffle(contenidos)
        
        # Encontrar índice del intruso
        indice_intruso = contenidos.index(elemento_intruso)
        
        return contenidos, indice_intruso, "elementos"
    
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and not self.esperando_siguiente_nivel:
            pos = pygame.mouse.get_pos()
            
            # Verificar clic en cartas
            for i, carta in enumerate(self.cartas):
                if carta.rect.collidepoint(pos):
                    return self.seleccionar_carta(i, carta)
        
        return None
    
    def seleccionar_carta(self, indice, carta):
        if indice == self.indice_intruso:
            # Intruso encontrado
            self.intruso_encontrado = True
            self.puntuacion.sumar_puntos(CONFIG_INTRUSO["puntos_acierto"])
            carta.encontrada = True
            
            # Reproducir sonido de acierto
            sistema_audio.reproducir_correcto()
            
            if self.nivel_actual < INTRUSO_NIVELES_MAX:
                # Avanzar al siguiente nivel
                self.esperando_siguiente_nivel = True
                self.tiempo_espera_nivel = pygame.time.get_ticks()
            else:
                # Juego completado
                return {
                    "estado": "game_over",
                    "victoria": True,
                    "puntuacion": self.puntuacion.puntos,
                    "tiempo": self.cronometro.obtener_tiempo_transcurrido()
                }
        else:
            # Carta incorrecta
            self.puntuacion.restar_puntos(abs(CONFIG_INTRUSO["puntos_error"]))
            # Removido: carta.incorrecta = True  # No queremos el efecto visual rojo
            
            # Reproducir sonido de error
            sistema_audio.reproducir_incorrecto()
        
        return None
    
    def avanzar_nivel(self):
        # Avanzar al siguiente nivel
        self.nivel_actual += 1
        self.intruso_encontrado = False
        self.esperando_siguiente_nivel = False
        # Usar el tiempo correspondiente al nivel actual
        tiempo_nivel = INTRUSO_TIEMPO_CRONOMETRO.get(self.nivel_actual, 10)  # 10 segundos por defecto
        self.cronometro.reiniciar(tiempo_nivel)
        self.crear_nivel()
    
    def actualizar(self):
        # Actualizar cronómetro
        self.cronometro.actualizar()
        
        # Verificar tiempo agotado
        if self.cronometro.tiempo_agotado():
            return {
                "estado": "game_over",
                "victoria": False,
                "puntuacion": self.puntuacion.puntos,
                "tiempo": self.cronometro.obtener_tiempo_transcurrido()
            }
        
        # Manejar espera entre niveles
        if self.esperando_siguiente_nivel:
            if pygame.time.get_ticks() - self.tiempo_espera_nivel > 2000:
                self.avanzar_nivel()
        
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
        
        # Instrucciones
        fuente_instruccion = pygame.font.Font(None, 32)
        texto_instruccion = fuente_instruccion.render(f"Encuentra el intruso entre {self.categoria_mayoria}:", True, ROJO_PRINCIPAL)
        instruccion_rect = texto_instruccion.get_rect(center=(self.ancho // 2, 120))
        self.pantalla.blit(texto_instruccion, instruccion_rect)
        
        # Dibujar cartas
        for carta in self.cartas:
            carta.dibujar(self.pantalla)
        
        # Mensaje de nivel completado
        if self.esperando_siguiente_nivel:
            fuente_mensaje = pygame.font.Font(None, 48)
            texto_mensaje = fuente_mensaje.render("¡Correcto! Siguiente nivel...", True, VERDE_EXITO)
            mensaje_rect = texto_mensaje.get_rect(center=(self.ancho // 2, self.alto - 50))
            self.pantalla.blit(texto_mensaje, mensaje_rect)