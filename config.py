import pygame

pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
DEBUG = False
FONT = pygame.font.Font("corpse.ttf", 60)
GROUND_LEVEL = 500
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 100
JSON_PATH = "levels.json"
MAP_LENGHT = 850