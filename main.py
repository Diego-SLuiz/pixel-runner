import pygame
from pygame import SCALED

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 400


def main() -> None:
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED, 1)
    pygame.display.set_caption("Pixel Runner")

    from src.game import Game

    pixel_runner: Game = Game()
    pixel_runner.main_loop()


if __name__ == "__main__":
    main()
