## imports
import numpy as np
import sys
import pygame

## constants
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PRIMARY_COLOR, ACCENT_COLOR, TEXT_COLOR, GRAY, BLACK, BG_COLOR, WHITE
)
from Button import Button

## menu class for all popups and buttons
class Menu:
    def __init__(self, menu_manager, title, text, user_options, button_dimensions=None, user_closable=False):

        self.menu_manager = menu_manager
        self.title = title
        self.text = text
        self.user_options = user_options
        self.user_closable=user_closable
        self.buttons = []
        self.close_button = None
        
        # default button layout if user doesn't specify
        default_button_dimensions = {
            "width": 200,
            "height": 40,
            "spacing": 20,
            "button_offset" : 70
        }
        # merge defaults with user-specified values
        self.button_dimensions = {**default_button_dimensions, **(button_dimensions or {})}

        self.title_font = pygame.font.Font(None, 40)
        self.text_font = pygame.font.Font(None, 24)
        self.button_text_font = pygame.font.Font(None, 30)

        # define the geometry for the menu
        self.width = 500
        self.height = 400
        self.x = (SCREEN_WIDTH - self.width) // 2 # so that the menu is centered
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self._menu_setup() # call the protected helper function to organize the menu interface

    # create wrapper so that after the callback from the dev is executed, we close out the memu
    def _create_button_callback(self, custom_callback):

        def wrapped_callback():
            result = custom_callback()
            self.menu_manager.close_menu()
            return result

        return wrapped_callback
    
    def _menu_setup(self):

        button_width = self.button_dimensions["width"]
        button_height = self.button_dimensions["height"]
        spacing = self.button_dimensions["spacing"]
        button_offset = self.button_dimensions["button_offset"]

        # calculate how to center the buttons
        starting_x_pos = self.x + (self.width - (button_width * len(self.user_options)) + (spacing * (len(self.user_options) - 1))) // 2

        button_y = self.y + self.height - button_offset

        # create the buttons for all the ones listed for the menu
        for i, (button_text, callback) in enumerate(self.user_options):

            button_x = starting_x_pos + (i * (button_width + spacing))
            button_box = (button_x, button_y, button_width, button_height)
            
            wrapped_callback = self._create_button_callback(callback)

            button = Button(dimensions=button_box, 
                            text=button_text, 
                            callback=wrapped_callback, 
                            font=self.button_text_font)
            self.buttons.append(button)

        # The 'x' button to close menu
        if self.user_closable:
            ## DONT HARD CODE THE VALS FIXME
            close_size = 20
            close_x = self.x + self.width - close_size - 10
            close_y = self.y + 10
            close_dims = (close_x, close_y, close_size, close_size)
            
            self.close_button = Button(dimensions=close_dims, 
                                       text="x", 
                                       callback=self.menu_manager.close_menu, 
                                       font=self.button_text_font,
                                       base_color=BG_COLOR, 
                                       hover_color=GRAY, 
                                       text_color=BLACK)
    
    # so that the text wraps around and is not cut off if too long
    def _wrap_text(self, surface, text, font, x, y, max_width):

        space = ' '
        words = text.split(space)
        lines = [] # curating line by line to fit the button width
        current_line = []
        for word in words:
            test = space.join(current_line + [word])

            # if adding a word is within the maximum width, add it
            if font.size(test)[0] < max_width:
                current_line.append(word)
            # if not, add a space and move to a new line
            else: 
                lines.append(space.join(current_line))
                current_line = [word]
        lines.append(space.join(current_line))

        for line in lines:
            text_surface = font.render(line, True, TEXT_COLOR)
            surface.blit(source=text_surface, 
                         dest=(x, y))
            
            y += font.get_linesize()

    # so that the whole menu container shows up on the screen
    def draw(self, surface):
        
        # dim the main window
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) ## DONT HARD CODE FIXME
        surface.blit(overlay, (0, 0))

        # draw the main menu window that pops up
        pygame.draw.rect(surface=surface, 
                         color=WHITE, 
                         rect=self.rect, 
                         border_radius=6)
        
        pygame.draw.rect(surface=surface, 
                         color=PRIMARY_COLOR, 
                         rect=self.rect, 
                         width=3, 
                         border_radius=6)

        # draw the title text
        title_surface = self.title_font.render(self.title, True, TEXT_COLOR)
        title_shape = title_surface.get_rect(centerx=self.rect.centerx, y=self.y + 30) # 30 is a placeholder FIXME
        surface.blit(title_surface, title_shape)
        
        # draw the main message text so that it doesn't overflow if the button is to
        self._wrap_text(surface=surface, 
                        text=self.text, 
                        font=self.text_font, 
                        x=self.x + 30, 
                        y=self.y + 90, 
                        max_width=self.width - 60) ## 30 pixel margin on both side dont hard code FIXME

        # draw the buttons
        for button in self.buttons:
            button.draw(surface=surface)
            
        # draw the close button
        if self.close_button:
            self.close_button.draw(surface=surface)

    # handle events for all the buttons possible
    def handle_event(self, event):

        for button in self.buttons:
            button.handle_event(event) # pass in the button's event handler that we created
            
        if self.close_button:
            self.close_button.handle_event(event)


## MenuManager Wrapper
class MenuManager:

    def __init__(self, main_data):

        self.main_buttons = []
        self.active_menu = None
        
        self._main_setup(main_data)

    def _main_setup(self, data):

        ## values hard coded for now FIXME
        button_width = 250
        button_height = 60
        start_y = 150
        spacing = 20

        # its callbacks should be the menu showing
        for i, (text, callback) in enumerate(data):
            rect = ((SCREEN_WIDTH - button_width) // 2, 
                    start_y + (i * (button_height + spacing)), 
                    button_width, 
                    button_height)
            
            button = Button(dimensions=rect, 
                            text=text, 
                            callback=callback, 
                            base_color=PRIMARY_COLOR, 
                            hover_color=ACCENT_COLOR)
            
            self.main_buttons.append(button)

    def open_menu(self, menu):

        self.active_menu = menu

    def close_menu(self):

        self.active_menu = None
        print("menu closed")

    def draw(self, surface):
        
        # draw main menu buttons
        for button in self.main_buttons:
            button.draw(surface)
            
        # draw modal menu last, so it appears on top
        if self.active_menu:
            self.active_menu.draw(surface)

    def handle_event(self, event):

        # Events are only handled by the menu if it is active
        if self.active_menu:
            self.active_menu.handle_event(event)
        else:
            # If no menu is active, allow interaction with main buttons.
            for button in self.main_buttons:
                button.handle_event(event)