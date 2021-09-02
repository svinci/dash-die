from typing import Optional

from pygame import Surface
from pygame.event import Event
from pygame.font import Font
from pygame.locals import (
    K_RETURN,
    KEYUP,
)

from model import Screen
from model.data import Configuration


class Menu(Screen):

    def __init__(self, screen: Surface, configuration: Configuration, score: Optional[int]):
        self.surface = screen
        self.configuration = configuration
        self.title_font = Font(configuration.font, round(configuration.font_size * 1.5))
        self.start_font = Font(configuration.font, round(configuration.font_size))
        self.instructions_font = Font(configuration.font, round(configuration.font_size * 0.8))
        self.start_game = False
        self.score = score

    def move_on(self):
        return self.start_game, None

    def handle_event(self, event: Event):
        if event.type == KEYUP and event.key == K_RETURN:
            self.start_game = True

    def render(self):
        self.surface.fill(self.configuration.background_color.get_tuple())
        if self.score is None:
            title = self.title_font.render('DASH or DIE', False, (255, 127, 0))
        else:
            title = self.title_font.render('Tu Puntaje: {}'.format(self.score), False, self.configuration.hud_font_color.get_tuple())

        start_instruction = self.start_font.render('Enter para jugar', False, self.configuration.hud_font_color.get_tuple())
        play_instruction_a = self.instructions_font.render('- Flechas = Movimiento', False, self.configuration.hud_font_color.get_tuple())
        play_instruction_b = self.instructions_font.render('- Barra espaciadora = DASH', False, self.configuration.hud_font_color.get_tuple())
        play_instruction_c = self.instructions_font.render('- Carga DASH en el planeta', False, self.configuration.hud_font_color.get_tuple())

        center_x, center_y = self.surface.get_rect().center
        self.surface.blit(title, (center_x - 350, center_y - 100))
        self.surface.blit(start_instruction, (center_x - 350, center_y))
        self.surface.blit(play_instruction_a, (center_x - 350, center_y + 70))
        self.surface.blit(play_instruction_b, (center_x - 350, center_y + 100))
        self.surface.blit(play_instruction_c, (center_x - 350, center_y + 130))
