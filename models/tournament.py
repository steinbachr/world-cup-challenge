from models.base import WCModel
from models.team import Team
from models.tree import ProbableTournamentTree
from populators.tournament_populator import TournamentPopulator
import math
import pdb


class Tournament(WCModel):
    """
    model entry point
    """
    fields = ['teams', 'probable_results_tree']

    def __init__(self):
        WCModel.__init__(self)
        self.tree = ProbableTournamentTree(self)
        TournamentPopulator(self).populate()

    def get_group_winners(self, group):
        """
        :param group: ``str`` the group letter to get winners of
        :return: ``tuple`` of winner and runner-up for the given group

        group stage works a bit different from all other stages, so this method gets the probable winners of the given
        ``group``
        """
        group_teams = Team.get_for_group(self.teams, group)
        group_wins = {}

        for team in group_teams:
            group_wins[team.country] = 0
            for opponent in group_teams:
                if opponent.country != team.country:
                    # if the team is likely to beat their opponent, increment the teams win counter
                    if team.winning_probabilities[opponent.country] > .5:
                        group_wins[team.country] += 1

        # TODO: better sorting function which uses base team score as a tie breaker
        winners = [Team.get_for_country(self.teams, c) for c, num_wins in
                   sorted(group_wins.items(), key=lambda x: x[1], reverse=True)][:2]
        return winners[0], winners[1]

    def run(self):
        pass

