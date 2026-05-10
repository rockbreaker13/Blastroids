from pygame import sprite

# ---- Game Config ----
W, H = 0, 0
screen = None
screen_shake = 0
boss_image_asset = None
shoot_sound, boom_sound, hit_sound = None, None, None
lv_req = 2
clock = None

# ---- Sprite Groups ----
ship = sprite.GroupSingle()
asteroids = sprite.Group()
lasers = sprite.Group()
enemy_lasers = sprite.Group()
pops = sprite.Group()
pows = sprite.Group()
buttons = sprite.Group()
ui_bars = sprite.Group()
upgs = sprite.Group()
effects = sprite.Group()
boss_group = sprite.GroupSingle()
overlay_ui = sprite.Group()
songs = {
    "main_menu_music": "assets/Chill the Axe.mp3",
    "zone1_music": "assets/blastroids.mp3",
}
zone = 1
grid_thickness = 3
