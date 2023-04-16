import pygame
from pygame import Surface, Rect
from pygame.key import ScancodeWrapper
from pygame.mixer import Sound
from pygame.sprite import Sprite

from main import SCREEN_WIDTH
from src.enum.direction import Direction
from src.enum.player_state import PlayerState


class Player(Sprite):
    __stand_surface: Surface = pygame.image.load(r"graphic/player/player_stand.png").convert_alpha()
    __jump_surface: Surface = pygame.image.load(r"graphic/player/player_jump.png").convert_alpha()
    __walk_surface_1: Surface = pygame.image.load(r"graphic/player/player_walk_1.png").convert_alpha()
    __walk_surface_2: Surface = pygame.image.load(r"graphic/player/player_walk_2.png").convert_alpha()
    __walk_images: list[Surface] = [__walk_surface_1, __walk_surface_2]
    __walk_index: float = 0

    __jump_sound: Sound = Sound(r"audio/jump.mp3")
    __jump_sound.set_volume(0.3)

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image: Surface = self.__stand_surface
        self.rect: Rect = self.__stand_surface.get_rect(bottomleft=(x, y))
        self.state: PlayerState = PlayerState.WALK
        self.gravity: float = 0
        self.direction: Direction = Direction.RIGHT
        self.vel: int = 8
        self.x: int = x
        self.y: int = y
        self.grounded: bool = True

    def __handle_input(self) -> None:
        keys: ScancodeWrapper = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.grounded:
            self.jump()

        elif keys[pygame.K_LEFT]:
            self.direction = Direction.LEFT
            self.move()

        elif keys[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT
            self.move()

        elif self.grounded:
            self.state = PlayerState.STAND

    def __apply_gravity(self) -> None:
        self.gravity += 1
        self.rect.y += int(self.gravity)
        self.rect.bottom = min(self.rect.bottom, self.y)

        if not self.grounded and self.rect.bottom >= self.y:
            self.grounded = True
            self.state = PlayerState.STAND

    def __update_animation(self) -> None:
        image: Surface

        if self.state == PlayerState.STAND:
            image = self.__stand_surface

        elif self.state == PlayerState.JUMP:
            image = self.__jump_surface

        else:
            self.__walk_index += 0.1

            if self.__walk_index >= len(self.__walk_images):
                self.__walk_index = 0

            image = self.__walk_images[int(self.__walk_index)]

        if self.direction == Direction.LEFT:
            image = pygame.transform.flip(image, True, False)

        self.image = image

    def jump(self) -> None:
        if self.grounded:
            self.__jump_sound.play()
            self.state = PlayerState.JUMP
            self.grounded = False
            self.gravity = -20

    def move(self) -> None:
        if self.state != PlayerState.JUMP:
            self.state = PlayerState.WALK

        if self.direction == Direction.LEFT:
            self.rect.x -= self.vel

            if self.rect.left < 0:
                self.rect.left = 0

        elif self.direction == Direction.RIGHT:
            self.rect.x += self.vel

            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

    def update(self) -> None:
        self.__handle_input()
        self.__apply_gravity()
        self.__update_animation()
