import pygame
import os

class SistemaAudio:
    def __init__(self):
        """Inicializa el sistema de audio del juego"""
        pygame.mixer.init()
        self.sonidos = {}
        self.musica_activa = False
        self.volumen_efectos = 0.7
        self.volumen_musica = 0.5
        
        # Cargar todos los sonidos
        self.cargar_sonidos()
    
    def cargar_sonidos(self):
        """Carga todos los archivos de sonido"""
        ruta_sonidos = os.path.join("Sonidos")
        
        try:
            # Sonidos de efectos
            self.sonidos['correcto'] = pygame.mixer.Sound(os.path.join(ruta_sonidos, "Correcto.mp3"))
            self.sonidos['incorrecto'] = pygame.mixer.Sound(os.path.join(ruta_sonidos, "Incorrecto.mp3"))
            self.sonidos['ganaste'] = pygame.mixer.Sound(os.path.join(ruta_sonidos, "Ganaste.mp3"))
            self.sonidos['perdiste'] = pygame.mixer.Sound(os.path.join(ruta_sonidos, "Perdiste.mp3"))
            self.sonidos['iniciar'] = pygame.mixer.Sound(os.path.join(ruta_sonidos, "Iniciarminijuego.mp3"))
            
            # Configurar volumen de efectos
            for sonido in self.sonidos.values():
                sonido.set_volume(self.volumen_efectos)
                
            # Música de fondo del menú
            self.musica_menu = os.path.join(ruta_sonidos, "MusicaMenu.mp3")
            
            print("✓ Sonidos cargados correctamente")
            
        except Exception as e:
            print(f"⚠ Error al cargar sonidos: {e}")
            # Crear sonidos vacíos para evitar errores
            for nombre in ['correcto', 'incorrecto', 'ganaste', 'perdiste', 'iniciar']:
                self.sonidos[nombre] = None
    
    def reproducir_efecto(self, nombre_sonido):
        """Reproduce un efecto de sonido"""
        if nombre_sonido in self.sonidos and self.sonidos[nombre_sonido]:
            try:
                self.sonidos[nombre_sonido].play()
            except Exception as e:
                print(f"Error al reproducir {nombre_sonido}: {e}")
    
    def iniciar_musica_menu(self):
        """Inicia la música de fondo del menú"""
        if not self.musica_activa:
            try:
                pygame.mixer.music.load(self.musica_menu)
                pygame.mixer.music.set_volume(self.volumen_musica)
                pygame.mixer.music.play(-1)  # -1 para loop infinito
                self.musica_activa = True
            except Exception as e:
                print(f"Error al reproducir música del menú: {e}")
    
    def detener_musica(self):
        """Detiene la música de fondo"""
        if self.musica_activa:
            pygame.mixer.music.stop()
            self.musica_activa = False
    
    def pausar_musica(self):
        """Pausa la música de fondo"""
        if self.musica_activa:
            pygame.mixer.music.pause()
    
    def reanudar_musica(self):
        """Reanuda la música de fondo"""
        if self.musica_activa:
            pygame.mixer.music.unpause()
    
    def ajustar_volumen_efectos(self, volumen):
        """Ajusta el volumen de los efectos de sonido (0.0 a 1.0)"""
        self.volumen_efectos = max(0.0, min(1.0, volumen))
        for sonido in self.sonidos.values():
            if sonido:
                sonido.set_volume(self.volumen_efectos)
    
    def ajustar_volumen_musica(self, volumen):
        """Ajusta el volumen de la música (0.0 a 1.0)"""
        self.volumen_musica = max(0.0, min(1.0, volumen))
        pygame.mixer.music.set_volume(self.volumen_musica)
    
    # Métodos específicos para cada sonido
    def reproducir_correcto(self):
        """Reproduce el sonido de respuesta correcta"""
        self.reproducir_efecto('correcto')
    
    def reproducir_incorrecto(self):
        """Reproduce el sonido de respuesta incorrecta"""
        self.reproducir_efecto('incorrecto')
    
    def reproducir_ganaste(self):
        """Reproduce el sonido de victoria"""
        self.reproducir_efecto('ganaste')
    
    def reproducir_perdiste(self):
        """Reproduce el sonido de derrota"""
        self.reproducir_efecto('perdiste')
    
    def reproducir_iniciar_juego(self):
        """Reproduce el sonido de iniciar juego"""
        self.reproducir_efecto('iniciar')

# Instancia global del sistema de audio
sistema_audio = SistemaAudio()