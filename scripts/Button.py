import pygame
import os
from .config import *

# Reusable standardized button class
class Button:

    # Button constructor
    def __init__(self, dimensions, text, callback, font=None,
                 text_color=BLACK, 
                 base_color=PRIMARY_COLOR, 
                 hover_color=ACCENT_COLOR,
                 is_building=False,
                 image_path=None,
                 fontsize=24,
                 scale_to_fit=True):
        
        self.rect = pygame.Rect(dimensions) 
        self.text = text
        self.font = pygame.font.Font(None, fontsize)
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.text_color = text_color
        self.border_color = self.text_color
        self.is_hovered = False
        self.is_building = is_building
        self.level = 1

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


    # Draw the button so it appears on the screen
    def draw(self, surface):

        if self.image:
            # Draw image directly
            surface.blit(self.image, self.rect)
            if self.is_hovered:
                # Slightly darken or highlight overlay
                overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 60))  # 60 alpha = slight tint
                surface.blit(overlay, self.rect.topleft)
        else:
            # Fallback: draw colored rectangle
            self.current_color = self.hover_color if self.is_hovered else self.base_color
            pygame.draw.rect(surface, self.current_color, self.rect, border_radius=4)
            pygame.draw.rect(surface, self.border_color, self.rect, width=1, border_radius=4)
    
        # Text overlay
        if self.text:
    
            padding = 0.5
            max_w = self.rect.width - padding * 2

            wrapped_lines = self.wrap_text(
                self.text,
                self.font,
                max_w
            )

            # Center vertically
            line_height = self.font.get_linesize()
            total_height = len(wrapped_lines) * line_height
            y = self.rect.y + (self.rect.height - total_height) // 2

            # Draw each wrapped line centered
            for line in wrapped_lines:
                surf = self.font.render(line, True, self.text_color)
                rect = surf.get_rect(center=(self.rect.centerx, y + line_height // 2))
                surface.blit(surf, rect)
                y += line_height

    # Handle all events for the button (so far just hover or click)
    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return self.callback() # Defined callback when the button is clicked
            
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        return None
    
    # Same functionality as wrap text in menu
    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
    
    # Handles upgrade building event
    def upgrade(self):
        if self.level < 3:
            self.level += 1
            return
        else:
            return    
