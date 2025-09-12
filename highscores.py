import pygame
from pathlib import Path
import json
import settings
import string
from menu import Menu, color

class Highscores:
    """class to load, render, update and save highscores"""
    def __init__(self):
        """load saved high scores or use the default ones from the settings"""
        self.allowed_chars = string.ascii_letters + string.digits # characters allowed in the players' names
        try:
            with open("highscores.json", "r", encoding="utf-8") as f:
                self.score_list = json.load(f)
        except FileNotFoundError:
            self.load_default_highscores()
        self.fill_list_with_zeros()
        self.render_lines()

    def load_default_highscores(self):
        self.score_list = sorted(settings.default_highscores, key=lambda x: x[1], reverse=True)[:settings.max_number_of_highscores]
        self.fill_list_with_zeros()
        self.render_lines()
        self.save()

    def fill_list_with_zeros(self):
        while len(self.score_list) < settings.max_number_of_highscores:
            self.score_list.append(("",0))
 
    def save(self):
        with open("highscores.json", "w", encoding="utf-8") as f:
            json.dump(self.score_list, f)

    def render_lines(self):
        #format the score list as a table with two columns       
        self.players = [Menu.text_font.render(str(score[0])+" ", False, color["white"]) for score in self.score_list]
        self.scores = [Menu.text_font.render(str(score[1]), False, color["white"]) for score in self.score_list]
        self.player_w = max(player.get_width() for player in self.players)
        self.player_h = max(player.get_height() for player in self.players)
        self.score_w = max(score.get_width() for score in self.scores)
        self.score_h = max(score.get_height() for score in self.scores)
        self.line_length = self.player_w + self.score_w
        self.line_height = max(self.player_h, self.score_h)
        background = pygame.Surface((self.line_length, self.line_height))
        background.fill(color["blue"])
        self.lines = [background.copy() for i in range(settings.max_number_of_highscores)]
        for i in range(settings.max_number_of_highscores):
            self.lines[i].blit(self.players[i],(0,0))
            self.lines[i].blit(self.scores[i],(self.line_length-self.scores[i].get_width(),0))

    def highscore_rank(self, score):
        beaten_scores = [i for i in range(settings.max_number_of_highscores) if score > self.score_list[i][1]]
        if beaten_scores:
            return beaten_scores[0]
        return None

    def insert_score(self, name, score, rank):
        self.score_list = self.score_list[:-1]
        self.score_list.insert(rank, [name, score])

    def update_name(self, name, rank):
        self.score_list[rank][0] = name
        self.render_lines()