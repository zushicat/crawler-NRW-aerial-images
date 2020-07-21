import cv2
import numpy as np
import pandas as pd
import requests


BASE_URL = "https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10"
FILETYPE_ENDING = "jp2"


def _recalc_image(image: np.array) -> None:
    dim = (1000, 1000)
    
    # resize image
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    # for testing
    cv2.imshow('image', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _get_images_data(image_file_name: str) -> None:
    '''
    Image format: jp2 (JPEG2000)
    Incoming filename has no filetype ending.
    '''
    url: str = f"{BASE_URL}/{image_file_name}.{FILETYPE_ENDING}"
    r = requests.get(url, stream=True).raw

    image = np.asarray(bytearray(r.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    _recalc_image(image)


def crawl_municipal_images(df_lookup_table: pd.DataFrame) -> None:
    '''
    Incoming dataframe with rows:
    Kachelname                   dop10rgbi_32_320_5648_1_nw
    Aktualitaet                                  2019-06-17
    Bildflugnummer                   1313/19 Erftkreis Köln
    Koordinatenursprung_East                         320000
    Koordinatenursprung_North                       5648000
    '''
    for index, row in df_lookup_table.iterrows():
        file_name: str = row["Kachelname"]
        print(index, file_name)
        _get_images_data(file_name)
        break