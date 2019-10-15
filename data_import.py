import argparse
import csv
import datetime
import dateutil.parser
from os import listdir
from os.path import isfile, join
from statistics import mean


class ImportData:
    def __init__(self, data_csv, resolution):
        self.type = self.set_type(data_csv)
        self._time = []
        self._value = []
        self._round_time = []
        self._round_value = []

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

            roundTimeArray(self, resolution)

        except FileNotFoundError:
            print(f"File: {data_csv} does not exist.")

    def set_type(self, file_name):
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
        value_list = []
        for i in range(len(times)):
            cur_time = times[i]
            if key_time == cur_time:
                value_list.append(values[i])

        return value_list


def roundTimeArray(obj, resolution):
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

        obj._round_time.append(new_time)

    unique_value = []
    for t in unique_time:
        values = obj.linear_search_value(t, obj._round_time, obj._value)
        if obj.type in ["activity", "bolus", "meal"]:
            unique_value.append(sum(values))
        elif obj.type in ["smbg", "hr", "cgm", "basal"]:
            unique_value.append(mean(values))

    obj._round_time = unique_time
    obj._round_value = unique_value


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='Import and combine data.',
                                     prog='dataImport')

    parser.add_argument('folder_name', type=str, help='Name of the folder')

    parser.add_argument('output_file', type=str, help='Name of Output file')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()

    folder_path = args.folder_name

    # pull all the folders in the file
    files_lst = [
        f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    # import all the files into a list of ImportData objects
    data_lst = []
    for f in files_lst:
        data_lst.append(ImportData(folder_path+'/'+f))
