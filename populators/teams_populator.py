from populators.players_populator import PlayersPopulator
from models.team import Team


class TeamsPopulator():
    """
    For each team that is created, set their independent winning probabilities (winning_probabilities)
    against every other team in the tournament.
    """
    teams = [('Brazil', 'A'), ('Croatia', 'A'), ('Mexico', 'A'), ('Cameroon', 'A'),
             ('Spain', 'B'), ('Netherlands', 'B'), ('Chile', 'B'), ('Australia', 'B'),
             ('Colombia', 'C'), ('Greece', 'C'), ('Cote d\'Ivoire', 'C'), ('Japan', 'C'),
             ('Uruguay', 'D'), ('Costa Rica', 'D'), ('England', 'D'), ('Italy', 'D'),
             ('Switzerland', 'E'), ('Ecuador', 'E'), ('France', 'E'), ('Honduras', 'E'),
             ('Argentina', 'F'), ('Bosnia-Herzegovina', 'F'), ('Iran', 'F'), ('Nigeria', 'F'),
             ('Germany', 'G'), ('Portugal', 'G'), ('Ghana', 'G'), ('United States', 'G'),
             ('Belgium', 'H'), ('Algeria', 'H'), ('Russia', 'H'), ('South Korea', 'H')]

    def __init__(self, tournament):
        self.tournament = tournament
        self.tournament.teams = [] if self.tournament.teams is None else self.tournament.teams

    def _get_fifa_rank(self, team):
        pass

    def populate(self):
        for country, group in self.teams:
            self.tournament.teams.append(Team(group=group, country=country))

        PlayersPopulator(self.tournament).populate()

        for team in self.tournament.teams:
            team.winning_probabilities = {}
            for other_team in self.tournament.teams:
                # only set winning probablities against team that isn't self
                if team.country != other_team.country:
                    #TODO: implement the winning probability function
                    team.winning_probabilities[other_team.country] = 1