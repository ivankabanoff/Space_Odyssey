import pygame
from load_image import load_image


class LaserBolt(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, big_enemy=False):
        pygame.sprite.Sprite.__init__(self)
        self.be_parent = big_enemy
        self.speed = 10
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(2):
            img = pygame.transform.rotate(load_image(f'data/laser_bolts/{i}.png', scale=2), -90)
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, group_1, group_2, group_3, player, laser_group):
        self.update_animation()
        laser_bolts_group = laser_group
        player_spaceship = player
        small_enemies_group = group_1
        medium_enemies_group = group_2
        big_enemies_group = group_3
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > 1000:
            self.kill()
        # Проверяем на коллизии
        if not self.be_parent:
            if pygame.sprite.spritecollide(self, small_enemies_group, False):
                hit_spaceships = pygame.sprite.spritecollide(self, small_enemies_group, False)
                for spaceship in hit_spaceships:
                    if spaceship.alive:
                        spaceship.health -= 5
                        player_spaceship.score += 1
                self.kill()
            if pygame.sprite.spritecollide(self, medium_enemies_group, False):
                hit_spaceships = pygame.sprite.spritecollide(self, medium_enemies_group, False)
                for spaceship in hit_spaceships:
                    if spaceship.alive:
                        spaceship.health -= 5
                        player_spaceship.score += 3
                self.kill()
            if pygame.sprite.spritecollide(self, big_enemies_group, False):
                hit_spaceships = pygame.sprite.spritecollide(self, big_enemies_group, False)
                for spaceship in hit_spaceships:
                    if spaceship.alive:
                        spaceship.health -= 5
                        player_spaceship.score += 5
                self.kill()
        else:
            if pygame.sprite.spritecollide(player_spaceship, laser_bolts_group, False):
                if player_spaceship.alive:
                    player_spaceship.health -= 2.5
                    self.kill()

    def update_animation(self):
        animation_cooldown = 120
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0