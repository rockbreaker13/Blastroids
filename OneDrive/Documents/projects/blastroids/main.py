def main():
    import sys
    import subprocess
    import importlib

    def ensure_dependencies(packages):
        for package in packages:
            try:
                importlib.import_module(package)
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    ensure_dependencies(["pygame"])

    import pygame
    from pygame import time, sprite, Vector2
    import random, math

    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("New Project")
    clock = time.Clock()
    pygame.mouse.set_visible(False)

    info = pygame.display.Info()

    W, H = info.current_w, info.current_h

    screen = pygame.display.set_mode((W, H))
    # Define screen_shake at the top level of main()
    global screen_shake
    screen_shake = 0

    boss_image_asset = None
    try:
        original_boss_img = pygame.image.load("assets/boss_name_1.png").convert_alpha()
        boss_image_asset = pygame.transform.scale(original_boss_img, (W - 100, 600))
        shoot_sound = pygame.mixer.Sound("assets/LaserShoot.wav")
        shoot_sound.set_volume(1)
        boom_sound = pygame.mixer.Sound("assets/explosion.wav")
        boom_sound.set_volume(1)
        hit_sound = pygame.mixer.Sound("assets/hitHurt.wav")
        hit_sound.set_volume(1)
        pygame.mixer.music.load("assets/blastroids.mp3")
    except Exception as e:
        print(f"Asset load failed: {e}")

    lv_req = 2
    # use this to easily change the level requirement for the special upgrades without having to search through the code

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

            # Update rect position to follow the vector
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
            # Ship 1
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

            # Ship 2
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

            # Ship 3
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

    class Ship(sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.pos = Vector2(W // 2, 832)
            self.vel = Vector2(0, -32)
            self.speed = 0.75
            self.rect = self.image.get_rect(center=self.pos)
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
                    lasers.add(
                        Laser(self.pos.copy(), "main", Vector2(i * 2, self.laser_vel.y))
                    )
                if self.sin_lasers == True:
                    lasers.add(
                        Laser(self.pos.copy(), "sin 1", Vector2(0, (-i - 5) * 2))
                    )
                    lasers.add(
                        Laser(self.pos.copy(), "sin 2", Vector2(0, (-i - 5) * 2))
                    )
                self.cooldown = self.shoot_delay
                shoot_sound.play()
            if mouse[2] and self.bomb_cooldown <= 0:
                # Bombs need a higher initial velocity so they don't explode immediately
                lasers.add(Laser(self.pos.copy(), "bomb", Vector2(0, -15)))
                self.bomb_cooldown = self.max_bomb_cooldown

            self.pos += self.vel
            self.vel *= 0.9
            self.rect.center = self.pos
            if self.is_rainbow:
                for i in range(2):
                    pows.add(
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
                    pows.add(Pow(self.pos.x, self.pos.y, 1, self.color, Vector2(0, 10)))

            if self.rect.centerx < 0 or self.rect.centerx > W:
                self.pos.x -= self.vel.x * 1.1
                self.vel.x = 0
            if self.rect.centery < 0 or self.rect.centery > H:
                self.pos.y -= self.vel.y * 1.1
                self.vel.y = 0

            if self.hp <= 0:
                self.kill()
                pops.add(Pop(self.pos.x, self.pos.y, 64, (255, 255, 255)))

        def draw(self, screen):
            # seperate colors at first
            if self.angular_lasers:
                self.color = (255, 0, 0)
            if self.sin_lasers:
                self.color = (0, 255, 0)
            if self.ray_bomb:
                self.color = (0, 0, 255)
            # combine colors if multiple are active
            if self.sin_lasers and self.angular_lasers:
                self.color = (255, 255, 0)
            if self.sin_lasers and self.ray_bomb:
                self.color = (0, 255, 255)
            if self.angular_lasers and self.ray_bomb:
                self.color = (255, 0, 255)
            if self.sin_lasers and self.angular_lasers and self.ray_bomb:
                self.is_rainbow = True
            if self.is_rainbow:
                self.hue = (self.hue + 1) % 360  # Increment hue and loop back at 360
                self.rainbow_color.hsva = (self.hue, 100, 100, 100)
                pygame.draw.polygon(
                    screen,
                    self.rainbow_color,
                    (
                        (self.pos.x, self.pos.y - self.image.get_height() // 2),
                        self.rect.bottomright,
                        self.rect.bottomleft,
                    ),
                )
            else:
                pygame.draw.polygon(
                    screen,
                    self.color,
                    (
                        (self.pos.x, self.pos.y - self.image.get_height() // 2),
                        self.rect.bottomright,
                        self.rect.bottomleft,
                    ),
                )

    class Astroid(sprite.Sprite):
        def __init__(self):
            super().__init__()
            size = random.randint(40, 80)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            self.pos = Vector2(random.randint(0, W), -100)
            self.speed = random.uniform(2, 4)
            self.rect = self.image.get_rect(center=self.pos)
            if ship.sprite:
                if ship.sprite.bosses_killed >= lv_req:
                    self.hp = (size * size) // (
                        640 // (2**ship.sprite.bosses_killed + 1)
                    )
                else:
                    self.hp = (size * size) // (1280 // (ship.sprite.bosses_killed + 1))

        def update(self):
            self.pos.y += self.speed
            if self.pos.y > H + 100:
                self.kill()
            self.rect.center = self.pos

        def draw(self, screen):
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 10, 15)

    class Laser(sprite.Sprite):
        # --- NEW CONSTANTS TO SOLVE YOUR ISSUE ---
        SHRAPNEL_RADIUS = 8  # Change this to make shrapnel smaller/bigger
        SHRAPNEL_SPEED = 8  # Base speed of shrapnel
        MAIN_LASER_WIDTH = 12  # Width of standard laser
        MAIN_LASER_HEIGHT = 30  # Height of standard laser
        # -----------------------------------------

        def __init__(self, pos, kind="main", vel=Vector2(0, -10)):
            super().__init__()
            self.kind = kind
            self.pos = Vector2(pos)
            self.vel = vel
            self.timer = 0
            self.color = (255, 255, 255)

            # Setup Hitbox and Colors
            if self.kind == "shrapnel":
                # Create a surface that matches our constant radius
                size = self.SHRAPNEL_RADIUS * 2
                self.image = pygame.Surface((size, size), pygame.SRCALPHA)
                self.rect = self.image.get_rect(center=self.pos)
            elif self.kind == "bomb":
                self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
                self.rect = self.image.get_rect(center=self.pos)
            elif self.kind in ["sin 1", "sin 2"]:
                self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
                self.color = (0, 255, 0)
                self.rect = self.image.get_rect(center=self.pos)
            elif self.kind == "ray":
                self.image = pygame.Surface(
                    (1, 1), pygame.SRCALPHA
                )  # Rays use line collision
                self.color = (0, 0, 255)
                self.rect = self.image.get_rect(center=self.pos)
            else:  # Main laser
                if ship.sprite and ship.sprite.angular_lasers:
                    self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
                    self.color = (255, 0, 0)
                else:
                    self.image = pygame.Surface(
                        (self.MAIN_LASER_WIDTH, self.MAIN_LASER_HEIGHT), pygame.SRCALPHA
                    )
                self.rect = self.image.get_rect(center=self.pos)

        def update(self):
            if self.kind == "main":
                self.pos += self.vel
                if self.pos.y < -50 or self.pos.y > H + 50:
                    self.kill()
            elif self.kind == "bomb":
                self.pos += self.vel
                self.vel *= 0.96
                if self.vel.length() < 0.5:
                    self.explode()
            elif self.kind == "shrapnel":
                self.pos += self.vel
                if not screen.get_rect().collidepoint(self.pos):
                    self.kill()
            elif self.kind in ["sin 1", "sin 2"]:
                self.timer += 0.25
                side = 1 if self.kind == "sin 1" else -1
                self.vel.x = math.sin(self.timer) * 25 * side
                self.pos += self.vel
                if not screen.get_rect().collidepoint(self.pos):
                    self.kill()
            elif self.kind == "ray":
                self.timer += 1
                if self.timer >= 30:
                    self.kill()

            self.rect.center = self.pos

        def explode(self):
            global screen_shake
            screen_shake = 15

            if ship.sprite:
                count = ship.sprite.shrapnel

            explode_color = self.color
            if ship.sprite and ship.sprite.angular_lasers:
                explode_color = (255, 0, 0)

            if self.kind == "bomb" and ship.sprite and ship.sprite.ray_bomb:
                for i in range(count):
                    # Calculate angle based on the count so they spread evenly
                    angle = (i / count) * 360
                    # Create the ray
                    new_laser = Laser(
                        self.pos,
                        "ray",
                        Vector2(
                            math.cos(math.radians(angle)), math.sin(math.radians(angle))
                        )
                        * self.SHRAPNEL_SPEED,
                    )
                    lasers.add(new_laser)

            # 3. THE SHRAPNEL LOGIC
            # This ensures that exactly 'count' lasers are created.
            elif self.kind == "bomb" and ship.sprite and ship.sprite.ray_bomb == False:
                for i in range(count):
                    # We spread the lasers evenly around 360 degrees
                    # This ensures they don't overlap and you can see the change in count!
                    angle = (i / count) * (math.pi * 2)

                    # Create the shrapnel laser
                    # We pass the color and ensure it's marked as shrapnel
                    new_laser = Laser(
                        self.pos,
                        "shrapnel",
                        Vector2(math.cos(angle), math.sin(angle)) * self.SHRAPNEL_SPEED,
                    )
                    lasers.add(new_laser)

            # Remove the bomb after it explodes
            self.kill()

        def draw(self, screen):
            if self.kind == "main":
                if ship.sprite and ship.sprite.angular_lasers:
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

            elif self.kind == "shrapnel":
                # Uses the constant directly for drawing
                pygame.draw.circle(screen, self.color, self.pos, self.SHRAPNEL_RADIUS)

            elif self.kind == "ray":
                width = max(1, 30 - self.timer)
                pygame.draw.line(
                    screen, self.color, self.pos, self.pos + self.vel * 1000, width
                )

            elif self.kind in ["sin 1", "sin 2"]:
                pygame.draw.circle(screen, self.color, self.pos, 10)

            elif self.kind == "bomb":
                pygame.draw.rect(screen, self.color, self.rect, border_radius=10)

    class eLaser(sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            self.pos = Vector2(pos.x, pos.y)
            self.speed = 6
            self.rect = self.image.get_rect(center=self.pos)

        def update(self):
            self.pos.y += self.speed
            if self.pos.y > H + 50:
                self.kill()
            self.rect.center = self.pos

        def draw(self, screen):
            pygame.draw.polygon(
                screen,
                (255, 255, 255),
                (self.rect.topleft, self.rect.topright, (self.pos.x, self.rect.bottom)),
            )

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
            self.image = pygame.Surface((W, H))
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
            self.pos = Vector2(148, H - 40 if kind == "hp" else H - 70)
            self.rect = pygame.Rect(0, 0, self.max_width, 20)
            self.rect.center = self.pos

        def draw(self, screen):
            if not ship.sprite:
                return
            pygame.draw.rect(screen, (50, 50, 50), self.rect, border_radius=10)
            ratio = (
                ship.sprite.hp / ship.sprite.max_hp
                if self.kind == "hp"
                else 1 - (ship.sprite.bomb_cooldown / ship.sprite.max_bomb_cooldown)
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
            self.type = None
            if ship.sprite and ship.sprite.bosses_killed >= lv_req:
                self.type = random.choice(
                    [
                        "shoot speed",
                        "laser velocity",
                        "ship repair",
                        "exploding lasers",
                        "multishot",
                        "more bomb shrapnel",
                    ]
                )
            else:
                self.type = random.choice(
                    [
                        "shoot speed",
                        "laser velocity",
                        "ship repair",
                        "exploding lasers",
                        "multishot",
                        "more bomb shrapnel",
                        "sin lasers",
                        "angular lasers",
                        "ray bombs",
                    ]
                )
            self.font = pygame.font.SysFont("corbel", 32, bold=False)
            self.text = self.font.render(self.type, True, (0, 0, 0))
            self.wait = 20
            self.current_size = 200
            self.target_size = 200
            self.lerp_speed = 0.2

        def update(self):
            if self.wait > 0:
                self.wait -= 1
            mouse_pos = pygame.mouse.get_pos()
            self.current_size += (
                self.target_size - self.current_size
            ) * self.lerp_speed
            if self.rect.collidepoint(mouse_pos):
                self.target_size = 500
                if pygame.mouse.get_pressed()[0] and self.wait <= 0:
                    if ship.sprite:
                        if self.type == "shoot speed":
                            if ship.sprite.shoot_delay >= 12:
                                ship.sprite.shoot_delay -= 2
                        elif self.type == "laser velocity":
                            if ship.sprite.laser_vel.y >= -26:
                                ship.sprite.laser_vel *= 1.5
                        elif self.type == "ship repair":
                            ship.sprite.hp = ship.sprite.max_hp
                        elif self.type == "exploding lasers":
                            if ship.sprite.laser_dmg < 2:
                                ship.sprite.laser_dmg += 1
                                ship.sprite.laser_exp += 1
                        elif self.type == "multishot":
                            if ship.sprite.multishot < 2:
                                ship.sprite.multishot += 1
                        elif self.type == "more bomb shrapnel":
                            if ship.sprite.shrapnel < 48:
                                ship.sprite.shrapnel += 4
                        elif self.type == "sin lasers":
                            if ship.sprite.bosses_killed >= lv_req:
                                ship.sprite.sin_lasers = True
                        elif self.type == "angular lasers":
                            if ship.sprite.bosses_killed >= lv_req:
                                ship.sprite.angular_lasers = True
                        elif self.type == "ray bombs":
                            if ship.sprite.bosses_killed >= lv_req:
                                ship.sprite.ray_bomb = True
                    for i in range(25):
                        pows.add(Pow(self.pos.x, self.pos.y, 20, (255, 255, 255)))
                    self.kill()
            else:
                self.target_size = 400

            scale_factor = self.current_size / 200.0
            new_dim = max(1, int(100 * scale_factor))
            self.image = pygame.Surface((new_dim * 1.5, new_dim / 1.5))
            self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect(center=self.pos)

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
            if boss_image_asset:
                self.image = boss_image_asset
            else:
                self.image = pygame.font.SysFont("Arial", 48, bold=True).render(
                    "THE GUARDIAN", True, (255, 255, 255)
                )
            self.rect = self.image.get_rect(center=(W // 2, 300))

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

    class Boss(sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.pos = Vector2(W // 2, 150)
            self.rect = pygame.Rect(0, 0, 150, 150)
            self.rect.center = self.pos
            self.max_hp = 150 * (ship.sprite.bosses_killed + 1)
            self.hp = self.max_hp
            self.timer = 0
            self.phase = 1
            self.next_phase = 600

        def update(self):
            self.next_phase -= 1
            if self.phase == 1:
                self.timer += 0.01
                self.pos.x = (W // 2) + math.tan(self.timer) * 350
                if self.next_phase % 20 == 0:
                    shoot_sound.play()
                    elasers.add(eLaser(self.pos.copy()))
            elif self.phase == 2:
                self.timer += 0.02
                self.pos.x = (W // 2) + math.cos(self.timer) * 350
                self.pos.y = 150 + math.sin(self.timer) * 50
                if round(self.timer, 2) in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:
                    shoot_sound.play()
                    elasers.add(eLaser(self.pos.copy()))
                if self.timer >= math.pi * 2:
                    self.timer = 0
            elif self.phase == 3:
                self.timer += 1
                self.pos = Vector2(W // 2, 150)
                if self.timer == 60:
                    shoot_sound.play()
                    for i in range(6):
                        elasers.add(eLaser(Vector2((W // 5) * i, -20)))
                if self.timer == 120:
                    self.timer = 0
                    shoot_sound.play()
                    for i in range(5):
                        elasers.add(eLaser(Vector2((W // 5) * i + (W // 10), -20)))
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

    def create_impact(pos, color=(255, 255, 255), count=5):
        for _ in range(count):
            pows.add(Pow(pos.x, pos.y, 10, color))
        pops.add(Pop(pos.x, pos.y, 20, color))

    ship = sprite.GroupSingle()
    astroids = sprite.Group()
    lasers = sprite.Group()
    elasers = sprite.Group()
    pops = sprite.Group()
    pows = sprite.Group()
    buttons = sprite.Group()
    ui_bars = sprite.Group()
    upgs = sprite.Group()
    effects = sprite.Group()
    boss_group = sprite.GroupSingle()
    overlay_ui = sprite.Group()

    def reset_game():
        global screen_shake
        screen_shake = 0
        astroids.empty()
        lasers.empty()
        elasers.empty()
        pops.empty()
        pows.empty()
        buttons.empty()
        ui_bars.empty()
        upgs.empty()
        effects.empty()
        boss_group.empty()
        overlay_ui.empty()
        ship.add(Ship())
        ui_bars.add(Bar("hp"))
        ui_bars.add(Bar("bomb cooldown"))
        return 30, 30, 0, True, 0.0, 0

    def play():
        pygame.mixer.music.play(-1)
        global screen_shake
        ast_cd, cacd, frames_passed, can_gen, bg_off, score = reset_game()
        running = True
        effects.add(ScreenEffect((0, 0, 0), 255, -5))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            bg_off = (bg_off + 1) % (H // 8)
            interval = (
                max(600, 3600 - (ship.sprite.bosses_killed * 200))
                if ship.sprite
                else 3600
            )
            if (
                frames_passed > 0
                and frames_passed % interval == 0
                and not boss_group.sprite
            ):
                boss_group.add(Boss())
                overlay_ui.add(BossName())
                effects.add(ScreenEffect((255, 255, 255), 200, -10))

            if can_gen and not boss_group.sprite:
                cacd -= 1
                if cacd <= 0:
                    cacd = ast_cd
                    for _ in range(
                        random.randint(
                            1,
                            2 + ship.sprite.bosses_killed if ship.sprite else 1,
                        )
                    ):
                        astroids.add(Astroid())

            ship.update()
            astroids.update()
            lasers.update()
            elasers.update()
            pops.update()
            pows.update()
            upgs.update()
            effects.update()
            boss_group.update()
            overlay_ui.update()
            buttons.update()

            if ship.sprite:
                for a in sprite.spritecollide(ship.sprite, astroids, True):
                    hit_sound.play()
                    ship.sprite.hp -= 1
                    screen_shake = 100
                    create_impact(ship.sprite.pos, (255, 0, 0), 10)
                for e in sprite.spritecollide(ship.sprite, elasers, True):
                    hit_sound.play()
                    ship.sprite.hp -= 1
                    screen_shake = 100
                    create_impact(ship.sprite.pos, (255, 255, 255), 10)

            hits = sprite.groupcollide(astroids, lasers, False, False)
            for ast, l_list in hits.items():
                hit_sound.play()
                for l in l_list:
                    # Determine hit color based on laser kind/state
                    hit_color = (255, 255, 255)
                    if l.kind in ["sin 1", "sin 2"]:
                        hit_color = (0, 255, 0)
                    elif (
                        ship.sprite and ship.sprite.angular_lasers and l.kind == "main"
                    ):
                        hit_color = (255, 0, 0)

                    create_impact(l.pos, hit_color, 4)
                    screen_shake = 1 + ship.sprite.laser_exp if ship.sprite else 1

                    if l.kind in ["sin 1", "sin 2"]:
                        ast.hp -= ship.sprite.laser_dmg * 2 if ship.sprite else 1.5
                    elif (
                        ship.sprite and ship.sprite.angular_lasers and l.kind == "main"
                    ):
                        ast.hp -= ship.sprite.laser_dmg * 2.5 if ship.sprite else 1
                    else:
                        ast.hp -= ship.sprite.laser_dmg if ship.sprite else 1

                    ast.pos.y -= 1

                    if ship.sprite and ship.sprite.laser_exp > 0:
                        pops.add(
                            Pop(l.pos.x, l.pos.y, ship.sprite.laser_exp * 20, hit_color)
                        )
                        for _ in range(
                            ship.sprite.laser_exp * 2
                            if ship.sprite.laser_exp <= 4
                            else 40
                        ):
                            pows.add(Pow(l.pos.x, l.pos.y, 12, hit_color))

                    if ship.sprite:
                        if l.kind == "main":
                            ship.sprite.bomb_cooldown = max(
                                0, ship.sprite.bomb_cooldown - 1
                            )

                    if l.kind == "bomb":
                        l.explode()
                    else:
                        l.kill()

                if ast.hp <= 0:
                    boom_sound.play()
                    ast.kill()
                    screen_shake = 2
                    score += 10
                    if random.randint(1, 8 + ship.sprite.bosses_killed) == 1:
                        upgs.add(
                            Upgrade(
                                random.randint(100, W - 100),
                                random.randint(100, H - 100),
                            )
                        )
                    pops.add(Pop(ast.pos.x, ast.pos.y, 40, (255, 255, 255)))

            # Ray collisions with astroids
            for laser in lasers:
                if laser.kind == "ray":
                    ray_start = laser.pos
                    ray_end = laser.pos + laser.vel.normalize() * 1000
                    for ast in astroids:
                        if ast.rect.clipline(ray_start, ray_end):
                            hit_sound.play()
                            hit_color = (0, 0, 255)
                            create_impact(laser.pos, hit_color, 4)
                            screen_shake = 1 + (
                                ship.sprite.laser_exp if ship.sprite else 0
                            )
                            ast.hp -= (
                                0.1 * ship.sprite.laser_dmg if ship.sprite else 0.1
                            )
                            ast.speed *= 0.9
                            ast.pos.y -= (
                                ship.sprite.laser_dmg * 1.5 if ship.sprite else 1.5
                            )
                            if ast.hp <= 0:
                                boom_sound.play()
                                ast.kill()
                                score += 10
                                screen_shake = 2
                                if (
                                    random.randint(1, 8 + ship.sprite.bosses_killed)
                                    == 1
                                ):
                                    upgs.add(
                                        Upgrade(
                                            random.randint(100, W - 100),
                                            random.randint(100, H - 100),
                                        )
                                    )
                                pops.add(Pop(ast.pos.x, ast.pos.y, 40, (255, 255, 255)))

            if boss_group.sprite:
                hits = sprite.spritecollide(boss_group.sprite, lasers, True)
                for l in hits:
                    if not boss_group.sprite:
                        break

                    hit_color = (255, 255, 255)
                    if l.kind in ["sin 1", "sin 2"]:
                        hit_color = (0, 255, 0)
                    elif (
                        ship.sprite and ship.sprite.angular_lasers and l.kind == "main"
                    ):
                        hit_color = (255, 0, 0)

                    create_impact(l.pos, hit_color, 6)

                    if ship.sprite and ship.sprite.laser_exp > 0:
                        pops.add(
                            Pop(l.pos.x, l.pos.y, ship.sprite.laser_exp * 20, hit_color)
                        )
                        for _ in range(
                            ship.sprite.laser_exp * 10
                            if ship.sprite.laser_exp <= 4
                            else 40
                        ):
                            pows.add(Pow(l.pos.x, l.pos.y, 10, hit_color))

                    if l.kind in ["sin 1", "sin 2"]:
                        boss_group.sprite.hp -= (
                            ship.sprite.laser_dmg * 2 if ship.sprite else 1.5
                        )
                    else:
                        boss_group.sprite.hp -= (
                            ship.sprite.laser_dmg if ship.sprite else 1
                        )

                    hit_sound.play()
                    if ship.sprite and l.kind == "main":
                        ship.sprite.bomb_cooldown = max(
                            0,
                            ship.sprite.bomb_cooldown
                            - 1
                            / (
                                (ship.sprite.bosses_killed + 1) / 2
                                if ship.sprite
                                else 1
                            ),
                        )

                    if boss_group.sprite.hp <= 0:
                        screen_shake = 30
                        boom_sound.play()
                        score += 100 * (boss_group.sprite.phase + 1)
                        for _ in range(50):
                            pows.add(
                                Pow(
                                    boss_group.sprite.pos.x,
                                    boss_group.sprite.pos.y,
                                    12,
                                    (255, 50, 50),
                                )
                            )
                        for _ in range(3):
                            upgs.add(
                                Upgrade(
                                    random.randint(100, W - 100),
                                    random.randint(100, H - 100),
                                )
                            )
                        if ship.sprite:
                            ship.sprite.bosses_killed += 1
                        boss_group.sprite.kill()

            # Ray collisions with boss
            if boss_group.sprite:
                for laser in lasers:
                    if laser.kind == "ray":
                        ray_start = laser.pos
                        ray_end = laser.pos + laser.vel.normalize() * 1000
                        if (
                            boss_group.sprite.rect.clipline(ray_start, ray_end)
                            and boss_group.sprite
                        ):
                            hit_color = (0, 0, 255)
                            create_impact(laser.pos, hit_color, 6)
                            if ship.sprite and ship.sprite.laser_exp > 0:
                                pops.add(
                                    Pop(
                                        laser.pos.x,
                                        laser.pos.y,
                                        ship.sprite.laser_exp * 20,
                                        hit_color,
                                    )
                                )
                                for _ in range(
                                    ship.sprite.laser_exp * 10
                                    if ship.sprite.laser_exp <= 4
                                    else 40
                                ):
                                    pows.add(
                                        Pow(laser.pos.x, laser.pos.y, 10, hit_color)
                                    )
                            boss_group.sprite.hp -= (
                                0.1 * ship.sprite.laser_dmg if ship.sprite else 0.1
                            )
                            hit_sound.play()
                            if boss_group.sprite.hp <= 0:
                                screen_shake = 30
                                boom_sound.play()
                                score += 100 * (boss_group.sprite.phase + 1)
                                for _ in range(50):
                                    pows.add(
                                        Pow(
                                            boss_group.sprite.pos.x,
                                            boss_group.sprite.pos.y,
                                            12,
                                            (255, 50, 50),
                                        )
                                    )
                                for _ in range(3):
                                    upgs.add(
                                        Upgrade(
                                            random.randint(100, W - 100),
                                            random.randint(100, H - 100),
                                        )
                                    )
                                if ship.sprite:
                                    ship.sprite.bosses_killed += 1
                                boss_group.sprite.kill()
                if l.kind == "bomb":
                    l.explode()
                else:
                    l.kill()

            if not ship.sprite:
                if not any(b.kind == "Play Again" for b in buttons):
                    buttons.add(Button(W // 2, H // 2, "Play Again"))
                for b in buttons:
                    if b.kind == "Play Again" and b.clicked:
                        ast_cd, cacd, frames_passed, can_gen, bg_off = reset_game()

            shake_offset = (
                Vector2(
                    random.uniform(-screen_shake, screen_shake),
                    random.uniform(-screen_shake, screen_shake),
                )
                if screen_shake > 0
                else Vector2(0, 0)
            )
            if screen_shake > 0:
                screen_shake *= 0.9

            screen.fill((0, 0, 0))
            for i in range(11):
                pygame.draw.line(
                    screen,
                    (40, 40, 40),
                    (W // 10 * i + shake_offset.x, 0),
                    (W // 10 * i + shake_offset.x, H),
                    1,
                )
            for i in range(-1, 10):
                y_pos = (i * (H // 8)) + bg_off + shake_offset.y
                pygame.draw.line(screen, (40, 40, 40), (0, y_pos), (W, y_pos), 1)

            def draw_group(group):
                for sprite in group:
                    # Check if the sprite has our custom 'draw' method
                    if hasattr(sprite, "draw"):
                        if hasattr(sprite, "rect"):
                            sprite.rect.center += shake_offset
                        elif hasattr(sprite, "pos"):
                            sprite.pos += shake_offset
                        sprite.draw(screen)

                    else:
                        if hasattr(sprite, "rect"):
                            sprite.rect.center += shake_offset
                        elif hasattr(sprite, "pos"):
                            sprite.pos += shake_offset
                        screen.blit(sprite.image, sprite.rect)

            draw_group(pops)
            draw_group(pows)
            draw_group(astroids)
            draw_group(lasers)
            draw_group(elasers)
            draw_group(ship)
            draw_group(upgs)
            draw_group(boss_group)

            for b in buttons:
                b.draw(screen)
            for bar in ui_bars:
                bar.draw(screen)
            for overlay in overlay_ui:
                overlay.draw(screen)
            for effect in effects:
                effect.draw(screen)

            if pygame.mouse.get_focused() and screen.get_rect().collidepoint(
                pygame.mouse.get_pos()
            ):
                pygame.draw.circle(
                    screen, (255, 0, 0), pygame.mouse.get_pos(), 20, int(10)
                )
                pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 5)

            score_font = pygame.font.SysFont("corbel", 48, bold=False)
            score_surf = score_font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_surf, (40, 40))
            score_font = pygame.font.SysFont("corbel", 32, bold=False)
            score_surf = score_font.render(
                f"Level: {ship.sprite.bosses_killed+1 if ship.sprite else "ur ded"}",
                True,
                (255, 255, 255),
            )
            screen.blit(score_surf, (40, 80))

            pygame.display.flip()
            clock.tick(60)
            if not boss_group.sprite:
                frames_passed += 1

    def main_menu():
        mmanim = Mmanim(W, H)
        buttons.empty()
        buttons.add(Button(W // 2, 650, "Play"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            buttons.update()
            mmanim.update()
            for b in buttons:
                if b.kind == "Play" and b.clicked:
                    return
            screen.fill((0, 0, 0))
            for i in range(11):
                pygame.draw.line(
                    screen, (40, 40, 40), (W // 10 * i, 0), (W // 10 * i, H), 1
                )
            for i in range(-1, 10):
                y_pos = i * (H // 8)
                pygame.draw.line(screen, (40, 40, 40), (0, y_pos), (W, y_pos), 1)
            mmanim.draw(screen)
            for b in buttons:
                b.draw(screen)

            if pygame.mouse.get_focused() and screen.get_rect().collidepoint(
                pygame.mouse.get_pos()
            ):
                pygame.draw.circle(
                    screen, (255, 0, 0), pygame.mouse.get_pos(), 20, int(10)
                )
                pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 5)

            pygame.display.flip()
            clock.tick(60)

    while True:
        print("Hello, World!")
        main_menu()
        play()


if __name__ == "__main__":
    main()
