from functools import reduce
import operator as op


class Distribution:
    def __init__(self):
        self.distribution = {}
        self.total_entries_count = 0
        self.probabilities = {}

    def add_test_statistic(self, test_statistic):
        if test_statistic not in self.distribution:
            self.distribution[test_statistic] = 1
        else:
            self.distribution[test_statistic] += 1

    def convert_to_probability(self, count):
        return count / self.total_entries_count

    def store_total_entries_count(self):
        self.total_entries_count = reduce(op.add, self.distribution.values(), 0)

    def calculate_probabilities(self):
        self.store_total_entries_count()
        for test_statisitc, count in self.distribution.items():
            self.probabilities[test_statisitc] = self.convert_to_probability(count)

    def get_probabilities(self):
        return self.probabilities
