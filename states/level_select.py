import pygame, sys
from core.state import State
from settings import *
# Importamos el estado de Juego y el de Victoria
from states.gamePlayState import GameplayState
from states.victory import VictoryState  # <--- IMPORTANTE

class LevelSelectState(State):
    def __init__(self, game, player_data):
        super().__init__(game)
        self.player_data = player_data 
        
        # --- NOTA: ELIMINAMOS LA LÓGICA DE "IF TERMINÓ" DE AQUÍ PARA EVITAR ERRORES ---
        # Primero cargamos todo, luego en 'update' revisamos si ganó.

        # Fondo espacial
        try:
            self.background = pygame.image.load("assets/images/BGgame_select.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((0,0,0))

        # Imágenes de los planetas
        self.planet_glacius = pygame.image.load("assets/images/glacius.png").convert_alpha()
        self.planet_volcanus = pygame.image.load("assets/images/volcanus.png").convert_alpha()
        self.planet_floria = pygame.image.load("assets/images/floria.png").convert_alpha()

        # Sonido
        self.sound_select = pygame.mixer.Sound("assets/music/rocket.mp3")
        self.sound_volume = 0.4 
        self.sound_max_ms = 700
        self.sound_fade_ms = 0
        self.sound_select.set_volume(self.sound_volume)

        # Posiciones
        self.positions = {
            "glacius": (200, 320),
            "volcanus": (400, 320),
            "floria": (600, 320)
        }
        self.base_size = 130
        self.hover_size = 150

    def update(self, dt=None):
        # --- AQUÍ ES DONDE REVISAMOS SI GANÓ ---
        total_planetas = 3 
        
        if len(self.player_data["levels_done"]) >= total_planetas:
            self.save_score_and_finish()

    def save_score_and_finish(self):
        """Calcula el tiempo, guarda y lanza la VICTORIA"""
        
        total_seconds = int(self.player_data["total_time"])
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_str = f"{minutes:02}:{seconds:02}"
        name = self.player_data["name"]

        print(f"¡JUEGO COMPLETADO! {name} Time :{time_str} min")

        # Guardar en TXT
        try:
            with open("puntajes_totales.txt", "a") as f:
                f.write(f"{name} Time :{time_str} min\n")
        except Exception as e:
            print("Error guardando:", e)
        
        # --- CAMBIO: IR A PANTALLA DE VICTORIA ---
        self.game.change_state(VictoryState(self.game, name, time_str))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from states.menu import MenuState
                self.game.change_state(MenuState(self.game))
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                for name, (x, y) in self.positions.items():
                    planet_rect = pygame.Rect(x - self.hover_size//2, y - self.hover_size//2, self.hover_size, self.hover_size)
                    
                    if planet_rect.collidepoint((mx, my)):
                        if name in self.player_data["levels_done"]:
                            print("¡Ya completaste este planeta!")
                        else:
                            # Reproducir sonido
                            self.sound_select.play(maxtime=self.sound_max_ms, fade_ms=self.sound_fade_ms)
                            # Ir al juego
                            self.game.change_state(GameplayState(self.game, name, self.player_data))

    def draw(self):
        screen = self.game.screen
        screen.blit(self.background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Dibujar planetas
        for name, (x, y) in self.positions.items():
            img = getattr(self, f"planet_{name}")
            
            # Opción visual: Si ya completó el nivel, hacerlo un poco transparente
            if name in self.player_data["levels_done"]:
                img.set_alpha(100)
            else:
                img.set_alpha(255)

            distance_rect = pygame.Rect(x - self.base_size//2, y - self.base_size//2, self.base_size, self.base_size)

            if distance_rect.collidepoint((mx, my)):
                img_scaled = pygame.transform.scale(img, (self.hover_size, self.hover_size))
            else:
                img_scaled = pygame.transform.scale(img, (self.base_size, self.base_size))

            rect = img_scaled.get_rect(center=(x, y))
            screen.blit(img_scaled, rect)

        # Títulos
        try:
            font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 35)
        except:
            font = pygame.font.SysFont("verdana", 35)

        # Dibujar nombres
        nombres = [("glacius", 200), ("volcanus", 400), ("floria", 600)]
        for txt, x_pos in nombres:
            color = (0, 255, 0) if txt in self.player_data["levels_done"] else (255, 255, 255)
            text_surf = font.render(txt, True, color)
            screen.blit(text_surf, text_surf.get_rect(center=(x_pos, 410)))