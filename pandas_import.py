import numpy as np
import pandas as pd
import datetime as dt


def main():

    # Read in data
    data_dict = {}
    data_dict['activity'] = pd.read_csv('./smallData/activity_small.csv')
    data_dict['basal'] = pd.read_csv('./smallData/basal_small.csv')
    data_dict['bolus'] = pd.read_csv('./smallData/bolus_small.csv')
    data_dict['cgm'] = pd.read_csv('./smallData/cgm_small.csv')
    data_dict['hr'] = pd.read_csv('./smallData/hr_small.csv')
    data_dict['meal'] = pd.read_csv('./smallData/meal_small.csv')
    data_dict['smbg'] = pd.read_csv('./smallData/smbg_small.csv')

    for df_name, df in data_dict.items():
        # Set the index to time
        df.index = pd.to_datetime(df.time)

        # Change format to float (drop strings)
        if df.value.dtype != float:
            df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()

        # Change value to data name
        df.rename(columns={"value": df_name}, inplace=True)

    # Separte cgm from others
    df_cgm = None
    df_list = []
    for df_name, df in data_dict.items():
        if df_name != 'cgm':
            df_list.append(df)
        else:
            df_cgm = df

    # Join frames together
    join_frame = df_cgm.join(df_list, how='left')

    # Clean out all NaN values
    join_frame.fillna(0, inplace=True)

    # Create time rounded columns
    join_frame['time5'] = join_frame.index.round('5min')
    join_frame['time15'] = join_frame.index.round('15min')

    # Sum values
    sum5 = join_frame[['activity', 'bolus',
                       'meal', 'time5']].groupby('time5').sum()
    sum15 = join_frame[['activity', 'bolus',
                        'meal', 'time15']].groupby('time15').sum()

    # Average values
    mean5 = join_frame[['smbg', 'hr', 'cgm',
                        'basal', 'time5']].groupby('time5').mean()
    mean15 = join_frame[['smbg', 'hr', 'cgm',
                         'basal', 'time15']].groupby('time15').mean()

    # Join sums and means
    join5 = mean5.join(sum5, how='left')
    join15 = mean15.join(sum15, how='left')

    # Print to CSV files
    join5.to_csv('./out/hw_data_5_pandas.csv', encoding='utf-8')
    join15.to_csv('./out/hw_data_15_pandas.csv', encoding='utf-8')


if __name__ == '__main__':
    main()
