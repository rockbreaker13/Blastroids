import random
import pygame
from pygame import sprite, Vector2

from blastroids import config, effects, upgrades

class Mmanim:
    def __init__(self, W, H):
        self.center = Vector2(W // 2, H // 2)
        self.timer = 0
        self.t1_center = Vector2(W // 2, -200)
        self.t2_center = Vector2(W // 3, -200)
        self.t3_center = Vector2((W // 3) * 2, -200)
        self.t1_target = Vector2(W // 2, 200)
        self.t2_target = Vector2(W // 3, 250)
        self.t3_target = Vector2((W // 3) * 2, 250)
        self.b_center = Vector2(W // 2, H + 200)
        self.b_target = Vector2(W // 2, 400)
        self.b_center2 = Vector2(W // 2, H + 200)
        self.b_target2 = Vector2(W // 2, 500)

        self.b_font = pygame.font.SysFont("corbel", 96, bold=True)
        self.b_surf = self.b_font.render("Blastroids", True, (255, 255, 255))
        self.b_rect = self.b_surf.get_rect(center=self.b_center)

        self.b_font2 = pygame.font.SysFont("corbel", 96, bold=False)
        self.b_surf2 = self.b_font2.render(
            "Tπe 3 Prime Functions", True, (255, 255, 255)
        )
        self.b_rect2 = self.b_surf2.get_rect(center=self.b_center2)

    def update(self):
        self.timer += 1
        ease = 0.12
        self.t1_center += (self.t1_target - self.t1_center) * ease
        self.t2_center += (self.t2_target - self.t2_center) * ease
        self.t3_center += (self.t3_target - self.t3_center) * ease
        self.b_center += (self.b_target - self.b_center) * ease
        self.b_center2 += (self.b_target2 - self.b_center2) * ease

        self.b_rect.center = self.b_center
        self.b_rect2.center = self.b_center2

        if abs(self.t1_center.y - self.t1_target.y) < 0.5:
            self.t1_center.y = self.t1_target.y
        if abs(self.t2_center.y - self.t2_target.y) < 0.5:
            self.t2_center.y = self.t2_target.y
        if abs(self.t3_center.y - self.t3_target.y) < 0.5:
            self.t3_center.y = self.t3_target.y
        if abs(self.b_center.y - self.b_target.y) < 0.5:
            self.b_center.y = self.b_target.y
        if abs(self.b_center2.y - self.b_target2.y) < 0.5:
            self.b_center2.y = self.b_target2.y

    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            (255, 0, 0),
            (
                (self.t1_center.x, self.t1_center.y - 100),
                (self.t1_center.x + 100, self.t1_center.y + 100),
                (self.t1_center.x - 100, self.t1_center.y + 100),
            ),
        )
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            (
                (self.t1_center.x, self.t1_center.y - 50),
                (self.t1_center.x + 60, self.t1_center.y + 75),
                (self.t1_center.x - 60, self.t1_center.y + 75),
            ),
        )

        pygame.draw.polygon(
            screen,
            (0, 255, 0),
            (
                (self.t2_center.x, self.t2_center.y - 100),
                (self.t2_center.x + 100, self.t2_center.y + 100),
                (self.t2_center.x - 100, self.t2_center.y + 100),
            ),
        )
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            (
                (self.t2_center.x, self.t2_center.y - 50),
                (self.t2_center.x + 60, self.t2_center.y + 75),
                (self.t2_center.x - 60, self.t2_center.y + 75),
            ),
        )

        pygame.draw.polygon(
            screen,
            (0, 0, 255),
            (
                (self.t3_center.x, self.t3_center.y - 100),
                (self.t3_center.x + 100, self.t3_center.y + 100),
                (self.t3_center.x - 100, self.t3_center.y + 100),
            ),
        )
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            (
                (self.t3_center.x, self.t3_center.y - 50),
                (self.t3_center.x + 60, self.t3_center.y + 75),
                (self.t3_center.x - 60, self.t3_center.y + 75),
            ),
        )

        screen.blit(self.b_surf, self.b_rect)
        screen.blit(self.b_surf2, self.b_rect2)


class Button(sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        self.pos = Vector2(x, y)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 75, 75)
        self.kind = kind
        self.font = pygame.font.SysFont("corbel", 48, bold=False)
        self.text = self.font.render(self.kind, True, (0, 0, 0))
        self.clicked = False
        self.current_size = 75
        self.target_size = 0

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self.current_size += (self.target_size - self.current_size) * 0.2
        self.rect.size = (self.current_size, self.current_size)
        if self.rect.collidepoint(mouse_pos):
            self.target_size = 150
            if mouse_click[0]:
                self.clicked = True
        else:
            self.target_size = 100
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=10)
        tr = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, tr)


class Bar(sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.max_width = 256
        self.kind = kind
        if kind == "hp":
            self.pos = Vector2(148, config.H - 40)
        else:
            self.pos = Vector2(148, config.H - 70)
        self.rect = pygame.Rect(0, 0, self.max_width, 20)
        self.rect.center = self.pos

    def draw(self, screen):
        if not config.ship.sprite:
            return
        pygame.draw.rect(screen, (50, 50, 50), self.rect, border_radius=10)
        if self.kind == "hp":
            ratio = config.ship.sprite.hp / config.ship.sprite.max_hp
        else:
            ratio = 1 - (
                config.ship.sprite.bomb_cooldown / config.ship.sprite.max_bomb_cooldown
            )
        fr = pygame.Rect(
            self.rect.left,
            self.rect.top,
            int(self.max_width * max(0, min(1, ratio))),
            20,
        )
        pygame.draw.rect(screen, (255, 255, 255), fr, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, 10)


class Upgrade(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 255, 255))
        self.pos = Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.upgrade_effect = None

        upgrade_options = [
            upgrades.ShootSpeedUpgrade(),
            upgrades.LaserVelocityUpgrade(),
            upgrades.ShipRepairUpgrade(),
            upgrades.ExplodingLasersUpgrade(),
            upgrades.MultishotUpgrade(),
            upgrades.MoreBombShrapnelUpgrade(),
        ]
        if config.ship.sprite and config.ship.sprite.bosses_killed >= config.lv_req:
            upgrade_options.extend(
                [
                    upgrades.SinLasersUpgrade(),
                    upgrades.AngularLasersUpgrade(),
                    upgrades.RayBombsUpgrade(),
                ]
            )

        self.upgrade_effect = random.choice(upgrade_options)
        self.font = pygame.font.SysFont("corbel", 32, bold=False)
        self.text = self.font.render(self.upgrade_effect.name, True, (0, 0, 0))
        self.wait = 20
        self.current_size = 200
        self.target_size = 200
        self.lerp_speed = 0.2

    def _handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.target_size = 500
            if pygame.mouse.get_pressed()[0] and self.wait <= 0 and config.ship.sprite:
                self.upgrade_effect.apply(config.ship.sprite)
                for i in range(25):
                    config.pows.add(
                        effects.Pow(self.pos.x, self.pos.y, 20, (255, 255, 255))
                    )
                self.kill()
        else:
            self.target_size = 400

    def _update_size(self):
        self.current_size += (self.target_size - self.current_size) * self.lerp_speed
        scale_factor = self.current_size / 200.0
        new_dim = max(1, int(100 * scale_factor))
        self.image = pygame.Surface((new_dim * 1.5, new_dim / 1.5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.wait > 0:
            self.wait -= 1
        self._handle_input()
        self._update_size()

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect,
            border_radius=int(self.rect.width / 4),
        )
        pygame.draw.rect(
            screen, (0, 0, 0), self.rect, 3, border_radius=int(self.rect.width / 4)
        )
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)


class BossName(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.life = 180
        self.alpha = 255
        if config.boss_image_asset:
            self.image = config.boss_image_asset
        else:
            self.image = pygame.font.SysFont("Arial", 48, bold=True).render(
                "THE GUARDIAN", True, (255, 255, 255)
            )
        self.rect = self.image.get_rect(center=(config.W // 2, 300))

    def update(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.alpha -= 5
            if self.alpha <= 0:
                self.kill()

    def draw(self, screen):
        self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)
