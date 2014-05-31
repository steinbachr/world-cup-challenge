from models.base import WCModel
from decimal import *
import math
import random
import csv
import pdb


class Player(WCModel):
    fields = ['name', 'age', 'skill_rank', 'is_star', 'is_injured']


class Team(WCModel):
    WIN, LOSS, DRAW = "win", "loss", "draw"
    fields = ['tournament', 'group', 'players', 'country', 'fifa_rank', 'friendly_results', 'base_score', 'matchup_scores',
              'winning_probabilities', 'plays_up']
    # key is the alternate spelling, value is our spelling
    alternate_spellings = {
        'bosnia and herzegovina': 'Bosnia-Herzegovina',
        "c\xc3\x94te d'ivoire": "Cote D'Ivoire",
        "c\xc3\xb4te divoire": "Cote D'Ivoire",
        "korea republic": "South Korea"
    }

    def __init__(self, **kwargs):
        WCModel.__init__(self, **kwargs)
        # set the precision for decimal calculations
        getcontext().prec = 4

    def __repr__(self):
        return self.country

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
        return (100 * len(self.friendly_results.get('wins', []))) / self._team_skill_score()

    def _past_results_score(self, opponent):
        """
        :param opponent: ``Team`` instance to calculate a past results score against
        :return: ``int`` the calculated past results score of this team against ``team``

        The past results score takes into account both direct wins (i.e. TeamX beat TeamY) as well as second degree wins
        (i.e. TeamX beat TeamY who beat TeamZ, so TeamX has a second degree win over TeamZ). The overally past results
        score is formalized by:
        1) Get the number of direct wins of this ``Team`` over ``opponent``. Store as Wa = 10n where n is the # direct wins.
        2) Get the number of second degree wins of this ``Team`` over ``opponent``. Store as Wb = 2n where n is the # of
        second degree wins.
        3) The past results score for this ``Team`` against ``opponent`` is Wa + Wb.
        """
        winners_against = self.friendly_results['wins']
        num_direct_wins = len(filter(lambda w: w is not None and w.country == opponent.country, winners_against))
        num_indirect_wins = 0
        for beaten_team in winners_against:
            if beaten_team is not None:
                second_degree_wins = beaten_team.friendly_results['wins']
                if opponent in second_degree_wins:
                    num_indirect_wins += 1

        return (10 * num_direct_wins) + (2 * num_indirect_wins)

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
        :param opponent: ``Team`` instance that this ``Team`` played, or ``str`` if the opponent isn't part of the WC
        :param ``result``: ``str`` the result of the friendly

        add a friendly result to self.friendly_results, which is a ``dict`` containing keys ``wins``, ``draws``, and
        ``losses``. The values are an array of ``Team`` instances (and ``str``) which represent those teams either
        beat, drawn, or lost to, respectively.
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

    def set_base_score(self):
        """
        :return: ``int`` this ``Team``'s base score

        the base score is the score for this ``Team`` completely independent of who they are playing. The formula
        for determining base score is:
        (x + y + z^2) - f where:
        x = player skill score
        y = chemistry score
        z = the number of stars on the team
        f = the fifa rank of this team
        """
        base_score = (self._team_skill_score() + self._chemistry_score() + math.pow(self._number_of_stars(), 2)) - self.fifa_rank
        setattr(self, 'base_score', base_score)
        return base_score

    def set_plays_up(self, teams):
        """
        :param teams: ``list`` of ``Team`` instances, the other teams in the WC
        :return: ``True`` if this ``Team`` play's up, ``False`` o/w

        set the plays_up attribute for this ``Team`` using the following algorithm:
        1. Get the number of friendly wins/draws against teams with a higher base score as B
        2. Perform (1) on all teams
        3. This team "plays up" if B is in the 75th percentile of results

        Note: the base score should be set for all teams prior to this method being called
        """
        def num_better_teams_beaten_or_tied(team):
            # we must check for opp is None because the friendly_results contain None entries for teams not making the WC
            better_teams = lambda opponents: [opp for opp in opponents
                                              if opp is not None and opp.base_score > team.base_score]
            return len(better_teams(team.friendly_results.get('wins', []))) + \
                   len(better_teams(team.friendly_results.get('draws', [])))

        self_play_up_results = num_better_teams_beaten_or_tied(self)
        others_play_up_results = sorted([num_better_teams_beaten_or_tied(t) for t in teams])
        plays_up = self_play_up_results > others_play_up_results[int(len(others_play_up_results) * .75)]

        setattr(self, 'plays_up', plays_up)
        return plays_up

    def set_matchup_score(self, opponent):
        """
        :param opponent: ``Team`` instance that we're setting the matchup score against
        :return: ``int`` the calculated matchup score

        Set the altered score for this ``Team`` when competing against ``opponent``. The altered score is similar to the
        base score except that it also takes into account the plays_up field as well as past matchups between this
        team and ``opponent`` (with one degree of separation).

        This teams matchup_score against ``opponent`` is defined by the formula:
        * [Past Results Score + ((self.base_score + team.base_score) / 2)] if self.plays_up and self.base_score < opponent.base_score
        * [Past Results Score + self.base_score] o/w
        """
        # if this team plays up and they normally are worse then they're opponent, then increase they're playing ability
        # to the level halfway between theirs and their opponent's ability
        if self.plays_up and self.base_score < opponent.base_score:
            matchup_score = self._past_results_score(opponent) + ((self.base_score + opponent.base_score) / 2)
        else:
            matchup_score = self._past_results_score(opponent) + self.base_score

        self.matchup_scores[opponent.country] = matchup_score
        return matchup_score

    def set_win_probability(self, opponent):
        """
        :param opponent: ``Team`` instance to set the winning probability against

        The win probability of this ``Team`` against ``opponent`` is defined as:
        x / (x + y) where x = this team's matchup score against ``opponent`` and y = ``opponent``'s matchup
        score against this ``Team``
        """
        matchup_score = self.matchup_scores.get(opponent.country, self.set_matchup_score(opponent))
        opponent_matchup_score = opponent.matchup_scores.get(self.country, opponent.set_matchup_score(self))
        self.winning_probabilities[opponent.country] = Decimal(matchup_score) / \
                                                       Decimal((opponent_matchup_score + matchup_score))

    def probability_to_advance_from_group(self):
        """
        :return: ``decimal`` the probability of this team to advance from group

        The way we calculate probability to advance is partially flawed, but should still be close to accurate. We take the
        probability that a team will win at least two games in group as their probability to advance (so 1 - this number
        is the probability of them being knocked out)
        """
        def _helper(game_num=1, num_wins=0, to_win=True):
            """
            :param game_num: ``int`` the game in group being played
            :param to_win: ``bool`` whether we're calculating the probability of this ``Team`` to win or lose in the ``game_num``
            game
            """
            group_teams = self.get_for_group(self.tournament.teams, self.group, exclude_team=self)
            current_matchup = group_teams[game_num - 1]
            winning_prob = self.winning_probabilities[current_matchup.country]
            prob = winning_prob if to_win else 1 - winning_prob

            if game_num == 3:
                #this is a path which leads to >=2 wins
                if num_wins >= 2 or (num_wins == 1 and to_win):
                    return prob
                else:
                    return Decimal(0)
            else:
                next_game = game_num + 1
                num_wins = num_wins + 1 if to_win else num_wins
                return (prob * _helper(game_num=next_game, num_wins=num_wins, to_win=False)) + \
                       (prob * _helper(game_num=next_game, num_wins=num_wins))

        return _helper() + _helper(to_win=False)

    def knockout_probability_at_stage(self, stage, to_win=False):
        """
        :param stage: ``int`` integer to calculate the probability to lose at
        :param to_win: ``bool`` if True, calculate the probability to win at ``stage``. False means prob to lose.
        :return: ``decimal`` the probability of this team to lose at ``stage``

        For group, 16, 8, and 4 we want the probability that this ``Team`` will be eliminated
        """
        if stage == 0:
            return 1 - self.probability_to_advance_from_group()
        else:
            # stage 0 in the tournament tree represents the round directly after group
            probable_opponent = self.tournament.tree.get_opponent_at_stage(self, stage - 1)
            winning_prob = self.winning_probabilities[probable_opponent.country]
            prob = winning_prob if to_win else 1 - winning_prob

            return prob * self.knockout_probability_at_stage(stage - 1, to_win=True)

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
    def get_for_group(cls, teams, group, exclude_team=None):
        """
        :param teams: ``list`` of ``Team`` instances
        :param group: ``str`` the group letter to get team instances belonging to
        :param exclude_team: ``Team`` instance. If given, exclude this team from the returned result
        :return: ``list`` of team instances belonging to the given group
        """
        matching_group = []
        for team in teams:
            if team.group == group:
                if not exclude_team or exclude_team.country != team.country:
                    matching_group.append(team)

        return matching_group