## imports
import pygame

## constants
from .config import (
    PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, BLACK, GRAY
)

## reusable standardized button class
class Button:

    ## button constructor
    def __init__(self, dimensions, text, callback, font=None,
                 text_color=TEXT_COLOR, 
                 base_color=PRIMARY_COLOR, 
                 hover_color=ACCENT_COLOR):
        
        self.rect = pygame.Rect(dimensions)
        self.text = text
        self.font = pygame.font.Font(None, 20)
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.text_color = text_color
        self.is_hovered = False

    ## draw the button so it appears on the screen
    def draw(self, surface):

        self.current_color = self.hover_color if self.is_hovered else self.base_color
        
        # draw button with rounded corners
        pygame.draw.rect(surface=surface,
                         color=self.current_color,
                         rect=self.rect,
                         border_radius=4)
        
        pygame.draw.rect(surface=surface, 
                         color=BLACK, 
                         rect=self.rect, 
                         width=1, 
                         border_radius=4)
    
        # draw text of the button in the center of the "rectangle"
        text_surface = self.font.render(self.text, True, self.text_color)
        text_shape = text_surface.get_rect(center=self.rect.center)
        surface.blit(source=text_surface, dest=text_shape)

    # handle all events for the button (so far just hover or click)
    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
                return self.callback() # defined callback when the button is clicked
            
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        return None