'''
:about: The script file content Flappy entity for the game.
:class Flappy: control the flappy entity.
'''
import pygame
from arcade import ease_value, ease_update, ease_out_sin

all = ("Flappy")


class Flappy(pygame.sprite.Sprite):
    '''
    :class: used to draw and control the flappy bird.
    '''
    all = ("blit", "update", "apply_gravity")

    def __init__(self, flappy_images: list, weight: int, fly_speed: int,
                 pos: tuple[int, int], **kw):
        super().__init__(**kw)
        # initializing flappy
        self.flappy_images = flappy_images
        self.image = self.flappy_images[0]
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = self.rect.inflate((-6, -4))

        # variables
        self.anim = 0  # used for animation
        self.anim_speed = 100
        # more weight the flappy is less its speed.
        self.weight = weight
        self.fly_speed = fly_speed
        self.speed = self.fly_speed / self.weight

        # after the flappy reached the certain height, flappy would fly again.
        self.btn_disable = False

        # timer for the flappy to active the button again.
        self.btn_pressed_delay_timer = 0

        # direction of the flappy `1` for UP and `-1` for down
        self.flappy_dir = pygame.math.Vector2(0, -1)
        self.flappy_rotate = 30
        self.flappy_rotatation_speed = 200
        # maximum height that flappy would allowed to fly
        self.max_flight_height = 80

        # tracking the easing data
        self.ease_y_data = None
        # appliying easing in the rotation of flappy
        self.rotate_time = 0.2
        self.ease_rotate_data = ease_value(30, -30, time=self.rotate_time,
                                           ease_function=ease_out_sin)

        self.esitmate_flight_height = 0
        # constant gravity for the flappy.
        self.gravity = 200

        self.lives = 3

    def __str__(self):
        return f"{self.__class__}: {self.all}"

    def blit(self, screen: pygame.Surface) -> None:
        ''':method: used to draw the flappy on to the surface.'''
        screen.blit(self.image, self.rect)

    def update(self, delta_time: float, **kw) -> None:
        ''':method: used to update the flappy'''
        self.apply_gravity(delta_time)
        done = False

        if kw["K_SPACE"] and not self.btn_disable:
            self.btn_disable = True
            self.esitmate_flight_height = self.rect.centery - self.max_flight_height
            self.ease_y_data = ease_value(self.rect.centery,
                                          self.esitmate_flight_height,
                                          time=0.3,
                                          ease_function=ease_out_sin)

        # flappy can fly with it flying speed, and also it change it direction and rotation
        if self.ease_y_data:
            done, self.rect.centery = ease_update(self.ease_y_data, delta_time)
            # self.rect.centery -= self.speed * delta_time
            self.flappy_dir.y = 1
            self.flappy_rotate = 30
            self.ease_rotate_data = None

        # flappy reach its limits of flying, and ready for new flight or back to ground
        if done:
            self.flappy_dir.y = -1
            self.ease_rotate_data = ease_value(30, -30, time=self.rotate_time,
                                               ease_function=ease_out_sin)
            self.btn_pressed_delay_timer = self.esitmate_flight_height + 5
            self.ease_y_data = None

        # flappy take some anticipation to fly again
        if self.btn_pressed_delay_timer and self.rect.centery > self.btn_pressed_delay_timer:
            self.btn_disable = False
            self.btn_pressed_delay_timer = 0

        if self.ease_rotate_data:
            self.flappy_rotate = ease_update(self.ease_rotate_data, delta_time)[1]

        self.apply_animation(delta_time)  # applying animation

        # finally flappy image gets updated along with rotation to it.
        self.image = pygame.transform.rotate(self.flappy_images[int(self.anim)],
                                             self.flappy_rotate)
        self.rect = self.image.get_rect(center=self.rect.center)

        # update the collision react
        self.collision_rect.center = self.rect.center

    def apply_gravity(self, delta_time: float) -> None:
        ''':method: used to apply gravity on the flappy'''
        self.rect.centery += self.gravity * delta_time

    def apply_animation(self, delta_time: float):
        ''':method: controls the animation of the flappy.'''

        if self.ease_y_data:
            self.anim = (len(self.flappy_images) - 1)* (self.rect.centery/ self.esitmate_flight_height)
        else:
            self.anim += self.anim_speed * delta_time

        self.anim = self.anim % (len(self.flappy_images) - 1)
