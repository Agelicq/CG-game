#!/usr/bin/env python3
"""Módulo del Estado de Confirmación de Salida.

Este módulo contiene la clase ExitConfirmState que maneja
la pantalla de confirmación cuando el jugador intenta
salir del juego desde el menú principal.
"""

# Importaciones de librerías estándar
import sys

# Importaciones de terceros
import pygame

# Importaciones locales
from core.state import State
from settings import WIDTH, HEIGHT


class ExitConfirmState(State):
    """Estado de confirmación de salida del juego.
    
    Muestra un diálogo modal con botones "Sí" y "No"
    para confirmar si el jugador realmente desea salir
    del juego o regresar al menú.
    
    Attributes:
        font: Fuente utilizada para renderizar el texto.
        buttons: Diccionario con los rectángulos de los botones.
    """

    def __init__(self, game):
        """Inicializa el estado de confirmación de salida.
        
        Configura la fuente y posiciona los botones de
        confirmación en la pantalla.
        
        Args:
            game: Referencia al gestor principal del juego.
        """
        super().__init__(game)
        
        # === CONFIGURACIÓN DE FUENTE ===
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 40)

        # === CONFIGURACIÓN DE BOTONES ===
        self.buttons = {
            "yes": pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 40, 120, 50),
            "no": pygame.Rect(WIDTH//2 + 30, HEIGHT//2 + 40, 120, 50)
        }

    def handle_events(self):
        """Procesa los eventos de entrada del usuario.
        
        Maneja la navegación con mouse y teclado para confirmar
        o cancelar la salida del juego.
        """
        for event in pygame.event.get():
            # === EVENTO DE SALIDA DIRECTA ===
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # === NAVEGACIÓN CON MOUSE ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()

                # Botón "Sí" - Confirmar salida
                if self.buttons["yes"].collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

                # Botón "No" - Regresar al menú
                if self.buttons["no"].collidepoint(mx, my):
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

            # === NAVEGACIÓN CON TECLADO ===
            if event.type == pygame.KEYDOWN:
                # ENTER - Confirmar salida
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()

                # ESC/BACKSPACE - Cancelar y regresar
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    from states.menu import MenuState
                    self.game.change_state(MenuState(self.game))

    def draw(self):
        """Renderiza la pantalla de confirmación de salida.
        
        Dibuja un overlay oscuro, una ventana de diálogo
        centrada y los botones interactivos con efectos hover.
        """
        # === OVERLAY OSCURO ===
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)  # Transparencia del 70%
        overlay.fill((0, 0, 0))
        self.game.screen.blit(overlay, (0, 0))

        # === VENTANA DE DIÁLOGO ===
        box_w, box_h = 600, 200
        box_rect = pygame.Rect(
            (WIDTH - box_w)//2,
            (HEIGHT - box_h)//2,
            box_w, box_h
        )
        
        # Fondo y borde de la ventana
        pygame.draw.rect(self.game.screen, (10, 10, 10), box_rect)
        pygame.draw.rect(self.game.screen, (0, 255, 255), box_rect, 3)

        # === TÍTULO DE CONFIRMACIÓN ===
        title = self.font.render("CONFIRMAR SALIDA DEL JUEGO?", True, (255, 255, 255))
        self.game.screen.blit(title, title.get_rect(center=(WIDTH//2, box_rect.y + 55)))

        # === BOTONES INTERACTIVOS ===
        mx, my = pygame.mouse.get_pos()
        
        for name, rect in self.buttons.items():
            # Efecto hover
            hovered = rect.collidepoint(mx, my)
            color = (0, 255, 255) if hovered else (255, 255, 255)

            # Fondo y borde del botón
            pygame.draw.rect(self.game.screen, (20, 20, 20), rect)
            pygame.draw.rect(self.game.screen, color, rect, 2)

            # Texto del botón
            label_text = "Sí" if name == "yes" else "No"
            label = self.font.render(label_text, True, color)
            self.game.screen.blit(label, label.get_rect(center=rect.center))
