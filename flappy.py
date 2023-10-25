'''
author: Ramayan Mardi
email: jaymisra.programmer@gmail.com
=======================================
:about: This is script file of the game,
:name: Flappy Game
:version: 1.0.1
:requirement:
    python -> 3.10.0 or upper
    pygame -> 2.5.2

This script file controls, all the game related stuff i.e game state, rendering etc.
:class Game: controls all the above stuff.
:function main: entry point of the game.
'''

import pygame
from pygame.locals import *
import os

# import in-built module/component
from component.utils import *
from component.flappy import Flappy
from component.pipes import ObsticalControler, MovingImage
from component.ui import GameUI

all = ("Game", "main")

# absolute path of the current files
ASSERT_PATH = "assert"
DATA_FILENAME = "data.json"

# Constants
SCREEN_SIZE = (640, 480)
TITLE = "Flappy Game"


class Game:
    ''':class: control the whole game, handles game state, handles rendering,
        handles inputs, handles I/O in file.
    '''
    FPS = None  # keep information of the the frame-per-second of the game
    all = ("setup", "update", "new_game", "run")

    def __init__(self, window_size: tuple[int, int], window_title: str):
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(window_title)

        # clock for the game controls the game time.
        self.clock = pygame.time.Clock()

        # store all the game data need for processing game
        self._gamedata = dict()

        # decide whether the game updates or not
        self._allow_update = True
        # decide whether the game-over or not
        self._gameover = False

        # store the game state
        self._game_state = "Menu"

    def setup(self) -> None:
        ''':method: used to load all the assert for the game'''

        # fetching all the data from the file.
        self._gamedata = fetch(os.path.join(ASSERT_PATH, DATA_FILENAME))

        # fetching all content for the about file.
        with open(os.path.join(ASSERT_PATH, "about.txt"), "r") as f:
            about_data = f.read()

        # load entity for the game.
        flappy_images = []

        for i in range(3):
            flappy_images.append(load_image(self._gamedata["yellowbird"][i], convert=(False, True)))

        # position of the player is in middle of the screen.
        self.flappy = Flappy(flappy_images=flappy_images, weight=self._gamedata["entity"]["weight"],
                             fly_speed=self._gamedata["entity"]["fly_speed"],
                             pos=(320, 184))

        # load all the obstical for the game.
        green_pipe = load_image(self._gamedata["game_objects"]["pipe-green"], convert=(True, False))
        self.obstical = ObsticalControler(green_pipe)

        # load all the environment for the game.
        self.background_day_image = MovingImage(load_image(
                                                self._gamedata["game_objects"]["background-day"],
                                                SCREEN_SIZE, (True, False)), (0, 0))
        self.base_image = MovingImage(load_image(self._gamedata["game_objects"]["base"], (640, 112),
                                                 convert=(True, False)), (0, 368))

        # load all sounds for the game.
        self.hit = pygame.mixer.Sound(self._gamedata["sfx"]["hit"])
        self.wing = pygame.mixer.Sound(self._gamedata["sfx"]["wing"])
        self.point = pygame.mixer.Sound(self._gamedata["sfx"]["point"])
        self.die = pygame.mixer.Sound(self._gamedata["sfx"]["die"])

        # load all the UI for the game.
        self.gameui = GameUI(self._gamedata)
        # text box for the game.
        self.textbox = TextBox(about_data, (0, 0), fontname=self._gamedata["font"]["gamefont"],
                               fontcolor="#F5EBEB", fontsize=22)

    def update(self, delta_time: float, **kw) -> None:
        ''':method: used to update all the game related stuff.

            kw: contains all the inputs data.
        '''

        # game code -------------------------------------
        if self._game_state == "Menu":
            self.screen.fill("#383838")
            self.gameui.show_gamemenu(self.screen)
            self.gameui.show_about_btn(self.screen)

            '''
            if continuation of the game is possible than the continue button gets
            highlighted.
            '''
            self.gameui.gamemenu_boxlayout.chlidren[1].active = self._gamedata["continue"]

            # trigger the functions according to the button pressed.
            # `New Game` button pressed.
            if self.gameui.gamemenu_boxlayout.chlidren[0].pressed:
                self._game_state = "Start New Game"  # game state changed
                '''
                only the the assert would draw and nothing gets updated.
                '''
                self._allow_update = False

            # `Continue` button pressed and continuation is possible.
            elif self.gameui.gamemenu_boxlayout.chlidren[1].pressed and self._gamedata["continue"]:
                # placing entity to the previous position.
                self.flappy.rect.topleft = self._gamedata["entity"]["pos"]

                # placing all the obstical for the game to the previous position.
                self.obstical._custom_pipe_pos(self._gamedata["pipes_pos"]["toppipe_list"],
                                               self._gamedata["pipes_pos"]["bottompipe_list"])

                # placing all the environment for the game to the previous position.
                self.base_image.moving_images["img1"][1].topleft = self._gamedata["other_entity"]["base_pos"]["img1"]
                self.base_image.moving_images["img2"][1].topleft = self._gamedata["other_entity"]["base_pos"]["img2"]
                self.background_day_image.moving_images["img1"][1].topleft = self._gamedata["other_entity"]["background_pos"]["img1"]
                self.background_day_image.moving_images["img2"][1].topleft = self._gamedata["other_entity"]["background_pos"]["img2"]

                # set previous score.
                self.obstical.score = self._gamedata["score"]
                self.obstical.previous_score = self._gamedata["previous_score"]

                # start the game as previous
                self._game_state = "Start New Game"
                self._allow_update = False

            # `Setting` button is pressed.
            elif self.gameui.gamemenu_boxlayout.chlidren[2].pressed:
                '''
                active the fps button which is using by the game.
                '''
                if self._gamedata["fps"] == 30:
                    self.gameui.settingmenu_boxlayout_1.chlidren[1].active = True
                else:
                    self.gameui.settingmenu_boxlayout_1.chlidren[2].active = True

                # changed the game state
                '''
                setting game state is required because in those blocks of settings.
                content a code that are updated in each frame when the game state
                is set to be "Settings"
                '''
                self._game_state = "Settings"

            # `About` button is pressed
            elif self.gameui.about_btn.pressed:
                # same reason as like the `Setting` button.
                self._game_state = "About"

        # Gets updated in each frame when 'Setting' is activate.
        elif self._game_state == "Settings":
            self.screen.fill("#383838")
            self.gameui.show_settingmenu(self.screen)

            if kw["K_x"]:
                self._game_state = "Menu"

            # trigger functions when the button inside the setting menu get pressed.
            children = self.gameui.settingmenu_boxlayout_1.chlidren

            # TODO: make the below code more clean.
            # handles the state of fps buttons and game fps setting
            if children[2].pressed:
                children[2].active = True
                # updates the entire game fps
                self._gamedata["fps"] = 60
            elif children[1].pressed:
                children[2].active = False
                # updates the entire game fps
                self._gamedata["fps"] = 30

            children[1].active = not children[2].active

        # Gets updated in each frame when 'About' is activate.
        elif self._game_state == "About":
            # textbox content all the details for the game gets visible.
            self.textbox.blit(self.screen)

            if kw["K_x"]:
                self._game_state = "Menu"

        # Gets updated in each frame when 'Start New Game' is activate.
        elif self._game_state == "Start New Game":
            # called when the game is not over and ready to play.
            if not self._gameover:
                # drawing game background.
                self.background_day_image.blit(self.screen)

                self.flappy.blit(self.screen)  # entity.

                # drawing game environment
                self.obstical.toppipe.draw(self.screen)
                self.obstical.bottompipe.draw(self.screen)
                self.base_image.blit(self.screen)
                self.gameui.show_number(self.screen, str(self.obstical.score))

                # if allow update is True
                if self._allow_update:
                    # update all the entities.
                    self.background_day_image.move_image(self.screen, 50, delta_time, (-1, 0))
                    self.flappy.update(delta_time, **kw)
                    self.obstical.update(delta_time)
                    self.base_image.move_image(self.screen, 100, delta_time, (-1, 0))

                    # check collision of entity with the pipes
                    if self.obstical.collision(self.flappy.collision_rect):
                        self.hit.play()
                        self._allow_update = False
                        self._gameover = True

                    # check collision of the entity with the base
                    if self.base_image.collision(self.flappy.collision_rect):
                        self.hit.play()
                        self._allow_update = False
                        self._gameover = True

                    '''
                    play the sound when the entity flap it's wings.
                    '''
                    if kw["K_SPACE"]:
                        self.wing.play()

                    '''
                    play sound when the point get incresed
                    '''
                    if self.obstical.score > self.obstical.previous_score:
                        self.point.play()
                        self.obstical.previous_score = self.obstical.score
                else:
                    # message show when update is False
                    '''
                    This message is show during the game start, continuation of the game,
                    and also during the game get paused.
                    '''
                    self.gameui.start_message(self.screen)

                '''
                below code handles the functionality of the pause mechanism by
                manipulating :attr self._allow_update:
                '''
                if kw["K_p"] and self._allow_update:
                    self._allow_update = False
                elif kw["K_p"] and not self._allow_update:
                    self._allow_update = True
                elif kw["K_SPACE"] and not self._allow_update:
                    self._allow_update = True

                '''
                during the game is running, and the back button is pressed then the
                continuation data gets save, and continuation gets updated.
                '''
                if kw["K_x"]:
                    # store the entity data.
                    self._gamedata["entity"] = {
                                            "weight": self.flappy.weight,
                                            "fly_speed": self.flappy.fly_speed,
                                            "pos": self.flappy.rect.center}

                    # store the list of pipe position as a data of both top-pipes and bottom-pipes.
                    self._gamedata["pipes_pos"] = {
                    "toppipe_list": [pipe.rect.topleft for pipe in self.obstical.toppipe_list],
                    "bottompipe_list": [pipe.rect.topleft for pipe in self.obstical.bottompipe_list]}

                    # store the data of other entities i.e environment stuff.
                    self._gamedata["other_entity"] = {"base_pos": {
                                "img1": self.base_image.moving_images["img1"][1].topleft,
                                "img2": self.base_image.moving_images["img2"][1].topleft
                                },
                                "background_pos": {
                                "img1": self.background_day_image.moving_images["img1"][1].topleft,
                                "img2": self.background_day_image.moving_images["img2"][1].topleft}
                    }

                    # continuation get activate and score is preserved.
                    self._gamedata["continue"] = True
                    self._gamedata["score"] = self.obstical.score
                    self._gamedata["previous_score"] = self.obstical.previous_score

                    # back to the main menu
                    self._game_state = "Menu"
                    self.new_game()

            # called when the game gets over.
            elif self._gameover:
                # store high-score data if score is greater.
                if self.obstical.score > self._gamedata["highscore"]:
                    self._gamedata["highscore"] = self.obstical.score

                # if high-score is greater than '0' it gets displayed on screen.
                if self._gamedata["highscore"]:
                    self.gameui.show_highscore(self.screen, self._gamedata["highscore"])

                # finally game-over message would be shown.
                self.gameui.gameover_message(self.screen)

                if kw["K_x"]:
                    # back to the main menu
                    self._game_state = "Menu"
                    # reset the game over button
                    self.new_game()
                    self._gamedata["continue"] = False

            if kw["K_r"] and self._gameover:
                # resume the game and its state
                self.new_game()

    def new_game(self) -> None:
        ''':method: used to set-up new game.'''

        # reset all the values.
        self._allow_update = True
        self.obstical.generate_pipe()
        self.obstical.score = 0
        self.obstical.previous_score = self.obstical.score

        self.flappy.rect.topleft = (480 // 2, 368 // 2)
        self._gameover = False

    def run(self) -> None:
        ''':method: main-loop of the game.'''

        # load all the assert for the game.
        self.setup()

        # running main-loop of the game
        running = True
        while running:
            # shortcut keys responsible for controlling inputs in the whole game.
            self.ShortCuts = {"K_SPACE": False, "K_r": False, "K_x": False,
                              "K_p": False}

            # tracking the pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                # check key presses for the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ShortCuts["K_SPACE"] = True

                    if event.key == pygame.K_p:
                        self.ShortCuts["K_p"] = True

                    if event.key == pygame.K_r:
                        self.ShortCuts["K_r"] = True

                    if event.key == pygame.K_x:
                        self.ShortCuts["K_x"] = True

            # delta time of the entire game.
            delta_time = self.clock.tick(self._gamedata["fps"]) / 1000.0
            # update the whole game.
            self.update(delta_time, **self.ShortCuts)
            pygame.display.update()

        # quit the game
        save(os.path.join(ASSERT_PATH, DATA_FILENAME), self._gamedata)
        pygame.quit()
        exit()


def main():
    ''':function: entry point of the game.'''
    pygame.init()  # initializing pygame
    Game(SCREEN_SIZE, TITLE).run()


if __name__ == '__main__':
    main()
