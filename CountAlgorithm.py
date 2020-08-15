from Source import Source
from CombinedSample import CombinedSample


class CountAlgorithm:
    def __init__(self):
        self.item_index = 0
        self.lookahead_index = 0
        self.occurence_counter = 0
        self.type_to_count = None
        self.combined_sample_counts = []

        self.combined_sample: CombinedSample | None = None

    def reset_item_index(self):
        self.item_index = 0

    def reset_lookahead_index(self):
        self.lookahead_index = 0

    def reset_occurrence_counter(self):
        self.occurence_counter = 0

    def reset_sample_counts(self):
        self.combined_sample_counts = []

    def reset_counting_algorithm_data(self):
        self.reset_item_index()
        self.reset_lookahead_index()
        self.reset_occurrence_counter()
        self.reset_sample_counts()

    def increment_item_index(self):
        self.item_index += 1

    def increment_lookahead_index(self):
        self.lookahead_index += 1

    def increment_occurence_counter(self):
        self.occurence_counter += 1

    def set_type_to_count(self, observation_from):
        self.type_to_count = observation_from

    def choose_sample_x_for_counting(self):
        self.set_type_to_count(Source.FORM_SAMPLE_X)

    def choose_sample_y_for_counting(self):
        self.set_type_to_count(Source.FORM_SAMPLE_Y)

    def is_item_index_less_than_test_sample_size(self):
        return self.item_index < self.combined_sample.combined_sample_size

    def advance_lookahead_index(self):
        self.lookahead_index = self.item_index + 1

    def is_lookahead_value_equal_to_item(self):
        if self.lookahead_index >= self.combined_sample.combined_sample_size:
            return False
        return self.combined_sample.combined_sample_values[self.item_index] == \
               self.combined_sample.combined_sample_values[self.lookahead_index]

    def is_lookahead_type_equal_to_counted_type(self):
        return self.combined_sample.attributions[self.lookahead_index] == self.type_to_count

    def is_item_type_equal_to_counted_type(self):
        return self.combined_sample.attributions[self.item_index] == self.type_to_count

    def is_item_index_less_than_lookahead_index(self):
        return self.item_index < self.lookahead_index

    def append_item_count_to_list(self):
        self.combined_sample_counts.append(self.occurence_counter)

    def count_occurrences(self):
        while self.is_item_index_less_than_test_sample_size():
            self.advance_lookahead_index()
            if self.is_item_type_equal_to_counted_type():
                self.increment_occurence_counter()

            while self.is_lookahead_value_equal_to_item():
                if self.is_lookahead_type_equal_to_counted_type():
                    self.increment_occurence_counter()
                self.increment_lookahead_index()

            while self.is_item_index_less_than_lookahead_index():
                self.append_item_count_to_list()
                self.increment_item_index()

    def configure_count_x(self):
        self.reset_counting_algorithm_data()
        self.choose_sample_x_for_counting()

    def configure_count_y(self):
        self.reset_counting_algorithm_data()
        self.choose_sample_y_for_counting()

    def visit(self, combined_sample):
        self.combined_sample = combined_sample
        self.count_occurrences()

    def output_occurrences(self):
        print(self.combined_sample_counts)

    def get_combined_sample_counts(self):
        return self.combined_sample_counts


if __name__ == '__main__':
    algorithm = CountAlgorithm()
    algorithm.configure_count_x()
    combined_sample_instance = CombinedSample(combined_sample_values=[3, 3, 3, 4, 4, 5, 6, 7],
                                              attributions=[0, 0, 1, 1, 1, 0, 1, 0])
    combined_sample_instance.run(algorithm)
    algorithm.output_occurrences()
