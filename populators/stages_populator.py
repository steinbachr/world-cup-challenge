from models.tournament import Stage


class StagesPopulator():
    def __init__(self):
        pass

    @staticmethod
    def _populate_games_for_stage(stage):
        """
        :param stage: ``Stage`` instance

        given a stage, populate the games for that stage
        """
        pass

    @classmethod
    def populate(cls):
        stages = []
        for i in range(1, 6):
            new_stage = Stage(number=i, is_group=(i == 1), games=[])
            cls._populate_games_for_stage(new_stage)
            stages.append(new_stage)

        return stages

