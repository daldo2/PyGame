import sys
import pygame
from src import config
from src.scenes.game_scene import GameScene


def main():
    pygame.init()

    monitor_info = pygame.display.Info()
    MONITOR_WIDTH = monitor_info.current_w
    MONITOR_HEIGHT = monitor_info.current_h

    # Skalowanie do full okna
    screen = pygame.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Evergreen")
    game_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


    scale_w = MONITOR_WIDTH / config.SCREEN_WIDTH
    scale_h = MONITOR_HEIGHT / config.SCREEN_HEIGHT

    scale = min(scale_w, scale_h)

    # Nowe wymiary gry po przeskalowaniu
    new_width = int(config.SCREEN_WIDTH * scale)
    new_height = int(config.SCREEN_HEIGHT * scale)

    # Obliczamy przesunięcie, żeby wyśrodkować obraz (czarne pasy)
    offset_x = (MONITOR_WIDTH - new_width) // 2
    offset_y = (MONITOR_HEIGHT - new_height) // 2

    clock = pygame.time.Clock()

    # 2. Załadowanie sceny początkowej
    # W przyszłości tutaj może być MenuScene
    current_scene = GameScene()

    running = True

    # 3. Główna Pętla Gry (Game Loop)
    while running:
        # Obliczanie Delta Time (dt) w sekundach
        # Np. przy 60 FPS, dt wyniesie ok. 0.016
        dt = clock.tick(config.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            current_scene.handle_input(event)

        # B. Logika (Update)
        current_scene.update(dt)

        # C. Renderowanie (Draw)
        current_scene.draw(game_surface)
        screen.fill((0, 0, 0))
        scaled_surface = pygame.transform.scale(game_surface, (new_width, new_height))
        screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()