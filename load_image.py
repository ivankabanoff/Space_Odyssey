import pygame


def load_image(name: str, colorkey: int | pygame.Color = None, scale: int = None) -> pygame.Surface:
    """
    Функция, для получения Surface с изображением

    :param name: Имя файла
    :param colorkey: Цвет, который необходимо изменить на прозрачный. В случае, если colorkey = -1,
    на прозрачный будет заменен цвет левого верхнего угла изображения
    :param scale: В случае, если масштаб изображения необходимо изменить, принимает кортеж с необходимой высотой
    и шириной
    :return: pygame.Surface
    """
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if scale:
        image = pygame.transform.scale_by(image, scale)
    return image