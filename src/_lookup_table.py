import pandas as pd


def _load_lookup_table() -> pd.DataFrame:
    '''
    Has columns: Kachelname, Aktualitaet, Bildflugnummer, Koordinatenursprung_East, Koordinatenursprung_North
    '''
    df_lookup_table = pd.read_csv("../data/meta/image_lookup_table.csv", delimiter=";")  
    return df_lookup_table


def _get_city_image_data(city_name: str, df_lookup_table: pd.DataFrame) -> pd.DataFrame:
    '''
    Get rows where city_name is found in Bildflugnummer and return rows
    '''
    df_lookup_table =  df_lookup_table[df_lookup_table["Bildflugnummer"].str.contains(city_name)]
    df_lookup_table.reset_index(inplace = True)
    return df_lookup_table


def get_city_data_lookup_table(city_name: str) -> pd.DataFrame:
    df_lookup_table = _load_lookup_table()
    df_lookup_table = _get_city_image_data(city_name, df_lookup_table)

    return df_lookup_table

