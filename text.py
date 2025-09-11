import pygame
from pygame.locals import *
import settings
import sound

#Fonts and menu formatting automatically rescale with the screen width

class Menu():
    """Class to create menus with a given title message and a given list of options"""
    pygame.font.init()
    menu_font_size = int(settings.menu_font_size*settings.screen_width/1600)
    text_font_size = int(settings.text_font_size*settings.screen_width/1600)
    menu_font = pygame.font.Font(settings.menu_font, menu_font_size)
    text_font = pygame.font.Font(settings.text_font, text_font_size)
    boundary_size = int(settings.menu_boundary*settings.screen_width/1600)
    title_distance = int(settings.title_menu_distance*settings.screen_width/1600)
    line_distance = int(settings.line_distance*settings.screen_width/1600)

    def __init__(self, message=["Press Return to continue."], options=["Continue"], current_selection=0):
        self.message = message
        self.options = options
        self.current_selection = current_selection
        self.number_of_lines = len(message)+len(options)
        self.lines = {}
        self.active_lines = {}
        for i in range(len(message)):
            # Renders each line of the title message
            self.lines[i] = Menu.text_font.render(
                message[i], False, (255, 255, 255))
        for j in range(len(options)):
            # Renders each of the options, inactive and active
            self.lines[len(message)+j] = Menu.menu_font.render(options[j],
                                                               False, (200, 200, 255), (0, 0, 255))
            self.active_lines[j] = Menu.menu_font.render(
                options[j], False, (255, 255, 0), (100, 100, 100))
        # Calculates size of the menu
        self.line_height = max(line.get_height()
                               for line in self.lines.values())
        self.line_length = max(line.get_width()
                               for line in self.lines.values())
        self.h = 2*Menu.boundary_size + self.number_of_lines * \
            (self.line_height+Menu.line_distance) + \
            Menu.title_distance - Menu.line_distance
        self.w = 2*Menu.boundary_size + self.line_length
        # Blit all the lines on a blue rectangle
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill((0, 0, 255))
        if message:
            #blit the title of the message in the center
            self.surface.blit(self.lines[0], ((self.w-self.lines[0].get_width())/2,
                              Menu.boundary_size))
        for i in range(1,len(message)):
            self.surface.blit(self.lines[i], (Menu.boundary_size,
                              Menu.boundary_size+i*(self.line_height+Menu.line_distance)))
        for i in range(len(message), self.number_of_lines):
            self.surface.blit(self.lines[i], ((self.w-self.lines[i].get_width(
            ))/2, Menu.title_distance+Menu.boundary_size+i*(self.line_height+Menu.line_distance)))
        # Create a surface for each possible highlighted option
        self.surface_highlighted = {}
        for j in range(len(self.options)):
            self.surface_highlighted[j] = self.surface.copy()
            self.surface_highlighted[j].blit(self.active_lines[j], ((self.w-self.active_lines[j].get_width(
            ))/2, Menu.title_distance+Menu.boundary_size+(len(message)+j)*(self.line_height+Menu.line_distance)))

    def move_selection(self, event_key):
        """Navigate through the menu"""
        sound.menu_move.play()
        if event_key == K_w:
            self.current_selection = (
                self.current_selection - 1) % len(self.options)
        if event_key == K_s:
            self.current_selection = (
                self.current_selection + 1) % len(self.options)

    def select(self):
        sound.menu_select.play()
        return self.options[self.current_selection]

    def blit(self, screen):
        """blits the menu with the current selection highlighted"""
        screen.blit(self.surface_highlighted[self.current_selection], ((
            screen.get_width()-self.w)/2, (screen.get_height()-self.h)/2))
