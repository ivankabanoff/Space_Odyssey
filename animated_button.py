import pygame


class AnimatedButton:
    """
    Класс, отвечающий за создание кнопок

    """

    def __init__(self, x, y, image1, image2, image3, scale, screen):
        self.screen = screen
        width = image1.get_width()
        height = image1.get_height()
        self.normal = pygame.transform.scale(image1, (int(width * scale), int(height * scale)))
        self.hover = pygame.transform.scale(image2, (int(width * scale), int(height * scale)))
        self.pressed = pygame.transform.scale(image3, (int(width * scale), int(height * scale)))
        self.rect = self.normal.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        left, middle, right = pygame.mouse.get_pressed()
        image = None
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            image = self.hover
            if left and self.rect.collidepoint(pygame.mouse.get_pos()):
                image = self.pressed
            else:
                image = self.hover
        else:
            image = self.normal
        self.screen.blit(image, self.rect)

    def is_pressed(self):
        left, middle, right = pygame.mouse.get_pressed()
        if left and self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False
