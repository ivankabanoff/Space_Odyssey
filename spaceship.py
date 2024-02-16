import pygame
from load_image import load_image
from laser_bolt import LaserBolt


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen, frames_alive, ch_type, x, y, speed, groups, fail_event, rotate=-90,  ai_enabled=False,
                 player=None):
        self.screen = screen
        self.small_enemies_group, self.medium_enemies_group, self.big_enemies_group = groups[0], groups[1], groups[2]
        self.laser_bolts_group = groups[3]
        self.fail_event = fail_event
        self.alive = True
        self.ch_type = ch_type
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.health = 5
        self.shoot_cooldown = 0
        self.shoot_ai_time = 0
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.score = 0
        if ch_type == 'player':
            self.direction = 1
            self.player_spaceship = self
        else:
            self.direction = -1
            self.player_spaceship = player
        temp_list = []
        for i in range(frames_alive):
            img = pygame.transform.rotate(load_image(f'data/{ch_type}_animation/{i}.png', scale=3), rotate)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(5):
            img = load_image(f'data/explosion/{i}.png', scale=3)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.animation_list[1].append(load_image('data/transp_background.png'))
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.ai_enabled = ai_enabled
        self.sound = pygame.mixer.Sound('data/sounds/laser.wav')

    def update(self):
        if self.ch_type != 'player':
            self.movement(self.speed)
        if self.ai_enabled:
            self.ai()
        self.update_animation()
        self.check_alive()
        self.check_collision()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_up_v, moving_down_v):
        # Обновляем переменные для движения
        if moving_up_v and self.rect.y > 2:
            self.rect.y -= self.speed
        if moving_down_v and self.rect.y < 520:
            self.rect.y += self.speed

    def update_animation(self):
        animation_cooldown = 120
        if self.action == 1:
            animation_cooldown = 80
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 1:
                self.kill()
                self.frame_index = len(self.animation_list[self.action]) - 1
                if self.ch_type == 'player':
                    pygame.event.set_blocked(3)
                    pygame.event.set_blocked(7)
                    pygame.event.set_allowed(6)
                    pygame.event.post(self.fail_event)
            else:
                self.frame_index = 0

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            if self.ai_enabled:
                laser_bolt = LaserBolt(self.rect.centerx +
                                       (0.8 * self.rect.size[0] * self.direction),
                                       self.rect.centery, self.direction, big_enemy=True)
                self.laser_bolts_group.add(laser_bolt)
            else:
                laser_bolt = LaserBolt(self.rect.centerx +
                                       (0.8 * self.rect.size[0] * self.direction),
                                       self.rect.centery, self.direction)
                self.laser_bolts_group.add(laser_bolt)
                self.sound.play()

    def movement(self, speed):
        self.rect.x -= speed

    def check_collision(self):
        if self.rect.right < -1:
            self.kill()
        if self.ch_type == 'player':
            if pygame.sprite.spritecollide(self, self.small_enemies_group, False):
                self.health -= 0.05
        else:
            if pygame.sprite.collide_rect(self.player_spaceship, self):
                self.health -= 5
            if self.ch_type == 'small_enemy':
                if pygame.sprite.spritecollide(self, self.medium_enemies_group, False):
                    self.health -= 5
                if pygame.sprite.spritecollide(self, self.big_enemies_group, False):
                    self.health -= 5
            if self.ch_type == 'medium_enemy':
                if pygame.sprite.spritecollide(self, self.big_enemies_group, False):
                    self.health -= 5

    def ai(self):
        shoot_cooldown = 1000
        if self.alive and self.player_spaceship.alive:
            if pygame.time.get_ticks() - self.shoot_ai_time > shoot_cooldown:
                self.shoot_ai_time = pygame.time.get_ticks()
                self.shoot()

    def update_action(self, new_action):
        # Проверяем отличается ли текущее состояние от нового
        if new_action != self.action:
            self.action += new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.update_action(1)
            self.alive = False

    def draw(self):
        self.screen.blit(self.image, self.rect)