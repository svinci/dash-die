from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)

from model.data import Position, Size
from model.graphics import SpriteObject


def is_dashing(actions: set, turbo_frames: int) -> bool:
    turbo_attempted = K_SPACE in actions
    return turbo_attempted and turbo_frames > 0


def get_velocity(actions: set, base_velocity: float, turbo_frames: int) -> (int, int):
    turbo = is_dashing(actions, turbo_frames)

    if turbo:
        return base_velocity * 3, -1
    else:
        return base_velocity, 0


def move(actions: set, player: SpriteObject, screen_size: Size, base_velocity: float,
         turbo_frames: int, dt: int) -> (Position, int):
    delta_x, delta_y = 0, 0
    velocity, turbo_delta = get_velocity(actions, base_velocity * dt, turbo_frames)

    for action in actions:

        if action == K_UP:
            delta_y -= velocity
        if action == K_DOWN:
            delta_y += velocity
        if action == K_LEFT:
            delta_x -= velocity
        if action == K_RIGHT:
            delta_x += velocity

    if delta_x == 0 and delta_y == 0:
        return player.position, 0, False

    if delta_x != 0 and delta_y != 0:
        delta_x *= 0.75
        delta_y *= 0.75

    new_x = player.position.x + delta_x
    new_y = player.position.y + delta_y

    half_width = player.size.width / 2
    half_height = player.size.height / 2

    if new_x - half_width < 0:
        new_x = half_width
    if new_x + half_width > screen_size.width:
        new_x = screen_size.width - half_width

    if new_y - half_height < 0:
        new_y = half_height
    if new_y + half_height > screen_size.height:
        new_y = screen_size.height - half_height

    new_position = Position(new_x, new_y)
    player.move(new_position)
    return new_position, turbo_delta, turbo_delta < 0
