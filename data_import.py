import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []
        self._round_time = []
        self._round_time_str = []

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
