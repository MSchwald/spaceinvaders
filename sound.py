import pygame

# Sound library for convenient access from other modules
class Sound:
    @classmethod
    def init(cls):
        pygame.mixer.init()          
        
        # Enemy sounds
        cls.alien_spawn = pygame.mixer.Sound("sounds/alien_spawn.wav")
        cls.alienblob = pygame.mixer.Sound("sounds/alienblob.wav")
        cls.blob_merge = pygame.mixer.Sound("sounds/blob_merge.ogg")
        cls.blob_spawns = pygame.mixer.Sound("sounds/blob_spawns.ogg")

        # Shooting sounds
        cls.alienshoot1 = pygame.mixer.Sound("sounds/alienshoot1.wav")
        cls.alienshoot2 = pygame.mixer.Sound("sounds/alienshoot2.wav")
        cls.alienshoot3 = pygame.mixer.Sound("sounds/alienshoot3.wav")
        cls.blubber = pygame.mixer.Sound("sounds/blubber.ogg")
        cls.bullet = pygame.mixer.Sound("sounds/bullet.wav")
        cls.enemy_shoot = pygame.mixer.Sound("sounds/enemy_shoot.ogg")
        cls.explosion = pygame.mixer.Sound("sounds/explosion.ogg")
        cls.shoot = pygame.mixer.Sound("sounds/shoot.ogg")

        # Hitting sounds
        cls.metal_hit = pygame.mixer.Sound("sounds/metal_hit.ogg")
        cls.player_hit = pygame.mixer.Sound("sounds/player_hit.ogg")
        cls.slime_hit = pygame.mixer.Sound("sounds/slime_hit.ogg")
        cls.asteroid = pygame.mixer.Sound("sounds/asteroid.ogg")
        cls.asteroid.set_volume(0.5)
        cls.small_asteroid = pygame.mixer.Sound("sounds/small_asteroid.ogg")
        cls.enemy_hit = pygame.mixer.Sound("sounds/enemy_hit.ogg")

        # Item sounds
        cls.bad_item = pygame.mixer.Sound("sounds/bad_item.ogg")
        cls.collect_missile = pygame.mixer.Sound("sounds/collect_missile.ogg")
        cls.extra_life = pygame.mixer.Sound("sounds/extra_life.ogg")
        cls.good_item = pygame.mixer.Sound("sounds/good_item.wav")
        cls.grow = pygame.mixer.Sound("sounds/grow.ogg")
        cls.item_collect = pygame.mixer.Sound("sounds/item_collect.ogg")
        cls.lose_life = pygame.mixer.Sound("sounds/lose_life.ogg")
        cls.ship_level_up = pygame.mixer.Sound("sounds/ship_level_up.ogg")
        cls.shrink = pygame.mixer.Sound("sounds/shrink.ogg")

        # Level status sounds
        cls.game_over = pygame.mixer.Sound("sounds/game_over.wav")
        cls.game_won = pygame.mixer.Sound("sounds/game_won.ogg")
        cls.level_solved = pygame.mixer.Sound("sounds/start.ogg")

        # Menu sounds
        cls.menu_move = pygame.mixer.Sound("sounds/menu_move.wav")
        cls.menu_select = pygame.mixer.Sound("sounds/menu_select.wav")
        cls.new_highscore = pygame.mixer.Sound("sounds/new_highscore.ogg")

        # Shield sounds
        cls.shield = pygame.mixer.Sound("sounds/shield.ogg")
        cls.shield_reflect = pygame.mixer.Sound("sounds/shield_reflect.ogg")

        # Unused sounds
        cls.teleport = pygame.mixer.Sound("sounds/teleport.wav")
        cls.laser1 = pygame.mixer.Sound("sounds/laser1.wav")
        cls.laser2 = pygame.mixer.Sound("sounds/laser2.wav")