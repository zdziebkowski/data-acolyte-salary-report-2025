import pandas as pd
import numpy as np


def split_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the dataset into two DataFrames based on the 'pracuje_z_danymi' column.

    Parameters:
    df (pd.DataFrame): The original DataFrame.

    Returns:
    tuple: A tuple containing two DataFrames - one for those working with data and one for those seeking work.
    """
    df_pracujacy = df[df['pracuje_z_danymi'] == 'Tak'].copy()
    df_oczekiwania = df[df['pracuje_z_danymi'] == 'Nie'].copy()
    return df_pracujacy, df_oczekiwania


def clean_salary_value(value: str) -> int:
    """
    Clean a single salary value by removing non-numeric characters and converting to numeric type.

    Parameters:
    value (str): The salary value as a string.

    Returns:
    float: The cleaned salary value as a float.
    """
    if isinstance(value, (int, float)):
        return float(value)

    value = value.replace('k', '').replace(' i więcej', '').replace(' i mniej', '')
    try:
        numeric_value = float(value)
        numeric_value *= 1000
        return numeric_value
    except ValueError:
        return np.nan


def clean_salary_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Clean the salary column by removing non-numeric characters and converting to numeric type.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the salary column.
    column_name (str): The name of the salary column to clean.

    Returns:
    pd.DataFrame: The DataFrame with the cleaned salary column.
    """
    df[column_name] = df[column_name].apply(clean_salary_value)
    return df


def clean_expirence_value(value: str) -> int:
    """
    Clean a single experience value by removing non-numeric characters and converting to numeric type.

    Parameters:
    value (str): The experience value as a string.

    Returns:
    float: The cleaned experience value as a float.
    """
    if isinstance(value, (int, float)):
        return float(value)
    
    if 'rok i mniej' in value:
        return 1.0
    if 'lat i więcej' in value or 'i więcej' in value:  # obsłuży "6 lat i więcej"
        return 6.0

    value = value.replace(' lata', '').replace(' lat', '')
    try:
        numeric_value = float(value)
        return numeric_value
    except ValueError:
        return np.nan
    

def clean_experience_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Clean the experience column by removing non-numeric characters and converting to numeric type.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the experience column.
    column_name (str): The name of the experience column to clean.

    Returns:
    pd.DataFrame: The DataFrame with the cleaned experience column.
    """
    df[column_name] = df[column_name].apply(clean_expirence_value)
    return df