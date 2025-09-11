import pygame
from pygame.locals import *
import settings
import sound

#Fonts and menu formatting automatically rescale with the screen width

color = {"white":(255, 255, 255), "blue": (0, 0, 200), "yellow": (255, 255, 0),
    "light_grey": (200, 200, 255), "grey": (100, 100, 100), "red": (180, 0, 0)}

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
        # Renders each line of title message and options
        self.lines = (
            [Menu.text_font.render(line, False, color["white"]) for line in message]
            +[Menu.menu_font.render(line, False, color["light_grey"], color["blue"]) for line in options]
        )
        self.active_lines = (
            [Menu.menu_font.render(line, False, color["yellow"], color["grey"]) for line in options]
        )
        # Calculates size of the menu
        self.line_height = max(line.get_height()
                               for line in self.lines)
        self.line_length = max(line.get_width()
                               for line in self.lines)
        self.h = 2*Menu.boundary_size + self.number_of_lines * \
            (self.line_height+Menu.line_distance) + \
            Menu.title_distance - Menu.line_distance
        if len(message) > 1:
            self.h += Menu.title_distance
        self.w = 2*Menu.boundary_size + self.line_length
        # Blit all the lines onto a blue rectangle with red boundary
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill((color["red"]))
        background = pygame.Surface((self.w-Menu.boundary_size, self.h-Menu.boundary_size))
        background.fill(color["blue"])
        self.surface.blit(background, (Menu.boundary_size//2,Menu.boundary_size//2))
        self.line_position = []
        for i in range(self.number_of_lines):
            if i in range(1,len(message)):
                x = Menu.boundary_size
            else:
                x = (self.w-self.lines[i].get_width())//2
            y = Menu.boundary_size+i*(self.line_height+Menu.line_distance)
            if i>0:
                y+=Menu.title_distance
            if i >= len(message) and len(message) > 1:
                y+=Menu.title_distance
            self.line_position.append((x, y))
            self.surface.blit(self.lines[i], (x, y))
            
    def blit(self, screen):
        """blits the menu with the current selection highlighted"""
        self.highlighted_surface = self.surface.copy()
        j = self.current_selection
        self.highlighted_surface.blit(self.active_lines[j], (self.line_position[j+len(self.message)]))
        screen.blit(self.highlighted_surface, ((
            screen.get_width()-self.w)//2, (screen.get_height()-self.h)//2))

    def move_selection(self, event_key):
        """Navigate through the menu"""
        sound.menu_move.play()
        self.current_selection = (
            (self.current_selection + {K_w : -1, K_s : 1}[event_key]) % len(self.options)
        )

    @classmethod
    def choose_current_selection(cls, game):
        sound.menu_select.play()
        match game.active_menu.options[game.active_menu.current_selection]:
            case "Restart" | "Start game":
                game.mode = "game"
                game.level.restart()
            case "Exit":
                game.running = False
            case "Continue":
                game.mode = "game"
                if game.active_menu == level_solved_menu:
                    game.level.next()
            case "Highscores":
                game.active_menu = Menu(message=["Highscores", "Do you think you can beat them?", ""]+[str(score[0]) + " " + str(score[1]) for score in game.highscores], options=["Go back"])
            case "Go back":
                game.active_menu = main_menu
            case "Buy Premium":
                game.active_menu = premium_menu
            case "Credits":
                game.active_menu = credits_menu
            case "Check high scores":
                if len(game.highscores) < settings.max_number_of_highscores or game.level.ship.score > game.highscores[-1][1]:
                    pygame.mixer.stop()
                    sound.new_highscore.play()
                    game.highscore_place = [i for i in range(len(game.highscores)) if game.highscores[i][1]<game.level.ship.score][0]
                    game.highscores.append(["", game.level.ship.score])
                    game.highscores = sorted(game.highscores, key=lambda x: x[1], reverse=True)[:settings.max_number_of_highscores]
                    game.mode = "enter name"
                else:
                    game.active_menu = Menu(message=["No new high score!", "Your score was too low,", "maybe next time!", ""]+[str(score[0]) + " " + str(score[1]) for score in game.highscores], options=["OK"])
            case _:
                game.active_menu = highscores_checked

# Menus in the game
main_menu = Menu(message=["Space invaders"],
                options=["Start game", "Highscores", "Buy Premium", "Credits", "Exit"])
pause_menu = Menu(message=["PAUSE"],
                options=["Continue", "Restart", "Exit"])
level_solved_menu = Menu(message=["Level solved!", "Press RETURN to", "start the next level."],
                options=["Continue"])
game_won_menu = Menu(message=["Congratulations!", "You have finished", "all available levels!"],
                options=["Check high scores","Restart", "Exit"])
game_over_menu = Menu(message=["Game over!", "You ran out of lives!"],
                options=["Check high scores","Restart", "Exit"])
highscores_checked = Menu(message=["Play again?"], options=["Restart", "Exit"])
premium_menu = Menu(message=["Haha", "Did you believe there", "is a premium version?"],
                options=["Go back"])
credits_menu = Menu(message=["Credits", "Programmed with pygame", "Sprites and sound effects from",
                "pixabay.com, craftpix.net,", "opengameart.net and Google Gemini"],
                options=["Go back"])