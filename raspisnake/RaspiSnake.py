import pygame
from pygame.locals import *
from sense_hat import SenseHat
from random import randint
from time import sleep

from raspisnake.Color import *
from raspisnake.Position import Position
from raspisnake.treats.TreatFactory import TreatFactory

DEFAULT_SPEED = 0.5


class RaspiSnake(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((640, 480))
        self._sense = SenseHat()
        self._speed = DEFAULT_SPEED
        self._sense.clear()
        starting_position = Position(3, 3)
        self._snake = [starting_position]
        self.set_snake_pixel(starting_position)
        self._crash = False
        self.reset_revert()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

    @property
    def crash(self):
        return self._crash

    @crash.setter
    def crash(self, crash):
        self._crash = crash

    @property
    def revertx(self):
        return self._revertx

    @revertx.setter
    def revertx(self, val):
        self._revertx = val

    @property
    def reverty(self):
        return self._revertx

    @reverty.setter
    def reverty(self, val):
        self._reverty = val

    def reset_revert(self):
        self._revertx = False
        self._reverty = False

    def set_snake_pixel(self, position):
        self.set_pixel(position, WHITE)

    def unset_snake_pixel(self, position):
        self.set_pixel(position, BLACK)

    def set_pixel(self, position, color):
        self._sense.set_pixel(position.x, position.y, color.r, color.g, color.b)

    def run(self):

        paused = False
        running = True
        last_direction = None
        points = 0
        turn = 0
        treat = self.generate_treat(turn)

        while running:
            for event in pygame.event.get():
                print(event)

                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if paused:
                            paused = False
                        else:
                            paused = True

                    if not paused:
                        if event.key in [K_DOWN, K_UP, K_RIGHT, K_LEFT]:
                            key = event.key
                            if self.reverty:
                                if key == K_DOWN:
                                    key = K_UP
                                elif key == K_UP:
                                    key = K_DOWN
                            if self.revertx:
                                if key == K_LEFT:
                                    key = K_RIGHT
                                elif key == K_RIGHT:
                                    key = K_LEFT
                            if len(self._snake) == 1 or self.get_next_position(key) != self._snake[-2]:
                                last_direction = key

                if event.type == QUIT:
                    running = False
                    self.stop(points)

            if not paused:
                if last_direction is not None:
                    turn += 1
                    next_position = self.get_next_position(last_direction)
                    if next_position == treat.position:
                        points += treat.get_points()
                        self.speed = DEFAULT_SPEED
                        self.reset_revert()
                        treat.on_contact(self)
                        treat = self.generate_treat(turn)
                    else:
                        self.remove_tail()

                    if treat.has_expired(turn):
                        self.unset_snake_pixel(treat.position)
                        treat = self.generate_treat(turn)

                    if not self._crash:
                        self._crash = self.has_crashed(next_position)

                    if not self._crash:
                        self.add_head(next_position)

            if self._crash:
                running = False
                self.stop(points)

            sleep(self._speed)

    def stop(self, points):
        self._sense.clear()
        self._sense.show_message(str(points) + "pts", scroll_speed=0.15, text_colour=WHITE.to_list(),
                                 back_colour=BLACK.to_list())
        sleep(1)
        self._sense.clear()
        print("Bye - you got " + str(points) + " points")

    def get_next_position(self, last_direction):
        last_position = self._snake[-1]

        if last_direction == K_DOWN:
            return Position(last_position.x, (last_position.y + 1) % 8)
        if last_direction == K_UP:
            return Position(last_position.x, (last_position.y - 1) % 8)
        if last_direction == K_RIGHT:
            return Position((last_position.x + 1) % 8, last_position.y)
        if last_direction == K_LEFT:
            return Position((last_position.x - 1) % 8, last_position.y)

        return None

    def has_crashed(self, position):
        for p in self._snake:
            if p == position:
                return True
        return False

    def remove_tail(self):
        self.unset_snake_pixel(self._snake[0])
        self._snake.pop(0)

    def add_head(self, head):
        self.set_snake_pixel(head)
        self._snake.append(head)

    def generate_treat(self, turn):
        empty_position = []
        for x in range(8):
            for y in range(8):
                p = Position(x, y)
                if not self.has_crashed(p):
                    empty_position.append(p)

        position = empty_position[randint(0, len(empty_position) - 1)]
        treat = TreatFactory.get_treat(position, turn)
        self.set_pixel(position, treat.color)
        return treat


if __name__ == "__main__":
    snake = RaspiSnake()
    snake.run()


