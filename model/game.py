from random import randint
from typing import List, Dict

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.locals import (KEYDOWN, KEYUP)
from pygame.mixer import Sound
from pygame.sprite import Group
from pygame.time import Clock

from engine.movement import move
from engine.pojectiles import handle_collisions, spawn_projectile, move_projectiles
from model import Screen
from model.data import Configuration, Position, Size, RGBColor
from model.graphics import SpriteObject, HUD


class Game(Screen):

    def __init__(self, clock: Clock, screen: Surface, images: Dict[str, Surface], sounds: Dict[str, Sound], configuration: Configuration):
        self.clock = clock
        self.screen = screen
        self.images = images
        self.sounds = sounds
        self.configuration = configuration
        self.turbo_frames = configuration.turbo_frames

        self.destroyed_projectiles = 0
        self.lost = False

        self.play_area_size = Size(configuration.screen_size.width - 50, configuration.screen_size.height - 150)
        self.play_area = Surface(self.play_area_size.get_tuple())

        hud_size = Size(configuration.screen_size.width, 100)
        hud_surface = Surface(hud_size.get_tuple())
        self.hud = HUD(hud_surface, configuration.font, configuration.font_size, configuration.hud_font_color,
                       configuration.background_color)

        self.actions = set()

        center_x, center_y = self.play_area.get_rect().center
        center_position = Position(center_x, center_y)

        self.player = SpriteObject(
            size=Size(20, 20),
            bg_color=RGBColor(0, 0, 255),
            position=center_position,
            image=images['player']
        )
        self.safe_house = SpriteObject(
            size=Size(50, 50),
            bg_color=RGBColor(0, 255, 0),
            position=center_position,
            image=images['planet']
        )

        self.projectiles: List[SpriteObject] = []

        self.channels = {}
        channel = 0
        for key, _ in self.sounds.items():
            self.channels[key] = channel
            channel += 1

    def move_on(self):
        return self.lost, self.destroyed_projectiles

    def handle_event(self, event: Event):
        if event.type == KEYDOWN:
            self.actions.add(event.key)
        if event.type == KEYUP and event.key in self.actions:
            self.actions.remove(event.key)

    def render(self):
        dt = self.clock.tick(self.configuration.fps)
        dashing = self.move_player(dt)
        self.move_projectiles(dt)

        lost, destroyed_projectiles = self.handle_collisions(dashing)
        self.destroyed_projectiles += destroyed_projectiles
        if lost:
            self.lost = True

        self.hud.destroyed_projectiles = self.destroyed_projectiles

        self.update_turbo_data()
        self.spawn_projectiles()
        self.draw()

    def move_player(self, dt: int):
        player_position, turbo_delta, dashing = move(self.actions, self.player, self.play_area_size,
                                                     self.configuration.player_velocity, self.turbo_frames, dt)

        if dashing:
            self.sounds['dash'].set_volume(0.2)
            self.sounds['dash'].play()
            # self.play_sound('dash', 0.4)
            self.player.set_image(self.images['player_dashing'])
        else:
            self.player.set_image(self.images['player'])

        self.turbo_frames += turbo_delta
        return dashing

    def move_projectiles(self, dt: int):
        move_projectiles(dt, self.play_area, self.projectiles)

    def update_turbo_data(self):
        if self.safe_house.check_collision(self.player):
            self.turbo_frames = self.configuration.turbo_frames

        turbo_gauge = round(self.turbo_frames / self.configuration.turbo_frames * 100)
        self.hud.set_turbo(turbo_gauge)

    def draw(self):
        self.screen.fill(self.configuration.background_color.get_tuple())

        self.screen.blit(self.hud.surface, (0, 0))
        self.screen.blit(self.play_area, (25, 125))
        self.hud.render()

        self.play_area.fill(self.configuration.play_area_background_color.get_tuple())

        projectile_sprites = map(lambda projectile: projectile.sprite, self.projectiles)
        all_group = Group(list(projectile_sprites) + [self.safe_house.sprite, self.player.sprite])
        all_group.draw(self.play_area)

    def spawn_projectiles(self):
        maybe_projectile = spawn_projectile(self.projectiles, self.destroyed_projectiles, self.play_area_size, self.images)
        if maybe_projectile is not None:
            self.projectiles.append(maybe_projectile)

    def random_coordinate(self, limit: int):
        return randint(0, limit)

    def random_coordinate_limit(self, limit: int):
        value = randint(0, 1)
        return 0 if value == 0 else limit

    def handle_collisions(self, dashing: bool):
        remaining_projectiles, lost, destroyed_projectiles = handle_collisions(dashing, self.projectiles, self.safe_house, self.player)

        self.projectiles = remaining_projectiles

        if destroyed_projectiles > 0:
            self.play_sound('explosion', 1.0)
        if lost:
            self.play_sound('laugh', 0.8)

        return lost, destroyed_projectiles

    def play_sound(self, sound_key: str, volume: float):
        self.sounds[sound_key].set_volume(volume)
        pygame.mixer.Channel(self.channels[sound_key]).set_volume(volume)
        pygame.mixer.Channel(self.channels[sound_key]).play(self.sounds[sound_key])
