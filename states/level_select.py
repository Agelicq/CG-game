import pygame
import sys
from core.state import State
from settings import *
from states.gamePlayState import GameplayState

class LevelSelectState(State):
    def __init__(self, game,player_data):
        super().__init__(game)
        self.player_data = player_data # Recibimos la mochila actualizada
        
        # --- VERIFICAR SI TERMINÓ EL JUEGO (3 PLANETAS) ---
        # Supongamos que tus planetas son: "glacius", "volcanus", "floria"
        total_planetas = 3 
        
        if len(self.player_data["levels_done"]) >= total_planetas:
            self.save_score_and_finish()
            return # Detenemos la carga del selector
        
        # Fondo espacial
        self.background = pygame.image.load("assets/images/BGgame_select.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Imágenes de los planetas (con transparencia)
        self.planet_glacius = pygame.image.load("assets/images/glacius.png").convert_alpha()
        self.planet_volcanus = pygame.image.load("assets/images/volcanus.png").convert_alpha()
        self.planet_floria = pygame.image.load("assets/images/floria.png").convert_alpha()

        # Sonido al seleccionar planeta
        self.sound_select = pygame.mixer.Sound("assets/music/rocket.mp3")
        # Parámetros de audio 
        self.sound_volume = 0.4       # rango 0.0 - 1.0
        self.sound_max_ms = 700      # duración máxima en ms (maxtime)
        self.sound_fade_ms = 0        # fade-in en ms al reproducir
        # Aplicar volumen inicial
        self.sound_select.set_volume(self.sound_volume)

        # Posiciones (centros)
        self.positions = {
            "glacius": (200, 320),
            "volcanus": (400, 320),
            "floria": (600, 320)
        }

        # Escala base
        self.base_size = 130
        self.hover_size = 150

    def save_score_and_finish(self):
        """Formatea el tiempo y guarda en el archivo"""
        
        # 1. CONVERTIR SEGUNDOS A MINUTOS:SEGUNDOS
        total_seconds = int(self.player_data["total_time"])
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        # Formato 00:00 (rellena con ceros)
        time_str = f"{minutes:02}:{seconds:02}"
        name = self.player_data["name"]

        print(f"¡JUEGO COMPLETADO! {name} Time :{time_str} min")

        # 2. GUARDAR EN TXT
        try:
            with open("puntajes_totales.txt", "a") as f:
                f.write(f"{name} Time :{time_str} min\n")
        except Exception as e:
            print("Error guardando:", e)
        
        # 3. REGRESAR AL MENÚ PRINCIPAL (O mostrar créditos)
        from states.menu import MenuState
        self.game.change_state(MenuState(self.game))
    
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
                        
                        # VALIDAR QUE NO REPITA PLANETA (OPCIONAL PERO RECOMENDADO)
                        if name in self.player_data["levels_done"]:
                            print("¡Ya completaste este planeta!")
                        else:
                            # Ir al nivel pasando la mochila
                            from states.gamePlayState import GameplayState
                            self.game.change_state(GameplayState(self.game, name, self.player_data))

    def update(self, dt=None):
        # Actualmente no usamos dt aquí, pero lo aceptamos para compatibilidad
        return

    def draw(self):
        screen = self.game.screen
        screen.blit(self.background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Dibujar planetas con efecto hover (escala)
        for name, (x, y) in self.positions.items():
            img = getattr(self, f"planet_{name}")
            distance_rect = pygame.Rect(x - self.base_size//2, y - self.base_size//2, self.base_size, self.base_size)

            if distance_rect.collidepoint((mx, my)):
                img_scaled = pygame.transform.scale(img, (self.hover_size, self.hover_size))
            else:
                img_scaled = pygame.transform.scale(img, (self.base_size, self.base_size))

            rect = img_scaled.get_rect(center=(x, y))
            screen.blit(img_scaled, rect)

        # Título
        try:
            font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 35)
        except Exception:
                font = pygame.font.SysFont("verdana", 35)

        text = font.render("glacius", True, COLOR_BLANCO)
        screen.blit(text, text.get_rect(center=(200, 410)))

        text = font.render("volcanus", True, COLOR_BLANCO)
        screen.blit(text, text.get_rect(center=(400, 410)))

        text = font.render("floria", True, COLOR_BLANCO)
        screen.blit(text, text.get_rect(center=(600, 410)))