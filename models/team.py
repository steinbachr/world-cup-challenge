from models.base import WCModel
import math
import random
import csv
import pdb


class Player(WCModel):
    fields = ['name', 'age', 'skill_rank', 'is_star', 'is_injured']

    def _will_be_injured(self):
        """
        :return: ``True`` if this player will be injured over the course of the cup, ``False`` otherwise

        Of course this expects a level of innaccuracy and postulation, but the factors we'll use to determine if this
        player will be injured are:
        * age
        * star rating
        * and whether they're a captain
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

    def overall_score(self):
        pass


class Team(WCModel):
    WIN, LOSS, DRAW = "win", "loss", "draw"
    fields = ['group', 'players', 'country', 'fifa_rank', 'friendly_results', 'base_score', 'winning_probabilities',
              'plays_up']
    # keys are the alternate spelling value is our spelling
    alternate_spellings = {
        'bosnia and herzegovina': 'Bosnia-Herzegovina',
        "c\xc3\x94te d'ivoire": "Cote D'Ivoire"
    }

    def _number_of_stars(self):
        """
        :return: ``int`` the number of star players on this team
        """
        return len([p for p in self.players if p.is_star])

    def _team_skill_score(self):
        """
        :return: ``int`` the average skill score of the players on the team
        """
        try:
            return reduce(lambda x, y: x + y.skill_rank, self.players, 0) / len(self.players)
        except ZeroDivisionError:
            print "team {t} doesn't have any players".format(t=self.country)
            return 0

    def _chemistry_score(self):
        """
        :return: ``float`` the calculated chemistry score for this ``Team``

        Chemistry score is calculated with the following formula:
            100 * (x / y) where:
            x = the # of friendly wins for this ``Team``
            y = the _team_skill_score for this ``Team``

        This means that a team with many wins but having a low skill score is a team with high chemistry while a team
        with a low number of wins but high team skill score is a team with low chemistry.
        """
        return 100 * (len(self.friendly_results.get('wins', [])) / self._team_skill_score())

    def set_plays_up(self, teams):
        """
        :param teams: ``list`` of ``Team`` instances, the other teams in the WC

        set the plays_up attribute for this ``Team`` using the following algorithm:
        1. Get the number of friendly wins/draws against teams with a higher base score as B
        2. Perform (1) on all teams
        3. This team "plays up" if B is in the 75th percentile of results
        """
        def num_better_teams_beaten_or_tied(team):
            # we must check for opp is None because the friendly_results contain None entries for teams not making the WC
            better_teams = lambda opponents: [opp for opp in opponents if opp is not None and opp.base_score > team.base_score]
            return len(better_teams(team.friendly_results.get('wins', []))) + \
                   len(better_teams(team.friendly_results.get('draws', [])))

        self_play_up_results = num_better_teams_beaten_or_tied(self)
        others_play_up_results = sorted([num_better_teams_beaten_or_tied(t) for t in teams])
        return self_play_up_results > others_play_up_results[int(len(others_play_up_results) * .75)]

    def set_base_score(self):
        """
        the base score is the score for this ``Team`` completely independent of who they are playing. The formula
        for determining base score is:
        (x + 2y + z^2) - f where:
        x = player skill score
        y = chemistry score
        z = the number of stars on the team
        f = the fifa rank of this team
        """
        self.base_score = (self._team_skill_score() + (2 * self._chemistry_score()) +
                           math.pow(self._number_of_stars(), 2)) - self.fifa_rank

    def result_from_scores(self, self_score, opponent_score):
        """
        :param self_score: ``int`` the score of this ``Team`` in a game
        :param opponent_score: ``int`` the score of this ``Team``'s opponent in a game
        :return: ``str`` one of ``WIN``, ``LOSS``, or ``DRAW`` depending on whether self_score is >, <, or = to opponent
        """
        if self_score > opponent_score:
            return self.WIN
        elif self_score < opponent_score:
            return self.LOSS
        else:
            return self.DRAW

    def add_friendly_result(self, opponent=None, result=WIN):
        """
        :param opponent: ``Team`` instance that this ``Team`` played, or None if the opponent isn't part of the WC
        :param ``result``: ``str`` the result of the friendly

        add a friendly result to self.friendly_results, which is a ``dict`` containing keys ``wins``, ``draws``, and
        ``losses``. The values are an array of ``Team`` instances which represent those teams either beat, drawn, or
        lost to, respectively.
        """
        if result == self.WIN:
            key = 'wins'
        elif result == self.LOSS:
            key = 'losses'
        else:
            key = 'draws'

        try:
            self.friendly_results.get(key, None).append(opponent)
        except AttributeError:
            self.friendly_results[key] = [opponent]

    @classmethod
    def get_for_country(cls, teams, country):
        """
        :param teams: ``list`` of ``Team`` instances
        :param country: ``str`` the name of a country
        :return: ``Team`` instance representing the given ``country``
        """
        country_lowered = country.lower()
        for team in teams:
            if team.country.lower() == country_lowered:
                return team

        # unicode handling / alternate spelling handling
        if country_lowered in cls.alternate_spellings.keys():
            return cls.get_for_country(teams, cls.alternate_spellings[country_lowered])

        return None

    @classmethod
    def get_for_group(cls, teams, group):
        """
        :param teams: ``list`` of ``Team`` instances
        :param group: ``str`` the group letter to get team instances belonging to
        :return: ``list`` of team instances belonging to the given group
        """
        matching_group = []
        for team in teams:
            if team.group == group:
                matching_group.append(team)

        return matching_group

    @classmethod
    def get_best_team(cls, teams):
        """
        :param teams: ``list`` of ``Team`` instances to choose the best team from
        :return: ``Team`` team instance with the highest probability to beat other teams in ``teams``
        """
        best_team = None
        winning_prob_high = 0
        for team in teams:
            winning_prob_total = 0
            for competitor in teams:
                if competitor.country != team.country:
                    winning_prob_total += team.winning_probabilities[competitor.country]

            if winning_prob_total > winning_prob_high:
                best_team = team
                winning_prob_high = winning_prob_total

        return best_team

