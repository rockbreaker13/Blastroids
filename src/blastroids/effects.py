import random
import pygame
from pygame import sprite, Vector2

from blastroids import config


class Pop(sprite.Sprite):
    def __init__(self, x, y, r, c=(255, 255, 255)):
        super().__init__()
        self.radius = r
        self.pos = Vector2(x, y)
        self.color = c
        self.v = 5

    def update(self):
        self.radius += self.v
        self.v -= 1
        if self.radius <= 1:
            self.kill()

    def draw(self, screen):
        if self.radius > 0:
            pygame.draw.circle(
                screen,
                self.color,
                self.pos,
                int(self.radius),
                max(1, int(self.radius // 5)),
            )


class Pow(sprite.Sprite):
    def __init__(self, x, y, m, c, d=Vector2(0, 0)):
        super().__init__()
        self.pos = Vector2(x, y)
        if d == Vector2(0, 0):
            self.vel = Vector2(random.uniform(-m, m), random.uniform(-m, m))
        else:
            self.vel = d
        self.color = c
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.size = random.randint(8, 16)
        self.direction = d

    def update(self):
        self.life -= self.decay
        if self.life <= 0:
            self.kill()
        self.pos += self.vel
        self.vel *= 0.95
        if self.direction == Vector2(0, 0):
            self.vel += Vector2(random.randint(-3, 3), random.randint(-3, 3))
        else:
            if self.direction.x != 0:
                self.vel.y += random.randint(-1, 1)
                if self.direction.y > 0:
                    self.vel.y += random.randint(0, 5)
                elif self.direction.y < 0:
                    self.vel.y += random.randint(-5, 0)
            elif self.direction.y != 0:
                self.vel.x += random.randint(-1, 1)
                if self.direction.x > 0:
                    self.vel.x += random.randint(0, 5)
                elif self.direction.x < 0:
                    self.vel.x += random.randint(-5, 0)

    def draw(self, screen):
        s = int(self.size * self.life)
        if s > 0:
            pygame.draw.circle(screen, self.color, self.pos, s)


class ScreenEffect(sprite.Sprite):
    def __init__(self, color=(0, 0, 0), initial_alpha=0, fade_speed=0):
        super().__init__()
        self.image = pygame.Surface((config.W, config.H))
        self.image.fill(color)
        self.alpha = initial_alpha
        self.fade_speed = fade_speed
        self.rect = self.image.get_rect()
        self.image.set_alpha(self.alpha)

    def update(self):
        self.alpha += self.fade_speed
        if self.alpha < 0:
            self.kill()
        elif self.alpha > 255:
            self.alpha = 255
        self.image.set_alpha(int(self.alpha))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
