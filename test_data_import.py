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


class TestDataImport(unittest.TestCase):

    def test_simple_file(self):
        file_name = 'test.csv'
        test_file = open(file_name, 'w')
        test_file.write('value,time\n')

        values = []
        times = []
        for i in range(0, 100):
            cur_value = random.randint(1, 100)
            cur_time = random_date(TIME_1, TIME_2)

            values.append(cur_value)
            times.append(cur_time)
            test_file.write(str(cur_value) + ',' + str(cur_time) + '\n')

        test_file.close()

        test_data = data_import.ImportData(file_name)

        for i in range(0, 100):
            self.assertEqual(test_data._value[i], values[i])
            self.assertEqual(test_data._time[i], times[i])

        os.remove(file_name)

    def test_bad_time(self):
        file_name = 'test.csv'
        test_file = open(file_name, 'w')
        test_file.write('value,time\n')

        values = []
        times = []
        for i in range(0, 100):
            cur_value = random.randint(1, 100)
            cur_time = random_date(TIME_1, TIME_2)

            if i == 15:
                test_file.write(str(cur_value) + ',' + 'BAD TIME' + '\n')
            else:
                values.append(cur_value)
                times.append(cur_time)
                test_file.write(str(cur_value) + ',' + str(cur_time) + '\n')

        test_file.close()
        test_data = data_import.ImportData(file_name)

        for i in range(0, 99):
            self.assertEqual(test_data._value[i], values[i])
            self.assertEqual(test_data._time[i], times[i])

        os.remove(file_name)

    def test_bad_value(self):
        file_name = 'test.csv'
        test_file = open(file_name, 'w')
        test_file.write('value,time\n')

        values = []
        times = []
        for i in range(0, 100):
            cur_value = random.randint(1, 100)
            cur_time = random_date(TIME_1, TIME_2)

            if i == 15:
                test_file.write(str(random.random()) + ','
                                + str(cur_time) + '\n')
            else:
                values.append(cur_value)
                times.append(cur_time)
                test_file.write(str(cur_value) + ',' + str(cur_time) + '\n')

        test_file.close()
        test_data = data_import.ImportData(file_name)

        for i in range(0, 99):
            self.assertEqual(test_data._value[i], values[i])
            self.assertEqual(test_data._time[i], times[i])

        os.remove(file_name)

    def test_bad_file(self):
        file_name = 'test.csv'

        test_data = data_import.ImportData(file_name)

        self.assertEqual(len(test_data._value), 0)
        self.assertEqual(len(test_data._time), 0)


if __name__ == '__main__':
    unittest.main()
