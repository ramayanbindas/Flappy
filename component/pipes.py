'''
:about: This script hold all the obstical and environmental code
:class Pipe: create the pipe object.
:class ObsticalControler: control the pipes movement.
:class MovingImage: controls the environmental movement.
'''
import pygame
from random import randint

all = ("Pipe", "ObsticalControler", "MovingImage")


class Pipe(pygame.sprite.Sprite):
    ''':class: create the flappy object'''
    all = ("blit")

    def __init__(self, pipe_image: str, pos: tuple[int, int], *args, **kw):
        super().__init__(*args, **kw)
        self.image = pipe_image
        self.rect = self.image.get_rect(topleft=pos)

    def __str__(self):
        return f"{self.__class__}: {self.all}"

    def blit(self, screen: pygame.Surface) -> None:
        ''':method: draw the pipe on the screen'''
        screen.blit(self.image, self.rect)


class ObsticalControler:
    '''
    :class: control the pipe movement as well as check collision with the entity,
    and keep track of score for the game.
    '''
    all = ("generate_pipe", "update", "collision")

    def __init__(self, pipe_image: pygame.Surface):
        self.pipe_image = pipe_image
        self.toppipe = pygame.sprite.Group()
        self.bottompipe = pygame.sprite.Group()

        # variables
        self.pipe_speed = 200
        # gap is used to separate the top and bottom pipe
        self.pipe_gap = 100

        # generate a pipes with random position
        self.generate_pipe()

        self.score = 0
        self.previous_score = self.score
        self.except_pipe = []  # used to calculate the score

    def __str__(self):
        return f"{self.__class__}: {self.all}"

    def generate_pipe(self) -> None:
        ''':method: used to regenerate the pipes'''

        # generating pipes
        # kill all the pipe sprite if present.
        self.toppipe.empty()
        self.bottompipe.empty()

        pipe_pos = [580, 0]
        for pipe in range(3):
            pipe_pos[0] += randint(200, 300)
            pipe_pos[1] = randint(129, 249)  # mid 189
            toppipe = Pipe(pygame.transform.flip(self.pipe_image, False, True), (0, 0))
            toppipe.rect.bottomleft = pipe_pos
            self.toppipe.add(toppipe)
            bottompipe = Pipe(self.pipe_image.copy(), (0, 0))
            bottompipe.rect.topleft = (pipe_pos[0], pipe_pos[1] + self.pipe_gap)
            self.bottompipe.add(bottompipe)

        self.toppipe_list = self.toppipe.sprites()
        self.bottompipe_list = self.bottompipe.sprites()
        self.pervious_pipe = None

    def _custom_pipe_pos(self, toppipe_list: list, bottompipe_list: list) -> None:
        ''':method: internal method assigning a custom position to a pipes.

            :param toppipe_list: list of position of the top pipe list.
            :param bottompip_list: list of position of the bottom pipe list.
        '''
        for pipe in range(len(toppipe_list)):
            self.toppipe_list[pipe].rect.topleft = toppipe_list[pipe]
            self.bottompipe_list[pipe].rect.topleft = bottompipe_list[pipe]

    def update(self, delta_time: float):
        ''':method: used to update the pipe.'''

        for pipe in range(len(self.toppipe_list)):
            self.toppipe_list[pipe].rect.x -= self.pipe_speed * delta_time
            self.bottompipe_list[pipe].rect.x -= self.pipe_speed * delta_time

            if self.toppipe_list[pipe].rect.right < 0:
                '''
                once the pipe is gets bound the screen it gets remove from the list
                for calculating again. This list is mainly used for calculating score.
                '''
                self.except_pipe.remove(self.toppipe_list[pipe])

                '''
                If the pipe is respond in the area greater than the screen width,
                than next pipe would respond in some distance from the previous one.
                '''
                if self.toppipe_list[pipe - 1].rect.right > 640:
                    pipe_pos = (self.toppipe_list[pipe - 1].rect.right + randint(200, 300),
                                randint(129, 249))
                else:
                    '''
                    If the pipe is respond on the screen, than next pipe would respond
                    just outside of the screen.

                    Note: Bottom pipe position are all depend on the top pipe position.
                    '''
                    pipe_pos = (640 + randint(200, 300), randint(200 - self.pipe_gap, 205))

                self.toppipe_list[pipe].rect.bottomleft = pipe_pos
                self.bottompipe_list[pipe].rect.topleft = (pipe_pos[0], pipe_pos[1] + self.pipe_gap)

            '''
            Increase the score each time the entity cross the pipe or pipe cross
            the center of the screen.
            '''
            if self.toppipe_list[pipe].rect.right < 320 and\
               self.toppipe_list[pipe] not in self.except_pipe:
                self.score += 1
                # once the pipe is used to add score it add to except pipe list.
                self.except_pipe.append(self.toppipe_list[pipe])

    def collision(self, entity: pygame.Rect) -> bool:
        ''':method: used to detect collision.

            :return bool: True if the collision occur else False.
        '''

        collision = False

        for pipe in range(len(self.toppipe_list)):
            if self.toppipe_list[pipe].rect.centerx < 640 and\
               self.toppipe_list[pipe].rect.centerx > 0:
                if self.toppipe_list[pipe].rect.colliderect(entity):
                    collision = True
                elif self.bottompipe_list[pipe].rect.colliderect(entity):
                    collision = True

        return collision


class MovingImage:
    ''':class: used to move the images in a desire direction.
    '''
    all = ("move_image", "collision", "blit")

    def __init__(self, image: pygame.Surface, pos: tuple[int, int]):
        '''
        Two images are used for the purpose.
        '''
        self.moving_images = {"img1": (image, image.get_rect(topleft=pos)),
                              "img2": (image.copy(), image.get_rect(topleft=pos))}

    def __str__(self):
        return f"{self.__class__}: {self.all}"

    def move_image(self, screen: pygame.Surface, speed: int, delta_time: float,
                   direction: tuple[int, int] = (0, 0)) -> None:
        ''':method: used for moving image along the direction

            :param direction: tuple(x_dir, y_dir) -> x_dir(-1/1) direction for x direction.
                y_dir(-1/1) -> for y direction
            :param speed: speed of moving
        '''

        # moving image in x direction from left -> right
        if direction[0] > 0:
            if self.moving_images["img1"][1].left > 640:
                self.moving_images = {"img1": self.moving_images["img2"],
                                      "img2": self.moving_images["img1"]}

            self.moving_images["img1"][1].x += speed * delta_time * direction[0]
            self.moving_images["img2"][1].right = self.moving_images["img1"][1].left

        # right -> left
        elif direction[0] < 0:
            if self.moving_images["img1"][1].right < 0:
                self.moving_images = {"img1": self.moving_images["img2"],
                                      "img2": self.moving_images["img1"]}

            self.moving_images["img1"][1].x += speed * delta_time * direction[0]
            self.moving_images["img2"][1].left = self.moving_images["img1"][1].right

        # moving image in y direction from top -> bottom
        elif direction[1] > 0:
            if self.moving_images["img1"][1].top > 480:
                self.moving_images = {"img1": self.moving_images["img2"],
                                      "img2": self.moving_images["img1"]}

            self.moving_images["img1"][1].y += speed * delta_time * direction[1]
            self.moving_images["img2"][1].bottom = self.moving_images["img1"][1].top

        # bottom -> top
        elif direction[1] < 0:
            if self.moving_images["img1"][1].bottom < 0:
                self.moving_images = {"img1": self.moving_images["img2"],
                                      "img2": self.moving_images["img1"]}

            self.moving_images["img1"][1].y += speed * delta_time * direction[1]
            self.moving_images["img2"][1].top = self.moving_images["img1"][1].bottom

    def blit(self, screen: pygame.Surface) -> None:
        ''':method: used to draw images on the screen

            :note: used this method for drawing the moving image.
        '''
        screen.blit(self.moving_images["img1"][0], self.moving_images["img1"][1])
        screen.blit(self.moving_images["img2"][0], self.moving_images["img2"][1])

    def collision(self, entity) -> bool:
        ''':method: used for detecting collision'''

        collision = False

        if self.moving_images["img1"][1].colliderect(entity):
            collision = True
        if self.moving_images["img2"][1].colliderect(entity):
            collision = True

        return collision
