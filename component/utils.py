'''
:about: script file contents all the supported class and function for the game.
:class: Text: create a pygame text surface with the given fontname.
:class: SysFont: create a pygame text surface with the system fontname.
:class: Label: used to display label in the screen.
:class: Button: used to display button on the screen.
:class: Boxlayout: used to align widgets horizontal and vertical order.
:class: TextBox: used display multi line text on the screen.

:function: fetch: used to fetch json data from the .json file.
:function: save: used to save json data to a .json file.
:function: load_image: used to load image and convert those image into pygame image.
'''
import pygame
import json

all = ("fetch", "save", "load_image", "Text", "SysFont", "Label", "Button",
           "BoxLayout", "Text")


def fetch(filename: str) -> dict:
    '''
    :function: used for fetching/reading data from the filename.

    :param filename: name of the file.

    :return: dictionary of data.
    '''
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        return data
    except FileNotFoundError as error:
        print(error)


def save(filename: str = None, data: dict = None, mode: str = 'w') -> None:
    '''
    :function: used to save the content in the file (filename) in the 'json' format,
    if no filename is passed than the default filename is selected.

    :param filename: name of the file or filename along with the path.
    :param mode: in which mode is to write in the file.
    '''
    with open(filename, mode) as f:
        json.dump(data, f, indent=4)


def load_image(filename: str, scale: tuple[int, int] = None,
               convert: tuple[bool, bool] = (False, False)) -> pygame.Surface:
    '''
    :method: used to load image from file and convert into pygame image.

    :param filename: name of image file.
    :param scale: if the image needs to scale.
    :param convert: (True, True) if the first one is true than the pygame.convert
    function was apply to the image and if second one is true then the pygame.convet_alpha
    function was apply.

    :return: pygame surface of image.
    '''

    image = pygame.image.load(filename)

    if scale:  # scale the image if needed
        image = pygame.transform.scale(image, scale)

    # apply conversion.
    if convert[0]:
        image = image.convert()
    elif convert[1]:
        image = image.convert_alpha()

    return image


# method is not used in this version.
# def extract_image_from_spritesheet(spritesheetname: str, split: tuple[int, int]) -> list:
#     ''''''
#     image = pygame.image.load(spritesheetname)
#     size = image.get_size()
#     x_size = size[0] // split[0]  # no. of slice in x direction
#     y_size = size[1] // split[1]  # no. of slice in y direction.
#     images = []  # hold the new slice images.

#     # slice in a order of left -> right of the image and
#     # top -> bottom from the topleft corner of the image
#     for y in range(0, size[0], y_size):
#         for x in range(0, size[1], x_size):
#             images.append(clip(image, x, y, size[0] // split[0], size[1] // split[1]))

#     return images


# def clip(surface: pygame.Surface, x: int, y: int,
#          x_size: int, y_size: int) -> pygame.Surface:
#     handle_surface = surface.copy()  # Sprite that will get process later
#     clipRect = pygame.Rect(x, y, x_size, y_size)  # Part of the image
#     handle_surface.set_clip(clipRect)  # Clip or you can call cropped
#     image = surface.subsurface(handle_surface.get_clip())  # Get subsurface
#     return image.copy()


class Text:
    ''':class: used create pygame font object and also content functionality to display
        font on the screen.
    '''
    all = ("setup", "render", "blit")

    def __init__(self, text: str, pos: tuple[int, int], **kw):
        self.text = text
        self.pos = pos

        # extracting all the values or accepted default values
        self.size = kw.get("size")
        self.h_align = kw.get("h_align") or False
        self.v_align = kw.get("v_align") or False
        self.fontname = kw.get("fontname")
        self.fontsize = kw.get("fontsize") or 32
        self.antialias = kw.get("antialias") or True
        self.fontcolor = kw.get("fontcolor") or "#000000"
        self.background = kw.get("background")
        self.alpha = kw.get("alpha") or 255
        self.bold = kw.get("bold") or False
        self.italic = kw.get("italic") or False
        self.underline = kw.get("underline") or False

        # calling in-class functions
        self.setup()
        self.render()

    def setup(self):
        ''':method: used to set up the font in the pygame'''
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)

    def render(self):
        ''':method: used to render font'''
        self.img = self.font.render(self.text, self.antialias, self.fontcolor, self.background)

        '''
        this section of script only executed when size parameter is passed, by using that
        it can align the text i.e left, right, center.
        '''
        if self.size:
            self.background = self.background or (0, 0, 0)
            # outer box that hold the text
            text_box = pygame.Surface(self.size)
            w, h = text_box.get_size()
            iw, ih = self.img.get_size()
            if self.h_align == 0:
                x = 0
            elif self.h_align == 2:
                x = (w - iw) // 2
            else:
                x = self.h_align

            if self.v_align == 0:
                y = 0
            elif self.v_align == 2:
                y = (h - ih) // 2
            else:
                y = self.v_align

            text_box.fill(self.background)
            text_box.blit(self.img, (x, y))
            self.img = text_box

        self.img.set_alpha(self.alpha)
        self.rect = self.img.get_rect(topleft=self.pos)

    def blit(self, screen: pygame.Surface):
        screen.blit(self.img, self.rect)


class SysFont(Text):
    '''
    :class: used create pygame font object and also content functionality to display
    font on the screen.

    Note: class used system font to display text.
    '''

    def __init__(self, text: str, pos: tuple[int, int], **kw):
        super().__init__(text, pos, **kw)

    def setup(self):
        ''':method: used to set up a system font in the pygame'''
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)


class Label(SysFont, Text):
    '''
    :class: used create label which would be display over the game.

    class had a functionality to use both system font as well as custom font
    by default it used system font.

    if :param size: is passed than the alignment functionality become activate
    see the :class Text: for more details.

    to use custom font
    label = Label(text = "Hello", pos = (0, 0), fontname = font_name,
                 fontsize = 16, sysfont=False)
'''

    def __init__(self, text: str, pos: tuple[int, int], **kw):
        self._sysfont = kw.get("sysfont") or True
        self._intialize(text, pos, **kw)

    def _intialize(self, text, pos, **kw):
        ''':method: used to decide which parent class would take domination.'''

        if self._sysfont:
            super(SysFont, self).__init__(text, pos, **kw)
        else:
            super(Text, self).__init__(text, pos, **kw)


class Button(Label):
    '''
    :class: used create button which would be display over the game.

    class had a functionality to use both system font as well as custom font
    by default it used system font.

    if :param size: is passed than the alignment functionality become activate
    see the :class Text: for more details.

    Note: To get full functionality of the class used the :method blit: to draw
    the widget on the screen.

    to use custom font
    btn = Button(text = "Hello", pos = (0, 0), fontname = font_name,
                 fontsize = 16, sysfont=False)
    '''

    def __init__(self, text: str, pos: tuple[int, int], command: object = None, **kw):
        super().__init__(text, pos, **kw)

        self.command = command
        self.focuscolor = kw.get("focuscolor") or "#57F0DB"
        self.alpha = kw.get("alpha") or 225
        self.active = kw.get("active") or False
        self.focused = kw.get("focused") or False
        self.activecolor = kw.get("activecolor") or "#48FA7B"
        self.img.set_alpha(self.alpha)

        self.focus_surf = pygame.Surface(self.rect.size)
        self.focus_surf.fill(self.focuscolor)
        self.focus_surf.set_alpha(100 * (self.alpha / 225))

        self.active_surf = pygame.Surface(self.rect.size)
        self.active_surf.fill(self.activecolor)
        self.active_surf.set_alpha(200 * (self.alpha / 225))

        self.disable = False

        # adding more function to the base class list
        self.all = (self.all, "on_press", "on_focus", "on_active")

    def on_press(self):
        ''':method: fired when the button clicked'''
        if callable(self.command) and self.pressed:
            self.command()

    def on_focus(self):
        ''':method: fired when the button get focused'''
        if self.focused:
            self.screen.blit(self.focus_surf, self.rect)

    def on_active(self):
        ''':method: fired when the button get activate.'''
        if self.active:
            self.screen.blit(self.active_surf, self.rect)

    def blit(self, screen: pygame.Surface):
        ''':method: used for updating the widget

           Note: used this function to get full control over the button functionality.
        '''
        self.screen = screen
        mouse_pos = pygame.mouse.get_pos()

        # default button
        self.screen.blit(self.img, self.rect)

        # if collide
        self.pressed = False
        self.focused = False
        if self.rect.collidepoint(mouse_pos):
            self.focused = True

            key = pygame.key.get_pressed()
            if (key[pygame.K_RETURN] or pygame.mouse.get_pressed(3)[0]) and not self.disable:
                self.pressed = True

        self.on_focus()
        self.on_active()
        self.on_press()


class BoxLayout:
    '''
    :class: used align widgets on the screen horizontally or vertically.

    Note: used the :method blit: to draw widgets in the screen if you use boxlayout,
    to apply alignments.

    i.e
    label = Label(...)
    boxlayout = BoxLayout(size=WindowSize, orientation="horizontal")
    boxlayout.add(label)
    boxlayout.blit(pygame.Surface)
    '''

    all = ("add", "blit")

    def __init__(self, size: tuple[int, int], **kw):
        self.orientation = kw.get("orientation") or "horizontal"
        self.spacing = kw.get("spacing") or 2
        self.size = size
        self.chlidren = []
        self._size = [0, 0]

    def add(self, *args) -> None:
        ''':method: add widget to the box layout'''
        for child in args:
            self.chlidren.append(child)
            self._size[0] += child.rect.width
            self._size[1] += child.rect.height

    def blit(self, screen: pygame.Surface) -> None:
        ''':method: used to update and draw widget on the screen

            Note: used this function rather than regular blit function.
        '''

        if self.orientation == "horizontal":
            x = (self.size[0] - self._size[0]) // 2

            for index, child in enumerate(self.chlidren):
                if index - 1 < 0:
                    child.rect.x = x
                else:
                    child.rect.x = self.chlidren[index - 1].rect.right + self.spacing

                child.blit(screen)

        if self.orientation == "vertical":
            y = (self.size[1] - self._size[1]) // 2

            for index, child in enumerate(self.chlidren):
                if index - 1 < 0:
                    child.rect.y = y
                else:
                    child.rect.y = self.chlidren[index - 1].rect.bottom + self.spacing
                child.blit(screen)


class TextBox:
    '''
    :class: used align widgets on the screen horizontally or vertically.

    Note: used the :method blit: to draw widgets in the screen if you use textbox,
    to apply alignments.

    i.e
    textbox = TextBox(text="multiline content", pos="position of the textbox")
    textbox.blit(pygame.Surface)
    '''

    all = ("blit")

    def __init__(self, text: str, pos: tuple[int, int], **kw):
        # split the text on the new line.
        self.text = text.split("\n")
        self.line_spacing = kw.get("line_spacing") or 10
        self.textbackground = kw.get("textbackground") or "#383838"
        self.pos = pos
        self.textgroup = []
        self._create_text(**kw)

    def _create_text(self, **kw) -> None:
        ''':method: used to create pygame label and adjust them

        Basically method create multiple label based on the number of lines are in
        the text and place them one after another.
        '''
        x, y = self.pos

        for text in self.text:

            # if there a multiple new line than add some spaces
            # note: newline are converted in '' after split the text.
            if text == '':
                y += self.line_spacing

            else:
                # creating the label one after another
                new_text = Label(text, (x, y), **kw)
                self.textgroup.append(new_text)
                y = new_text.rect.bottom

    def blit(self, screen: pygame.Surface):
        ''':method: update and draw textbox on the screen.

            note: used this method to draw the textbox.
        '''
        screen.fill(self.textbackground)
        for item in self.textgroup:
            item.blit(screen)
