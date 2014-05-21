from models.base import WCModel
import math
import random


class Player(WCModel):
    fields = ['name', 'number', 'age', 'skill_rank', 'is_star', 'is_captain', 'is_injured']

    def _will_be_injured(self):
        """
        :return: ``True`` if this player will be injured over the course of the cup, ``False`` otherwise

        Of course this expects a level of innaccuracy and postulation, but the factors we'll use to determine if this
        player will be injured are:
        * age
        * star rating
        * and whether they're a captain

        If they have is_injured = True, then of course True will be returned
        """
        # this injury threshold is being used as it represents the injury rating of 1/2 of a non-star, 35-year old. So,
        # this means that this player would have a 50% chance at being injured, which sounds reasonable
        INJURY_THRESHOLD = 25
        star_boost = 2 if self.is_star else 1
        years_since_28 = self.age - 28

        age_factor = 1
        if years_since_28 > 0:
            age_factor = math.pow(years_since_28, 2)

        injury_rating = age_factor * star_boost
        will_be_injured = random.randint(0, injury_rating) > INJURY_THRESHOLD

        return self.is_injured or will_be_injured


    def _is_clutch(self):
        pass

    def overall_score(self):
        pass


class Team(WCModel):
    fields = ['group', 'players', 'country', 'fifa_rank', 'fans_score', 'winning_probabilities']

    def _past_performances(self):
        """
        :return: ``list`` of ``Game`` that this team has played in the past
        """
        pass

    def _plays_better_in_bad_weather(self):
        """
        :return: ``True`` if this team plays better in rainy weather relative to their clear day performances.
        (meaning they're win % is as high or higher when playing in bad weather as opposed to clear weather). If
        they play better with good weather, return ``False``
        """
        pass

    def _plays_better_at_night(self):
        """
        :return: ``True`` if this team plays better at night (defined as after 6PM) relative to their day performances.
        (meaning they're win % is as high or higher when playing at night as opposed to during the day). If
        they play better during the day, return ``False``
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