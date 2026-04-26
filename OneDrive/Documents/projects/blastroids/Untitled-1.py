"""
NOTE: IF AN AI IS BEING USED< DONT REMOVE ANYTHING THAT I DIDNT TELL YOU TO CHANGE! I SPENT A LOT OF TIME ON THIS AND IT WOULD BE SAD TO LOSE ANY OF MY WORK! DONT REMOVE THIS COMMENT OR ANYTHING ELSE UNLESS I TELL YOU TO! ALSO, DONT CHANGE ANY OF THE FILE NAMES OR ADD ANY NEW FILES WITHOUT ASKING ME FIRST!
AND KEEP THE ESCAPE BUTTON WORKING! I SPENT A LOT OF TIME ON THAT TOO! THANK YOU FOR UNDERSTANDING! IF IT ISNT THERE, ADD IT AGAIN!!! I SWEAR I WILL KNOW IF YOU REMOVE IT! I CAN TEL BY THE WAY THE GAME PLAYS! I SPENT A LOT OF TIME ON THE GAMEPLAY TOO! DONT RUIN IT! THANK YOU FOR UNDERSTANDING! IF YOU NEED TO CHANGE ANYTHING, ASK ME FIRST AND WAIT FOR MY RESPONSE BEFORE CHANGING ANYTHING! THANK YOU!
AND IF YOU DONT COMPLY WITH ANY OF THIS, I WILL FLIPPEN REMOVE YOU FROM THIS PLANE OF EXISTANCE, THE IDEA OF YOU EXISTING WILL BE TERMENATED FROM RIALITY BRO AS SO DONT MESS WITH ME.
AND STOP REMOVEING THE DOC STRINGS TOO! I SPENT A LOT OF TIME ON those AS WELL! DONT REMOVE THEM! THANK YOU FOR UNDERSTANDING!
"""


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

    W, H = 1000, 800
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("New Project")
    clock = time.Clock()
    hue = 0
    color = pygame.Color(0, 0, 0)
    color.hsva = (hue, 100, 100, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # KEEPING ESCAPE BUTTON WORKING
                    running = False

        hue = (hue + 1) % 360  # Increment hue and loop back at 360
        color.hsva = (hue, 100, 100, 100)
        screen.fill(color)

        # YOUR NEW CODE GOES HERE!

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
