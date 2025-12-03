#!/usr/bin/env python3
"""Módulo de la Secuencia de Introducción.

Este módulo contiene la clase IntroState que maneja
la secuencia cinematática de introducción del juego,
incluyendo la historia y transición al menú principal.
"""

# Importaciones de librerías estándar
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from settings import *
from core.state import State
from states.menu import MenuState


class IntroState(State):
    """Estado de la secuencia de introducción del juego.
    
    Maneja la presentación cinematática inicial con
    diapositivas de la historia, texto narrativo y
    música de fondo. Permite avance manual o automático.
    
    Attributes:
        start_time: Tiempo de inicio de la diapositiva actual.
        duration_per_slide: Duración en ms de cada diapositiva.
        story_texts: Lista de textos narrativos por diapositiva.
        font: Fuente para renderizar texto.
        images: Lista de imágenes cargadas de la historia.
        current_index: Índice de la diapositiva actual.
        transition_done: Flag para evitar transiciones múltiples.
    """
    def __init__(self, game):
        """Inicializa el estado de la introducción.
        
        Carga las imágenes de la historia, configura los textos
        narrativos y reproduce la música de fondo.
        
        Args:
            game: Referencia al gestor principal del juego.
        """
        super().__init__(game)
        
        # === CONFIGURACIÓN DE TIMING ===
        self.start_time = pygame.time.get_ticks()
        self.duration_per_slide = 4000  # 4 segundos por diapositiva
        
        # === ARCHIVOS DE IMÁGENES DE LA HISTORIA ===
        image_files = [
            "intro2.png", "historia_1.png", "historia_2.png", 
            "historia_3.png", "historia_4.png", "historia_5.png"
        ]
        
        # === TEXTOS NARRATIVOS (uno por diapositiva) ===
        self.story_texts = [
            None,  # Primera imagen sin texto
            "Viaje espacial Nebulosa del olvido...",
            "...LLUVIA DE ASTEROIDES...",
            "¡Impacto inminente!",
            "la fuente de energia principal se ha fragmentado...",
            "ASTRO-BOT eres nuestra esperanza, recupera la FEP..."
        ]
        
        # === CONFIGURACIÓN DE FUENTE ===
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 35)
        
        # === CONTROL DE ESTADO ===
        self.images = []
        self.current_index = 0
        self.transition_done = False
    
        # === CARGA DE IMÁGENES ===
        print("Cargando historia...")
        for file_name in image_files:
            try:
                path = f"assets/images/{file_name}"
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                self.images.append(img)
            except FileNotFoundError:
                print(f"Error: No se encontró {file_name}")
        
        # Fallback: imagen negra si no se carga ninguna
        if not self.images:
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((0, 0, 0))
            self.images.append(surf)

        # === CONFIGURACIÓN DE MÚSICA ===
        try:
            pygame.mixer.music.load("assets/music/Soliloquy.mp3")
            pygame.mixer.music.set_volume(0.4)  # Volumen moderado
            pygame.mixer.music.play(loops=-1)   # Loop infinito
        except Exception as e:
            print(f"No se pudo cargar la música: {e}")
            
            
    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Permite salir del juego o avanzar manualmente
        las diapositivas con cualquier clic o tecla.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # === AVANCE MANUAL DE DIAPOSITIVAS ===
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._advance_slide()

    def update(self):
        """Actualiza el estado de la introducción.
        
        Verifica si ha transcurrido suficiente tiempo
        para avanzar automáticamente a la siguiente diapositiva.
        """
        current_time = pygame.time.get_ticks()
        
        # Avance automático por tiempo
        if current_time - self.start_time > self.duration_per_slide:
            self._advance_slide()
            
    def _advance_slide(self):
        """Avanza a la siguiente diapositiva de la historia.
        
        Incrementa el índice de la diapositiva actual o
        transite al menú principal si es la última.
        """
        if self.transition_done:
            return

        # Reiniciar temporizador para la nueva diapositiva
        self.start_time = pygame.time.get_ticks()
        
        # Avanzar o finalizar
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
        else:
            self._to_menu()
    
    def _to_menu(self):
        """Transición al menú principal.
        
        Evita transiciones múltiples usando el flag
        transition_done y cambia al estado del menú.
        """
        if not self.transition_done:
            self.transition_done = True
            self.game.change_state(MenuState(self.game))

    def draw(self):
        """Renderiza la diapositiva actual de la introducción.
        
        Dibuja la imagen de fondo y el texto narrativo
        correspondiente con fondo semitransparente para
        mejorar la legibilidad.
        """
        # === IMAGEN DE FONDO ===
        if self.images:
            current_image = self.images[self.current_index]
            self.game.screen.blit(current_image, (0, 0))

        # === TEXTO NARRATIVO ===
        if self.current_index < len(self.story_texts):
            text_string = self.story_texts[self.current_index]

            # Renderizar solo si hay texto válido
            if text_string and str(text_string).strip():
                # Crear superficie de texto
                text_surf = self.font.render(text_string, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT - 45))

                # === FONDO SEMITRANSPARENTE PARA LEGIBILIDAD ===
                bg_rect = text_rect.inflate(20, 10)
                background = pygame.Surface((bg_rect.width, bg_rect.height))
                background.set_alpha(150)  # Transparencia del 59%
                background.fill((0, 0, 0))
                self.game.screen.blit(background, bg_rect.topleft)

                # === RENDERIZAR TEXTO ===
                self.game.screen.blit(text_surf, text_rect)
