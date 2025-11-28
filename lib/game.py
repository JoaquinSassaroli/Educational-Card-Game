import pygame
from .menu import Menu
from .modo_parejas import ModoParejas
from .modo_intruso import ModoIntruso
from .game_over import GameOver
from .Color import *
from .Var import *

class Game:
    # Estados del juego
    MENU = "menu"
    PAREJAS = "parejas"
    INTRUSO = "intruso"
    GAME_OVER = "game_over"
    
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.estado_actual = self.MENU
        
        # Inicializar componentes
        self.menu = Menu(pantalla, ancho, alto)
        self.modo_parejas = None
        self.modo_intruso = None
        self.game_over = None
        
        # Variables para game over
        self.puntuacion_final = 0
        self.tiempo_total = 0
        
        # Variables para materias seleccionadas
        self.materias_seleccionadas = []
    
    def manejar_evento(self, evento):
        # Manejo de eventos según el estado actual
        if self.estado_actual == self.MENU:
            resultado = self.menu.manejar_evento(evento)
            if resultado:
                if resultado["accion"] == "parejas":
                    self.materias_seleccionadas = resultado["materias"]
                    self.iniciar_modo_parejas()
                elif resultado["accion"] == "intruso":
                    self.materias_seleccionadas = resultado["materias"]
                    self.iniciar_modo_intruso()
                elif resultado["accion"] == "salir":
                    return {"accion": "salir"}
        
        elif self.estado_actual == self.PAREJAS:
            if self.modo_parejas:
                resultado = self.modo_parejas.manejar_evento(evento)
                if resultado:
                    if resultado["estado"] == "game_over":
                        self.puntuacion_final = resultado["puntuacion"]
                        self.tiempo_total = resultado["tiempo"]
                        self.iniciar_game_over(resultado["victoria"])
        
        elif self.estado_actual == self.INTRUSO:
            if self.modo_intruso:
                resultado = self.modo_intruso.manejar_evento(evento)
                if resultado:
                    if resultado["estado"] == "game_over":
                        self.puntuacion_final = resultado["puntuacion"]
                        self.tiempo_total = resultado["tiempo"]
                        self.iniciar_game_over(resultado["victoria"])
        
        elif self.estado_actual == self.GAME_OVER:
            if self.game_over:
                resultado = self.game_over.manejar_evento(evento)
                if resultado:
                    if resultado["accion"] == "reiniciar":
                        # Reiniciar el modo actual
                        if self.modo_parejas:
                            self.iniciar_modo_parejas()
                        elif self.modo_intruso:
                            self.iniciar_modo_intruso()
                    elif resultado["accion"] == "menu":
                        self.volver_al_menu()
    
    def actualizar(self):
        # Actualizar el estado actual del juego
        if self.estado_actual == self.PAREJAS and self.modo_parejas:
            resultado = self.modo_parejas.actualizar()
            if resultado and resultado["estado"] == "game_over":
                self.puntuacion_final = resultado["puntuacion"]
                self.tiempo_total = resultado["tiempo"]
                self.iniciar_game_over(resultado["victoria"])
        elif self.estado_actual == self.INTRUSO and self.modo_intruso:
            resultado = self.modo_intruso.actualizar()
            if resultado and resultado["estado"] == "game_over":
                self.puntuacion_final = resultado["puntuacion"]
                self.tiempo_total = resultado["tiempo"]
                self.iniciar_game_over(resultado["victoria"])
    
    def dibujar(self):
        # Dibujar según el estado actual
        if self.estado_actual == self.MENU:
            self.menu.dibujar()
        elif self.estado_actual == self.PAREJAS and self.modo_parejas:
            self.modo_parejas.dibujar()
        elif self.estado_actual == self.INTRUSO and self.modo_intruso:
            self.modo_intruso.dibujar()
        elif self.estado_actual == self.GAME_OVER and self.game_over:
            self.game_over.dibujar()
    
    def iniciar_modo_parejas(self):
        # Inicializar modo parejas
        self.estado_actual = self.PAREJAS
        self.modo_parejas = ModoParejas(self.pantalla, self.ancho, self.alto, self.materias_seleccionadas)
        self.modo_intruso = None
        self.game_over = None
    
    def iniciar_modo_intruso(self):
        # Inicializar modo intruso
        self.estado_actual = self.INTRUSO
        self.modo_intruso = ModoIntruso(self.pantalla, self.ancho, self.alto, self.materias_seleccionadas)
        self.modo_parejas = None
        self.game_over = None
    
    def iniciar_game_over(self, victoria):
        # Inicializar pantalla de game over
        self.estado_actual = self.GAME_OVER
        self.game_over = GameOver(
            self.pantalla, 
            self.ancho, 
            self.alto, 
            self.puntuacion_final, 
            self.tiempo_total,
            victoria
        )
    
    def volver_al_menu(self):
        # Volver al menú principal
        self.estado_actual = self.MENU
        self.modo_parejas = None
        self.modo_intruso = None
        self.game_over = None