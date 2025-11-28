import pygame
import math
from .Color import *
from .sonidos import sistema_audio

class GameOver:
    """Pantalla de Game Over con estadísticas y opciones"""
    
    def __init__(self, pantalla, ancho, alto, puntuacion_final, tiempo_total, victoria):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.puntuacion_final = puntuacion_final
        self.tiempo_total = tiempo_total
        self.victoria = victoria
        
        # Reproducir sonido según el resultado
        if victoria:
            sistema_audio.reproducir_ganaste()
        else:
            sistema_audio.reproducir_perdiste()
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_subtitulo = pygame.font.Font(None, 48)
        self.fuente_estadistica = pygame.font.Font(None, 36)
        self.fuente_boton = pygame.font.Font(None, 32)
        
        # Crear botones y formatear tiempo
        self.crear_botones()
        self.tiempo_formateado = self.formatear_tiempo(tiempo_total)
        self.mouse_pos = (0, 0)
    
    def crear_botones(self):
        """Crea los botones de la pantalla"""
        centro_x = self.ancho // 2
        self.boton_reiniciar = pygame.Rect(centro_x - 120, 420, 240, 60)
        self.boton_menu = pygame.Rect(centro_x - 120, 500, 240, 60)
    
    def formatear_tiempo(self, tiempo_segundos):
        """Formatea tiempo en mm:ss"""
        if tiempo_segundos < 0:
            tiempo_segundos = 0
        minutos = int(tiempo_segundos // 60)
        segundos = int(tiempo_segundos % 60)
        return f"{minutos:02d}:{segundos:02d}"
    
    def manejar_evento(self, evento):
        """Maneja eventos de mouse y teclado"""
        if evento.type == pygame.MOUSEMOTION:
            self.mouse_pos = evento.pos
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Click izquierdo
                if self.boton_reiniciar.collidepoint(evento.pos):
                    return {"accion": "reiniciar"}
                elif self.boton_menu.collidepoint(evento.pos):
                    return {"accion": "menu"}
        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                return {"accion": "reiniciar"}
            elif evento.key == pygame.K_m or evento.key == pygame.K_ESCAPE:
                return {"accion": "menu"}
        
        return None
    
    def dibujar(self):
        """Dibuja todos los elementos de la pantalla"""
        # Fondo clarito con poca opacidad para ambos carteles (victoria y derrota)
        panel_fondo = pygame.Surface((self.ancho, self.alto))
        panel_fondo.set_alpha(80)  # Poca opacidad
        panel_fondo.fill(CREMA)  # Color clarito
        self.pantalla.blit(panel_fondo, (0, 0))
        
        # Título
        titulo = "¡VICTORIA!" if self.victoria else "GAME OVER"
        color_titulo = VERDE_EXITO if self.victoria else ROJO_PRINCIPAL
        texto_titulo = self.fuente_titulo.render(titulo, True, color_titulo)
        titulo_rect = texto_titulo.get_rect(center=(self.ancho // 2, 200))
        self.pantalla.blit(texto_titulo, titulo_rect)
        
        # Subtítulo
        subtitulo = "¡Felicitaciones! Completaste el juego" if self.victoria else "¡Inténtalo de nuevo!"
        texto_subtitulo = self.fuente_subtitulo.render(subtitulo, True, MARRON_OSCURO)
        subtitulo_rect = texto_subtitulo.get_rect(center=(self.ancho // 2, 260))
        self.pantalla.blit(texto_subtitulo, subtitulo_rect)
        
        # Estadísticas
        y_estadisticas = 320
        
        # Puntuación
        texto_puntuacion = f"Puntuación Final: {self.puntuacion_final}"
        render_puntuacion = self.fuente_estadistica.render(texto_puntuacion, True, MARRON_OSCURO)
        puntuacion_rect = render_puntuacion.get_rect(center=(self.ancho // 2, y_estadisticas))
        self.pantalla.blit(render_puntuacion, puntuacion_rect)
        
        # Tiempo
        texto_tiempo = f"Tiempo Jugado: {self.tiempo_formateado}"
        render_tiempo = self.fuente_estadistica.render(texto_tiempo, True, MARRON_OSCURO)
        tiempo_rect = render_tiempo.get_rect(center=(self.ancho // 2, y_estadisticas + 50))
        self.pantalla.blit(render_tiempo, tiempo_rect)
        
        # Botón Reiniciar
        color_reiniciar = AZUL_INFO if self.boton_reiniciar.collidepoint(self.mouse_pos) else GRIS_OSCURO
        pygame.draw.rect(self.pantalla, color_reiniciar, self.boton_reiniciar)
        pygame.draw.rect(self.pantalla, BLANCO, self.boton_reiniciar, 3)
        
        texto_reiniciar = self.fuente_boton.render("Jugar de Nuevo", True, BLANCO)
        reiniciar_rect = texto_reiniciar.get_rect(center=self.boton_reiniciar.center)
        self.pantalla.blit(texto_reiniciar, reiniciar_rect)
        
        # Botón Menú
        color_menu = AZUL_INFO if self.boton_menu.collidepoint(self.mouse_pos) else GRIS_OSCURO
        pygame.draw.rect(self.pantalla, color_menu, self.boton_menu)
        pygame.draw.rect(self.pantalla, BLANCO, self.boton_menu, 3)
        
        texto_menu = self.fuente_boton.render("Menú Principal", True, BLANCO)
        menu_rect = texto_menu.get_rect(center=self.boton_menu.center)
        self.pantalla.blit(texto_menu, menu_rect)
        
        # Decoración
        self.dibujar_decoracion()
    
    def dibujar_decoracion(self):
        """Dibuja decoración adicional"""
        if self.victoria:
            # Estrellas doradas para victoria
            self.dibujar_estrella(self.ancho // 2, 120, 20, AMARILLO_DORADO)
            self.dibujar_estrella(self.ancho // 2 - 80, 140, 15, AMARILLO_DORADO)
            self.dibujar_estrella(self.ancho // 2 + 80, 140, 15, AMARILLO_DORADO)
            self.dibujar_estrella(self.ancho // 2 - 120, 180, 12, AMARILLO_DORADO)
            self.dibujar_estrella(self.ancho // 2 + 120, 180, 12, AMARILLO_DORADO)
    
    def dibujar_estrella(self, x, y, radio, color):
        """Dibuja una estrella"""
        import math
        puntos = []
        for i in range(10):
            angulo = i * math.pi / 5
            if i % 2 == 0:
                r = radio
            else:
                r = radio * 0.5
            px = x + r * math.cos(angulo - math.pi / 2)
            py = y + r * math.sin(angulo - math.pi / 2)
            puntos.append((px, py))
        
        if len(puntos) >= 3:
            pygame.draw.polygon(self.pantalla, color, puntos)