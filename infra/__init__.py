import sys

import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from pygame.time import Clock

from model import Screen
from model.data import Configuration


def setup(configuration: Configuration):
    pygame.init()
    pygame.font.init()
    clock = Clock()
    screen = pygame.display.set_mode(configuration.screen_size.get_tuple())

    images = {}
    for key, path in configuration.images.items():
        images[key] = pygame.image.load(path).convert_alpha()

    pygame.mixer.music.load(configuration.music)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    sounds = {}
    for key, path in configuration.sounds.items():
        sounds[key] = pygame.mixer.Sound(path)

    pygame.mixer.set_num_channels(len(sounds))

    return clock, screen, images, sounds


def loop(screen: Screen):

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
            elif event.type == QUIT:
                sys.exit()

            screen.handle_event(event)

        screen.render()

        pygame.display.flip()

        move_on, result = screen.move_on()
        if move_on:
            return result
