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

    def _past_performances(self):
        """
        :return: ``list`` of ``Game`` that this team has played in the past
        """
        pass

    def _plays_well_in_bad_weather(self):
        """
        :return:
        """
        pass

    def _plays_well_at_night(self):
        """
        :return: ``int`` > 0 the scoring value for being a team that plays well at night (defined as after 6PM)
        relative to their day performance. (meaning they're win % is as high or higher when playing at night as
        opposed to during the day). If they play better during the day, return 0
        """
        pass

    def _team_skill_score(self):
        """
        :return: ``int`` the sum total of the skill levels of the team players divided by the scoring value for team
        skills
        """
        pass

    def _chemistry_score(self):
        """
        :return: ``int`` > 0 the chemistry scoring value for this team, or 0 if the team has bad chemistry.
        Determining whether the team has good chemistry follows this algorithm:

        1. Get the ``_team_skill_score`` for this team.
        2. Find the overall win % of the team.
        3. Compare the win % to the _team_skill_score. If this team has a high win % relative to its skill score, then
        it has good chemistry. If not, then it has bad chemistry.

        We are doing this qualitively rather than quantitively because it is immensely difficult to quantify a chemistry
        value.
        """
        pass

    def _fans_score(self):
        """
        :return: ``int`` > 0 the the fans scoring value for this team, or 0 if the team has bad fans.
        Determining whether the team has good fans follows this algorithm:

        1. Get past results for this team
        2. Find % of wins which came at home
        3. Check if this % is high
        """
        pass

    def _plays_up(self):
        pass

    def overall_score(self):
        pass

    def probability_to_advance(self, stage):
        """
        :param stage: ``Stage`` instance
        :return: ``float`` the probability for this team to advance past the given ``stage``
        """
        if stage.is_group:
            pass
        else:
            pass

    @classmethod
    def get_for_country(cls, teams, country):
        """
        :param teams: ``list`` of ``Team`` instances
        :param country: ``str`` the name of a country
        :return: ``Team`` instance representing the given ``country``
        """
        for team in teams:
            if team.country.lower() == country.lower():
                return team

        return None