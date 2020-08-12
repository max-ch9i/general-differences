class TestSample:
    FORM_SAMPLE_X = 0
    FORM_SAMPLE_Y = 1

    def __init__(self, sample_x: list, sample_y: list):
        self.sample_x = sample_x
        self.sample_y = sample_y
        self.sample_size_x = len(self.sample_x)
        self.sample_size_y = len(self.sample_y)
        self.sample_size_x_y = self.sample_size_x + self.sample_size_y

        self.next_value_x = 0
        self.next_value_y = 0
        self.next_value = None
        self.next_value_source_sample = None

        # Process algorithm data
        self.attributions = []
        self.test_sample = []
        self.x_index = 0
        self.y_index = 0

        # Occurrence algorithm data
        self.item_index = 0
        self.lookahead_index = 0
        self.occurence_counter = 0
        self.type_to_count = None
        self.test_sample_counts = []

    def are_there_more_items_left(self):
        return self.x_index + self.y_index < self.sample_size_x_y

    def reset_item_index(self):
        self.item_index = 0

    def reset_lookahead_index(self):
        self.lookahead_index = 0

    def reset_occurrence_counter(self):
        self.occurence_counter = 0

    def reset_sample_counts(self):
        self.test_sample_counts = []

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

    def increment_x_index(self):
        self.x_index += 1

    def increment_y_index(self):
        self.y_index += 1

    def order_samples(self):
        self.sample_x.sort()
        self.sample_y.sort()

    @staticmethod
    def get_next_value(sample, sample_size, index):
        return sample[index] if index < sample_size else float('inf')

    def append_to_test_sample(self, next_value, from_sample):
        self.test_sample.append(next_value)
        self.attributions.append(from_sample)

    def get_next_value_x(self):
        self.next_value_x = self.get_next_value(self.sample_x, self.sample_size_x, self.x_index)

    def get_next_value_y(self):
        self.next_value_y = self.get_next_value(self.sample_y, self.sample_size_y, self.y_index)

    def is_next_x_less_than_y(self):
        return self.next_value_x <= self.next_value_y

    def append_next_x_value_to_test_sample(self):
        self.append_to_test_sample(self.next_value_x, self.FORM_SAMPLE_X)

    def append_next_y_value_to_test_sample(self):
        self.append_to_test_sample(self.next_value_y, self.FORM_SAMPLE_Y)

    def combine_samples(self):
        while self.are_there_more_items_left():
            self.get_next_value_x()
            self.get_next_value_y()
            if self.is_next_x_less_than_y():
                self.append_next_x_value_to_test_sample()
                self.increment_x_index()
            else:
                self.append_next_y_value_to_test_sample()
                self.increment_y_index()

    def prepare(self):
        self.order_samples()
        self.combine_samples()

    def output_test_sample(self):
        print(self.test_sample)
        print(self.attributions)

    def set_type_to_count(self, observation_from):
        self.type_to_count = observation_from

    def choose_sample_x_for_counting(self):
        self.set_type_to_count(self.FORM_SAMPLE_X)

    def choose_sample_y_for_counting(self):
        self.set_type_to_count(self.FORM_SAMPLE_Y)

    def is_item_index_less_than_test_sample_size(self):
        return self.item_index < self.sample_size_x_y

    def advance_lookahead_index(self):
        self.lookahead_index = self.item_index + 1

    def is_lookahead_value_equal_to_item(self):
        if self.lookahead_index >= self.sample_size_x_y:
            return False
        return self.test_sample[self.item_index] == self.test_sample[self.lookahead_index]

    def is_lookahead_type_equal_to_counted_type(self):
        return self.attributions[self.lookahead_index] == self.type_to_count

    def is_item_type_equal_to_counted_type(self):
        return self.attributions[self.item_index] == self.type_to_count

    def is_item_index_less_than_lookahead_index(self):
        return self.item_index < self.lookahead_index

    def append_item_count_to_list(self):
        self.test_sample_counts.append(self.occurence_counter)

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

    def count_x_in_test_sample(self):
        self.reset_counting_algorithm_data()
        self.choose_sample_x_for_counting()
        self.count_occurrences()

    def count_y_in_test_sample(self):
        self.reset_counting_algorithm_data()
        self.choose_sample_y_for_counting()
        self.count_occurrences()

    def output_occurrences(self):
        print(self.test_sample_counts)

    def get_occurrences(self):
        return self.test_sample_counts

    @staticmethod
    def make_test_sample(sample_x, sample_y):
        return TestSample(sample_x, sample_y)