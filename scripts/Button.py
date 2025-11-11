## imports
import pygame
import os

## constants
from .config import *

## reusable standardized button class
class Button:

    ## button constructor
    def __init__(self, dimensions, text, callback, font=None,
                 text_color=BLACK, 
                 base_color=PRIMARY_COLOR, 
                 hover_color=ACCENT_COLOR,
                 image_path=None,
                 fontsize=24,
                 scale_to_fit=True):
        
        self.rect = pygame.Rect(dimensions) # dimensions should be x,y,width,height
        self.text = text
        self.font = pygame.font.Font(None, fontsize)
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.text_color = text_color
        self.border_color = self.text_color
        self.is_hovered = False

        self.image = None
        if image_path:
            try:
                SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
                full_path = os.path.join(SCRIPT_DIR, image_path)
                loaded = pygame.image.load(full_path).convert_alpha()
                if scale_to_fit:
                    self.image = pygame.transform.smoothscale(loaded, self.rect.size)
                else:
                    self.image = loaded
            except Exception as e:
                print(f"Could not load image for button ({image_path}): {e}")
                self.image = None


    ## draw the button so it appears on the screen
    def draw(self, surface):

        if self.image:
            # draw image directly
            surface.blit(self.image, self.rect)
            if self.is_hovered:
                # slightly darken or highlight overlay
                overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 60))  # 60 alpha = slight tint
                surface.blit(overlay, self.rect.topleft)
        else:
            # fallback: draw colored rectangle
            self.current_color = self.hover_color if self.is_hovered else self.base_color
            pygame.draw.rect(surface, self.current_color, self.rect, border_radius=4)
            pygame.draw.rect(surface, self.border_color, self.rect, width=1, border_radius=4)
    
        # -- text overlay --
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_shape = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_shape)

    # handle all events for the button (so far just hover or click)
    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return self.callback() # defined callback when the button is clicked
            
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        return None