from infra import setup, loop
from model.data import Configuration, Size, RGBColor
from model.game import Game
from model.menu import Menu


def main():
    configuration = Configuration(
        fps=60,
        player_velocity=0.5,
        screen_size=Size(800, 800),
        turbo_frames=250,
        font='./assets/fonts/PressStart2P-Regular.ttf',
        font_size=30,

        background_color=RGBColor(100, 100, 100),
        hud_font_color=RGBColor(0, 0, 0),
        play_area_background_color=RGBColor(0, 0, 0),

        images={
            'meteor': './assets/images/meteor.png',
            'planet': './assets/images/planet.png',
            'player': './assets/images/ship.png',
            'player_dashing': './assets/images/ship_dashing.png',
        },
        music='./assets/sound/music.wav',
        sounds={
            'explosion': './assets/sound/explosion.wav',
            'laugh': './assets/sound/laugh.wav',
            'dash': './assets/sound/dash.wav',
        },
    )
    clock, screen, images, sounds = setup(configuration)

    menu = Menu(screen=screen, configuration=configuration, score=None)
    loop(menu)

    while True:
        game = Game(clock=clock, screen=screen, images=images, sounds=sounds, configuration=configuration)
        score = loop(game)

        menu = Menu(screen=screen, configuration=configuration, score=score)
        loop(menu)


if __name__ == '__main__':
    main()
