from models.team import Team
from models.tournament import Tournament
import unittest


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.tournament = Tournament()
        self.teams = self.tournament.teams

    def test_add_friendly_result(self):
        usa = Team.get_for_country(self.teams, 'United States')
        brazil = Team.get_for_country(self.teams, 'Brazil')

        usa.add_friendly_result(opponent=brazil)
        usa.add_friendly_result(opponent=brazil, result=Team.DRAW)
        usa.add_friendly_result(opponent=brazil, result=Team.LOSS)

        self.assertIn(brazil, usa.friendly_results['wins'])
        self.assertIn(brazil, usa.friendly_results['draws'])
        self.assertIn(brazil, usa.friendly_results['losses'])

        # try adding a friendly result for a team not in the tourney
        prev_draws = len(usa.friendly_results['draws'])
        usa.add_friendly_result(opponent=Team.get_for_country(self.teams, "Israel"), result=Team.DRAW)
        self.assertEqual(prev_draws + 1, len(usa.friendly_results['draws']))

    def test_get_for_country(self):
        self.assertEqual(Team.get_for_country(self.teams, 'Brazil').country, 'Brazil')

    def test_get_for_group(self):
        self.assertIn(Team.get_for_country(self.teams, 'Brazil'), Team.get_for_group(self.teams, 'A'))
        self.assertNotIn(Team.get_for_country(self.teams, 'Brazil'), Team.get_for_group(self.teams, 'B'))

    def test_get_best_team(self):
        self.assertEqual(Team.get_best_team(Team.get_for_group(self.teams, 'A')).country, 'Brazil')


if __name__ == '__main__':
    unittest.main()