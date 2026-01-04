import pygame
from src import config

class Camera:
    def __init__(self, map_width, map_height):
        # The offset (x, y) that we will apply to everything we draw
        self.offset = pygame.Vector2(0, 0)
        self.offset.y = -100
        self.map_width = map_width
        self.map_height = map_height

    def follow(self, target):
        desired_x = (config.SCREEN_WIDTH // 2) - target.rect.centerx
        min_offset = -(self.map_width - config.SCREEN_WIDTH)
        self.offset.x = max(min_offset, min(0, desired_x))