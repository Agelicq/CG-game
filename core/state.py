#!/usr/bin/env python3
"""State Base Class Module.

This module contains the abstract State class that serves as the base
for all game states in Astro Lost (menu, gameplay, intro, etc.).
"""

class State:
    """Abstract base class for all game states.
    
    Defines the interface that all game states must implement.
    Each state handles its own events, updates, and rendering.
    
    Attributes:
        game (GameManager): Reference to the main game manager instance.
    """
    
    def __init__(self, game):
        """Initialize the state.
        
        Args:
            game (GameManager): The main game manager instance.
        """
        self.game = game

    def handle_events(self):
        """Handle input events for this state.
        
        Should be overridden by subclasses to handle pygame events
        such as key presses, mouse clicks, window events, etc.
        """
        pass

    def update(self, dt=None):
        """Update the state logic.
        
        Should be overridden by subclasses to update game logic,
        animations, physics, etc.
        
        Args:
            dt (float, optional): Delta time in seconds since last frame.
            None for backwards compatibility.
        """
        pass

    def draw(self):
        """Render the state to the screen.
        
        Should be overridden by subclasses to handle all drawing
        operations for this state.
        """
        pass
