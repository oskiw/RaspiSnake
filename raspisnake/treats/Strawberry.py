from raspisnake.Color import RED
from raspisnake.treats.Treat import Treat


class Strawberry(Treat):

    def __init__(self, position, start_turn):
        super(Strawberry, self).__init__(RED, position, start_turn, 20)

    def on_contact(self, snake):
        snake.crash = True

    def get_points(self):
        return 0
