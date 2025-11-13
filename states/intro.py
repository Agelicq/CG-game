import pygame, sys
from settings import *
from core.state import State
from states.menu import MenuState

class IntroState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.start_time = pygame.time.get_ticks()
        self.duration_per_slide = 4000 
        
        # 1. LISTA DE IMÁGENES
        image_files = ["historia_1.png", "historia_2.png", "historia_3.png", "historia4.png", "historia_5.png"]
        
        # 2. LISTA DE TEXTOS (Debe haber uno por cada imagen)
        self.story_texts = [
            "Viaje espacial Nebulosa del olvido...",
            "...LLUVIA DE ASTEROIDES...",
            "IMPACTOOOOOOOOOO...",
            "Se rompio la fuente de energia principal en fragmentos...",
            "ASTRO _ BOT eres nuestra esperanza recupera los fragmentos....."
        ]
        
        # 3. FUENTE PARA EL TEXTO
        # Usamos una fuente predeterminada, tamaño 30
        self.font = pygame.font.SysFont("Arial", 30)

        self.images = []
        self.current_index = 0
        self.transition_done = False
    
        print("Cargando historia...")
        for file_name in image_files:
            try:
                path = f"assets/images/{file_name}"
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                self.images.append(img)
            except FileNotFoundError:
                print(f"⚠️ Error: No se encontró {file_name}")
        
        if not self.images:
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((0, 0, 0))
            self.images.append(surf)

        try:
            # Cargar música
            pygame.mixer.music.load("assets/music/Soliloquy.mp3")
            
            # Volumen bajo para que no asuste (0.4 es buen punto de partida)
            pygame.mixer.music.set_volume(0.4) 
            
            # Play con loop infinito
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            print(f"No se pudo cargar la música: {e}")
            
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._advance_slide()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration_per_slide:
            self._advance_slide()
            
    def _advance_slide(self):
        if self.transition_done: return

        self.start_time = pygame.time.get_ticks()
        
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
        else:
            self._to_menu()
    
    def _to_menu(self):
        if not self.transition_done:
            self.transition_done = True
            self.game.change_state(MenuState(self.game))

    def draw(self):
        # 1. Dibujar imagen de fondo
        if self.images:
            current_image = self.images[self.current_index]
            self.game.screen.blit(current_image, (0, 0))

        # 2. Dibujar el texto de la historia
        # Verificamos que exista un texto para el índice actual
        if self.current_index < len(self.story_texts):
            text_string = self.story_texts[self.current_index]
            
            # Renderizar el texto (Color Blanco)
            text_surf = self.font.render(text_string, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT - 80)) # Posición: Abajo centrado

            # --- FONDO NEGRO PARA EL TEXTO (Opcional pero recomendado) ---
            # Creamos una caja negra un poco más grande que el texto
            bg_rect = text_rect.inflate(20, 10) 
            s = pygame.Surface((bg_rect.width, bg_rect.height))  # la superficie del tamaño de la caja
            s.set_alpha(150)                # Transparencia (0-255)
            s.fill((0, 0, 0))               # Color negro
            self.game.screen.blit(s, bg_rect.topleft)
            # -------------------------------------------------------------

            # Dibujar el texto encima de la caja negra
            self.game.screen.blit(text_surf, text_rect)
