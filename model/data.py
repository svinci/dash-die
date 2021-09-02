from __future__ import annotations

from typing import Dict


class Position:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_tuple(self) -> tuple: return self.x, self.y


class Size:

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def get_tuple(self) -> tuple: return self.width, self.height


class RGBColor:

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def get_tuple(self) -> tuple: return self.r, self.g, self.b


class Configuration:

    def __init__(self, fps: int, player_velocity: float, screen_size: Size, turbo_frames: int, font: str, font_size: int,
                 background_color: RGBColor, hud_font_color: RGBColor, play_area_background_color: RGBColor,
                 images: Dict[str, str], music: str, sounds: Dict[str, str]):
        self.fps = fps
        self.player_velocity = player_velocity
        self.screen_size = screen_size
        self.turbo_frames = turbo_frames
        self.font = font
        self.font_size = font_size

        self.background_color = background_color
        self.hud_font_color = hud_font_color
        self.play_area_background_color = play_area_background_color
        self.images = images
        self.music = music
        self.sounds = sounds
