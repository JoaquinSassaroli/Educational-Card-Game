import pygame
import os
import time
from .Color import *
from .Var import *

class Carta:
    """Representa una carta del juego con contenido y animaciones"""
    
    def __init__(self, x, y, ancho, alto, contenido, categoria):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.contenido = contenido
        self.categoria = categoria
        self.mostrar_frente = False
        self.eliminada = False
        
        # Estados adicionales para compatibilidad
        self.volteada = False
        self.encontrada = False
        self.incorrecta = False
        
        # Cargar sprites
        try:
            self.sprite_frente = pygame.image.load(os.path.join("Sprite", "Carta", "CartaFrente.png"))
            self.sprite_frente = pygame.transform.scale(self.sprite_frente, (ancho, alto))
        except:
            self.sprite_frente = pygame.Surface((ancho, alto))
            self.sprite_frente.fill(BLANCO)
        
        try:
            self.sprite_detras = pygame.image.load(os.path.join("Sprite", "Carta", "CartaDetras.png"))
            self.sprite_detras = pygame.transform.scale(self.sprite_detras, (ancho, alto))
        except:
            self.sprite_detras = pygame.Surface((ancho, alto))
            self.sprite_detras.fill(AZUL_INFO)
        
        self.fuente = pygame.font.Font(None, 28)
        self.tiempo_animacion = 0
        self.animando = False
    
    def voltear(self):
        """Voltea la carta"""
        self.mostrar_frente = not self.mostrar_frente
        self.volteada = self.mostrar_frente
    
    def mostrar(self):
        """Muestra el frente de la carta"""
        self.mostrar_frente = True
        self.volteada = True
    
    def ocultar(self):
        """Oculta el frente de la carta"""
        self.mostrar_frente = False
        self.volteada = False
    
    def mostrar_frente_temporal(self, duracion):
        """Muestra el frente temporalmente"""
        self.mostrar_frente = True
        self.tiempo_animacion = time.time() + duracion
        self.animando = True
    
    def actualizar(self):
        """Actualiza animaciones"""
        if self.animando and time.time() > self.tiempo_animacion:
            self.mostrar_frente = False
            self.animando = False
    
    def dibujar(self, pantalla):
        """Dibuja la carta"""
        if self.eliminada:
            return
        
        # Color de fondo según estado
        color_fondo = None
        if self.incorrecta:
            color_fondo = ROJO_PRINCIPAL
        # Removido el fondo verde para cartas encontradas
        
        if self.mostrar_frente:
            pantalla.blit(self.sprite_frente, self.rect)
            if color_fondo:
                overlay = pygame.Surface((self.rect.width, self.rect.height))
                overlay.set_alpha(128)
                overlay.fill(color_fondo)
                pantalla.blit(overlay, self.rect)
            
            # Manejar el contenido que puede ser una lista o un string
            if isinstance(self.contenido, list):
                # Si es una lista, tomar el primer elemento o unir con comas
                if len(self.contenido) == 1:
                    contenido_texto = str(self.contenido[0])
                else:
                    # Para listas con múltiples elementos, mostrar el más corto o el primero
                    contenido_texto = min(self.contenido, key=len) if self.contenido else ""
            else:
                contenido_texto = str(self.contenido)
            
            # Limpiar caracteres especiales de listas si quedaron
            contenido_texto = contenido_texto.replace("[", "").replace("]", "").replace("'", "").replace('"', '')
            
            # Si el contenido es muy largo, dividirlo en líneas
            if len(contenido_texto) > 18:
                # Dividir en palabras y crear líneas
                palabras = contenido_texto.split()
                lineas = []
                linea_actual = ""
                for palabra in palabras:
                    if len(linea_actual + " " + palabra) <= 18:
                        linea_actual += " " + palabra if linea_actual else palabra
                    else:
                        if linea_actual:
                            lineas.append(linea_actual)
                        linea_actual = palabra
                if linea_actual:
                    lineas.append(linea_actual)
                
                # Dibujar cada línea
                y_offset = self.rect.centery - (len(lineas) * 14) // 2
                for i, linea in enumerate(lineas):
                    texto = self.fuente.render(linea, True, NEGRO)
                    texto_rect = texto.get_rect(center=(self.rect.centerx, y_offset + i * 28))
                    pantalla.blit(texto, texto_rect)
            else:
                texto = self.fuente.render(contenido_texto, True, NEGRO)
                texto_rect = texto.get_rect(center=self.rect.center)
                pantalla.blit(texto, texto_rect)
        else:
            pantalla.blit(self.sprite_detras, self.rect)
            if color_fondo:
                overlay = pygame.Surface((self.rect.width, self.rect.height))
                overlay.set_alpha(128)
                overlay.fill(color_fondo)
                pantalla.blit(overlay, self.rect)
    
    def contiene_punto(self, punto):
        """Verifica si un punto está dentro de la carta"""
        return self.rect.collidepoint(punto)

class Cronometro:
    """Maneja el tiempo del juego"""
    
    def __init__(self, x, y, tiempo_inicial):
        self.rect = pygame.Rect(x, y, CRONOMETRO_ANCHO, CRONOMETRO_ALTO)
        self.tiempo_inicial = tiempo_inicial
        self.tiempo_restante = tiempo_inicial
        self.pausado = False
        self.ultimo_tiempo = time.time()
        
        # Cargar sprite
        try:
            self.sprite = pygame.image.load(os.path.join("Sprite", "Componentes", "Cronometro.png"))
            self.sprite = pygame.transform.scale(self.sprite, (CRONOMETRO_ANCHO, CRONOMETRO_ALTO))
        except:
            self.sprite = pygame.Surface((CRONOMETRO_ANCHO, CRONOMETRO_ALTO))
            self.sprite.fill(GRIS_OSCURO)
        
        self.fuente = pygame.font.Font(None, 45)
    
    def actualizar(self):
        """Actualiza el cronómetro"""
        if not self.pausado and self.tiempo_restante > 0:
            tiempo_actual = time.time()
            self.tiempo_restante -= tiempo_actual - self.ultimo_tiempo
            self.ultimo_tiempo = tiempo_actual
            if self.tiempo_restante < 0:
                self.tiempo_restante = 0
    
    def pausar(self):
        """Pausa el cronómetro"""
        self.pausado = True
    
    def reanudar(self):
        """Reanuda el cronómetro"""
        self.pausado = False
        self.ultimo_tiempo = time.time()
    
    def reiniciar(self, nuevo_tiempo):
        """Reinicia con nuevo tiempo"""
        self.tiempo_inicial = nuevo_tiempo
        self.tiempo_restante = nuevo_tiempo
        self.pausado = False
        self.ultimo_tiempo = time.time()
    
    def tiempo_agotado(self):
        """Verifica si el tiempo se agotó"""
        return self.tiempo_restante <= 0
    
    def obtener_tiempo_transcurrido(self):
        """Obtiene tiempo transcurrido"""
        return self.tiempo_inicial - self.tiempo_restante
    
    def dibujar(self, pantalla):
        """Dibuja el cronómetro"""
        # No dibujamos el sprite ya que está integrado en la imagen de fondo
        # Solo dibujamos el texto del tiempo
        
        minutos = int(self.tiempo_restante // 60)
        segundos = int(self.tiempo_restante % 60)
        tiempo_texto = f"{minutos:02d}:{segundos:02d}"
        
        color = ROJO_PRINCIPAL if self.tiempo_restante <= 10 else NEGRO
        texto = self.fuente.render(tiempo_texto, True, color)
        texto_rect = texto.get_rect(center=(self.rect.x + 115, self.rect.y + 30))
        pantalla.blit(texto, texto_rect)

class Puntuacion:
    """Maneja la puntuación del juego"""
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PUNTUACION_ANCHO, PUNTUACION_ALTO)
        self.puntos = 0
        
        # Cargar sprite
        try:
            self.sprite = pygame.image.load(os.path.join("Sprite", "Componentes", "Puntuacion.png"))
            self.sprite = pygame.transform.scale(self.sprite, (PUNTUACION_ANCHO, PUNTUACION_ALTO))
        except:
            self.sprite = pygame.Surface((PUNTUACION_ANCHO, PUNTUACION_ALTO))
            self.sprite.fill(GRIS_OSCURO)
        
        self.fuente = pygame.font.Font(None, 45)
    
    def sumar_puntos(self, cantidad):
        """Suma puntos"""
        self.puntos += cantidad
    
    def restar_puntos(self, cantidad):
        """Resta puntos"""
        self.puntos -= cantidad
    
    def reiniciar(self):
        """Reinicia puntuación"""
        self.puntos = 0
    
    def obtener_puntos(self):
        """Obtiene puntos actuales"""
        return self.puntos
    
    def dibujar(self, pantalla):
        """Dibuja la puntuación"""
        # No dibujamos el sprite ya que está integrado en la imagen de fondo
        # Solo dibujamos el texto de la puntuación
        
        texto = self.fuente.render(str(self.puntos), True, NEGRO)
        texto_rect = texto.get_rect(center=(self.rect.x + 132, self.rect.y + 30))
        pantalla.blit(texto, texto_rect)