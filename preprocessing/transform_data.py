import polars as pl
import pandas as pd

def feature_list():
    """creates a list of columns which should be used for transforming

    Returns:
        col_list: list of columns for importing
    """
    #number of the smart features to be imported
    number_list = [1,3,4,5,7,9,10,12,187,188,192,193,194,197,198,199]    
    col_list = [] # ['serial_number', 'failure']
    for n in number_list:
    #   string1 = f"smart_{n}_normalized"
        string2 = f"smart_{n}_raw"
    #   col_list.append(string1)
        col_list.append(string2)
    return col_list

def timeseries_batches(df, window=14):
    """splits up a timeseries into batches of a specified window size

    Args:
        df (polars DataFrame): time-series of a single hard drive
        window (int, optional): the size of the batches the time series should be split into. Defaults to 14.
    Returns:
        list_df: list of DataFrames
    """
    length = len(df)       
    leftover = length % window
    df_sorted = df.sort(by="date").to_pandas()
    #cut df down to multiples of the window size (cutoff happens at beginning)
    if leftover != 0:
        df_cut = df_sorted.loc[leftover: , :]
    else:
        df_cut = df_sorted
    #create batches of window size as a list of dataframes
    list_df = [df_cut[i:i+window] for i in range(0,len(df_cut),window)]
    return(list_df)


def transform_rocket(list_df, df_rocket):
    """transform batches of time series in a list of DataFrames into a DataFrame format for sktime rocket.

    Args:
        list_df (list of DataFrames): time series batches in a list
        df_rocket (pandas DataFrame): DataFrame to which the time series should be added (in sktime rocket format)
    Returns:
        df_rocket (pandas DataFrame): DataFrame with new row with time series from the list of DataFrames.
    """
    features = feature_list()
    for df in list_df:
        feature_dict = {}
        for f in features:
            feature_dict[f] = (df[f]).reset_index(drop=True)

        df_rocket = df_rocket.append(feature_dict, ignore_index = True)
    return(df_rocket)




if __name__ == "__main__":
    pass
