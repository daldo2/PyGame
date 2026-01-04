import pygame


class UI:
    def __init__(self, player):
        self.player = player

        # Settings
        self.bar_width = 100
        self.bar_height = 12
        self.hp_color = (200, 40, 40)  # Red
        self.mp_color = (40, 40, 200)  # Blue
        self.bg_color = (30, 30, 30)  # Dark Gray background

    def draw(self, screen):
        # 1. Draw HP Bar (Top Left: 10, 10)
        self.draw_bar(screen, 10, 10, self.player.current_hp, self.player.max_hp, self.hp_color)

        # 2. Draw Mana Bar (Below HP: 10, 25)
        self.draw_bar(screen, 10, 25, self.player.current_mp, self.player.max_mp, self.mp_color)

    def draw_bar(self, screen, x, y, current, max_val, color):
        if max_val <= 0: return

        # Calculate Ratio
        ratio = current / max_val
        fill_width = int(self.bar_width * ratio)

        # Rectangles
        bg_rect = pygame.Rect(x, y, self.bar_width, self.bar_height)
        fill_rect = pygame.Rect(x, y, fill_width, self.bar_height)

        # Draw: Background -> Fill -> Border
        pygame.draw.rect(screen, self.bg_color, bg_rect)
        pygame.draw.rect(screen, color, fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)  # White border