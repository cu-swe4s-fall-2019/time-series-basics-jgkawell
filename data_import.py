import argparse
import csv
import datetime
import dateutil.parser
from os import listdir
from os.path import isfile, join
from statistics import mean


class ImportData:
    def __init__(self, data_csv):
        """
        Imports time and value entries from a csv file.

        Parameters
        ----------
        data_csv : the file name (or path)

        Returns
        ----------
        None

        """

        self.type = self.set_type(data_csv)
        self._time = []
        self._value = []

        time_error = False
        value_error = False

        try:
            with open(data_csv, "r") as f_handle:
                reader = csv.DictReader(f_handle)
                for row in reader:
                    try:
                        self._time.append(dateutil.parser.parse(row['time']))
                    except ValueError:
                        time_error = True
                        # skip this row completely
                        continue

                    try:
                        self._value.append(int(row['value']))
                    except ValueError:
                        value_error = True
                        # remove the last time so that we don't get out of sync
                        self._time.pop(-1)

                f_handle.close()

            if time_error:
                print(f"File: {data_csv}"
                      + "\nOne or more times couldn\'t be parsed."
                      + " Results may be incomplete")

            if value_error:
                print(f"File: {data_csv}"
                      + "\nOne or more values couldn\'t be parsed."
                      + " Results may be incomplete")

        except FileNotFoundError:
            print(f"File: {data_csv} does not exist.")

    def set_type(self, file_name):
        """
        Sets the data type for deciding how to merge
        duplicate time entries when rounding time.

        Parameters
        ----------
        file_name : the file name (or path)

        Returns
        ----------
        type : string type name

        """

        if "activity" in file_name.lower():
            return "activity"
        elif "basal" in file_name.lower():
            return "basal"
        elif "bolus" in file_name.lower():
            return "bolus"
        elif "cgm" in file_name.lower():
            return "cgm"
        elif "hr" in file_name.lower():
            return "hr"
        elif "meal" in file_name.lower():
            return "meal"
        elif "smbg" in file_name.lower():
            return "smbg"
        else:
            print(f"Unknown type for file: {file_name}")

    def linear_search_value(self, key_time, times, values):
        """
        Runs a linear search over the times and returns a list
        of values associated with the given time.

        Parameters
        ----------
        key_time : a datetime value to search for
        times : the list of times to search through
        values : the list of values to retrieve from

        Returns
        ----------
        value_list : the list of values returned from the search

        """

        value_list = []
        for i in range(len(times)):
            cur_time = times[i]
            if key_time == cur_time:
                value_list.append(values[i])

        return value_list


def roundTimeArray(obj, resolution):
    """
    Creates time and value arrays where the times are rounded
    to the resolution specified (in minutes). Merges duplicate
    values based on data type.

    Parameters
    ----------
    obj : the DataImport object
    resolution : the resolution (in minutes) to round to

    Returns
    ----------
    zip(time, value) : a zip of the rounded times and values

    """

    round_time = []
    unique_time = []
    for cur_time in obj._time:
        min_minus = datetime.timedelta(minutes=(cur_time.minute % resolution))
        min_plus = datetime.timedelta(minutes=resolution) - min_minus
        if (cur_time.minute % resolution) <= resolution/2:
            new_time = cur_time - min_minus
        else:
            new_time = cur_time + min_plus

        if new_time not in unique_time:
            unique_time.append(new_time)

        round_time.append(new_time)

    unique_value = []
    for t in unique_time:
        values = obj.linear_search_value(t, round_time, obj._value)
        if obj.type in ["activity", "bolus", "meal"]:
            unique_value.append(sum(values))
        elif obj.type in ["smbg", "hr", "cgm", "basal"]:
            unique_value.append(mean(values))

    return zip(unique_time, unique_value)


def printArray(data_list, annotation_list, base_name, key_file):
    """
    Creates a csv which aligns the data in a list of zip objects based on
    key_file. The first column is time, the second column is the data
    from key_file, and then the remaining headings. The function first
    prints the time and value from the key_file associated with that
    time. For each other file, the function finds if a value from that file
    exists for the already printed time and (if exists) prints the value
    (else) prints 0.

    Parameters
    ----------
    data_list : a list of zip objects of data (time, value) pairs
    annotation_list : a list of strings with column labels for the data value
    base_name : the file name you want to print as
    key_file : the name from annotation_list you want to align the data on

    Returns
    ----------
    Nothing (creates file of output)

    """

    # find index with data you want
    base_data = []
    key_idx = 0
    for i in range(len(annotation_list)):
        if annotation_list[i] == key_file:
            base_data = data_list[i]
            print('base data is: '+annotation_list[i])
            key_idx = i
            break
        if i == len(annotation_list):
            print('Key not found')

    file = open(base_name, 'w')
    file.write('time,')
    # write the file name (strip off .csv)
    file.write(annotation_list[key_idx][0:-4] + ', ')
    # create list of keys (excluding the base key)
    non_key = list(range(0, len(annotation_list)))
    non_key.remove(key_idx)
    # write the list of keys
    for idx in non_key:
        file.write(annotation_list[idx][0:-4] + ', ')

    file.write('\n')
    # iterate through the base data
    for time, value in base_data:
        # write the base data
        file.write(str(time) + ', ' + str(value) + ', ')
        # iterate through the other data
        for n in non_key:
            done = False
            for t, v in data_list[n]:
                if time == t:
                    file.write(str(v) + ', ')
                    done = True
                    break

            if not done:
                file.write('0, ')
        file.write('\n')
    file.close()


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='Import and combine data.',
                                     prog='dataImport')

    parser.add_argument('folder_name', type=str,
                        help='Name of the folder')
    parser.add_argument('output_file', type=str,
                        help='Name of Output file')
    parser.add_argument('resolution', type=int,
                        help='The time resolution to round to (min)')

    args = parser.parse_args()

    folder_path = args.folder_name

    # pull all the folders in the file
    files_lst = [
        f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    # import all the files into a list of ImportData objects
    data_lst = []
    for f in files_lst:
        data_lst.append(ImportData(folder_path+'/'+f))

    # NOTE: This is for user-defined resolution
    # convert to zipped, rounded data
    zip_data = []
    for data in data_lst:
        zip_data.append(roundTimeArray(data, args.resolution))

    # print to a csv file
    printArray(zip_data, files_lst, args.output_file, 'cgm_small.csv')

    # NOTE: This is for 5min resolution
    # convert to zipped, rounded data
    zip_data = []
    for data in data_lst:
        zip_data.append(roundTimeArray(data, 5))

    # print to a csv file
    printArray(zip_data, files_lst, 'hw_data_5.csv', 'cgm_small.csv')

    # NOTE: This is for 15min resolution
    # convert to zipped, rounded data
    zip_data = []
    for data in data_lst:
        zip_data.append(roundTimeArray(data, 15))

    # print to a csv file
    printArray(zip_data, files_lst, 'hw_data_15.csv', 'cgm_small.csv')
