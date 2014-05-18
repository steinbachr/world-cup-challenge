from populators.populator_ops import XPathOps
from models.team import Player, Team
import requests
import pdb


class PlayersPopulator():
    url = 'http://pesdb.net/pes2014/index.php'

    def __init__(self):
        pass

    @classmethod
    def populate(cls, teams):
        """
        :param teams: ``list`` of ``Team`` instances to create player information for
        :return: ``list`` the ``teams`` with player information added
        """
        pages = 3
        #pages = 212
        for page in range(1, pages):
            ops = XPathOps(url='{base}?sort=overall_rating&order=d&page={page}'.format(base=cls.url, page=page),
                           xpath='//tr',
                           css_class_root='players')
            table_rows = ops.get_nodes_at_xpath()

            name_i, country_i, age_i, skill_i = 1, 3, 6, 7
            for row in table_rows:
                name = ops.get_val_from_node(row[name_i])
                country = ops.get_val_from_node(row[country_i])
                age = ops.get_val_from_node(row[age_i])
                skill_rank = ops.get_val_from_node(row[skill_i])

                team = Team.get_for_country(teams, country)
                if team:
                    new_player = Player(name=name, age=age, skill_rank=skill_rank)
                    team.players = team.players + [new_player] if team.players is not None else [new_player]
        return teams

