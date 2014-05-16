from populators.teams import TeamsPopulator
from populators.players import PlayersPopulator
from models.team import Team
import unittest


class TestPlayersPopulator(unittest.TestCase):

    def setUp(self):
        countries = TeamsPopulator.teams
        self.teams = [Team(country=c) for c in countries]
        self.usa = [t for t in self.teams if t.country == 'USA'][0]

    def test_create_players(self):
        first_team = self.teams[0]
        self.assertIsNone(first_team.players)

        PlayersPopulator.create_players(self.teams)
        self.assertGreater(len(first_team.players), 0)

        dempsey = [p for p in self.usa if p.name.lower() == 'dempsey']
        self.assertGreater(len(dempsey), 0)
        self.assertEqual(dempsey.age, 30)
        self.assertEqual(dempsey.skill_rank, 85)


if __name__ == '__main__':
    unittest.main()