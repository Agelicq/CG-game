import pygame, sys, os
from core.state import State
from settings import *
from states.menu import MenuState

class ScoreState(State):
    def __init__(self, game):
        super().__init__(game)

        # 1. Cargar fondo (Podemos reusar el del menú o poner uno oscuro)
        try:
            self.background = pygame.image.load("assets/images/bgpuntajes.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            # Oscurecerlo un poco para que se lea el texto
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.background.blit(overlay, (0,0))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((20, 20, 40))

        # Fuentes
        try:
            self.font_title = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 60)
            self.font_text = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 35)
        except:
            self.font_title = pygame.font.SysFont("Arial", 50, bold=True)
            self.font_text = pygame.font.SysFont("Arial", 30)

        # 2. CARGAR Y ORDENAR PUNTAJES
        self.top_scores = self.load_and_sort_scores()

    def load_and_sort_scores(self):
        scores_list = []
        file_path = "puntajes_totales.txt"

        if not os.path.exists(file_path):
            return [] # Si no existe el archivo, devolvemos lista vacía

        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            # Formato esperado: "Pepe Time :04:20 min"
            # Vamos a "parsear" (analizar) el texto
            try:
                # Separamos el nombre del tiempo usando " Time :" como separador
                parts = line.split(" Time :")
                name = parts[0].strip()
                
                # Tomamos la parte del tiempo "04:20 min" y quitamos el " min"
                time_str = parts[1].replace(" min", "").strip() # queda "04:20"
                
                # Convertimos "04:20" a segundos totales para poder ordenar
                mins, secs = map(int, time_str.split(":"))
                total_seconds = mins * 60 + secs
                
                # Guardamos un diccionario con los datos limpios
                scores_list.append({
                    "name": name,
                    "time_str": time_str,
                    "seconds": total_seconds
                })
            except Exception as e:
                print(f"Línea corrupta ignorada: {line} - Error: {e}")

        # 3. ORDENAR LA LISTA (De menor tiempo a mayor tiempo)
        # La clave (key) para ordenar es 'seconds'
        scores_list.sort(key=lambda x: x['seconds'])

        # 4. DEVOLVER SOLO LOS 10 PRIMEROS
        return scores_list[:5]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Volver al menú con ESC o ENTER
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    # Importación local para evitar error circular
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

    def draw(self):
        # Dibujar fondo
        self.game.screen.blit(self.background, (0, 0))

        # Título
        title = self.font_title.render("MEJORES PILOTOS (TOP 5)", True, (255, 215, 0)) # Dorado
        rect_title = title.get_rect(center=(WIDTH//2, 80))
        self.game.screen.blit(title, rect_title)

        # Dibujar la lista de puntajes
        start_y = 150
        
        if not self.top_scores:
            msg = self.font_text.render("No hay registros aún.", True, (200, 200, 200))
            self.game.screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
        else:
            # Cabecera de columnas
            header = self.font_text.render(f"{'RANGO':<5}   {'PILOTO':<15}   {'TIEMPO'}", True, (100, 255, 100))
            self.game.screen.blit(header, (WIDTH//2 - 200, start_y))
            start_y += 40
            
            # Línea separadora
            pygame.draw.line(self.game.screen, (255,255,255), (WIDTH//2 - 200, start_y), (WIDTH//2 + 200, start_y), 2)
            start_y += 20

            # Filas de datos
            for index, score in enumerate(self.top_scores):
                rank = f"#{index + 1}"
                name = score['name']
                # Si el nombre es muy largo, lo cortamos visualmente
                if len(name) > 12: name = name[:10] + ".."
                
                time_s = score['time_str']

                # Formatear el texto alineado
                line_str = f"{rank:<5}   {name:<15}   {time_s}"
                
                # Color especial para los 3 primeros
                color = (255, 255, 255)
                if index == 0: color = (255, 215, 0) # Oro
                elif index == 1: color = (192, 192, 192) # Plata
                elif index == 2: color = (205, 127, 50) # Bronce

                text_surf = self.font_text.render(line_str, True, color)
                self.game.screen.blit(text_surf, (WIDTH//2 - 200, start_y))
                
                start_y += 35 # Espacio entre líneas

        # Texto para regresar
        back_label = self.font_text.render("Presiona ENTER para volver", True, (150, 150, 150))
        self.game.screen.blit(back_label, back_label.get_rect(center=(WIDTH//2, HEIGHT - 50)))