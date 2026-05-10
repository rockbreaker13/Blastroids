from abc import ABC, abstractmethod

from blastroids import config


class UpgradeEffect(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def apply(self, ship):
        raise NotImplementedError


class ShootSpeedUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "shoot speed"

    def apply(self, ship):
        if ship.shoot_delay >= 12:
            ship.shoot_delay -= 2


class LaserVelocityUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "laser velocity"

    def apply(self, ship):
        if ship.laser_vel.y >= -26:
            ship.laser_vel *= 1.5


class ShipRepairUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "ship repair"

    def apply(self, ship):
        ship.hp = ship.max_hp


class ExplodingLasersUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "exploding lasers"

    def apply(self, ship):
        if ship.laser_dmg < 2:
            ship.laser_dmg += 1
            ship.laser_exp += 1


class MultishotUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "multishot"

    def apply(self, ship):
        if ship.multishot < 2:
            ship.multishot += 1


class MoreBombShrapnelUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "more bomb shrapnel"

    def apply(self, ship):
        if ship.shrapnel < 48:
            ship.shrapnel += 4


class SinLasersUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "sin lasers"

    def apply(self, ship):
        if ship.bosses_killed >= config.lv_req:
            ship.sin_lasers = True


class AngularLasersUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "angular lasers"

    def apply(self, ship):
        if ship.bosses_killed >= config.lv_req:
            ship.angular_lasers = True


class RayBombsUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "ray bombs"

    def apply(self, ship):
        if ship.bosses_killed >= config.lv_req:
            ship.ray_bomb = True


class BetterMultishotUpgrade(UpgradeEffect):
    @property
    def name(self):
        return "multishot+"

    def apply(self, ship):
        if config.zone <= 1:
            if ship.multishot < 3:
                ship.multishot += 1
