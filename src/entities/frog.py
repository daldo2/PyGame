import pygame
from src import config
from src.core.physics import move_and_slide


class Frog:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 40
        self.direction = 1  # 1 = Right, -1 = Left

        # 2. Load & Slice Sprite Sheet
        self.frames = []
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Switch frame every 0.1 seconds
        self.is_grounded = False

        self.load_sprites("assets/graphics/enemies/Frog001.png", frame_count=3)
        self.image = self.frames[0]
        self.debug_floor_sensor = None
        self.debug_wall_sensor = None
        self.max_hp = 2
        self.current_hp = 2

    def load_sprites(self, path, frame_count):

        sheet = pygame.image.load(path).convert_alpha()
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        # Calculate width of a single frame
        frame_width = sheet_width // frame_count

        for i in range(frame_count):
            # Cut out the frame
            # subsurface(x, y, width, height)
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))

            # Scale it up (optional, e.g., to 32x32)
            scaled_frame = pygame.transform.scale(frame, (config.TILE_SIZE, config.TILE_SIZE))
            self.frames.append(scaled_frame)

    def update(self, dt, tiles):
        safe_dt = min(dt, 0.05)

        # 1. AI Logic
        self.update_ai(tiles)
        self.velocity.x = self.speed * self.direction

        # 2. Apply Gravity ONCE
        self.apply_gravity(safe_dt)

        # 3. Move ONCE (No loop)
        self.rect, collisions = move_and_slide(self.rect, self.velocity, tiles, safe_dt)

        # 4. Check Ground
        self.is_grounded = collisions['bottom']
        if self.is_grounded:
            self.velocity.y = 0

        self.animate(safe_dt)

    def update_ai(self, tiles):
        # Allow checking sensors even if slightly in air to catch ledge transitions
        # Or simply check: If I am grounded OR I was just grounded.

        # Sensor Logic
        offset_x = 20
        check_x = self.rect.centerx + (offset_x * self.direction)  # Dynamic direction check

        floor_sensor = pygame.Rect(check_x, self.rect.bottom, 4, 4)  # Removed +2 gap to be tighter

        has_floor = False
        for tile in tiles:
            if tile.colliderect(floor_sensor):
                has_floor = True
                break

        # Wall Sensor
        wall_sensor_y = self.rect.centery - 5
        wall_sensor_x = self.rect.right if self.direction == 1 else self.rect.left - 4
        wall_sensor_rect = pygame.Rect(wall_sensor_x, wall_sensor_y, 4, 10)

        hits_wall = False
        for tile in tiles:
            if tile.colliderect(wall_sensor_rect):
                hits_wall = True
                break

        # Decision: Turn if hitting wall OR (we are grounded AND there is no floor ahead)
        # We add 'self.is_grounded' here to prevent turning around mid-air if falling from spawn
        if hits_wall or (self.is_grounded and not has_floor):
            self.direction *= -1

    def move(self, dt):
        self.velocity.x = self.speed * self.direction

    def apply_gravity(self, dt):
        self.velocity.y += config.GRAVITY * dt

    def animate(self, dt):
        # Increment timer
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1

            # Loop back to 0
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[self.frame_index]

    def draw_health_bar(self, screen, offset):
        # Configuration
        bar_width = 14
        bar_height = 2
        offset_y = 12  # Distance above the slime's head
        centering_offset = (self.rect.width - bar_width) // 2

        # Calculate Screen Position (World Pos + Camera Offset)
        screen_x = self.rect.x + offset.x +centering_offset
        screen_y = self.rect.y + offset.y + offset_y

        # Calculate Health Ratio
        ratio = self.current_hp / self.max_hp
        fill_width = int(bar_width * ratio)

        # Define Rects
        border_rect = pygame.Rect(screen_x, screen_y, bar_width, bar_height)
        fill_rect = pygame.Rect(screen_x, screen_y, fill_width, bar_height)

        # Draw (Red background, Green health)
        pygame.draw.rect(screen, (200, 0, 0), border_rect)
        pygame.draw.rect(screen, (0, 200, 0), fill_rect)

    def draw(self, screen, offset):
        draw_pos = self.rect.topleft + offset

        # Flip sprite if moving left
        if self.direction == 1:
            screen.blit(self.image, draw_pos)
        else:
            flipped = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped, draw_pos)
        self.draw_health_bar(screen, offset)