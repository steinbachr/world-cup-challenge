from models.base import WCModel


class Player(WCModel):
    fields = ['name', 'number', 'age', 'number_yellows', 'number_reds', 'skill_rank', 'is_star', 'is_captain',
              'is_injured']

    def _is_injury_prone(self):
        pass

    def _is_clutch(self):
        pass

    def overall_score(self):
        pass


class Team(WCModel):
    fields = ['players', 'country', 'fifa_rank', 'fans_score']

    def _plays_well_in_bad_weather(self):
        pass

    def _plays_well_at_night(self):
        pass

    def _team_skill_score(self):
        pass

    def _chemistry_score(self):
        pass

    def _fans_score(self):
        pass

    def _is_underdog(self):
        pass

    def _plays_up(self):
        pass

    def overall_score(self):
        pass

    def probability_to_win_game(self, game):
        """
        :param game: a ``Game`` instance.
        :return: ``float`` between 0 - 1(exclusive) describing the probablity that this team will win ``game``
        """
        pass

    def probability_to_advance(self, stage):
        pass

    @classmethod
    def get_for_country(cls, teams, country):
        """
        :param teams: ``list`` of ``Team`` instances
        :param country: ``str`` the name of a country
        :return: ``Team`` instance representing the given ``country``
        """
        for team in teams:
            if team.country == country:
                return team

        return None