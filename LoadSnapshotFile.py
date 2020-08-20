import sys
import png

from SamplesXY import SamplesXY
from CombineAlgorithm import CombineAlgorithm
from TestStatisticDistribution import TestStatisticDistribution


def convert_to_colour(test_statistic_value):
    return 50 if test_statistic_value > 1.358 else 250


def chunks(lst, chunk_length):
    """
    Yield successive n-sized chunks from lst.
    """
    for i in range(0, len(lst), chunk_length):
        yield lst[i:i + chunk_length]


if __name__ == '__main__':
    print('Opening file...')
    file_original = open('original', 'rb')
    file_modified = open('a', 'rb')
    file_original.seek(0, 2)
    file_length = file_original.tell()
    file_original.seek(0)
    file_original.read(1)
    byte_of_number_of_frames = file_original.read(1)
    file_modified.read(2)
    number_of_parallel_frames = int.from_bytes(byte_of_number_of_frames, sys.byteorder)
    print('Number of parallel frames is {}'.format(number_of_parallel_frames))
    print('Loading pixel distributions, {} observed values at a time...'.format(number_of_parallel_frames))
    pixel_samples_original = []
    pixel_samples_modified = []

    while True:
        byte_colour = file_original.read(number_of_parallel_frames)
        sample = list(byte_colour)
        pixel_samples_original.append(sample)
        if file_length == file_original.tell():
            break
    print('Loaded {} samples'.format(len(pixel_samples_original)))
    while True:
        byte_colour = file_modified.read(number_of_parallel_frames)
        sample = list(byte_colour)
        pixel_samples_modified.append(sample)
        if file_length == file_modified.tell():
            break
    print('Loaded {} samples'.format(len(pixel_samples_modified)))

    pixel_test_statistic = []
    for index, samples in enumerate(zip(pixel_samples_original, pixel_samples_modified)):
        if index % 1500 == 0:
            print(index)
        samples_x_y_instance = SamplesXY(sample_x=samples[0], sample_y=samples[1])
        algorithm_instance = CombineAlgorithm()

        # Combine the two samples into one, noting the samples the values came from
        samples_x_y_instance.run(algorithm_instance)
        combined_sample_instance = algorithm_instance.get_combined_sample()

        distribution = TestStatisticDistribution(samples_x_y=samples_x_y_instance,
                                                 shared_combined_sample=combined_sample_instance)
        distribution.make_test_statistic_approximate()
        test_statistic = distribution.get_test_statistic()
        pixel_test_statistic.append(test_statistic)

    output_file = open('distribution.png', 'wb')
    writer = png.Writer(width=300, height=300, greyscale=True)
    output_colours = map(convert_to_colour, pixel_test_statistic)
    writer.write(output_file, list(chunks(list(output_colours), 300)))
