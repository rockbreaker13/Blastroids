import math
import random

import pygame
from pygame import sprite, Vector2

from . import config
from .effects import Pop, Pow


class Ship(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.pos = Vector2(config.W // 2, 832)
        self.vel = Vector2(0, -32)
        self.speed = 0.75
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.width *= 0.8
        self.max_hp = 10
        self.hp = 10
        self.cooldown = 0
        self.shoot_delay = 16
        self.max_bomb_cooldown = 100
        self.bomb_cooldown = self.max_bomb_cooldown
        self.laser_vel = Vector2(0, -10)
        self.laser_dmg = 1
        self.bosses_killed = 0
        self.multishot = 0
        self.shrapnel = 12
        self.laser_exp = 1
        self.sin_lasers = False
        self.angular_lasers = False
        self.ray_bomb = False
        self.color = (255, 255, 255)
        self.is_rainbow = False
        self.hue = 0
        self.rainbow_color = pygame.Color(0, 0, 0)
        self.rainbow_color.hsva = (self.hue, 0, 0, 0)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.vel.x += self.speed
        if keys[pygame.K_a]:
            self.vel.x -= self.speed
        if keys[pygame.K_w]:
            self.vel.y -= self.speed
        if keys[pygame.K_s]:
            self.vel.y += self.speed

        if self.cooldown > 0:
            self.cooldown -= 1

        mouse = pygame.mouse.get_pressed()
        if mouse[0] and self.cooldown <= 0:
            for i in range(-self.multishot, self.multishot + 1):
                config.lasers.add(
                    MainLaser(self.pos.copy(), Vector2(i * 2, self.laser_vel.y))
                )
            if self.sin_lasers:
                config.lasers.add(SinLaser(self.pos.copy(), Vector2(0, (-i - 5) * 2), "sin 1"))
                config.lasers.add(SinLaser(self.pos.copy(), Vector2(0, (-i - 5) * 2), "sin 2"))
            self.cooldown = self.shoot_delay
            config.shoot_sound.play()
        if mouse[2] and self.bomb_cooldown <= 0:
            config.lasers.add(Bomb(self.pos.copy(), Vector2(0, -15)))
            self.bomb_cooldown = self.max_bomb_cooldown

        self.pos += self.vel
        self.vel *= 0.9
        self.rect.center = self.pos
        if self.is_rainbow:
            for i in range(2):
                config.pows.add(
                    Pow(
                        self.pos.x,
                        self.pos.y,
                        1,
                        self.rainbow_color,
                        Vector2(0, 10),
                    )
                )
        else:
            for i in range(2):
                config.pows.add(Pow(self.pos.x, self.pos.y, 1, self.color, Vector2(0, 10)))

        if self.rect.centerx < 0 or self.rect.centerx > config.W:
            self.pos.x -= self.vel.x * 1.1
            self.vel.x = 0
        if self.rect.centery < 0 or self.rect.centery > config.H:
            self.pos.y -= self.vel.y * 1.1
            self.vel.y = 0

        if self.hp <= 0:
            self.kill()
            config.pops.add(Pop(self.pos.x, self.pos.y, 64, (255, 255, 255)))

    def draw(self, screen):
        if self.angular_lasers:
            self.color = (255, 0, 0)
        if self.sin_lasers:
            self.color = (0, 255, 0)
        if self.ray_bomb:
            self.color = (0, 0, 255)
        if self.sin_lasers and self.angular_lasers:
            self.color = (255, 255, 0)
        if self.sin_lasers and self.ray_bomb:
            self.color = (0, 255, 255)
        if self.angular_lasers and self.ray_bomb:
            self.color = (255, 0, 255)
        if self.sin_lasers and self.angular_lasers and self.ray_bomb:
            self.is_rainbow = True

        visual_rect = self.image.get_rect(center=self.pos)
        if self.is_rainbow:
            self.hue = (self.hue + 1) % 360
            self.rainbow_color.hsva = (self.hue, 100, 100, 100)
            pygame.draw.polygon(
                screen,
                self.rainbow_color,
                (
                    (self.pos.x, self.pos.y - self.image.get_height() // 2),
                    visual_rect.bottomright,
                    visual_rect.bottomleft,
                ),
            )
        else:
            pygame.draw.polygon(
                screen,
                self.color,
                (
                    (self.pos.x, self.pos.y - self.image.get_height() // 2),
                    visual_rect.bottomright,
                    visual_rect.bottomleft,
                ),
            )


class Asteroid(sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(40, 80)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.pos = Vector2(random.randint(0, config.W), -100)
        self.speed = random.uniform(2, 4)
        self.rect = self.image.get_rect(center=self.pos)
        if config.ship.sprite:
            if config.ship.sprite.bosses_killed >= config.lv_req:
                self.hp = (size * size) // (
                    640 // (2 ** config.ship.sprite.bosses_killed + 1)
                )
            else:
                self.hp = (size * size) // (
                    1280 // (config.ship.sprite.bosses_killed + 1)
                )

    def update(self):
        self.pos.y += self.speed
        if self.pos.y > config.H + 100:
            self.kill()
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 10, 15)


class Laser(sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()
        self.pos = Vector2(pos)
        self.vel = vel
        self.timer = 0
        self.color = (255, 255, 255)


class MainLaser(Laser):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        if config.ship.sprite and config.ship.sprite.angular_lasers:
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            self.color = (255, 0, 0)
        else:
            self.image = pygame.Surface((12, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += self.vel
        if self.pos.y < -50 or self.pos.y > config.H + 50:
            self.kill()
        self.rect.center = self.pos

    def draw(self, screen):
        if config.ship.sprite and config.ship.sprite.angular_lasers:
            pygame.draw.polygon(
                screen,
                self.color,
                [
                    self.pos + Vector2(0, -25),
                    self.pos + Vector2(12, 12),
                    self.pos,
                    self.pos + Vector2(-12, 12),
                ],
            )
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=5)


class Bomb(Laser):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += self.vel
        self.vel *= 0.96
        if self.vel.length() < 0.5:
            self.explode()
        self.rect.center = self.pos

    def explode(self):
        config.screen_shake = 15
        if config.ship.sprite:
            count = config.ship.sprite.shrapnel
            if config.ship.sprite.ray_bomb:
                for i in range(count):
                    angle = (i / count) * 360
                    vel = Vector2(
                        math.cos(math.radians(angle)), math.sin(math.radians(angle))
                    ) * 8
                    config.lasers.add(Ray(self.pos, vel))
            else:
                for i in range(count):
                    angle = (i / count) * (math.pi * 2)
                    vel = Vector2(math.cos(angle), math.sin(angle)) * 8
                    config.lasers.add(Shrapnel(self.pos, vel))
        self.kill()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)


class Shrapnel(Laser):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += self.vel
        if not config.screen.get_rect().collidepoint(self.pos):
            self.kill()
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, 8)


class SinLaser(Laser):
    def __init__(self, pos, vel, kind):
        super().__init__(pos, vel)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.color = (0, 255, 0)
        self.rect = self.image.get_rect(center=self.pos)
        self.kind = kind

    def update(self):
        self.timer += 0.25
        if self.kind == "sin 1":
            side = 1
        else:
            side = -1
        self.vel.x = math.sin(self.timer) * 25 * side
        self.pos += self.vel
        if not config.screen.get_rect().collidepoint(self.pos):
            self.kill()
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, 10)


class Ray(Laser):
    def __init__(self, pos, vel):
        super().__init__(pos, vel)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.color = (0, 0, 255)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.timer += 1
        if self.timer >= 30:
            self.kill()
        self.rect.center = self.pos

    def draw(self, screen):
        width = max(1, 30 - self.timer)
        pygame.draw.line(
            screen, self.color, self.pos, self.pos + self.vel * 1000, width
        )


class EnemyLaser(sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.pos = Vector2(pos.x, pos.y)
        self.speed = 6
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos.y += self.speed
        if self.pos.y > config.H + 50:
            self.kill()
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            (self.rect.topleft, self.rect.topright, (self.pos.x, self.rect.bottom)),
        )


class Boss(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = Vector2(config.W // 2, 150)
        self.rect = pygame.Rect(0, 0, 150, 150)
        self.rect.center = self.pos
        self.max_hp = 150 * (config.ship.sprite.bosses_killed + 1)
        self.hp = self.max_hp
        self.timer = 0
        self.phase = 1
        self.next_phase = 600

    def update(self):
        self.next_phase -= 1
        if self.phase == 1:
            self.timer += 0.01
            self.pos.x = (config.W // 2) + math.tan(self.timer) * 350
            if self.next_phase % 20 == 0:
                config.shoot_sound.play()
                config.enemy_lasers.add(EnemyLaser(self.pos.copy()))
        elif self.phase == 2:
            self.timer += 0.02
            self.pos.x = (config.W // 2) + math.cos(self.timer) * 350
            self.pos.y = 150 + math.sin(self.timer) * 50
            if round(self.timer, 2) in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:
                config.shoot_sound.play()
                config.enemy_lasers.add(EnemyLaser(self.pos.copy()))
            if self.timer >= math.pi * 2:
                self.timer = 0
        elif self.phase == 3:
            self.timer += 1
            self.pos = Vector2(config.W // 2, 150)
            if self.timer == 60:
                config.shoot_sound.play()
                for i in range(6):
                    config.enemy_lasers.add(EnemyLaser(Vector2((config.W // 5) * i, -20)))
            if self.timer == 120:
                self.timer = 0
                config.shoot_sound.play()
                for i in range(5):
                    config.enemy_lasers.add(EnemyLaser(Vector2((config.W // 5) * i + (config.W // 10), -20)))
        if self.next_phase == 0:
            self.next_phase = 600
            self.phase += 1
            self.timer = 0
            if self.phase == 4:
                self.phase = 1
        self.rect.center = self.pos

    def draw(self, screen):
        color = (255, 255, 255)
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            (
                self.pos + Vector2(20, -20),
                self.pos + Vector2(20, 20),
                self.pos + Vector2(-20, 20),
            ),
        )
        pygame.draw.line(
            screen,
            (0, 0, 0),
            self.pos + Vector2(-40, 20),
            self.pos + Vector2(40, 20),
            5,
        )
        pygame.draw.line(
            screen,
            (0, 0, 0),
            self.pos + Vector2(20, 40),
            self.pos + Vector2(20, -40),
            5,
        )
        pygame.draw.line(
            screen,
            (0, 0, 0),
            self.pos + Vector2(-35, 35),
            self.pos + Vector2(35, -35),
            int(7.5),
        )
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 5, border_radius=15)
        health_rect = pygame.Rect(
            self.rect.left, self.rect.top - 30, self.rect.width, 10
        )
        pygame.draw.rect(screen, (50, 0, 0), health_rect)
        fill_w = int((self.hp / self.max_hp) * self.rect.width)
        pygame.draw.rect(
            screen, (255, 0, 0), (health_rect.left, health_rect.top, fill_w, 10)
        )
