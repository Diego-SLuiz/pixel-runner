import sys
from random import randint

import pygame
from pygame import Surface, Rect, Color
from pygame.font import Font
from pygame.mixer import Sound
from pygame.sprite import GroupSingle, Group
from pygame.time import Clock

from main import SCREEN_WIDTH, SCREEN_HEIGHT
from src.enum.direction import Direction
from src.enum.game_state import GameState
from src.fly import Fly
from src.player import Player
from src.snail import Snail

FRAMERATE: int = 60

SpawnRange = tuple[tuple[int, int], tuple[int, int]]
SpawnZone = tuple[SpawnRange, SpawnRange]
EnemySpeed = tuple[int, int]

PLAYER_POS: tuple[int, int] = (50, 300)
SNAIL_SPAWN_ZONE: SpawnZone = (((-400, -100), (900, 1200)), ((300, 300), (300, 300)))
SNAIL_SPEED: EnemySpeed = (4, 6)
FLY_SPAWN_ZONE: SpawnZone = (((-400, -100), (900, 1200)), ((100, 300), (100, 300)))
FLY_SPEED: EnemySpeed = (6, 8)


class Game:
    __game_font: Font = Font(r"font/pixeltype.ttf", 48)
    __game_text_color: Color = Color("white")
    __music_sound: Sound = Sound(r"audio/music.wav")
    __music_sound.set_volume(0.2)
    __hurt_sound: Sound = Sound(r"audio/hurt.mp3")
    __hurt_sound.set_volume(0.3)

    __sky_surface: Surface = pygame.image.load(r"graphic/background/sky.png").convert_alpha()
    __sky_rect: Rect = __sky_surface.get_rect(topleft=(0, 0))

    __ground_surface: Surface = pygame.image.load(r"graphic/background/ground.png").convert_alpha()
    __ground_rect: Rect = __ground_surface.get_rect(topleft=(0, __sky_surface.get_height()))

    __gameplay_background_surface: Surface = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    __gameplay_background_rect: Rect = __gameplay_background_surface.get_rect(topleft=(0, 0))
    __gameplay_background_surface.blit(__sky_surface, __sky_rect)
    __gameplay_background_surface.blit(__ground_surface, __ground_rect)

    __gameover_background_surface: Surface = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    __gameover_background_rect: Rect = __gameover_background_surface.get_rect(topleft=(0, 0))
    __gameover_background_color: Color = Color("#5782A3")
    __gameover_background_surface.fill(__gameover_background_color)

    def __init__(self) -> None:
        self.surface = pygame.display.get_surface()
        self.clock = Clock()
        self.state: GameState = GameState.GAMEOVER
        self.player_group: GroupSingle[Player] = GroupSingle(Player(*PLAYER_POS))
        self.enemy_group: Group[Snail | Fly] = Group()
        self.spawn_event: int = pygame.USEREVENT
        self.score: int = 0
        self.score_adjust: int = 0
        self.highest_score: int = 0
        pygame.time.set_timer(self.spawn_event, 1250)

    def main_loop(self) -> None:
        while True:
            self.clock.tick(FRAMERATE)
            self.handle_input()

            if self.state == GameState.GAMEPLAY:
                self.gameplay_screen()

            elif self.state == GameState.GAMEOVER:
                self.gameover_screen()

            pygame.display.update()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == GameState.GAMEPLAY:
                if event.type == self.spawn_event:
                    self.spawn_enemy()

            elif self.state == GameState.GAMEOVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.new_game()

    def spawn_enemy(self) -> None:
        direction: Direction = Direction(randint(1, 2))
        vel: int
        x_pos: int
        y_pos: int

        if randint(1, 2) == 1:
            vel = randint(*SNAIL_SPEED)

            if direction == Direction.LEFT:
                x_pos = randint(*SNAIL_SPAWN_ZONE[0][1])
                y_pos = randint(*SNAIL_SPAWN_ZONE[1][1])

            else:
                x_pos = randint(*SNAIL_SPAWN_ZONE[0][0])
                y_pos = randint(*SNAIL_SPAWN_ZONE[1][0])

            self.enemy_group.add(Snail(direction, vel, x_pos, y_pos))

        if randint(1, 2) == 1:
            vel = randint(*FLY_SPEED)

            if direction == Direction.LEFT:
                x_pos = randint(*FLY_SPAWN_ZONE[0][1])
                y_pos = randint(*FLY_SPAWN_ZONE[1][1])

            else:
                x_pos = randint(*FLY_SPAWN_ZONE[0][0])
                y_pos = randint(*FLY_SPAWN_ZONE[1][0])

            self.enemy_group.add(Fly(direction, vel, x_pos, y_pos))

    def new_game(self) -> None:
        self.score_adjust = pygame.time.get_ticks() // 10
        self.enemy_group.empty()
        self.player_group.sprite.rect.bottomleft = PLAYER_POS
        self.player_group.sprite.gravity = 0
        self.state = GameState.GAMEPLAY
        self.__music_sound.play()

    def end_game(self) -> None:
        self.__hurt_sound.play()
        self.__music_sound.stop()
        self.highest_score = max(self.score, self.highest_score)
        self.state = GameState.GAMEOVER

    def gameplay_screen(self) -> None:
        # background
        self.surface.blit(self.__gameplay_background_surface, self.__gameplay_background_rect)

        # score
        self.score = pygame.time.get_ticks() // 10 - self.score_adjust
        score_surface: Surface = self.__game_font.render(f"Score: {self.score}", False, self.__game_text_color)
        score_rect: Rect = score_surface.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
        self.surface.blit(score_surface, score_rect)

        # player
        self.player_group.update()
        self.player_group.draw(self.surface)

        # enemies
        self.enemy_group.update()
        self.enemy_group.draw(self.surface)

        # collision
        for enemy in self.enemy_group.sprites():
            if enemy.rect.colliderect(self.player_group.sprite.rect):
                self.end_game()

    def gameover_screen(self) -> None:
        # background
        self.surface.blit(self.__gameover_background_surface, self.__gameover_background_rect)

        # title
        title: str = "Pixel Runner"
        title_surface: Surface = self.__game_font.render(title, False, self.__game_text_color)
        title_rect: Rect = title_surface.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
        self.surface.blit(title_surface, title_rect)

        # player
        player_surface: Surface = pygame.image.load(r"graphic/player/player_stand.png").convert_alpha()
        player_size: tuple[int, int] = (player_surface.get_width() * 2, player_surface.get_height() * 2)
        player_scaled: Surface = pygame.transform.scale(player_surface, player_size)
        player_rect: Rect = player_scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.surface.blit(player_scaled, player_rect)

        # message
        message: str = "Press 'space' to run!"

        if self.highest_score != 0:
            message = f"Highest score: {self.highest_score}"

        message_surface: Surface = self.__game_font.render(message, False, self.__game_text_color)
        message_rect: Rect = message_surface.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.surface.blit(message_surface, message_rect)
