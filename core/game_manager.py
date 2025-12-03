"""Game Manager Module.

This module contains the main GameManager class that controls the game loop,
state management, and core game functionality for Astro Lost.
"""

import sys
import pygame

from settings import WIDTH, HEIGHT, FPS
from states.intro import IntroState


class GameManager:
    """Main game manager class.
    
    Handles the main game loop, state transitions, and core game systems.
    Manages pygame initialization, display setup, and frame timing.
    
    Attributes:
        screen (pygame.Surface): The main display surface.
        clock (pygame.time.Clock): Game clock for frame rate control.
        state (State): Current active game state.
    """
    
    def __init__(self):
        """Initialize the game manager.
        
        Sets up pygame, creates the display window, initializes the clock,
        and sets the initial game state to IntroState.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Astro Lost")
        self.clock = pygame.time.Clock()
        self.state = IntroState(self)  # Estado inicial

    def change_state(self, new_state):
        """Change the current game state.
        
        Args:
            new_state (State): The new state to transition to.
        """
        self.state = new_state

    def run(self):
        """Start and run the main game loop.
        
        Continuously processes events, updates game state, and renders frames.
        Handles delta time calculation and backwards compatibility for states
        that don't accept dt parameter.
        
        The loop runs indefinitely until the game is closed.
        """
        while True:
            # Handle events for current state
            self.state.handle_events()

            # Calculate delta time in seconds for smooth animations
            dt_ms = self.clock.tick(FPS)
            dt = dt_ms / 1000.0

            # Update current state with delta time (backwards compatible)
            try:
                self.state.update(dt)
            except TypeError:
                # Fallback for states that don't accept dt parameter
                self.state.update()

            # Render current state and update display
            self.state.draw()
            pygame.display.flip()
