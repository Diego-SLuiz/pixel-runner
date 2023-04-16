import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

from src.enum.direction import Direction


class Fly(Sprite):
    __fly_surface_1: Surface = pygame.image.load(r"graphic/fly/fly_1.png").convert_alpha()
    __fly_surface_2: Surface = pygame.image.load(r"graphic/fly/fly_2.png").convert_alpha()
    __fly_images: list[Surface] = [__fly_surface_1, __fly_surface_2]
    __fly_index: float = 0

    def __init__(self, direction: Direction, vel: int, x: int, y: int):
        super().__init__()
        self.image: Surface
        self.rect: Rect

        if direction == Direction.LEFT:
            self.rect = self.__fly_surface_1.get_rect(bottomleft=(x, y))
            self.image = self.__fly_surface_1

        elif direction == Direction.RIGHT:
            self.rect = self.__fly_surface_1.get_rect(bottomright=(x, y))
            self.image = pygame.transform.flip(self.__fly_surface_1, True, False)

        self.direction: Direction = direction
        self.vel: int = vel

    def __update_animation(self) -> None:
        self.__fly_index += 0.1

        if self.__fly_index >= len(self.__fly_images):
            self.__fly_index = 0

        image = self.__fly_images[int(self.__fly_index)]

        if self.direction == Direction.LEFT:
            self.image = image

        elif self.direction == Direction.RIGHT:
            self.image = pygame.transform.flip(image, True, False)

    def move(self) -> None:
        if self.direction == Direction.LEFT:
            self.rect.x -= self.vel

        elif self.direction == Direction.RIGHT:
            self.rect.x += self.vel

        if self.direction == Direction.LEFT and self.rect.left <= -1000:
            self.kill()

        elif self.direction == Direction.RIGHT and self.rect.right >= 2000:
            self.kill()

    def update(self) -> None:
        self.__update_animation()
        self.move()
