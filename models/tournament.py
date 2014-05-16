from models.base import WCModel
from models.team import Team
from populators.teams import TeamsPopulator
import math
import pdb


class Game(WCModel):
    fields = ['team1', 'team2', 'stage', 'time']

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

    def _is_night_game(self):
        """
        :return: ``True`` if it this is a night game, ``False`` otherwise
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
    @staticmethod
    def _populate_detailed_info():
        """
        This method populates the more detailed info for elements of the tournament (i.e. for teams, it fills in the
        fifa rank for all teams)
        """
        pass

    @staticmethod
    def _populate_basic_info():
        """
        this method populates basic info for tournament elemenents (i.e. for teams, it fills out the teams country)
        """
        stages = [Stage(number=i, teams=[], games=[]) for i in range(1, 6)]

        # populate team information
        countries = TeamsPopulator.teams
        first_stage = stages[0]
        for country in countries:
            first_stage.teams.append(Team(country=country))

        # populate player information
        test = ''
        # populate game information

    @staticmethod
    def run():
        Tournament._populate_basic_info()

