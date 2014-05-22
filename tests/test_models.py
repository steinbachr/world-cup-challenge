from models.team import Team
from models.tournament import Tournament
import unittest


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.tournament = Tournament()
        self.teams = self.tournament.teams

    def test_get_for_country(self):
        self.assertEqual(Team.get_for_country(self.teams, 'Brazil').country, 'Brazil')

    def test_get_for_group(self):
        self.assertIn(Team.get_for_country(self.teams, 'Brazil'), Team.get_for_group(self.teams, 'A'))
        self.assertNotIn(Team.get_for_country(self.teams, 'Brazil'), Team.get_for_group(self.teams, 'B'))

    def test_get_best_team(self):
        self.assertEqual(Team.get_best_team(Team.get_for_group(self.teams, 'A')).country, 'Brazil')


if __name__ == '__main__':
    unittest.main()