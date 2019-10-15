import unittest
import data_import
import statistics
import random
import math
import os
import datetime


TIME_1 = datetime.datetime.strptime('1/1/2008 1:00', '%m/%d/%Y %I:%M')
TIME_2 = datetime.datetime.strptime('1/1/2008 1:15', '%m/%d/%Y %I:%M')


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def generate_data(num):
    values = []
    times = []
    for i in range(0, 100):
        values.append(random.randint(1, 100))
        times.append(random_date(TIME_1, TIME_2))
    return values, times


class TestDataImport(unittest.TestCase):

    def test_simple_file(self):
        file_name = 'test.csv'
        num = 100
        test_file = open(file_name, 'w')
        test_file.write('value,time\n')

        values, times = generate_data(num)
        for v, t in zip(values, times):
            test_file.write(str(v) + ',' + str(t) + '\n')

        test_file.close()

        test_data = data_import.ImportData(file_name, 10)

        for i in range(0, 100):
            self.assertEqual(test_data._value[i], values[i])
            self.assertEqual(test_data._time[i], times[i])

        os.remove(file_name)

    def test_bad_time(self):
        file_name = 'test.csv'
        num = 100
        test_file = open(file_name, 'w')
        test_file.write('value,time\n')

        values, times = generate_data(num)
        times[15] = 'BAD TIME'
        for v, t in zip(values, times):
            test_file.write(str(v) + ',' + str(t) + '\n')
        times.pop(15)
        values.pop(15)

        test_file.close()
        test_data = data_import.ImportData(file_name, 10)

        for i in range(0, num-1):
            self.assertEqual(test_data._value[i], values[i])
            self.assertEqual(test_data._time[i], times[i])

        os.remove(file_name)

    def test_bad_value(self):
        file_name = 'test.csv'
        num = 100
        test_file = open(file_name, 'w')
        test_file.write('value,time\n')

        values, times = generate_data(num)
        values[15] = random.random()
        for v, t in zip(values, times):
            test_file.write(str(v) + ',' + str(t) + '\n')
        times.pop(15)
        values.pop(15)

        test_file.close()
        test_data = data_import.ImportData(file_name, 10)

        for i in range(0, num-1):
            self.assertEqual(test_data._value[i], values[i])
            self.assertEqual(test_data._time[i], times[i])

        os.remove(file_name)

    def test_bad_file(self):
        file_name = 'test.csv'

        test_data = data_import.ImportData(file_name, 10)

        self.assertEqual(len(test_data._value), 0)
        self.assertEqual(len(test_data._time), 0)

    def test_linear_search(self):
        file_name = 'test.csv'
        num = 100
        test_file = open(file_name, 'w')
        test_file.write('value,time\n')

        values, times = generate_data(num)
        for v, t in zip(values, times):
            test_file.write(str(v) + ',' + str(t) + '\n')

        test_file.close()

        test_data = data_import.ImportData(file_name, 10)

        for value, time in zip(values, times):
            cur_value = test_data.linear_search_value(time,
                                                      test_data._time,
                                                      test_data._value)
            self.assertIn(value, cur_value)

        os.remove(file_name)

    def test_rounding_unique(self):
        file_name = 'smallData/activity_small.csv'

        test_data = data_import.ImportData(file_name, 10)
        # make sure the rounded times are unique
        self.assertFalse(
            len(test_data._round_time) > len(test_data._round_time))

    def test_rounding_resolution(self):
        file_name = 'smallData/activity_small.csv'
        resolution = 5

        test_data = data_import.ImportData(file_name, resolution)
        # make sure the rounded times correct resolution
        for t in test_data._round_time:
            self.assertTrue(t.minute % resolution == 0)


if __name__ == '__main__':
    unittest.main()
