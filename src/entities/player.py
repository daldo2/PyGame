import pygame
from src import config
from src.core.physics import move_and_slide
from src.abilities.fireball import Fireball

class Player:
    def __init__(self, x, y, projectile_list):
        self.rect = pygame.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE * 2)
        path = "assets/graphics/player/Wizard-0001.png"
        raw_image = pygame.image.load(path).convert_alpha()
        self.idle_image = pygame.transform.scale(raw_image, (32, 64))
        self.image = pygame.image.load(path)

        self.velocity = pygame.Vector2(0, 0)
        self.speed = 200

        self.is_grounded = False
        self.facing_right = True
        self.jump_pressed = False
        self.double_jump_pressed = False
        self.is_crouching = False
        self.possible_to_stand = False
        self.is_standing = False
        self.is_casting = False
        self.is_attacking = False
        self.damage_dealt = False

        self.double_jump_option = True
        self.fireball_option = True
        self.running = False
        self.fireball_timer = 0
        self.fireball_cooldown = 5
        self.fireball_ability = Fireball(self, projectile_list)

        self.max_hp = 100
        self.current_hp = 80
        self.max_mp = 5500
        self.current_mp = 5000
        self.invincible_timer = 0
        self.invincible_duration = 2.0
        self.stun_timer = 0

        self.frames_idle = []
        self.frames_run = []
        self.frames_crouch = []
        self.frames_cast = []
        self.frames_attack = []

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.08

        self.load_crouch_sprites("assets/graphics/player/crunching.png", 8)
        self.load_run_sprites("assets/graphics/player/running.png", 4)
        self.load_cast_sprites("assets/graphics/player/casting.png", 6)
        self.load_attack_sprites("assets/graphics/player/attacking.png", 8)
        # Default image
        self.image = self.frames_crouch[0]

    def load_crouch_sprites(self, path, frame_count):

        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            # Scale to player size
            scaled_frame = pygame.transform.scale(frame, (32, 64))
            self.frames_crouch.append(scaled_frame)

    def load_run_sprites(self, path, frame_count):

        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (32, 64))
            self.frames_run.append(scaled_frame)

    def load_attack_sprites(self, path, frame_count):
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (64, 64))
            self.frames_attack.append(scaled_frame)

    def load_cast_sprites(self, path, frame_count):

        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (32, 64))
            self.frames_cast.append(scaled_frame)

    def update(self, dt, tiles):
        # Don't handle input for a short period after taking damage
        if self.stun_timer > 0:
            self.stun_timer -= dt
            # slowing down
            self.velocity.x *= 0.95
        else:
            self.handle_input()

        self.apply_gravity(dt)
        self.rect, collisions = move_and_slide(self.rect, self.velocity, tiles, dt)

        if collisions['right'] or collisions['left']:
            self.is_standing = True
            self.running = False

        if collisions['bottom']:
            self.is_grounded = True
            self.velocity.y = 0
            self.double_jump_pressed = False

        else:
            self.is_grounded = False


        if collisions['top']:
            self.velocity.y = 0

        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        self.can_stand(dt, tiles)
        self.animate(dt)
        self.fireball_ability.update(dt)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0

        self.running = False
        if not self.is_casting:
            if keys[pygame.K_LEFT]:
                self.velocity.x = -self.speed
                self.facing_right = False
                self.running = True
            if keys[pygame.K_RIGHT]:
                self.velocity.x = self.speed
                self.facing_right = True
                self.running = True

        if keys[pygame.K_z]:
            if not self.jump_pressed:
                if self.is_grounded:
                    self.jump()
                elif not self.double_jump_pressed:
                    self.jump()
                    self.double_jump_pressed = True

                self.jump_pressed = True
        else:
            self.jump_pressed = False

        if keys[pygame.K_DOWN] and (self.is_grounded or self.is_crouching):
            self.is_crouching = True
            self.is_standing = False
        else:
            if self.is_crouching and self.possible_to_stand:
                self.is_crouching = False
                self.stand_up()

        if self.possible_to_stand:

            if keys[pygame.K_v] and self.fireball_option and not self.is_casting:
                self.fireball_ability.trigger()
                self.is_casting = True
                self.frame_index = 0

            if keys[pygame.K_x] and not self.is_attacking and not self.is_casting:
                self.frame_index = 0
                self.is_attacking = True

    def can_stand(self, dt, tiles):
        self.possible_to_stand = True
        top_rectangle = pygame.Rect(self.rect.x, self.rect.y, 32, 32)
        for tile in tiles:
            if top_rectangle.colliderect(tile):
                self.possible_to_stand = False

    def stand_up(self):
        if self.rect.height != 64:
            self.rect = pygame.Rect(self.rect.x, self.rect.y - 32, 32, 64)

    def shrink_hitbox(self):
        if self.rect.height != 32:
            self.rect = pygame.Rect(self.rect.x, self.rect.y + 32, 32, 32)

    def apply_gravity(self, dt):
        current_gravity = config.GRAVITY

        if self.velocity.y > 0:
            current_gravity *= 1.3

        elif self.velocity.y < 0 and not pygame.key.get_pressed()[pygame.K_z]:
            current_gravity *= 3.0

        self.velocity.y += current_gravity * dt

    def jump(self):
        self.velocity.y = config.JUMP_FORCE

    def check_attack_hit(self, enemies):

        if self.is_attacking and self.frame_index == 3 and self.damage_dealt == False:
            attack_rect = None

            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right, self.rect.y + 16, 32, 32)
            else:
                attack_rect = pygame.Rect(self.rect.left - 32, self.rect.y + 16, 32, 32)

            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.current_hp -= 1
                    self.damage_dealt = True

                    enemy.velocity.x = 400 if self.facing_right else -400
                    enemy.velocity.y = -200

    def take_damage(self, amount, source_rect):
        if self.invincible_timer <= 0:
            self.current_hp -= amount
            self.invincible_timer = self.invincible_duration
            self.stun_timer = 1
            print(f"Ouch! HP: {self.current_hp}")

            # Knock back
            self.velocity.y = -400
            if source_rect.right > self.rect.right:
                self.velocity.x = -200
            else:
                self.velocity.x = 200

    def animate(self, dt):
        self.animation_timer += dt

        if self.is_attacking:

            attack_speed = 0.035

            if self.animation_timer >= attack_speed:
                self.animation_timer = 0
                if self.frame_index < len(self.frames_attack) - 1:
                    self.frame_index += 1
                else:
                    self.is_attacking = False
                    self.damage_dealt = False
                    self.frame_index = 0

            if self.frame_index >= len(self.frames_attack):
                self.frame_index = 0
            self.image = self.frames_attack[self.frame_index]

        elif self.is_casting:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.frame_index < len(self.frames_cast) - 1:
                    self.frame_index += 1
                else:
                    self.is_casting = False
                    self.frame_index = 0

            if self.frame_index >= len(self.frames_cast): self.frame_index = 0
            self.image = self.frames_cast[self.frame_index]

        elif self.is_crouching:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0

                # Increment frame only if we haven't reached the end
                if self.frame_index < len(self.frames_crouch) - 1:
                    self.frame_index += 1
                else:
                    self.shrink_hitbox()
            if self.frame_index >= len(self.frames_crouch): self.frame_index = 0
            self.image = self.frames_crouch[self.frame_index]

        elif self.running:
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.frame_index < len(self.frames_run) - 1:
                    self.frame_index += 1
                else :
                    self.frame_index = 0

            if self.frame_index >= len(self.frames_run): self.frame_index = 0
            self.image = self.frames_run[self.frame_index]

        # elif self.is_standing:
        #     if self.animation_timer >= self.animation_speed:
        #         self.animation_timer = 0
        #         if self.frame_index < len(self.frames_run) - 1:
        #             self.frame_index += 1
        #         else:
        #             self.frame_index = 0
        #
        #     if self.frame_index >= len(self.frames_cast): self.frame_index = 0
        #     self.image = self.frames_run[self.frame_index]
        else:
            if self.rect.height == 64:
                self.frame_index = 0
                self.image = self.idle_image
                self.is_standing = True

    def draw(self, screen, offset):
        draw_pos = self.rect.topleft + offset

        width_diff = self.image.get_width() - self.rect.width

        if width_diff > 0 and not self.facing_right:
            draw_pos.x -= width_diff

        if self.rect.height == 32:
            draw_pos.y -= 32
        if not self.facing_right:
            screen.blit(self.image, draw_pos)
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, draw_pos)