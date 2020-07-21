from _lookup_table import get_city_data_lookup_table
from _image_crawler import crawl_municipal_images

import click
import pandas as pd


@click.command()
@click.option('--municipal', default="Köln", help="NRW municipal / city (Default: \"Köln\")")
@click.option('--resolution', default=1000,  help="Height and width pixel resolution (Default: 1000)")
def request_images(municipal, resolution) -> None:
    df_lookup_table: pd.DataFrame = get_city_data_lookup_table(municipal)
    crawl_municipal_images(df_lookup_table)


if __name__ == "__main__":
    request_images()
