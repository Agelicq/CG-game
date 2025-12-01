import pygame
import time
from settings import WIDTH  # Importamos el ancho para calcular la posición

class GameTimer:
    def __init__(self):
        # Intentamos cargar la fuente pixelada, si falla usa una normal
        try:
            self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 45)
        except:
            self.font = pygame.font.SysFont("Consolas", 35, bold=True)
            
        self.color_text = (255, 255, 255) # Blanco
        self.color_shadow = (0, 0, 0)     # Negro

    def draw(self, screen, start_time):
        # 1. Calcular tiempo transcurrido
        current_time = time.time()
        elapsed = int(current_time - start_time)
        
        # 2. Formato Minutos:Segundos
        minutes = elapsed // 60
        seconds = elapsed % 60
        time_str = f"TIME {minutes:02}:{seconds:02}"
        
        # 3. Renderizar texto y sombra
        text_surf = self.font.render(time_str, True, self.color_text)
        shadow_surf = self.font.render(time_str, True, self.color_shadow)
        
        # 4. Posición (Esquina Superior Derecha)
        # Usamos WIDTH de settings o el ancho de la pantalla
        x = screen.get_width() - text_surf.get_width() - 20
        y = 20 # Margen superior
        
        # 5. Dibujar
        screen.blit(shadow_surf, (x + 2, y + 2))
        screen.blit(text_surf, (x, y))