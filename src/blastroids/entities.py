import math
import random

import pygame
from pygame import sprite, Vector2

from blastroids import config, effects, ui


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
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel.x += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel.x -= self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
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
                config.lasers.add(
                    SinLaser(self.pos.copy(), Vector2(0, (-i - 5) * 2), "sin 1")
                )
                config.lasers.add(
                    SinLaser(self.pos.copy(), Vector2(0, (-i - 5) * 2), "sin 2")
                )
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
                    effects.Pow(
                        self.pos.x,
                        self.pos.y,
                        1,
                        self.rainbow_color,
                        Vector2(0, 10),
                    )
                )
        else:
            for i in range(2):
                config.pows.add(
                    effects.Pow(self.pos.x, self.pos.y, 1, self.color, Vector2(0, 10))
                )

        if self.rect.centerx < 0 or self.rect.centerx > config.W:
            self.pos.x -= self.vel.x * 1.1
            self.vel.x = 0
        if self.rect.centery < 0 or self.rect.centery > config.H:
            self.pos.y -= self.vel.y * 1.1
            self.vel.y = 0

        if self.hp <= 0:
            self.kill()
            config.pops.add(effects.Pop(self.pos.x, self.pos.y, 64, (255, 255, 255)))

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
            self.hp = (size * size) // (
                1280
                // (
                    (config.ship.sprite.bosses_killed + 1)
                    * (config.zone * 2.5 if config.zone != 1 else 1)
                )
            )
        else:
            self.hp = (size * size) // 1280

    def update(self):
        self.pos.y += self.speed
        if self.pos.y > config.H + 100:
            self.kill()
        self.rect.center = self.pos

    def draw(self, screen):
        if config.zone == 1:
            self.color = (255, 255, 255)
        if config.zone == 2:
            self.color = (255, 255, 0)
        pygame.draw.rect(screen, self.color, self.rect, 10, 15)


class Laser(sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()
        config.shoot_sound.play()
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
                    vel = (
                        Vector2(
                            math.cos(math.radians(angle)), math.sin(math.radians(angle))
                        )
                        * 8
                    )
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
        pygame.draw.circle(screen, self.color, self.pos, 16, 4)


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
    def __init__(self, pos, vel=Vector2(0, 5), kind="ball"):
        super().__init__()
        config.shoot_sound.play()
        self.kind = kind
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        self.pos = Vector2(pos.x, pos.y)
        self.vel = vel
        self.rect = self.image.get_rect(center=self.pos)
        if self.kind == "ball":
            self.color = (255, 200, 200)
            self.timer = 0
            # Draw the circle onto the Surface itself, not the screen
            pygame.draw.circle(self.image, self.color, (30, 30), 30)
        if self.kind == "aim":
            self.color = (255, 200, 200)
            self.timer = 0
            self.phase = 1
            # Calculate direction to ship once at spawn
            if config.ship.sprite:
                self.direction = (config.ship.sprite.pos - self.pos).angle_to(
                    Vector2(0, 1)
                )
            else:
                self.direction = 0

            # FIX: Draw relative to the Surface (30, 30 is center), not global self.pos
            pygame.draw.polygon(
                self.image,
                (255, 0, 0),
                [
                    Vector2(30, 30) + Vector2(0, -30),
                    Vector2(30, 30) + Vector2(10, -10),
                    Vector2(30, 30) + Vector2(30, 0),
                    Vector2(30, 30) + Vector2(10, 10),
                    Vector2(30, 30) + Vector2(0, 30),
                    Vector2(30, 30) + Vector2(-10, 10),
                    Vector2(30, 30) + Vector2(-30, 0),
                    Vector2(30, 30) + Vector2(-10, -10),  # Fixed the duplicate point
                ],
            )

    def update(self):
        if self.kind == "ball":
            if config.screen.get_rect().contains(self.rect) == False:
                self.timer += 1
                new_alpha = max(0, 255 - int(self.timer * 2.55))
                self.image.set_alpha(new_alpha)
                if new_alpha <= 0:
                    self.kill()
            self.pos += self.vel
            self.rect.center = self.pos
        if self.kind == "aim":
            start = self.pos
            self.pos += self.vel
            if config.screen.get_rect().contains(self.rect) == False:
                self.timer += 1
                new_alpha = max(0, 255 - int(self.timer * 2.55))
                self.image.set_alpha(new_alpha)
                if new_alpha <= 0:
                    self.kill()
            if self.phase == 1:
                self.vel *= 0.9
                # After slowing down enough, transition to phase 2
                if self.vel.length() < 0.5:
                    self.phase = 2
                    # Re-calculate direction just before firing for better accuracy
                    if config.ship.sprite:
                        target_vel = config.ship.sprite.pos - self.pos
                        if target_vel.length() > 0:
                            self.vel = target_vel.normalize() * 12
                        else:
                            self.vel = Vector2(0, 12)
                    else:
                        self.vel = Vector2(0, 12)

            # Update rect after movement
            self.rect.center = self.pos
            config.effects.add(effects.Line(start, self.pos, (255, 0, 0), 10))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Boss1(sprite.Sprite):
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
        self.dm = 1 + (config.ship.sprite.bosses_killed * 0.15)

    def update(self):
        self.next_phase -= 1
        if round(self.dm) == 1:
            if self.phase == 1:
                self.timer += 0.01
                self.pos.x = (config.W // 2) + math.tan(self.timer) * 350
                if self.next_phase % 20 == 0:
                    config.enemy_lasers.add(EnemyLaser(self.pos.copy()))
            elif self.phase == 2:
                self.timer += 0.02
                self.pos.x = (config.W // 2) + math.cos(self.timer) * 350
                self.pos.y = 150 + math.sin(self.timer) * 50
                if round(self.timer, 2) in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:

                    config.enemy_lasers.add(EnemyLaser(self.pos.copy()))
                if self.timer >= math.pi * 2:
                    self.timer = 0
            elif self.phase == 3:
                self.timer += 1
                self.pos = Vector2(config.W // 2, 150)
                if self.timer == 60:

                    for i in range(6):
                        config.enemy_lasers.add(
                            EnemyLaser(Vector2((config.W // 5) * i, -20))
                        )
                if self.timer == 120:
                    self.timer = 0

                    for i in range(5):
                        config.enemy_lasers.add(
                            EnemyLaser(
                                Vector2((config.W // 5) * i + (config.W // 10), -20)
                            )
                        )
        elif round(self.dm) >= 2:
            if self.phase == 1:
                self.timer += 1
                if self.timer in [5, 25, 45, 65, 85]:
                    self.pos = Vector2(
                        random.randint(50, config.W - 50),
                        random.randint(50, 400),
                    )
                    self.rect.center = self.pos
                    # shoot three lasers in a spread pattern
                    for i in range(3):
                        config.enemy_lasers.add(
                            EnemyLaser(self.pos, Vector2(-2 + (i * 2), 5))
                        )
                if self.timer == 240:
                    self.timer = 0
            if self.phase == 2:
                self.timer += 1
                if self.timer == 60:
                    self.timer = 0
                    self.pos = Vector2(
                        random.randint(50, config.W - 50),
                        random.randint(50, 400),
                    )
                    self.rect.center = self.pos
                    for i in range(12):
                        angle = (i / 12) * 360
                        vel = (
                            Vector2(
                                math.cos(math.radians(angle)),
                                math.sin(math.radians(angle)),
                            )
                            * 5
                        )
                        config.enemy_lasers.add(EnemyLaser(self.pos.copy(), vel))

            if self.phase == 3:
                self.timer += 1

                # Movement Math: timer never resets, so movement is continuous
                angle = self.timer / 50
                radius_x = 350
                radius_y = 150
                center_x = config.W // 2
                center_y = 200

                self.pos.x = center_x + math.cos(angle) * radius_x
                self.pos.y = center_y + math.sin(angle) * radius_y
                self.rect.center = self.pos

                if random.randint(0, 20) == 0:
                    amount_x = random.randint(3, 6)
                    for i in range(amount_x):
                        config.enemy_lasers.add(
                            EnemyLaser(
                                Vector2(random.randint(32, config.W - 32), -20),
                                Vector2(0, random.uniform(5, 15)),
                            )
                        )

        if self.next_phase == 0:
            self.next_phase = 600
            self.phase += 1
            self.timer = 0
            self.pos = Vector2(config.W // 2, 150)
            self.rect.center = self.pos

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


class Boss2(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = Vector2(config.W // 2, 150)
        self.rect = pygame.Rect(0, 0, 150, 150)
        self.rect.center = self.pos
        self.max_hp = 300 * (config.ship.sprite.bosses_killed + 1)
        self.hp = self.max_hp
        self.timer = 0
        self.phase = 3
        self.next_phase = 600
        self.dm = 2 + (config.ship.sprite.bosses_killed * 0.15)

    def update(self):
        self.next_phase -= 1
        if round(self.dm) == 1:
            if self.phase == 1:
                self.timer += 0.01
                if self.timer % 0.25 < 0.01:
                    for i in range(amount := 10):
                        direction = Vector2(5, 5).rotate(i * (360 / amount))
                        # By using the actual self.timer value here,
                        # each wave will have a different starting rotation.
                        config.enemy_lasers.add(
                            EnemyLaser(
                                self.pos.copy(),
                                direction.rotate(self.timer * (540 / amount)),
                            )
                        )
            if self.phase == 2:
                self.timer += 0.005
                if round(self.timer, 3) in [
                    0.1,
                    0.2,
                    0.3,
                    0.4,
                    0.5,
                ]:
                    for i in range(5):
                        config.enemy_lasers.add(
                            EnemyLaser(
                                self.pos.copy(),
                                Vector2((i - 2) * 7.5, 10),
                            )
                        )
                if self.timer >= 1:
                    self.timer = 0
                    start = self.pos
                    self.pos = Vector2(
                        random.randint(50, config.W - 50),
                        random.randint(50, 400),
                    )
                    config.effects.add(effects.Line(start, self.pos, (255, 255, 0), 50))
            if self.phase == 3:
                self.timer += 1
                if self.timer % 50 == 24:
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(100, 100),
                            self.pos - Vector2(100, -100),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(100, -100),
                            self.pos - Vector2(100, 100),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(-100, 100),
                            self.pos - Vector2(100, 100),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(100, 100),
                            self.pos - Vector2(-100, 100),
                            (255, 255, 0),
                        )
                    )
                elif self.timer % 50 == 0:
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(0, 141),
                            self.pos - Vector2(141, 0),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(141, 0),
                            self.pos - Vector2(0, 141),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(0, -141),
                            self.pos - Vector2(141, 0),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(141, 0),
                            self.pos - Vector2(0, -141),
                            (255, 255, 0),
                        )
                    )

                if self.timer % 25 == 0:
                    config.enemy_lasers.add(
                        EnemyLaser(
                            self.pos.copy(),
                            Vector2(17.5, 17.5).rotate(random.randint(1, 180) - 90),
                            "aim",
                        )
                    )
        elif round(self.dm) >= 2:
            if self.phase == 1:
                self.timer += 0.01
                if self.timer % 0.20 < 0.01:
                    for i in range(amount := 10):
                        direction = Vector2(10, 10).rotate(i * (360 / amount))
                        # By using the actual self.timer value here,
                        # each wave will have a different starting rotation.
                        config.enemy_lasers.add(
                            EnemyLaser(
                                self.pos.copy(),
                                direction.rotate(self.timer * (540 / amount)),
                            )
                        )
            if self.phase == 2:
                self.timer += 0.005
                if round(self.timer, 3) in [
                    0.1,
                    0.2,
                    0.3,
                    0.4,
                    0.5,
                ]:
                    for i in range(5):
                        config.enemy_lasers.add(
                            EnemyLaser(self.pos.copy(), Vector2(i - 2, 10), "aim")
                        )
                if self.timer >= 1:
                    self.timer = 0
                    start = self.pos
                    self.pos = Vector2(
                        random.randint(50, config.W - 50),
                        random.randint(50, 400),
                    )
                    config.effects.add(effects.Line(start, self.pos, (255, 255, 0), 50))
            if self.phase == 3:
                self.timer += 1
                if self.timer % 50 == 24:
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(100, 100),
                            self.pos - Vector2(100, -100),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(100, -100),
                            self.pos - Vector2(100, 100),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(-100, 100),
                            self.pos - Vector2(100, 100),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(100, 100),
                            self.pos - Vector2(-100, 100),
                            (255, 255, 0),
                        )
                    )
                elif self.timer % 50 == 0:
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(0, 141),
                            self.pos - Vector2(141, 0),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(141, 0),
                            self.pos - Vector2(0, 141),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(0, -141),
                            self.pos - Vector2(141, 0),
                            (255, 255, 0),
                        )
                    )
                    config.effects.add(
                        effects.Line(
                            self.pos + Vector2(141, 0),
                            self.pos - Vector2(0, -141),
                            (255, 255, 0),
                        )
                    )

                if self.timer % 20 == 0:
                    config.enemy_lasers.add(
                        EnemyLaser(
                            self.pos.copy(),
                            Vector2(17.5, 17.5).rotate(random.randint(1, 180) - 90),
                            "aim",
                        )
                    )

        if self.next_phase == 0:
            self.next_phase = 600
            self.phase += 1
            self.timer = 0
            self.pos = Vector2(config.W // 2, 150)
            self.rect.center = self.pos

            if self.phase == 4:
                self.phase = 1
        self.rect.center = self.pos

    def draw(self, screen):

        color = (255, 255, 0)
        pygame.draw.circle(screen, color, self.pos, 75)
        pygame.draw.line(
            screen,
            (color[0] - 50, color[1] - 50, color[2]),
            self.pos - Vector2(0, 74),
            self.pos + Vector2(0, 74),
            5,
        )
        pygame.draw.line(
            screen,
            (color[0] - 50, color[1] - 50, color[2]),
            self.pos - Vector2(74, 0),
            self.pos + Vector2(74, 0),
            5,
        )
        pygame.draw.polygon(
            screen,
            (color[0] - 75, color[1] - 75, color[2]),
            [self.pos + Vector2(37.5, -37.5), self.pos, self.pos + Vector2(37.5, 0)],
            5,
        )
        pygame.draw.circle(
            screen, (color[0] - 75, color[1] - 75, color[2]), self.pos, 75, 10
        )
        health_rect = pygame.Rect(
            self.rect.left, self.rect.top - 30, self.rect.width, 10
        )
        pygame.draw.rect(screen, (50, 0, 0), health_rect)
        fill_w = int((self.hp / self.max_hp) * self.rect.width)
        pygame.draw.rect(
            screen, (255, 0, 0), (health_rect.left, health_rect.top, fill_w, 10)
        )
