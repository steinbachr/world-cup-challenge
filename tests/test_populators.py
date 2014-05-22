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
        self.tournament_populator = TournamentPopulator(self.tournament)

    def test_populate(self):
        self.tournament_populator.populate()
        self.assertGreater(len(self.tournament.teams), 0)

    def test_get_opponents_group_at_stage(self):
        self.tournament_populator.populate()
        gdt = self.tournament.group_distribution_tree
        self.assertIsNotNone(gdt)

        test_team = Team.get_for_group(self.tournament.teams, 'A')[0]

        self.assertEqual(gdt.get_opponents_group_at_stage(test_team, 0), 'B')
        self.assertEqual(gdt.get_opponents_group_at_stage(test_team, 1), 'CD')
        self.assertEqual(gdt.get_opponents_group_at_stage(test_team, 2), 'EFGH')


class TestPlayersPopulator(unittest.TestCase):
    def setUp(self):
        self.tournament = Tournament()
        TournamentPopulator(self.tournament).populate()
        self.teams = self.tournament.teams
        Team.get_for_country(self.teams, 'USA')

    def test_populate(self):
        first_team = self.teams[0]
        self.assertIsNotNone(first_team.players)
        self.assertGreater(len(first_team.players), 0)

        dempsey = [p for p in self.usa if p.name.lower() == 'dempsey']
        self.assertGreater(len(dempsey), 0)
        self.assertEqual(dempsey.age, 30)
        self.assertEqual(dempsey.skill_rank, 85)


if __name__ == '__main__':
    unittest.main()