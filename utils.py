
import numpy as np
import pandas as pd
import os
from collections import defaultdict


def optimize_dataframe(df):
    """
    Optimize the data types of a pandas DataFrame to reduce memory usage.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to optimize.
    
    Returns:
    pd.DataFrame: A new DataFrame with optimized data types.
    """
    optimized_df = df.copy()
    
    # Optimize numeric columns
    for col in optimized_df.select_dtypes(include=['int', 'float']).columns:
        col_min = optimized_df[col].min()
        col_max = optimized_df[col].max()
        
        if pd.api.types.is_integer_dtype(optimized_df[col]):
            if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                optimized_df[col] = optimized_df[col].astype(np.int8)
            elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                optimized_df[col] = optimized_df[col].astype(np.int16)
            elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                optimized_df[col] = optimized_df[col].astype(np.int32)
            else:
                optimized_df[col] = optimized_df[col].astype(np.int64)
        else:
            if col_min >= np.finfo(np.float16).min and col_max <= np.finfo(np.float16).max:
                optimized_df[col] = optimized_df[col].astype(np.float16)
            elif col_min >= np.finfo(np.float32).min and col_max <= np.finfo(np.float32).max:
                optimized_df[col] = optimized_df[col].astype(np.float32)
            else:
                optimized_df[col] = optimized_df[col].astype(np.float64)
    
    # Optimize object columns
    for col in optimized_df.select_dtypes(include=['object']).columns:
        num_unique_values = len(optimized_df[col].unique())
        num_total_values = len(optimized_df[col])
        if num_unique_values / num_total_values < 0.5:
            optimized_df[col] = optimized_df[col].astype('category')
    
    return optimized_df

def optimize_dfs(data_dict,category):
    '''
    Loads data according to the category in a df and stores it in the dictionary

    '''
    for index,path in enumerate(data_dict[category]): 
        print(path)   
        temp_df = pd.read_csv(path)
        optimized_df = optimize_dataframe(temp_df)
        optimized_df.to_pickle(f'{optimized_df_path}/{category}_{index}.pkl')
        data_dict[index] = f'{optimized_df_path}/{category}_{index}.pkl'

def load_data(data_dict,category):
    '''
    Loads data according to the category in a df and stores it in the dictionary

    the data should be pickle files
    '''
    df_list = []
    for path in data_dict[category]:    
        temp_df = pd.read_pickle(path)
        df_list.append(temp_df)
    data_dict[category] = df_list