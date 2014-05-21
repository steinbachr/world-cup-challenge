class TournamentPopulator():
    """
    The steps for populating a tournament are as follows:
    1. For each team, set their independent winning probabilities (winning_probabilities) against every other team in
    the tournament.
    2. Create a tree detailing the probable winners at each stage in the tournament
    """
    def __init__(self, tournament):
        self.tournament = tournament

    def populate(self):
        for team in self.tournament.teams:
            for other_team in self.tournament.teams:
                # only set winning probablities against team that isn't self
                if team.country != other_team.country:
                    #TODO: implement the winning probability function
                    team.winning_probabilities[other_team.country] = 1