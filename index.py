from SamplesXY import SamplesXY
from CombineAlgorithm import CombineAlgorithm
from TestStatisticDistribution import TestStatisticDistribution

if __name__ == '__main__':
    # two samples [1,2,3] [2,3,4]
    # get J distribution
    # get the value J of the test statistic for the samples
    # print them

    # Combine the two samples into one
    algorithm_instance = CombineAlgorithm()
    # Example 1
    # samples_x_y_instance = SamplesXY(sample_x=[1], sample_y=[2, 3, 4])
    # Example 2
    # samples_x_y_instance = SamplesXY(sample_x=[5, 10], sample_y=[2, 2, 10])
    # Example 3
    samples_x_y_instance = SamplesXY(sample_x=[2, 2, 4, 4, 4, 4, 4, 4], sample_y=[2, 2, 2, 2, 2, 3, 3, 3])
    samples_x_y_instance.run(algorithm_instance)
    combined_sample_instance = algorithm_instance.get_combined_sample()

    distribution = TestStatisticDistribution(sample_size_y=samples_x_y_instance.sample_size_y,
                                             shared_combined_sample=combined_sample_instance)

    # Get the value of the test statistic for the samples
    distribution.make_test_statistic()
    print(distribution.get_test_statistic())

    # Make test statistic distribution
    distribution.make_test_statistic_distribution()
    print(distribution.get_probabilities())
