from populators.teams_populator import TeamsPopulator
from populators.players_populator import PlayersPopulator
from populators.tournament_populator import TournamentPopulator
from models.team import Team
from models.tournament import Tournament
import unittest
import pdb


class TestTournamentPopulator(unittest.TestCase):
    def setUp(self):
        self.tournament = Tournament()

    def test_populate(self):
        self.assertGreater(len(self.tournament.teams), 0)


class TestTeamPopulator(unittest.TestCase):
    def setUp(self):
        self.tournament = Tournament()
        self.teams = self.tournament.teams
        self.argentina = Team.get_for_country(self.teams, 'Argentina')
        self.cote = Team.get_for_country(self.teams, "Cote D'Ivoire")

    def test_populate(self):
        self.assertIsNotNone(self.teams)
        self.assertGreater(len(self.teams), 0)
        self.assertIsNotNone(self.argentina.friendly_results)

        # argentina beat mexico, make sure this is apparent
        self.assertIn(Team.get_for_country(self.teams, 'Mexico'), self.argentina.friendly_results['wins'])
        self.assertIn(self.argentina, Team.get_for_country(self.teams, "Mexico").friendly_results['losses'])

        self.assertIsNotNone(self.cote.friendly_results.get('wins', None))
        self.assertIsNotNone(self.cote.friendly_results.get('losses', None))

        # make sure all teams have at least one win and one loss (draws could possibly be missing)
        for team in self.teams:
            self.assertIsNotNone(len(team.friendly_results.get('wins', None)))
            self.assertIsNotNone(len(team.friendly_results.get('losses', None)))


class TestPlayersPopulator(unittest.TestCase):
    def setUp(self):
        self.tournament = Tournament()
        self.teams = self.tournament.teams
        self.argentina = Team.get_for_country(self.teams, 'Argentina')

    def test_populate(self):
        first_team = self.teams[0]
        self.assertIsNotNone(first_team.players)
        self.assertGreater(len(first_team.players), 0)

        messi = [p for p in self.argentina.players if p.name.lower() == 'messi'][0]
        self.assertEqual(messi.age, '26')
        self.assertEqual(messi.skill_rank, 98)


if __name__ == '__main__':
    unittest.main()