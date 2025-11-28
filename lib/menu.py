import pygame
import os
from .Color import *
from .Var import *
from .sonidos import sistema_audio

class Menu:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        
        # Iniciar música de fondo del menú
        sistema_audio.iniciar_musica_menu()
        
        # Cargar imagen de fondo del menú con mejor calidad
        try:
            self.fondo_menu = pygame.image.load(os.path.join("Sprite", "Fondo", "fondomenu.png")).convert_alpha()
            # Usar smoothscale para mejor calidad de escalado
            self.fondo_menu = pygame.transform.smoothscale(self.fondo_menu, (ancho, alto))
        except:
            self.fondo_menu = None
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_subtitulo = pygame.font.Font(None, 48)
        self.fuente_boton = pygame.font.Font(None, 36)
        self.fuente_texto = pygame.font.Font(None, 32)
        
        # Opciones de juego
        self.modos = ["Parejas", "Intruso"]
        self.materias = ["Matemáticas", "Historia", "Química", "Geografía"]
        
        # Selecciones actuales
        self.modo_seleccionado = 0
        self.materia_seleccionada = 0  # Índice de la materia seleccionada (por defecto Matemáticas)
        
        # Crear botones
        self.crear_botones()
    
    def crear_botones(self):
        # Botones de modo
        self.botones_modo = []
        for i, modo in enumerate(self.modos):
            x = self.ancho // 2 - 200 + i * 200
            y = 250
            rect = pygame.Rect(x, y, 180, 50)
            self.botones_modo.append(rect)
        
        # Botones de materia
        self.botones_materia = []
        for i, materia in enumerate(self.materias):
            x = self.ancho // 2 - 400 + i * 200
            y = 350
            rect = pygame.Rect(x, y, 180, 50)
            self.botones_materia.append(rect)
        
        # Botones de acción
        self.boton_jugar = pygame.Rect(self.ancho // 2 - 100, 450, 200, 60)
        self.boton_salir = pygame.Rect(self.ancho // 2 - 100, 530, 200, 60)
    
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Verificar botones de modo
            for i, boton in enumerate(self.botones_modo):
                if boton.collidepoint(pos):
                    self.modo_seleccionado = i
            
            # Verificar botones de materia (selección única)
            for i, boton in enumerate(self.botones_materia):
                if boton.collidepoint(pos):
                    self.materia_seleccionada = i
            
            # Verificar botón jugar
            if self.boton_jugar.collidepoint(pos):
                # Reproducir sonido de iniciar juego
                sistema_audio.reproducir_iniciar_juego()
                # Obtener materia seleccionada
                materia_activa = [self.materias[self.materia_seleccionada]]
                modo = self.modos[self.modo_seleccionado].lower()
                return {
                    "accion": modo,
                    "materias": materia_activa
                }
            
            # Verificar botón salir
            if self.boton_salir.collidepoint(pos):
                return {"accion": "salir"}
        
        return None
    
    def dibujar(self):
        # Fondo
        if self.fondo_menu:
            self.pantalla.blit(self.fondo_menu, (0, 0))
        else:
            self.pantalla.fill(MARRON_OSCURO)
        
        # Subtítulo modo
        subtitulo_modo = self.fuente_subtitulo.render("Selecciona Modo:", True, BLANCO)
        subtitulo_modo_rect = subtitulo_modo.get_rect(center=(self.ancho // 2, 200))
        self.pantalla.blit(subtitulo_modo, subtitulo_modo_rect)
        
        # Botones de modo
        for i, (boton, modo) in enumerate(zip(self.botones_modo, self.modos)):
            color = AMARILLO_DORADO if i == self.modo_seleccionado else CORAL
            pygame.draw.rect(self.pantalla, color, boton)
            pygame.draw.rect(self.pantalla, NEGRO, boton, 2)
            
            texto = self.fuente_boton.render(modo, True, NEGRO)
            texto_rect = texto.get_rect(center=boton.center)
            self.pantalla.blit(texto, texto_rect)
        
        # Subtítulo materia
        subtitulo_materia = self.fuente_subtitulo.render("Selecciona Materia:", True, BLANCO)
        subtitulo_materia_rect = subtitulo_materia.get_rect(center=(self.ancho // 2, 320))
        self.pantalla.blit(subtitulo_materia, subtitulo_materia_rect)
        
        # Botones de materia
        for i, (boton, materia) in enumerate(zip(self.botones_materia, self.materias)):
            color = AMARILLO_DORADO if i == self.materia_seleccionada else CORAL
            pygame.draw.rect(self.pantalla, color, boton)
            pygame.draw.rect(self.pantalla, NEGRO, boton, 2)
            
            texto = self.fuente_texto.render(materia, True, NEGRO)
            texto_rect = texto.get_rect(center=boton.center)
            self.pantalla.blit(texto, texto_rect)
        
        # Botón jugar
        pygame.draw.rect(self.pantalla, ROJO_PRINCIPAL, self.boton_jugar)
        pygame.draw.rect(self.pantalla, NEGRO, self.boton_jugar, 3)
        texto_jugar = self.fuente_boton.render("JUGAR", True, BLANCO)
        texto_jugar_rect = texto_jugar.get_rect(center=self.boton_jugar.center)
        self.pantalla.blit(texto_jugar, texto_jugar_rect)
        
        # Botón salir
        pygame.draw.rect(self.pantalla, GRIS_OSCURO, self.boton_salir)
        pygame.draw.rect(self.pantalla, NEGRO, self.boton_salir, 3)
        texto_salir = self.fuente_boton.render("SALIR", True, BLANCO)
        texto_salir_rect = texto_salir.get_rect(center=self.boton_salir.center)
        self.pantalla.blit(texto_salir, texto_salir_rect)