from SamplesXY import SamplesXY
from Source import Source
from CombinedSample import CombinedSample


class CombineAlgorithm:
    def __init__(self):
        self.next_value_x = 0
        self.next_value_y = 0
        self.next_value = None
        self.next_value_source_sample = None

        self.attributions_list = []
        self.combined_sample_list = []
        self.x_index = 0
        self.y_index = 0

        self.samples_x_y_object: SamplesXY | None = None

    def are_there_more_items_left(self):
        return self.x_index + self.y_index < self.samples_x_y_object.sample_size_x_y

    def increment_x_index(self):
        self.x_index += 1

    def increment_y_index(self):
        self.y_index += 1

    def order(self):
        self.samples_x_y_object.sample_x.sort()
        self.samples_x_y_object.sample_y.sort()

    @staticmethod
    def get_next_value(sample, sample_size, index):
        return sample[index] if index < sample_size else float('inf')

    def append_to_test_sample(self, next_value, from_sample):
        self.combined_sample_list.append(next_value)
        self.attributions_list.append(from_sample)

    def get_next_value_x(self):
        self.next_value_x = self.get_next_value(self.samples_x_y_object.sample_x, self.samples_x_y_object.sample_size_x,
                                                self.x_index)

    def get_next_value_y(self):
        self.next_value_y = self.get_next_value(self.samples_x_y_object.sample_y, self.samples_x_y_object.sample_size_y,
                                                self.y_index)

    def is_next_x_less_than_y(self):
        return self.next_value_x <= self.next_value_y

    def append_next_x_value_to_test_sample(self):
        self.append_to_test_sample(self.next_value_x, Source.FORM_SAMPLE_X)

    def append_next_y_value_to_test_sample(self):
        self.append_to_test_sample(self.next_value_y, Source.FORM_SAMPLE_Y)

    def combine_samples(self):
        self.order()
        while self.are_there_more_items_left():
            self.get_next_value_x()
            self.get_next_value_y()
            if self.is_next_x_less_than_y():
                self.append_next_x_value_to_test_sample()
                self.increment_x_index()
            else:
                self.append_next_y_value_to_test_sample()
                self.increment_y_index()

    def visit(self, samples_x_y_object):
        self.samples_x_y_object = samples_x_y_object
        self.combine_samples()

    def output_test_sample(self):
        print(self.combined_sample_list)
        print(self.attributions_list)

    def get_combined_sample(self):
        return CombinedSample(self.combined_sample_list, self.attributions_list)


if __name__ == '__main__':
    algorithm = CombineAlgorithm()
    samples_x_y = SamplesXY(sample_x=[3, 3, 5, 7], sample_y=[3, 4, 4, 6])
    samples_x_y.run(algorithm)
    algorithm.output_test_sample()
