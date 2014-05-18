from populators.populator_ops import XPathOps
import pdb


class GamesPopulator():
    def __init__(self):
        pass

    @classmethod
    def populate(cls):
        """
        :return: ``dict`` containing keys ``Team`` with values ``list`` of ``Game`` that each team is playing.
        """
        with open("data/games_schedule.html", "r") as games:
            html = games.read()
            ops = XPathOps(html=html,
                           xpath=XPathOps.classlist_contains('fixture'),
                           css_class_root='matches')
            matches = ops.get_nodes_at_xpath()

            team_xpath = './mu-m/{teamx}'.format(teamx=XPathOps.classlist_contains('t'))
            for match in matches:
                teams = ops.get_nodes_at_xpath(from_node=match, xpath=team_xpath)
                pdb.set_trace()
