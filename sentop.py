class SenTop:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def test(self):
        print("test")