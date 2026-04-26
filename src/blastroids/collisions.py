import random
from pygame import sprite
from . import config
from .effects import Pop, Pow
from .entities import MainLaser, SinLaser, Bomb, Shrapnel, Ray
from .ui import Upgrade


def create_impact(pos, color=(255, 255, 255), count=5):
    for _ in range(count):
        config.pows.add(Pow(pos.x, pos.y, 10, color))
    config.pops.add(Pop(pos.x, pos.y, 20, color))


def handle_player_collisions():
    if config.ship.sprite:
        collided_asteroids = sprite.spritecollide(
            config.ship.sprite, config.asteroids, True
        )
        for _ in collided_asteroids:
            config.hit_sound.play()
            config.ship.sprite.hp -= 1
            config.screen_shake = 100
            create_impact(config.ship.sprite.pos, (255, 0, 0), 10)

        collided_enemy_lasers = sprite.spritecollide(
            config.ship.sprite, config.enemy_lasers, True
        )
        for _ in collided_enemy_lasers:
            config.hit_sound.play()
            config.ship.sprite.hp -= 1
            config.screen_shake = 100
            create_impact(config.ship.sprite.pos, (255, 255, 255), 10)


def _handle_asteroid_laser_collision(ast, l, score):
    hit_color = l.color

    create_impact(l.pos, hit_color, 4)
    if config.ship.sprite:
        config.screen_shake = 1 + config.ship.sprite.laser_exp
    else:
        config.screen_shake = 1

    if isinstance(l, SinLaser):
        damage = config.ship.sprite.laser_dmg * 2 if config.ship.sprite else 1.5
    elif isinstance(l, MainLaser) and config.ship.sprite.angular_lasers:
        damage = config.ship.sprite.laser_dmg * 2.5 if config.ship.sprite else 1
    else:
        damage = config.ship.sprite.laser_dmg if config.ship.sprite else 1
    ast.hp -= damage

    ast.pos.y -= 1

    if config.ship.sprite and config.ship.sprite.laser_exp > 0:
        config.pops.add(
            Pop(l.pos.x, l.pos.y, config.ship.sprite.laser_exp * 20, hit_color)
        )
        num_pows = (
            config.ship.sprite.laser_exp * 2
            if config.ship.sprite.laser_exp <= 4
            else 40
        )
        for _ in range(num_pows):
            config.pows.add(Pow(l.pos.x, l.pos.y, 12, hit_color))

    if config.ship.sprite and isinstance(l, MainLaser):
        config.ship.sprite.bomb_cooldown = max(
            0, config.ship.sprite.bomb_cooldown - 1
        )

    if isinstance(l, Bomb):
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
    return score


def handle_asteroid_collisions(score):
    hits = sprite.groupcollide(config.asteroids, config.lasers, False, False)
    for ast, l_list in hits.items():
        config.hit_sound.play()
        for l in l_list:
            score = _handle_asteroid_laser_collision(ast, l, score)
    return score


def _handle_boss_laser_collision(l, score):
    if not config.boss_group.sprite:
        return score

    hit_color = l.color

    create_impact(l.pos, hit_color, 6)

    if config.ship.sprite and config.ship.sprite.laser_exp > 0:
        config.pops.add(
            Pop(l.pos.x, l.pos.y, config.ship.sprite.laser_exp * 20, hit_color)
        )
        num_pows = (
            config.ship.sprite.laser_exp * 10
            if config.ship.sprite.laser_exp <= 4
            else 40
        )
        for _ in range(num_pows):
            config.pows.add(Pow(l.pos.x, l.pos.y, 10, hit_color))

    if isinstance(l, SinLaser):
        damage = config.ship.sprite.laser_dmg * 2 if config.ship.sprite else 1.5
    else:
        damage = config.ship.sprite.laser_dmg if config.ship.sprite else 1
    config.boss_group.sprite.hp -= damage

    config.hit_sound.play()
    if config.ship.sprite and isinstance(l, MainLaser):
        bomb_cooldown_reduction = (
            1 / ((config.ship.sprite.bosses_killed + 1) / 2)
            if config.ship.sprite
            else 1
        )
        config.ship.sprite.bomb_cooldown = max(
            0,
            config.ship.sprite.bomb_cooldown - bomb_cooldown_reduction,
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
    return score


def handle_boss_collisions(score):
    if config.boss_group.sprite:
        hits = sprite.spritecollide(config.boss_group.sprite, config.lasers, True)
        for l in hits:
            score = _handle_boss_laser_collision(l, score)
    return score
