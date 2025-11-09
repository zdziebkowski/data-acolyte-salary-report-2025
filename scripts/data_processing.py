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


TOOL_MAPPING = {
    'pbi': 'power bi',
    'power query': 'power bi',
    'power bi desktop': 'power bi',
    'power bi service': 'power bi',
    'fabric': 'microsoft fabric',
    'postgres': 'postgresql',
}

SPECIAL_CASES = {
    'Sql': 'SQL',
    'Sap': 'SAP',
    'Dax': 'DAX',
    'Ai': 'AI',
    'Power Bi': 'Power BI',
    
    'Ssms': 'SSMS',
    'Ssrs': 'SSRS',
    'Ssas': 'SSAS',
    'Ssis': 'SSIS',
    'T-Sql': 'T-SQL',
    
    'Javascript': 'JavaScript',
    'Php': 'PHP',
    'C#': 'C#',
    
    'Latex': 'LaTeX',
    'Postgresql': 'PostgreSQL',
    'Ms Lists': 'MS Lists',
    'Langchain': 'LangChain',
    'Microsoft Fabric': 'Microsoft Fabric',
}


def normalize_tool_name(tool_name: str) -> str or None:
    """
    Normalize a single tool name.
    1. Remove garbage
    2. Map synonyms (only real synonyms)
    3. Capitalize all
    4. Override special cases (acronyms)
    
    Returns None for garbage entries.
    """
    if not isinstance(tool_name, str):
        return None
    
    normalized = tool_name.strip().lower()
    
    if len(normalized) > 30:
        return None
    if '!' in normalized or '?' in normalized:
        return None
    if len(normalized) < 2:
        return None
    
    if normalized in TOOL_MAPPING:
        normalized = TOOL_MAPPING[normalized]
    
    normalized = normalized.title()
    
    if normalized in SPECIAL_CASES:
        normalized = SPECIAL_CASES[normalized]
    
    return normalized

def clean_tools_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Clean the tools column by splitting the string into a list of tools.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the tools column.
    column_name (str): The name of the tools column to clean.

    Returns:
    pd.DataFrame: The DataFrame with the cleaned tools column.
    """
    def clean_and_normalize(x):
        if not isinstance(x, str):
            pass
        
        tools = [tool.strip() for tool in x.split(',')]
        
        normalized_tools = [normalize_tool_name(tool) for tool in tools]
        
        clean_tools = [t for t in normalized_tools if t is not None]
        
        return clean_tools
    
    df[column_name] = df[column_name].apply(clean_and_normalize)
    return df


def clean_working_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove irrelevant columns from working people dataset.
    """
    return df.drop(columns=['oczekiwania_junior'])


def clean_jobseekers_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove work-related columns from job seekers dataset.
    """
    columns_to_drop = ['stanowisko', 'typ_umowy', 'wymiar', 'zarobki', 'doswiadczenie', 'narzedzia']
    return df.drop(columns=columns_to_drop)