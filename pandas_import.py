import numpy as np
import pandas as pd
import datetime as dt

if __name__ == '__main__':

    data_dict = {}

    # Read in data
    data_dict['activity'] = pd.read_csv('./smallData/activity_small.csv')
    data_dict['basal'] = pd.read_csv('./smallData/basal_small.csv')
    data_dict['bolus'] = pd.read_csv('./smallData/bolus_small.csv')
    data_dict['cgm'] = pd.read_csv('./smallData/cgm_small.csv')
    data_dict['hr'] = pd.read_csv('./smallData/hr_small.csv')
    data_dict['meal'] = pd.read_csv('./smallData/meal_small.csv')
    data_dict['smbg'] = pd.read_csv('./smallData/smbg_small.csv')
