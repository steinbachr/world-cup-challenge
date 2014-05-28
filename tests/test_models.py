from models.team import Team
from models.tournament import Tournament
import unittest


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.tournament = Tournament()
        self.teams = self.tournament.teams
        self.usa = Team.get_for_country(self.teams, 'United States')
        self.brazil = Team.get_for_country(self.teams, 'Brazil')

    def test_add_friendly_result(self):
        self.usa.add_friendly_result(opponent=self.brazil)
        self.usa.add_friendly_result(opponent=self.brazil, result=Team.DRAW)
        self.usa.add_friendly_result(opponent=self.brazil, result=Team.LOSS)

        self.assertIn(self.brazil, self.usa.friendly_results['wins'])
        self.assertIn(self.brazil, self.usa.friendly_results['draws'])
        self.assertIn(self.brazil, self.usa.friendly_results['losses'])

        # try adding a friendly result for a team not in the tourney
        prev_draws = len(self.usa.friendly_results['draws'])
        self.usa.add_friendly_result(opponent=Team.get_for_country(self.teams, "Israel"), result=Team.DRAW)
        self.assertEqual(prev_draws + 1, len(self.usa.friendly_results['draws']))

    def test_base_score(self):
        # these tests operate using some basic, commonly held assumptions (which could actually be a source of human error)
        self.assertGreater(self.brazil.base_score, self.usa.base_score)
        self.assertGreater(self.usa.base_score, Team.get_for_country(self.teams, "Ghana").base_score)

    def test_get_for_country(self):
        self.assertEqual(Team.get_for_country(self.teams, 'Brazil').country, 'Brazil')

    def test_get_for_group(self):
        self.assertIn(Team.get_for_country(self.teams, 'Brazil'), Team.get_for_group(self.teams, 'A'))
        self.assertNotIn(Team.get_for_country(self.teams, 'Brazil'), Team.get_for_group(self.teams, 'B'))

    def test_get_best_team(self):
        self.assertEqual(Team.get_best_team(Team.get_for_group(self.teams, 'A')).country, 'Brazil')



if __name__ == '__main__':
    unittest.main()