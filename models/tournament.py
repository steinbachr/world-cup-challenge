from models.base import WCModel
from models.team import Team
from models.tree import ProbableTournamentTree
from populators.tournament_populator import TournamentPopulator
from decimal import *
import math
import pdb


class Tournament(WCModel):
    """
    model entry point
    """
    fields = ['teams', 'probable_results_tree']

    def __init__(self):
        WCModel.__init__(self)
        TournamentPopulator(self).populate()
        self.tree = ProbableTournamentTree(self)

    def get_group_winners(self, group):
        """
        :param group: ``str`` the group letter to get winners of
        :return: ``tuple`` of winner and runner-up for the given group

        group stage works a bit different from all other stages, so this method gets the probable winners of the given
        ``group``
        """
        group_teams = Team.get_for_group(self.teams, group)
        probs_to_advance = []

        for team in group_teams:
            prob_to_advance = team.probability_to_advance_from_group()
            probs_to_advance.append((team, prob_to_advance))

        winners = [team for team, prob_to_advance in sorted(probs_to_advance, key=lambda x: x[1], reverse=True)][:2]
        return winners[0], winners[1]

    def run(self):
        """
        For every team in the tournament, calculate the teams probability to be knocked out.
        """
        for team in self.teams:
            stages_probabilities = []

            # probability knocked out in group
            stages_probabilities.append(str(team.knockout_probability_at_stage(0)))
            for stage in range(1, self.tree.MAX_LEVEL + 1):
                stages_probabilities.append(str(team.knockout_probability_at_stage(stage)))
            # probability to win
            stages_probabilities.append(str(team.knockout_probability_at_stage(self.tree.MAX_LEVEL - 1, to_win=True)))

            print "{team}\t{probabilities}\n".format(team=team.country, probabilities="\t".join(stages_probabilities))


