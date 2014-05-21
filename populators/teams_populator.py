from models.team import Team


class TeamsPopulator():
    teams = [('Brazil', 'A'), ('Croatia', 'A'), ('Mexico', 'A'), ('Cameroon', 'A'),
             ('Spain', 'B'), ('Netherlands', 'B'), ('Chile', 'B'), ('Australia', 'B'),
             ('Colombia', 'C'), ('Greece', 'C'), ('Cote d\'Ivoire', 'C'), ('Japan', 'C'),
             ('Uruguay', 'D'), ('Costa Rica', 'D'), ('England', 'D'), ('Italy', 'D'),
             ('Switzerland', 'E'), ('Ecuador', 'E'), ('France', 'E'), ('Honduras', 'E'),
             ('Argentina', 'F'), ('Bosnia-Herzegovina', 'F'), ('Iran', 'F'), ('Nigeria', 'F'),
             ('Germany', 'G'), ('Portugal', 'G'), ('Ghana', 'G'), ('United States', 'G'),
             ('Belgium', 'H'), ('Algeria', 'H'), ('Russia', 'H'), ('South Korea', 'H')]

    def __init__(self):
        pass

    @classmethod
    def _get_fifa_rank(cls, team):
        pass

    @classmethod
    def populate(cls):
        teams = []
        for country, group in cls.teams:
            teams.append(Team(group=group, country=country))

        return teams