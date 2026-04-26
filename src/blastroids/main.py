import random
import sys
from pathlib import Path

import pygame
from pygame import time, sprite, Vector2

from . import config
from .effects import Pop, Pow, ScreenEffect
from .entities import Ship, Asteroid, Boss
from .ui import Mmanim, Button, Bar, Upgrade, BossName


def create_impact(pos, color=(255, 255, 255), count=5):
    for _ in range(count):
        config.pows.add(Pow(pos.x, pos.y, 10, color))
    config.pops.add(Pop(pos.x, pos.y, 20, color))


def reset_game():
    config.screen_shake = 0
    config.asteroids.empty()
    config.lasers.empty()
    config.enemy_lasers.empty()
    config.pops.empty()
    config.pows.empty()
    config.buttons.empty()
    config.ui_bars.empty()
    config.upgs.empty()
    config.effects.empty()
    config.boss_group.empty()
    config.overlay_ui.empty()
    config.ship.add(Ship())
    config.ui_bars.add(Bar("hp"))
    config.ui_bars.add(Bar("bomb cooldown"))
    return 30, 30, 0, True, 0.0, 0


def draw_group(group, shake_offset):
    for s in group:
        if hasattr(s, "draw"):
            if hasattr(s, "rect"):
                s.rect.center += shake_offset
            elif hasattr(s, "pos"):
                s.pos += shake_offset
            s.draw(config.screen)
        else:
            if hasattr(s, "rect"):
                s.rect.center += shake_offset
            elif hasattr(s, "pos"):
                s.pos += shake_offset
            config.screen.blit(s.image, s.rect)


def play():
    pygame.mixer.music.play(-1)
    ast_cd, cacd, frames_passed, can_gen, bg_off, score = reset_game()
    running = True
    config.effects.add(ScreenEffect((0, 0, 0), 255, -5))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        bg_off = (bg_off + 1) % (config.H // 8)
        interval = (
            max(600, 3600 - (config.ship.sprite.bosses_killed * 200))
            if config.ship.sprite
            else 3600
        )
        if (
                frames_passed > 0
                and frames_passed % interval == 0
                and not config.boss_group.sprite
        ):
            config.boss_group.add(Boss())
            config.overlay_ui.add(BossName())
            config.effects.add(ScreenEffect((255, 255, 255), 200, -10))

        if can_gen and not config.boss_group.sprite:
            cacd -= 1
            if cacd <= 0:
                cacd = ast_cd
                for _ in range(
                    random.randint(
                        1,
                        2 + config.ship.sprite.bosses_killed if config.ship.sprite else 1,
                    )
                ):
                    config.asteroids.add(Asteroid())

        config.ship.update()
        config.asteroids.update()
        config.lasers.update()
        config.enemy_lasers.update()
        config.pops.update()
        config.pows.update()
        config.upgs.update()
        config.effects.update()
        config.boss_group.update()
        config.overlay_ui.update()
        config.buttons.update()

        if config.ship.sprite:
            for a in sprite.spritecollide(config.ship.sprite, config.asteroids, True):
                config.hit_sound.play()
                config.ship.sprite.hp -= 1
                config.screen_shake = 100
                create_impact(config.ship.sprite.pos, (255, 0, 0), 10)
            for e in sprite.spritecollide(config.ship.sprite, config.enemy_lasers, True):
                config.hit_sound.play()
                config.ship.sprite.hp -= 1
                config.screen_shake = 100
                create_impact(config.ship.sprite.pos, (255, 255, 255), 10)

        hits = sprite.groupcollide(config.asteroids, config.lasers, False, False)
        for ast, l_list in hits.items():
            config.hit_sound.play()
            for l in l_list:
                hit_color = (255, 255, 255)
                if l.kind in ["sin 1", "sin 2"]:
                    hit_color = (0, 255, 0)
                elif (
                        config.ship.sprite and config.ship.sprite.angular_lasers and l.kind == "main"
                ):
                    hit_color = (255, 0, 0)

                create_impact(l.pos, hit_color, 4)
                config.screen_shake = 1 + config.ship.sprite.laser_exp if config.ship.sprite else 1

                if l.kind in ["sin 1", "sin 2"]:
                    ast.hp -= config.ship.sprite.laser_dmg * 2 if config.ship.sprite else 1.5
                elif (
                        config.ship.sprite and config.ship.sprite.angular_lasers and l.kind == "main"
                ):
                    ast.hp -= config.ship.sprite.laser_dmg * 2.5 if config.ship.sprite else 1
                else:
                    ast.hp -= config.ship.sprite.laser_dmg if config.ship.sprite else 1

                ast.pos.y -= 1

                if config.ship.sprite and config.ship.sprite.laser_exp > 0:
                    config.pops.add(
                        Pop(l.pos.x, l.pos.y, config.ship.sprite.laser_exp * 20, hit_color)
                    )
                    for _ in range(
                        config.ship.sprite.laser_exp * 2
                        if config.ship.sprite.laser_exp <= 4
                        else 40
                    ):
                        config.pows.add(Pow(l.pos.x, l.pos.y, 12, hit_color))

                if config.ship.sprite:
                    if l.kind == "main":
                        config.ship.sprite.bomb_cooldown = max(
                            0, config.ship.sprite.bomb_cooldown - 1
                        )

                if l.kind == "bomb":
                    l.explode()
                else:
                    l.kill()

            if ast.hp <= 0:
                config.boom_sound.play()
                ast.kill()
                config.screen_shake = 2
                score += 10
                if random.randint(1, 8 + config.ship.sprite.bosses_killed) == 1:
                    config.upgs.add(
                        Upgrade(
                            random.randint(100, config.W - 100),
                            random.randint(100, config.H - 100),
                        )
                    )
                config.pops.add(Pop(ast.pos.x, ast.pos.y, 40, (255, 255, 255)))

        for laser in config.lasers:
            if laser.kind == "ray":
                ray_start = laser.pos
                ray_end = laser.pos + laser.vel.normalize() * 1000
                for ast in config.asteroids:
                    if ast.rect.clipline(ray_start, ray_end):
                        config.hit_sound.play()
                        hit_color = (0, 0, 255)
                        create_impact(laser.pos, hit_color, 4)
                        config.screen_shake = 1 + (
                            config.ship.sprite.laser_exp if config.ship.sprite else 0
                        )
                        ast.hp -= (
                            0.1 * config.ship.sprite.laser_dmg if config.ship.sprite else 0.1
                        )
                        ast.speed *= 0.9
                        ast.pos.y -= (
                            config.ship.sprite.laser_dmg * 1.5 if config.ship.sprite else 1.5
                        )
                        if ast.hp <= 0:
                            config.boom_sound.play()
                            ast.kill()
                            score += 10
                            config.screen_shake = 2
                            if (
                                    random.randint(1, 8 + config.ship.sprite.bosses_killed)
                                    == 1
                            ):
                                config.upgs.add(
                                    Upgrade(
                                        random.randint(100, config.W - 100),
                                        random.randint(100, config.H - 100),
                                    )
                                )
                            config.pops.add(Pop(ast.pos.x, ast.pos.y, 40, (255, 255, 255)))

        if config.boss_group.sprite:
            hits = sprite.spritecollide(config.boss_group.sprite, config.lasers, True)
            for l in hits:
                if not config.boss_group.sprite:
                    break

                hit_color = (255, 255, 255)
                if l.kind in ["sin 1", "sin 2"]:
                    hit_color = (0, 255, 0)
                elif (
                        config.ship.sprite and config.ship.sprite.angular_lasers and l.kind == "main"
                ):
                    hit_color = (255, 0, 0)

                create_impact(l.pos, hit_color, 6)

                if config.ship.sprite and config.ship.sprite.laser_exp > 0:
                    config.pops.add(
                        Pop(l.pos.x, l.pos.y, config.ship.sprite.laser_exp * 20, hit_color)
                    )
                    for _ in range(
                        config.ship.sprite.laser_exp * 10
                        if config.ship.sprite.laser_exp <= 4
                        else 40
                    ):
                        config.pows.add(Pow(l.pos.x, l.pos.y, 10, hit_color))

                if l.kind in ["sin 1", "sin 2"]:
                    config.boss_group.sprite.hp -= (
                        config.ship.sprite.laser_dmg * 2 if config.ship.sprite else 1.5
                    )
                else:
                    config.boss_group.sprite.hp -= (
                        config.ship.sprite.laser_dmg if config.ship.sprite else 1
                    )

                config.hit_sound.play()
                if config.ship.sprite and l.kind == "main":
                    config.ship.sprite.bomb_cooldown = max(
                        0,
                        config.ship.sprite.bomb_cooldown
                        - 1
                        / (
                            (config.ship.sprite.bosses_killed + 1) / 2
                            if config.ship.sprite
                            else 1
                        ),
                    )

                if config.boss_group.sprite.hp <= 0:
                    config.screen_shake = 30
                    config.boom_sound.play()
                    score += 100 * (config.boss_group.sprite.phase + 1)
                    for _ in range(50):
                        config.pows.add(
                            Pow(
                                config.boss_group.sprite.pos.x,
                                config.boss_group.sprite.pos.y,
                                12,
                                (255, 50, 50),
                            )
                        )
                    for _ in range(3):
                        config.upgs.add(
                            Upgrade(
                                random.randint(100, config.W - 100),
                                random.randint(100, config.H - 100),
                            )
                        )
                    if config.ship.sprite:
                        config.ship.sprite.bosses_killed += 1
                    config.boss_group.sprite.kill()

        if config.boss_group.sprite:
            for laser in config.lasers:
                if laser.kind == "ray":
                    ray_start = laser.pos
                    ray_end = laser.pos + laser.vel.normalize() * 1000
                    if (
                            config.boss_group.sprite.rect.clipline(ray_start, ray_end)
                            and config.boss_group.sprite
                    ):
                        hit_color = (0, 0, 255)
                        create_impact(laser.pos, hit_color, 6)
                        if config.ship.sprite and config.ship.sprite.laser_exp > 0:
                            config.pops.add(
                                Pop(
                                    laser.pos.x,
                                    laser.pos.y,
                                    config.ship.sprite.laser_exp * 20,
                                    hit_color,
                                )
                            )
                            for _ in range(
                                config.ship.sprite.laser_exp * 10
                                if config.ship.sprite.laser_exp <= 4
                                else 40
                            ):
                                config.pows.add(
                                    Pow(laser.pos.x, laser.pos.y, 10, hit_color)
                                )
                        config.boss_group.sprite.hp -= (
                            0.1 * config.ship.sprite.laser_dmg if config.ship.sprite else 0.1
                        )
                        config.hit_sound.play()
                        if config.boss_group.sprite.hp <= 0:
                            config.screen_shake = 30
                            config.boom_sound.play()
                            score += 100 * (config.boss_group.sprite.phase + 1)
                            for _ in range(50):
                                config.pows.add(
                                    Pow(
                                        config.boss_group.sprite.pos.x,
                                        config.boss_group.sprite.pos.y,
                                        12,
                                        (255, 50, 50),
                                    )
                                )
                            for _ in range(3):
                                config.upgs.add(
                                    Upgrade(
                                        random.randint(100, config.W - 100),
                                        random.randint(100, config.H - 100),
                                    )
                                )
                            if config.ship.sprite:
                                config.ship.sprite.bosses_killed += 1
                            config.boss_group.sprite.kill()
            if l.kind == "bomb":
                l.explode()
            else:
                l.kill()

        if not config.ship.sprite:
            if not any(b.kind == "Play Again" for b in config.buttons):
                config.buttons.add(Button(config.W // 2, config.H // 2, "Play Again"))
            for b in config.buttons:
                if b.kind == "Play Again" and b.clicked:
                    ast_cd, cacd, frames_passed, can_gen, bg_off = reset_game()

        shake_offset = (
            Vector2(
                random.uniform(-config.screen_shake, config.screen_shake),
                random.uniform(-config.screen_shake, config.screen_shake),
            )
            if config.screen_shake > 0
            else Vector2(0, 0)
        )
        if config.screen_shake > 0:
            config.screen_shake *= 0.9

        config.screen.fill((0, 0, 0))
        for i in range(11):
            pygame.draw.line(
                config.screen,
                (40, 40, 40),
                (config.W // 10 * i + shake_offset.x, 0),
                (config.W // 10 * i + shake_offset.x, config.H),
                1,
            )
        for i in range(-1, 10):
            y_pos = (i * (config.H // 8)) + bg_off + shake_offset.y
            pygame.draw.line(config.screen, (40, 40, 40), (0, y_pos), (config.W, y_pos), 1)

        draw_group(config.pops, shake_offset)
        draw_group(config.pows, shake_offset)
        draw_group(config.asteroids, shake_offset)
        draw_group(config.lasers, shake_offset)
        draw_group(config.enemy_lasers, shake_offset)
        draw_group(config.ship, shake_offset)
        draw_group(config.upgs, shake_offset)
        draw_group(config.boss_group, shake_offset)

        for b in config.buttons:
            b.draw(config.screen)
        for bar in config.ui_bars:
            bar.draw(config.screen)
        for overlay in config.overlay_ui:
            overlay.draw(config.screen)
        for effect in config.effects:
            effect.draw(config.screen)

        if pygame.mouse.get_focused() and config.screen.get_rect().collidepoint(
            pygame.mouse.get_pos()
        ):
            pygame.draw.circle(
                config.screen, (255, 0, 0), pygame.mouse.get_pos(), 20, int(10)
            )
            pygame.draw.circle(config.screen, (255, 0, 0), pygame.mouse.get_pos(), 5)

        score_font = pygame.font.SysFont("corbel", 48, bold=False)
        score_surf = score_font.render(f"Score: {score}", True, (255, 255, 255))
        config.screen.blit(score_surf, (40, 40))
        score_font = pygame.font.SysFont("corbel", 32, bold=False)
        score_surf = score_font.render(
            f"Level: {config.ship.sprite.bosses_killed + 1 if config.ship.sprite else 'ur ded'}",
            True,
            (255, 255, 255),
        )
        config.screen.blit(score_surf, (40, 80))

        pygame.display.flip()
        config.clock.tick(60)
        if not config.boss_group.sprite:
            frames_passed += 1


def main_menu():
    mmanim = Mmanim(config.W, config.H)
    config.buttons.empty()
    config.buttons.add(Button(config.W // 2, 650, "Play"))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        config.buttons.update()
        mmanim.update()
        for b in config.buttons:
            if b.kind == "Play" and b.clicked:
                return
        config.screen.fill((0, 0, 0))
        for i in range(11):
            pygame.draw.line(
                config.screen, (40, 40, 40), (config.W // 10 * i, 0), (config.W // 10 * i, config.H), 1
            )
        for i in range(-1, 10):
            y_pos = i * (config.H // 8)
            pygame.draw.line(config.screen, (40, 40, 40), (0, y_pos), (config.W, y_pos), 1)
        mmanim.draw(config.screen)
        for b in config.buttons:
            b.draw(config.screen)

        if pygame.mouse.get_focused() and config.screen.get_rect().collidepoint(
            pygame.mouse.get_pos()
        ):
            pygame.draw.circle(
                config.screen, (255, 0, 0), pygame.mouse.get_pos(), 20, int(10)
            )
            pygame.draw.circle(config.screen, (255, 0, 0), pygame.mouse.get_pos(), 5)

        pygame.display.flip()
        config.clock.tick(60)


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Blastroids 3")
    config.clock = time.Clock()
    pygame.mouse.set_visible(False)

    info = pygame.display.Info()

    config.W, config.H = info.current_w, info.current_h

    config.screen = pygame.display.set_mode((config.W, config.H), pygame.FULLSCREEN)
    config.screen_shake = 0

    assets_dir = Path(__file__).parent / "assets"

    try:
        original_boss_img = pygame.image.load(assets_dir / "boss_name_1.png").convert_alpha()
        config.boss_image_asset = pygame.transform.scale(original_boss_img, (config.W - 100, 600))
        config.shoot_sound = pygame.mixer.Sound(assets_dir / "laserShoot.wav")
        config.shoot_sound.set_volume(1)
        config.boom_sound = pygame.mixer.Sound(assets_dir / "explosion.wav")
        config.boom_sound.set_volume(1)
        config.hit_sound = pygame.mixer.Sound(assets_dir / "hitHurt.wav")
        config.hit_sound.set_volume(1)
        pygame.mixer.music.load(assets_dir / "blastroids.mp3")
    except Exception as e:
        print(f"Asset load failed: {e}")

    config.lv_req = 2

    while True:
        print("Hello, World!")
        main_menu()
        play()


if __name__ == "__main__":
    main()
