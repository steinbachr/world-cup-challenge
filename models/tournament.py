from models.base import WCModel
from models.team import Team
from populators.teams_populator import TeamsPopulator
from populators.stages_populator import StagesPopulator
import math
import pdb


class Stadium(WCModel):
    fields = ['weather', 'seating_capacity']
    possible_weathers = ['clear', 'cloudy', 'rainy']


class Game(WCModel):
    TIE, WIN = 1, 3
    fields = ['team1', 'team2', 'time', 'stadium']

    def _underdog(self):
        """
        :return: ``Team`` instance which is an underdog in the match

        This code currently just uses FIFA rank as its metric for underdog, and so could be improved by accounting for
        more factors
        """
        return self.team1 if self.team1.fifa_rank < self.team2.fifa_rank else self.team2

    def _expected_weather(self):
        """
        :return: one of 'clear', 'cloudy', or 'rainy' depending on weather at this game's stadium
        """
        return self.stadium.weather

    def _pressure_level(self):
        """
        :return: ``int`` between 1 - 10 (inclusive) which represents how much pressure this game will probably have
        for the teams
        """
        pass

    def _friendly_winner(self):
        """
        :return: ``team1`` if team1 has won more friendlies (from our results.csv file). ``team2`` if they've won more
        friendlies. The points system for calculating 'won' more friendlies is:
        -1 point for a win, so team1 beats team2 is 1 point for team1
        -if team1 beat a team which beat team2, .5 points to team1. So each level of separation decreases the point
        value by half. That is, if team1 beat a team which beat a team which beat team2, then .25  points to team1
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
    fields = ['number', 'is_group', 'games']

    def _get_group_winners(self, teams_to_points={}):
        """
        :param teams_to_points: ``dict`` containing each team's country as keys and the number of points they earned
        in group as the value
        :return: ``list`` of ``Team`` instances to advance from group
        """
        advance_teams = []
        for group in TeamsPopulator.groups:
            winners = 0
            for team, points in sorted(teams_to_points.items(), key=lambda it: it[1]):
                if team.country in group:
                    if winners < 2:
                        advance_teams.append(team)
                        winners += 1
                    else:
                        break

        return advance_teams

    def create_games(self, teams):
        """
        :param teams: ``list`` of ``Team`` instances to create games for
        :return: ``list`` of ``Game`` instances that were dynamically created from ``teams``

        This method is used for stages after group (where the teams aren't known till runtime).
        """
        pass

    def run_games(self):
        """
        :return: ``list`` of teams that should advance to the next stage

        This method simply calculates the winner of a game by taking that games ``winning_probabilities``
        and choosing the winner as the team with the higher winning probability (except for group stage, where more
        work is required).
        """
        def set_team_points(team, points):
            existing_points = teams_to_points.get(team.country, 0)
            teams_to_points[team] = existing_points + points

        advancing_teams = []
        if self.is_group:
            # mapping of teams to how many points they've earned in group stage
            teams_to_points = {}
            for game in self.games:
                # a caveat here is that for group, if the winning probabilities are within 20% of each other
                # (so 40-60 would be the highest variance allowed), we'll assume a tie occurs
                winning_probs = game.winning_probabilities()
                if winning_probs['team1'] > 40 or winning_probs['team2'] > 40:
                    set_team_points(game.team1, Game.TIE)
                    set_team_points(game.team2, Game.TIE)
                elif winning_probs['team1'] > winning_probs['team2']:
                    set_team_points(game.team1, Game.WIN)
                else:
                    set_team_points(game.team2, Game.WIN)
            advancing_teams = self._get_group_winners(teams_to_points=teams_to_points)
        else:
            for game in self.games:
                winning_probs = game.winning_probabilities()
                if winning_probs['team1'] > winning_probs['team2']:
                    advancing_teams.append(game.team1)
                else:
                    advancing_teams.append(game.team2)

        return advancing_teams


class Tournament(WCModel):
    """
    model entry point
    """
    fields = ['teams', 'stages']

    def _populate(self):
        """
        this method populates basic info for tournament elemenents (i.e. for teams, it fills out the teams country)
        """
        self.teams = TeamsPopulator.populate()
        self.stages = StagesPopulator.populate()

    def _simulate(self):
        """
        this method simulates the actual running of the games now that instance data has been created. The way tournament
        data flows is as follows:

        1. Run the games in a stage, this will return a list of teams that should advance to the next stage.
        2. Feed this data to the next stage and repeat
        """
        winning_teams = []
        for stage in self.stages:
            stage.games = stage.create_games(winning_teams) if winning_teams else stage.games
            winning_teams = stage.run_games()

    def run(self):
        self._populate()
        self._simulate()

