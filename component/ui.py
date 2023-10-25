'''
:about: controls and setup all UI for the game.

:class: GameUI: controls and set the UI for the game.
'''
import pygame

# import in-build module
from .utils import load_image, Label, Button, BoxLayout

all = ("GameUI")


class GameUI:
    '''
    :class: controls and setup all the UI asserts and functionality for the game.
    '''
    all = ("start_message", "gameover_message", "show_number", "setup_gamemenu",
               "show_gamemenu", "setup_settingmenu", "show_settingmenu", "show_highscore",
               "show_about_btn")

    GAMEFONT = None
    GAMEFONTSIZE = 40
    GAMEFONTCOLOR = "#F2CACA"

    def __init__(self, data: dict):
        self._gamedata = data
        GameUI.GAMEFONT = data["font"]["gamefont"]
        # load all the UI assert
        self.start_message_img = load_image(data["ui"]["message"], (284, 480),
                                            convert=(False, True))
        self.gameover_message_img = load_image(data["ui"]["gameover"], (292, 42),
                                               convert=(False, True))

        # load numbers for the game.
        self.number_image = []
        for i in range(10):
            self.number_image.append(load_image(data["ui"]["numbers"][i],
                                                convert=(False, True)))

        # load widget for the game
        self.restart_font = Label("Press R to restart", (175, 250), fontname=GameUI.GAMEFONT,
                                  fontsize=GameUI.GAMEFONTSIZE, fontcolor=GameUI.GAMEFONTCOLOR)
        self.back_font = Label("Press X to back", (175, self.restart_font.rect.bottom),
                               fontname=GameUI.GAMEFONT, fontsize=GameUI.GAMEFONTSIZE,
                               fontcolor=GameUI.GAMEFONTCOLOR)
        self.about_btn = Button("About", (580, 0), fontsize=22,
                                fontname=GameUI.GAMEFONT,
                                fontcolor="#1BABB5", focuscolor="#E8E8E8")

        # calling in-class functions
        self.setup_gamemenu()
        self.setup_settingmenu()

    def __str__(self):
        ''':method: string representation of the class'''
        return f"{self.__class__}: {self.all}"

    def start_message(self, screen: pygame.Surface) -> None:
        ''':method: used to show start message'''
        screen.blit(self.start_message_img, (158, 0))

    def gameover_message(self, screen: pygame.Surface) -> None:
        '''method: show game over UI, play again and back button'''

        screen.blit(self.gameover_message_img, (175, 198))
        screen.blit(self.restart_font.img, self.restart_font.rect)
        screen.blit(self.back_font.img, self.back_font.rect)

    def show_number(self, screen: pygame.Surface, number: str) -> None:
        ''':method: used to show the score over the screen'''

        pos = (320 - (24 * len(number)), 0)
        count = 1
        '''
        numbers are separated horizontally with 24 pixel a part.
        '''
        for num in number:
            screen.blit(self.number_image[eval(num)], (pos[0] + (24 * count), pos[1]))
            count += 1

    def setup_gamemenu(self) -> None:
        ''':method: used to setup start-game-menu stuff'''

        new_game_btn = Button("New Game", (250, 0), fontsize=32, fontname=GameUI.GAMEFONT,
                              fontcolor="#F5EBEB", focuscolor="#E8E8E8")
        con_game_btn = Button("Continue", (250, 0), fontsize=32, fontname=GameUI.GAMEFONT,
                              fontcolor="#F5EBEB", focuscolor="#E8E8E8")
        set_game_btn = Button("Settings", (250, 0), fontsize=32, fontname=GameUI.GAMEFONT,
                              fontcolor="#F5EBEB", focuscolor="#E8E8E8")

        # creating a box layout for auto alignment
        self.gamemenu_boxlayout = BoxLayout((640, 480), spacing=10, orientation="vertical")
        self.gamemenu_boxlayout.add(new_game_btn, con_game_btn, set_game_btn)

    def setup_settingmenu(self) -> None:
        ''':method: used to setup setting-menu stuff'''

        fps_label = Label("FPS", (0, 100), fontsize=32, fontname=GameUI.GAMEFONT,
                          fontcolor="#F5EBEB")
        fps_30_btn = Button("30", (0, 100), fontsize=32, fontname=GameUI.GAMEFONT,
                            fontcolor="#F5EBEB", focuscolor="#E8E8E8")
        fps_60_btn = Button("60", (0, 100), fontsize=32, fontname=GameUI.GAMEFONT,
                            fontcolor="#F5EBEB", focuscolor="#E8E8E8")

        # creating a box layout for auto alignment
        self.settingmenu_boxlayout_1 = BoxLayout((640, 480), spacing=5, orientation="horizontal")
        self.settingmenu_boxlayout_1.add(fps_label, fps_30_btn, fps_60_btn)

    def show_gamemenu(self, screen: pygame.Surface) -> None:
        ''':method: used to display game-menu into the screen'''
        self.gamemenu_boxlayout.blit(screen)

    def show_settingmenu(self, screen: pygame.Surface) -> None:
        ''':method: used to display settings-menu into the screen'''
        self.settingmenu_boxlayout_1.blit(screen)

    def show_highscore(self, screen: pygame.Surface, score: int) -> None:
        ''':method: used to display high-score into the screen'''
        score = Label(f"High Score: {score}", (175, 150), fontname=GameUI.GAMEFONT,
                      fontcolor="#F5EBEB")
        score.blit(screen)

    def show_about_btn(self, screen: pygame.Surface) -> None:
        ''':method: used to display about text into the screen'''
        self.about_btn.blit(screen)

    def show_message(self, message: str, screen: pygame.Surface,
                     pos: tuple[int, int], **kw) -> None:
        ''':method: used to display message over the screen'''
        message = Label(message, pos, **kw)
        message.blit(screen)
