class WCModel():
    fields = []

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.fields:
                setattr(self, key, val)