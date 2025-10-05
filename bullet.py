import pygame, settings, sound
from display import Display
from sprite import Sprite
from image import Image
from math import ceil

class Bullet(Sprite):
    """A class to manage the bullets shot by the player or enemies"""

    def __init__(self, type, size=None, owner=None, damage=None, effect_time = None, image=None,
            v=None, grid=None, center=None, x=0, y=0, direction=None,
            constraints=None,
            boundary_behaviour="vanish",
            animation_type=None, frames=None, fps=None, animation_time=None):
        self.type = type
        self.owner = owner or settings.bullet_owner[type]
        self.damage = damage or settings.bullet_damage[type]
        self.effect_time = effect_time or settings.bullet_effect_time[type]
        constraints = constraints or pygame.Rect([0, 0, Display.screen_width, Display.screen_height])
        v = v if v is not None else settings.bullet_speed[type]
        if direction is None:
            if self.owner == "player":
                direction = (0,-1)
            else:
                direction = (0,1)
        match type:
            case 1 | 2 | 3:
                if image is None:
                    image = Image.load(f'images/bullet/{type}.png')
            case "blubber":
                self.size = size or settings.alien_energy["blob"]
                image = Image.blubber[size-1]
                self.damage = ceil(size/settings.alien_energy["blob"]*settings.bullet_damage[type])
            case "missile":
                frames = Image.load(f"images/bullet/explosion")
                animation_type, animation_time = "vanish", settings.missile_duration
                self.hit_enemies = pygame.sprite.Group()
            case "g":
                frames = Image.load(f"images/bullet/g")
                animation_type, animation_time = "once", 0.5
        self.play_firing_sound()
        super().__init__(image, grid=grid, center=center, x=x, y=y, v=v, direction=direction,
            constraints=constraints, boundary_behaviour=boundary_behaviour,
            animation_type=animation_type, frames=frames, animation_time=animation_time)

    def play_firing_sound(self):
        match self.type:
            case 1 | 2 | 3:
                sound.bullet.play()
            case "blubber":
                sound.blubber.play()
            case "g":
                sound.alienshoot1.play()
            case "missile":
                sound.explosion.play()

    def update(self, dt):
        #timer, movement and animation get handled in the Sprite class
        super().update(dt)
        # explosions by missiles need to get deleted manually after their duration
        if self.effect_time is not None and self.timer > self.effect_time:
            self.kill()

    def reflect(self):
        sound.shield.stop()
        sound.shield_reflect.play()
        if self.type == "blubber":
            self.direction = (-self.direction[0],-self.direction[1])
            self.change_image(Image.reflected_blubber[self.size-1])
        else:
            super().reflect(flip_x=True, flip_y=True)