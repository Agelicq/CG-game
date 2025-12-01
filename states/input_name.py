import pygame, sys
from core.state import State
from settings import *

class InputNameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.input_text = ""
        # Fuente para el texto
        try:
            self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 50)
        except:
            self.font = pygame.font.Font(None, 50)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Al dar ENTER, pasamos a seleccionar nivel enviando el nombre
                if event.key == pygame.K_RETURN:
                    if len(self.input_text) > 0:
                        
                        # CREAMOS LA MOCHILA DE DATOS
                        player_data = {
                            "name": self.input_text,
                            "total_time": 0.0,      # Tiempo acumulado
                            "levels_done": []       # Lista de niveles terminados
                        }

                        from states.level_select import LevelSelectState
                        # Pasamos el diccionario completo
                        self.game.change_state(LevelSelectState(self.game, player_data))
                
                # Borrar carácter
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                
                # Escribir letras/números (limite de 12 caracteres)
                else:
                    if len(self.input_text) < 12 and event.unicode.isprintable():
                        self.input_text += event.unicode

    def update(self, dt=None):
        pass

    def draw(self):
        self.game.screen.fill(COLOR_FONDO_OSCURO)
        
        # Títulos
        title = self.font.render("IDENTIFICATE PILOTO", True, COLOR_BLANCO)
        prompt = self.font.render("Escribe tu nombre y presiona ENTER:", True, (150, 150, 150))
        
        # El nombre que escribe el usuario
        name_surf = self.font.render(self.input_text, True, COLOR_NEON_CIAN)
        
        # Centrar todo
        rect_title = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        rect_prompt = prompt.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        rect_name = name_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        
        # Dibujar cajita
        pygame.draw.rect(self.game.screen, COLOR_BLANCO, rect_name.inflate(40, 20), 2)
        
        self.game.screen.blit(title, rect_title)
        self.game.screen.blit(prompt, rect_prompt)
        self.game.screen.blit(name_surf, rect_name)