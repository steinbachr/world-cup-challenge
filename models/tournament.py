from models.base import WCModel
from models.team import Team
from populators.teams_populator import TeamsPopulator
from populators.tournament_populator import TournamentPopulator
import math
import pdb


class Tournament(WCModel):
    """
    model entry point
    """
    fields = ['teams', 'group_distribution_tree']

    def __init__(self):
        WCModel.__init__(self)
        TournamentPopulator(self).populate()

    def run(self):
        pass

