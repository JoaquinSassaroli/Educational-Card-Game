"""
Archivo principal del juego "Cartas en Juego"
Este archivo inicializa pygame y ejecuta el bucle principal del juego.
Autor: Asistente IA
Fecha: 2024
"""

import pygame
import sys
from lib.game import Game
from lib.Var import ANCHO_VENTANA, ALTO_VENTANA, FPS, TITULO_JUEGO

def main():
    # Inicializar pygame
    pygame.init()
    
    # Crear la ventana del juego
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption(TITULO_JUEGO)
    
    # Crear el reloj para controlar los FPS
    reloj = pygame.time.Clock()
    
    # Crear la instancia del juego
    juego = Game(pantalla, ANCHO_VENTANA, ALTO_VENTANA)
    
    # Bucle principal del juego
    ejecutando = True
    while ejecutando:
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            else:
                # Pasar eventos al juego
                resultado = juego.manejar_evento(evento)
                if resultado and resultado.get("accion") == "salir":
                    ejecutando = False
        
        # Actualizar el juego
        resultado = juego.actualizar()
        if resultado == "salir":
            ejecutando = False
        
        # Dibujar todo
        juego.dibujar()
        
        # Actualizar la pantalla
        pygame.display.flip()
        
        # Controlar FPS
        reloj.tick(FPS)
    
    # Salir del juego
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()