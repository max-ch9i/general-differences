class SamplesXY:
    def __init__(self, sample_x: list, sample_y: list):
        self.sample_x = sample_x
        self.sample_y = sample_y
        self.sample_size_x = len(self.sample_x)
        self.sample_size_y = len(self.sample_y)
        self.sample_size_x_y = self.sample_size_x + self.sample_size_y

    def run(self, visitor):
        visitor.visit(self)

