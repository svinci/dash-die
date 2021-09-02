from __future__ import annotations

from typing import Optional

import pygame
from pygame import Surface, Rect
from pygame.font import Font
from pygame.sprite import Sprite

from model.data import Size, RGBColor, Position


class SpriteObject:

    def __init__(self, size: Size, bg_color: RGBColor, position: Position, image: Optional[Surface]):
        self.sprite = Sprite()

        self.sprite.image = image if image else Surface(size.get_tuple())
        if not image:
            self.sprite.image.fill(bg_color.get_tuple())

        self.sprite.rect = Rect(0, 0, size.width, size.height)
        self.sprite.rect.center = position.get_tuple()
        self.position = position
        self.size = size

    def check_collision(self, collider: SpriteObject) -> bool:
        return self.sprite.rect.colliderect(collider.sprite.rect)

    def check_containement(self, contained: SpriteObject) -> bool:
        return self.sprite.rect.contains(contained.sprite.rect)

    def move(self, position: Position):
        self.position = position
        self.sprite.rect.center = position.get_tuple()

    def fill(self, bg_color: RGBColor):
        self.sprite.image.fill(bg_color.get_tuple())

    def resize(self, size: Size):
        self.sprite.rect.size = size.get_tuple()

    def set_image(self, image: Surface):
        self.sprite = Sprite()
        self.sprite.image = image
        self.sprite.rect = Rect(0, 0, self.size.width, self.size.height)
        self.sprite.rect.center = self.position.get_tuple()


class HUD:

    def __init__(self, surface: Surface, font: str, font_size: int, font_color: RGBColor,
                 background_color: RGBColor):
        self.surface = surface
        self.font = Font(font, font_size)
        self.font_color = font_color
        self.background_color = background_color

        self.turbo = 100
        self.destroyed_projectiles = 0

    def set_turbo(self, turbo: int):
        self.turbo = turbo

    def render(self):
        self.surface.fill(self.background_color.get_tuple())
        self.render_destroyed_projectiles()
        self.render_turbo_gauge()

    def render_turbo_gauge(self):
        turbo_gauge = self.font.render('DASH:', False, self.font_color.get_tuple())
        self.surface.blit(turbo_gauge, (10, 10))

        pygame.draw.rect(self.surface, (0, 0, 0), (177, 7, 106, 36), 3)
        pygame.draw.rect(self.surface, (255, 127, 0), pygame.Rect(180, 10, self.turbo, 30))

    def render_destroyed_projectiles(self):
        kill_counter = self.font.render('PUNTAJE: {}'.format(self.destroyed_projectiles), False, self.font_color.get_tuple())
        self.surface.blit(kill_counter, (10, 50))
