import pygame
from src import config
from src.entities.player import Player
from src.core.level_loader import load_level
from src.core.camera import Camera
from src.entities.slime import Slime
from src.core.ui import UI
import math
import random

class GameScene:
    def __init__(self):
        bg_path = "assets/graphics/background/bg-01.png"

        raw_bg = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(raw_bg, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


        data = load_level("assets/levels/level1.tmx")
        self.tmx_data = data[0]
        self.walls = data[1]
        self.hazards = data[2]
        self.visuals = data[3]
        spawn_point = data[4]
        slime_spawns = data[5]


        spawn_x, spawn_y = spawn_point
        self.player = Player(spawn_x, spawn_y)
        self.ui = UI(self.player)

        self.enemies = []
        for pos in slime_spawns:
            self.enemies.append(Slime(pos[0], pos[1]))

        path = "assets/graphics/tilesets/bloczek.png"
        try:
            self.block_img = pygame.image.load(path).convert()
        except FileNotFoundError:
            self.block_img = pygame.Surface((32, 32))

        map_width = self.tmx_data.width * config.TILE_SIZE
        map_height = self.tmx_data.height * config.TILE_SIZE

        # 3. Przekaż rozmiar do Kamery (NOWE)
        self.camera = Camera(map_width, map_height)

        self.damage_overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        # Rysujemy na niej stałą czerwoną ramkę (grubość np. 30px)
        border_thickness = 1000
        red_color = (255, 0, 0, 255)  # Czerwony, pełna widoczność (alfa zmienimy przy rysowaniu)
        # Top
        pygame.draw.rect(self.damage_overlay, red_color, (0, 0, config.SCREEN_WIDTH, border_thickness))
        # Bottom
        pygame.draw.rect(self.damage_overlay, red_color,
                         (0, config.SCREEN_HEIGHT - border_thickness, config.SCREEN_WIDTH, border_thickness))
        # Left
        pygame.draw.rect(self.damage_overlay, red_color, (0, 0, border_thickness, config.SCREEN_HEIGHT))
        # Right
        pygame.draw.rect(self.damage_overlay, red_color,
                         (config.SCREEN_WIDTH - border_thickness, 0, border_thickness, config.SCREEN_HEIGHT))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Pauza (TODO)")

    def update(self, dt):
        self.player.update(dt, self.walls)
        self.camera.follow(self.player)

        # Działa tylko wtedy, gdy gracz jest ogłuszony
        if self.player.stun_timer > 0:
            intensity = 1
            shake_x = 0.1 * random.randint(-intensity, intensity)
            shake_y = 0.1 * random.randint(-intensity, intensity)
            self.camera.offset.x += shake_x

        # Update Enemies
        for enemy in self.enemies:
            enemy.update(dt, self.walls)
        # check if player touches other
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(10, enemy.rect)

        # Removing dead enemies
        self.enemies = [e for e in self.enemies if e.current_hp > 0]

    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        for image, rect in self.visuals:
            # Oblicz pozycję z uwzględnieniem kamery
            draw_pos = rect.topleft + self.camera.offset
            if -64 < draw_pos.x < config.SCREEN_WIDTH + 64 and -64 < draw_pos.y < config.SCREEN_HEIGHT + 64:
                screen.blit(image, draw_pos)

        for enemy in self.enemies:
            enemy.draw(screen, self.camera.offset)
        self.player.draw(screen, self.camera.offset)
        self.ui.draw(screen)

        # Damage indicator
        if self.player.stun_timer > 0:
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2  # Wartość od 0.0 do 1.0
            alpha_value = int(pulse * 50)

            # Ustawiamy przezroczystość całej powierzchni overlay
            self.damage_overlay.set_alpha(alpha_value)
            screen.blit(self.damage_overlay, (0, 0))