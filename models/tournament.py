from models.base import WCModel
import math


class Game(WCModel):
    fields = ['team1', 'team2', 'stage']

    def _better_fans(self):
        """
        :return: the Team instance which has better fans
        """
        pass

    def _expected_weather(self):
        """
        :return: one of 'clear', 'cloudy', or 'rainy' depending on
        """
        pass

    def _pressure_level(self):
        """
        :return: ``int`` between 1 - 10 (inclusive) which represents how much pressure this game will probably have
        for the teams
        """
        pass

    def winning_probabilities(self):
        """
        :return: ``dict`` containing keys ``team1`` and ``team2`` which holds the calculated probability of team1 winning
        and team2 winning the game.
        """
        pass


class Stage(WCModel):
    fields = ['number', 'teams', 'games']

    def num_slots(self):
        """
        :return: ``int`` the number of available slots in this stage
        """
        exponent = 5 - self.number # 5 is the number of stages in the tourney
        return math.pow(2, exponent)


class Tournament(WCModel):
    """
    model entry point
    """
    fields = ['stages']