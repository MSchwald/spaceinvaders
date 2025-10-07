import pygame, settings, sound
from image import Image, GraphicData
from sprite import Sprite
from bullet import Bullet
from display import Display
from item import Item
from random import random, choice, randint, sample
from math import pi, sqrt, sin, cos
from settings import AlienType, ALIEN, BULLET, ITEM
from physics import Vector, norm, normalize, inelastic_collision, ball_collision_data

class Alien(Sprite):
    """Manage sprites, spawning and actions of enemies"""

    def __init__(self, type: AlienType, level, energy=None, v=None,
                constraints=None, boundary_behaviour="reflect",
                **pos_kwargs):
        # level: needs access to the level object from the game file
        # energy and v allow overwriting their standard settings for given AlienType        
        self.type = type
        v = v if v is not None else type.speed
        constraints = constraints or pygame.Rect(0, 0, Display.screen_width, Display.screen_height)
        self.energy = energy or type.energy
        self.level = level
        self.random_cycle_time = type.random_cycle_time
        if self.random_cycle_time:
            self.cycle_time = randint(self.random_cycle_time[0],self.random_cycle_time[1])
            self.action_timer = 0
        else:
            self.cycle_time, self.action_timer = None, None

        # Load alien graphics
        if type.name == "blob":
            self.parent_center = None
            graphic = GraphicData(image = Image.blob[self.energy-1])
        else:
            graphic = GraphicData(path = f"images/alien/{type.name}", scaling_width = type.width, colorkey = type.colorkey,
                    animation_type = type.animation_type, fps = type.fps)
                
        super().__init__(graphic = graphic,
                v=v, constraints=constraints, boundary_behaviour=boundary_behaviour, **pos_kwargs)
            

    def play_spawing_sound(self):
        match self.type.name:
            case "purple": sound.alien_spawn.play()
            case "blob": sound.blob_spawns.play()

    @property
    def mass(self):
        """mass of an enemy, relevant for collisions between asteroids and blobs"""
        match self.type.name:
            case "blob": return self.energy
            case "big_asteroid" | "small_asteroid":
                return (self.w/Display.grid_width)**3
            case _:
                return None

    def update(self, dt):
        #asteroids can collide (elastic collision of 2d balls)
        if self.type.name in ["big_asteroid","small_asteroid"]:
            for ast in self.level.asteroids:
                ball1, ball2 = self.ball, ast.ball
                collision_time, new_v1, new_v2 = ball_collision_data(ball1, ball2)
                if collision_time is not None:
                    super().update_position(collision_time)
                    Sprite.update_position(ast, collision_time)
                    self.direction, ast.direction = tuple(new_v1), tuple(new_v2)
                    self.v, ast.v = norm(new_v1), norm(new_v2)                   
                    super().update_position(-collision_time)
                    Sprite.update_position(ast,-collision_time)
            super().update(dt)

        # aliens move without collisions
        else:
            #checks if it is time for the alien to do an action
            if self.cycle_time and not self.timer_on_hold and self.level.status != "start":
                self.action_timer += dt
                if self.action_timer >= self.cycle_time:
                    self.action_timer -= self.cycle_time
                    if self.random_cycle_time:
                        self.cycle_time = randint(self.random_cycle_time[0],self.random_cycle_time[1])
                    self.do_action()
            #blobs gravitate towards their parent center where they split last
            if self.type.name == "blob" and self.parent_center:
                x1, y1 = self.parent_center
                x2, y2 = self.rect.center
                n = normalize(Vector(x1, y1) - Vector(x2, y2))
                vr = Vector(self.vx, self.vy) * n
                ar = - ALIEN.BLOB.acceleration * (vr - self.splitting_speed) * abs(vr + self.splitting_speed)
                self.a = tuple(ar * n)
            #timer, movement and animation get handled in the Sprite class
            super().update(dt)

    def do_action(self):
        match self.type.name:
            case "purple": self.shoot(BULLET.GREEN)
            case "ufo": self.throw_alien(ALIEN.PURPLE)
            case "blob": self.shoot(BULLET.BLUBBER, size=self.energy)

    # types of alien actions
    def shoot(self, bullet_type, size=None):
        bullet = Bullet(bullet_type,size=size,center=self.rect.midbottom)
        self.level.bullets.add(bullet)
        bullet.play_firing_sound()

    def throw_alien(self, alien_type):
        self.level.aliens.add(Alien(ALIEN.PURPLE,self.level,center=self.rect.midbottom, direction=(2*random()-1,1)))

    def get_damage(self, damage):
        if self.type.name == "big_asteroid":
            self.energy = 0
        elif self.type.name == "blob":
            self.kill()
        else:
            self.energy = max(self.energy-damage,0)
            if self.energy > 0 and self.type.name not in ["big_asteroid", "small_asteroid"]:
                {"purple": sound.enemy_hit, "ufo": sound.metal_hit}[self.type.name].play()
            else:
                self.kill()

    def split(self, new_type: AlienType, amount):
        if self.direction==(0,0):
            phi = random()
            w = (cos(2*pi*phi),sin(2*pi*phi))
        else:
            w = (self.direction[0] / self.norm, self.direction[1] / self.norm) 
        if new_type.name == "blob":
            #blobs split into smaller blobs with integer mass
            m = self.mass // amount
            diff = self.mass - amount * m
            masses = [m + 1 if i < diff else m for i in sample(range(amount), amount)]
        pieces = []
        for i in range(amount):
            if new_type.name == "blob":
                if masses[i] == 0:
                    continue
                speed_factor = masses[i] ** (-1/2)
            else:
                speed_factor = 1
            phi_i = (2*i+1) * pi / amount
            dir_i = Vector(self.vx, self.vy) + new_type.speed * speed_factor * Vector(w[0]*cos(phi_i)-w[1]*sin(phi_i), w[0]*sin(phi_i)+w[1]*cos(phi_i))
            energy = masses[i] if new_type.name == "blob" else None
            pieces.append(Alien(new_type, self.level, energy=energy, direction=tuple(dir_i), v=norm(dir_i), center=self.rect.center,
                constraints=self.constraints, boundary_behaviour=self.boundary_behaviour))
        return(pieces)

    @classmethod
    def merge(cls, blob1, blob2):
        """merges two blobs, but could be generalized to other aliens"""
        x1, y1 = blob1.rect.center
        x2, y2 = blob2.rect.center
        p1, p2 = Vector(x1, y1), Vector(x2, y2)
        v1, v2 = Vector(blob1.vx, blob1.vy), Vector(blob2.vx, blob2.vy)
        m1, m2 = blob1.mass, blob2.mass
        new_center, new_v = inelastic_collision(p1, p2, v1, v2, m1, m2)
        return Alien(ALIEN.BLOB, blob1.level, energy = blob1.energy + blob2.energy,
                center = tuple(new_center), direction = tuple(new_v), v = norm(new_v))

    def kill(self):
        """removes an enemy, triggers splitting for asteroids and blobs""" 
        if self.energy <= 0:
            {"big_asteroid": sound.asteroid, "small_asteroid": sound.small_asteroid, "purple": sound.alienblob, "ufo":sound.alienblob, "blob":sound.alienblob}[self.type.name].play()
            self.level.ship.get_points(self.type.points)
            if random() <= ITEM.PROBABILITY:
                self.level.items.add(Item(choice(ITEM.LIST), self.level, center=self.rect.center))
        if self.type.name == "big_asteroid":
            # big asteroids split into smaller asteroids when hit
            for piece in self.split(ALIEN.SMALL_ASTEROID, self.type.pieces):
                self.level.asteroids.add(piece)
        if self.type.name == "blob":
            if self.energy > 1:
                sound.slime_hit.play()
                for blob in self.split(ALIEN.BLOB, self.type.pieces):
                    blob.splitting_speed = blob.v # needed later to calculate the gravitation towards the parent center
                    blob.parent_center = self.rect.center
                    self.level.aliens.add(blob)
                    self.level.blobs.add(blob)
            elif self.energy == 1:
                sound.alienblob.play()
                self.level.ship.get_points(self.type.points)
                self.hard_kill()
        super().kill()

    def hard_kill(self):
        """removes an enemy without further splitting"""
        self.level.aliens.remove(self)
        self.level.blobs.remove(self)
        super(Alien, self).kill()

    def reflect(self):
        if self.level.status != "start":
            sound.shield.stop()
            sound.shield_reflect.play()
        super().reflect(flip_x=False, flip_y=False)