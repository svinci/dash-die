from random import randint
from typing import List, Optional, Dict

from pygame import Surface

from model.data import Size, RGBColor, Position
from model.graphics import SpriteObject


def move_projectiles(dt: int, play_area: Surface, projectiles: List[SpriteObject]):
    center_x, center_y = play_area.get_rect().center
    center_position = Position(center_x, center_y)

    for projectile in projectiles:
        delta_x = center_position.x - projectile.position.x
        delta_y = center_position.y - projectile.position.y

        divider = (abs(delta_x) + abs(delta_y)) * dt
        if divider == 0:
            continue

        x_speed = delta_x / divider
        y_speed = delta_y / divider
        projectile.move(Position(projectile.position.x + (x_speed * dt), projectile.position.y + (y_speed * dt)))


def handle_collisions(dashing: bool, projectiles: List[SpriteObject], safe_house: SpriteObject,
                      player: SpriteObject) -> (List[SpriteObject], bool, int):
    remaining_projectiles = []
    safe_house_hits = 0
    destroyed_projectiles = 0
    player_hits = 0

    for projectile in projectiles:
        if projectile.check_collision(safe_house):
            safe_house_hits += 1

        if projectile.check_collision(player):
            if dashing:
                destroyed_projectiles += 1
            else:
                player_hits += 1
                remaining_projectiles.append(projectile)
        else:
            remaining_projectiles.append(projectile)

    return remaining_projectiles, safe_house_hits > 0 or player_hits > 0, destroyed_projectiles


def spawn_projectile(projectiles: List[SpriteObject], destroyed_projectiles: int, play_area_size: Size,
                     images: Dict[str, Surface]) -> Optional[SpriteObject]:
    max_projectiles = max(1, round(destroyed_projectiles / 4))
    if len(projectiles) < max_projectiles:  # TODO
        randomize_x = randint(0, 1)
        if randomize_x:
            x = random_coordinate(play_area_size.width)
            y = random_coordinate_limit(play_area_size.height)
        else:
            x = random_coordinate_limit(play_area_size.width)
            y = random_coordinate(play_area_size.height)

        return SpriteObject(
            Size(30, 30),
            bg_color=RGBColor(255, 0, 0),
            position=Position(x, y),
            image=images['meteor']
        )
    return None


def random_coordinate(limit: int):
    return randint(0, limit)


def random_coordinate_limit(limit: int):
    value = randint(0, 1)
    return 0 if value == 0 else limit
