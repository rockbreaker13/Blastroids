import random
import sys
from pathlib import Path

import pygame
from pygame import time, Vector2

from blastroids import config, collisions, effects, entities, ui

def create_impact(pos, color=(255, 255, 255), count=5):
    for _ in range(count):
        config.pows.add(effects.Pow(pos.x, pos.y, 10, color))
    config.pops.add(effects.Pop(pos.x, pos.y, 20, color))


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
    config.ship.add(entities.Ship())
    config.ui_bars.add(ui.Bar("hp"))
    config.ui_bars.add(ui.Bar("bomb cooldown"))
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


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
    return True


def update_game_state(score, frames_passed, can_gen, ast_cd, cacd):
    bg_off = (frames_passed + 1) % (config.H // 8)
    if config.ship.sprite:
        interval = max(600, 3600 - (config.ship.sprite.bosses_killed * 200))
    else:
        interval = 3600

    if (
        frames_passed > 0
        and frames_passed % interval == 0
        and not config.boss_group.sprite
    ):
        config.boss_group.add(entities.Boss())
        config.overlay_ui.add(ui.BossName())
        config.effects.add(effects.ScreenEffect((255, 255, 255), 200, -10))

    if can_gen and not config.boss_group.sprite:
        cacd -= 1
        if cacd <= 0:
            cacd = ast_cd
            if config.ship.sprite:
                num_asteroids = random.randint(1, 2 + config.ship.sprite.bosses_killed)
            else:
                num_asteroids = random.randint(1, 1)
            for _ in range(num_asteroids):
                config.asteroids.add(entities.Asteroid())

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

    return score, frames_passed + 1, can_gen, ast_cd, cacd, bg_off


def handle_collisions(score):
    collisions.handle_player_collisions()
    score = collisions.handle_asteroid_collisions(score)
    score = collisions.handle_boss_collisions(score)
    return score


def render_screen(score, bg_off):
    if config.screen_shake > 0:
        shake_offset = Vector2(
            random.uniform(-config.screen_shake, config.screen_shake),
            random.uniform(-config.screen_shake, config.screen_shake),
        )
        config.screen_shake *= 0.9
    else:
        shake_offset = Vector2(0, 0)

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
    if config.ship.sprite:
        level_text = f"Level: {config.ship.sprite.bosses_killed + 1}"
    else:
        level_text = "ur ded"
    score_surf = score_font.render(
        level_text,
        True,
        (255, 255, 255),
    )
    config.screen.blit(score_surf, (40, 80))

    pygame.display.flip()


def handle_game_over():
    if not config.ship.sprite:
        if not any(b.kind == "Play Again" for b in config.buttons):
            config.buttons.add(ui.Button(config.W // 2, config.H // 2, "Play Again"))
        for b in config.buttons:
            if b.kind == "Play Again" and b.clicked:
                return reset_game()
    return None


def play():
    pygame.mixer.music.play(-1)
    ast_cd, cacd, frames_passed, can_gen, bg_off, score = reset_game()
    running = True
    config.effects.add(effects.ScreenEffect((0, 0, 0), 255, -5))

    while running:
        running = handle_input()
        score, frames_passed, can_gen, ast_cd, cacd, bg_off = update_game_state(
            score, frames_passed, can_gen, ast_cd, cacd
        )
        score = handle_collisions(score)
        render_screen(score, bg_off)

        game_over_state = handle_game_over()
        if game_over_state:
            ast_cd, cacd, frames_passed, can_gen, bg_off, score = game_over_state

        config.clock.tick(60)


def main_menu():
    mmanim = ui.Mmanim(config.W, config.H)
    config.buttons.empty()
    config.buttons.add(ui.Button(config.W // 2, 650, "Play"))
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
                config.screen,
                (40, 40, 40),
                (config.W // 10 * i, 0),
                (config.W // 10 * i, config.H),
                1,
            )
        for i in range(-1, 10):
            y_pos = i * (config.H // 8)
            pygame.draw.line(
                config.screen, (40, 40, 40), (0, y_pos), (config.W, y_pos), 1
            )
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
        original_boss_img = pygame.image.load(
            assets_dir / "boss_name_1.png"
        ).convert_alpha()
        config.boss_image_asset = pygame.transform.scale(
            original_boss_img, (config.W - 100, 600)
        )
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
        main_menu()
        play()


if __name__ == "__main__":
    main()
