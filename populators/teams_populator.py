from models.team import Team


class TeamsPopulator():
    teams = ['Algeria', 'Cameroon', "Cote d'lvoire", 'Ghana', 'Nigeria', 'Australia', 'Iran', 'Japan', 'Korea Republic',
             'Belgium', 'Bosnia and Herzegovina', 'Croatia', 'England', 'France', 'Germany', 'Greece', 'Italy', 'Netherlands',
             'Portugal', 'Russia', 'Spain', 'Switzerland', 'Costa Rica', 'Honduras', 'Mexico', 'USA', 'Argentina',
             'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Uruguay']
    groups = [(), (), ()]

    def __init__(self):
        pass

    @classmethod
    def _get_fifa_rank(cls, team):
        pass

    @classmethod
    def populate(cls):
        countries = cls.teams
        teams = []
        for country in countries:
            teams.append(Team(country=country))

        return teams