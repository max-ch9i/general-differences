class CombinedSample:
    def __init__(self, combined_sample_values: list, attributions: list):
        self.attributions = attributions
        self.combined_sample_values = combined_sample_values
        self.combined_sample_size = len(self.combined_sample_values)

    def set_attributions(self, next_attributions: list):
        self.attributions = next_attributions

    def get_attributions_copy(self):
        return self.attributions[:]

    def run(self, visitor):
        visitor.visit(self)
