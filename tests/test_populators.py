from populators.teams_populator import TeamsPopulator
from populators.players_populator import PlayersPopulator
from populators.games_populator import GamesPopulator
from populators.stages_populator import StagesPopulator
from models.team import Team
import unittest
import pdb


class TestStagesPopulator(unittest.TestCase):
    def setUp(self):
        pass

    def test_populate(self):
        stages = StagesPopulator.populate()
        self.assertGreater(len(stages), 0)
        self.assertIs(stages[0].is_group, True)
        self.assertIs(stages[1].is_group, False)


class TestPlayersPopulator(unittest.TestCase):
    def setUp(self):
        countries = TeamsPopulator.teams
        self.teams = [Team(country=c) for c in countries]
        self.usa = [t for t in self.teams if t.country == 'USA'][0]

    def test_populate(self):
        first_team = self.teams[0]
        self.assertIsNone(first_team.players)

        PlayersPopulator.populate(self.teams)
        self.assertGreater(len(first_team.players), 0)

        dempsey = [p for p in self.usa if p.name.lower() == 'dempsey']
        self.assertGreater(len(dempsey), 0)
        self.assertEqual(dempsey.age, 30)
        self.assertEqual(dempsey.skill_rank, 85)


class TestGamesPopulator(unittest.TestCase):
    def setUp(self):
        countries = TeamsPopulator.teams
        self.teams = [Team(country=c) for c in countries]
        self.usa = [t for t in self.teams if t.country == 'USA'][0]

    def test_populate(self):
        games = GamesPopulator.populate()
        self.assertGreater(len(games), 0)


if __name__ == '__main__':
    unittest.main()