from raspisnake.Color import ORANGE
from raspisnake.treats.Treat import Treat


class Orange(Treat):

    def __init__(self, position, start_turn):
        super(Orange, self).__init__(ORANGE, position, start_turn, 30)

    def on_contact(self, snake):
        snake.set_reverty(True)

    def get_points(self):
        return 3
