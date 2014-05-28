from populators.players_populator import PlayersPopulator
from models.team import Team
import csv
import pdb


class TeamsPopulator():
    """
    For each team that is created, set their independent winning probabilities (winning_probabilities)
    against every other team in the tournament.
    """
    teams = [('Brazil', 'A', 4), ('Croatia', 'A', 20), ('Mexico', 'A', 19), ('Cameroon', 'A', 50),
             ('Spain', 'B', 1), ('Netherlands', 'B', 15), ('Chile', 'B', 13), ('Australia', 'B', 60),
             ('Colombia', 'C', 5), ('Greece', 'C', 10), ('Cote d\'Ivoire', 'C', 21), ('Japan', 'C', 48),
             ('Uruguay', 'D', 6), ('Costa Rica', 'D', 34), ('England', 'D', 11), ('Italy', 'D', 9),
             ('Switzerland', 'E', 8), ('Ecuador', 'E', 28), ('France', 'E', 16), ('Honduras', 'E', 31),
             ('Argentina', 'F', 7), ('Bosnia-Herzegovina', 'F', 27), ('Iran', 'F', 37), ('Nigeria', 'F', 44),
             ('Germany', 'G', 2), ('Portugal', 'G', 3), ('Ghana', 'G', 38), ('United States', 'G', 14),
             ('Belgium', 'H', 12), ('Algeria', 'H', 26), ('Russia', 'H', 18), ('South Korea', 'H', 57)]

    def __init__(self, tournament):
        self.tournament = tournament
        self.tournament.teams = [] if self.tournament.teams is None else self.tournament.teams

    def _set_friendly_results(self):
        """
        populate the friendly_results hash for each team from results.csv
        """
        with open('data/results.csv') as results_csv:
            reader = csv.reader(results_csv)
            for result in reader:
                get_team = lambda index: Team.get_for_country(self.tournament.teams, result[index].strip())
                home_team, away_team = get_team(1), get_team(2)
                home_goals, away_goals = result[3], result[4]

                try:
                    home_team.add_friendly_result(opponent=away_team, result=home_team.result_from_scores(home_goals,
                                                                                                          away_goals))
                except AttributeError:
                    # either the header row or the away / home team isn't in the tourney
                    print "error: not able to parse home team: ", result
                try:
                    away_team.add_friendly_result(opponent=home_team, result=away_team.result_from_scores(away_goals,
                                                                                                          home_goals))
                except AttributeError:
                    # either the header row or the away team isn't in the tourney
                    print "error: not able to parse away team: ", result

    def _set_scores_and_winning_probabilities(self):
        """
        set the base scores for the teams in the tournament and set their winning probabilities against each other
        """
        for team in self.tournament.teams:
            team.set_base_score()
            for other_team in self.tournament.teams:
                # only set winning probablities against team that isn't self
                if team.country != other_team.country:
                    #TODO: implement the winning probability function
                    team.winning_probabilities[other_team.country] = 1

    def populate(self):
        # instantiate each team with basic information
        for country, group, fifa_rank in self.teams:
            self.tournament.teams.append(Team(group=group, country=country, fifa_rank=fifa_rank, friendly_results={},
                                              winning_probabilities={}))

        PlayersPopulator(self.tournament).populate()
        self._set_friendly_results()
        self._set_scores_and_winning_probabilities()

        # can't set the play up ability of a team until we have all the base scores for all teams
        [t.set_plays_up(self.tournament.teams) for t in self.tournament.teams]
