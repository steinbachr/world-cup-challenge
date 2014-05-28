from populators.populator_ops import XPathOps
from models.team import Player, Team
import csv
import pdb
import os


class PlayersPopulator():
    url = 'http://pesdb.net/pes2014/index.php'
    csv_path = 'data/players.csv'

    def __init__(self, tournament):
        self.tournament = tournament

    def _create_csv_from_webpage(self):
        """
        create a csv file containing all the player data from the page at self.url
        """
        pages = 212
        with open(self.csv_path, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # for each page of results, fetch the nodes from the page to use, then iterate over those nodes and write
            # the values to csv
            for page in range(1, pages):
                print "Page ", page
                ops = XPathOps(url='{base}?sort=overall_rating&order=d&page={page}'.format(base=self.url, page=page),
                               xpath='//tr',
                               css_class_root='players')
                table_rows = ops.get_nodes_at_xpath()

                name_i, country_i, age_i, skill_i = 1, 3, 6, 7
                for row in table_rows:
                    name = ops.get_val_from_node(row[name_i])
                    country = ops.get_val_from_node(row[country_i])
                    age = ops.get_val_from_node(row[age_i])
                    skill_rank = ops.get_val_from_node(row[skill_i])

                    # write unless this is a header row
                    if name != 'Player Name':
                        writer.writerow([name.encode('utf8'), country.encode('utf8'), age, skill_rank])

    def _players_csv_exists(self):
        """
        :return: ``True`` if the players.csv file exists, ``False`` otherwise
        """
        return os.path.isfile(self.csv_path)

    def populate(self):
        """
        :return: ``list`` the ``teams`` with player information added
        """
        if not self._players_csv_exists():
            self._create_csv_from_webpage()

        teams = self.tournament.teams
        with open(self.csv_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for i, row in enumerate(reader):
                team = Team.get_for_country(teams, row[1])
                if team:
                    # since the players are sorted by skill level, we say the best 50 players are stars
                    new_player = Player(name=row[0], age=row[2], skill_rank=int(row[3]), is_star=i < 50)
                    team.players = team.players + [new_player] if team.players is not None else [new_player]

        return teams

