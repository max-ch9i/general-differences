from itertools import combinations
from math import gcd
from fractions import Fraction
import operator as op
from functools import reduce
from testsample2 import TestSample

X_ITEM = 0
Y_ITEM = 1


def ncr(n, r):
    r = min(r, n - r)
    numerator = reduce(op.mul, range(n, n - r, -1), 1)
    denominator = reduce(op.mul, range(1, r + 1), 1)
    return numerator // denominator


class TestConfig:
    def __init__(self, sample_size_x=0, sample_size_y=0):
        self.sample_size_x = sample_size_x
        self.sample_size_y = sample_size_y
        self.sample_x_y_positions = [x for x in range(0, self.get_sample_size_x_y())]

    def get_sample_x_y_positions(self):
        return self.sample_x_y_positions

    def get_sample_size_x(self):
        return self.sample_size_x

    def get_sample_size_y(self):
        return self.sample_size_y

    def get_sample_size_x_y(self):
        return self.sample_size_x + self.sample_size_y


class Distribution:
    def __init__(self, test_config: TestConfig):
        self.distribution = {}
        self.test_config = test_config
        self.total_entries_count = 0

    def add_test_statistic(self, test_statistic):
        if test_statistic not in self.distribution:
            self.distribution[test_statistic] = 1
        else:
            self.distribution[test_statistic] += 1

    def convert_to_probability(self, count):
        return count / self.total_entries_count

    def store_total_entries_count(self):
        self.total_entries_count = reduce(op.add, self.distribution.values(), 0)

    def get_distribution(self):
        probabilities = {}
        self.store_total_entries_count()
        for test_statisitc, count in self.distribution.items():
            probabilities[test_statisitc] = self.convert_to_probability(count)
        print(self.total_entries_count)
        return probabilities


class Meshing:
    def __init__(self, meshing_list):
        self.meshing_list = meshing_list
        self.meshing_list_length = len(self.meshing_list)
        self.counts_of_x = self.get_counts_of_symbol(X_ITEM)
        self.counts_of_y = self.get_counts_of_symbol(Y_ITEM)
        self.sample_x_length = self.counts_of_x[-1]
        self.sample_y_length = self.counts_of_y[-1]
        self.sample_x_y_lengths_gcd = gcd(self.sample_x_length, self.sample_y_length)

    def get_meshing_list(self):
        return self.meshing_list

    def get_counts_of_symbol(self, symbol):
        counts = [0 for _ in range(self.meshing_list_length + 1)]

        for i, list_symbol in enumerate(self.meshing_list, start=1):
            current_contribution = 1 if list_symbol == symbol else 0
            counts[i] = counts[i - 1] + current_contribution

        counts.pop(0)

        return counts

    def get_cumulative_probability_of_x(self, count_x):
        return Fraction(count_x, self.sample_x_length)

    def get_cumulative_probability_of_y(self, count_y):
        return Fraction(count_y, self.sample_y_length)

    def get_meshing_test_statistic(self):
        cumulative_difference_at_t = [0 for _ in range(self.meshing_list_length)]
        for t, counts in enumerate(zip(self.counts_of_x, self.counts_of_y)):
            count_x = counts[0]
            count_y = counts[1]
            cumulative_x = self.get_cumulative_probability_of_x(count_x)
            cumulative_y = self.get_cumulative_probability_of_y(count_y)
            cumulative_difference_at_t[t] = abs(cumulative_x - cumulative_y)
        max_cumulative_difference = max(cumulative_difference_at_t)
        factor = self.sample_x_length * self.sample_y_length / self.sample_x_y_lengths_gcd
        test_statistic = factor * max_cumulative_difference
        return test_statistic

    @staticmethod
    def make_meshing_from_y_items(test_config: TestConfig, y_items):
        meshing_list = [X_ITEM for _ in range(0, test_config.get_sample_size_x_y())]
        for y_item_index in y_items:
            meshing_list[y_item_index] = Y_ITEM
        return Meshing(meshing_list)


def get_meshing_test_statistic(test_config: TestConfig, y_items):
    meshing = Meshing.make_meshing_from_y_items(test_config, y_items)
    return meshing.get_meshing_test_statistic()


def get_y_item_combinations(test_config: TestConfig):
    return combinations(test_config.get_sample_x_y_positions(), test_config.get_sample_size_y())


def get_meshings(sample_size_x, sample_size_y):
    test_config = TestConfig(sample_size_x, sample_size_y)
    distribution = Distribution(test_config)
    y_items = get_y_item_combinations(test_config)
    for y_item in y_items:
        test_statisitc = get_meshing_test_statistic(test_config, y_item)
        distribution.add_test_statistic(test_statisitc)
    print(distribution.get_distribution())


if __name__ == '__main__':
    # get_meshings(sample_size_x=6, sample_size_y=6)
    test_sample = TestSample.make_test_sample(sample_x=[3, 3, 5, 7], sample_y=[3, 4, 4, 6])
    test_sample.prepare()
    test_sample.output_test_sample()

    test_sample.count_y_in_test_sample()
    test_sample.output_occurrences()
