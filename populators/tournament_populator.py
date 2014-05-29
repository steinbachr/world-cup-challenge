from populators.teams_populator import TeamsPopulator
import pdb


class TournamentPopulator():
    def __init__(self, tournament):
        self.tournament = tournament

    def populate(self):
        TeamsPopulator(self.tournament).populate()