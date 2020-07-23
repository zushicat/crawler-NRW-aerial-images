import os
import shutil

import cv2
import glymur
import numpy as np
import pandas as pd
import requests


# suppress warnings
import warnings
warnings.filterwarnings("ignore")


BASE_URL = "https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10"
FILETYPE_ENDING = "jp2"
TMP_IMAGE_PATH = "../data/tmp"

BOUNDING_BOX_COLOGNE_CITY = (352568, 5640781, 360564, 5648837)  # (6.903348, 50.899846, 7.013891, 50.974231)


def _show_image(image: np.array) -> None:
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _resize_image(image: np.array, resolution: int) -> np.ndarray:
    dim = (resolution, resolution)
    image = cv2.resize(image, dim)
    
    return image


def _split_into_subimages(municipal: str, image_file_name: str, coord_x: int, coord_y: int, resolution: int) -> None:
    '''
    https://stackoverflow.com/a/53388729
    '''
    print("split into tiles...")
    image = cv2.imread(f"{TMP_IMAGE_PATH}/{image_file_name}.png")
    
    tmp_image = image
    height, width = image.shape[:2]

    # move origin value of top left point
    coord_x = coord_x
    coord_y = coord_y + 1000

    add_to_coord = 100

    CROP_W_SIZE = 10 # Number of pieces Horizontally 
    CROP_H_SIZE = 10 # Number of pieces Vertically to each Horizontal  

    for i in range(CROP_W_SIZE):
        for j in range(CROP_H_SIZE):

            x = int(width / CROP_W_SIZE * i)
            y = int(height / CROP_H_SIZE * j)

            h = int(height / CROP_H_SIZE)
            w = int(width / CROP_W_SIZE)

            new_coord_x = coord_x + i * add_to_coord
            new_coord_y = coord_y - (j+1) * add_to_coord

            new_file_name = f"{new_coord_x}_{new_coord_y}_{new_coord_x + add_to_coord}_{new_coord_y + add_to_coord}"
            
            tmp_image = tmp_image[y:y+h, x:x+w]
            tmp_image = _resize_image(tmp_image, resolution)
            
            # save tile
            _save_resized_tile_image(tmp_image, new_file_name, municipal)
            
            tmp_image = image
    
    # delete image
    os.remove(f"{TMP_IMAGE_PATH}/{image_file_name}.png")


def _save_rgb_image(image_file_name: str) -> None:
    print("converting image to rgb...")
    # 4 channel jp2 seems to be problematic in opencv
    jp2 = glymur.Jp2k(f"{TMP_IMAGE_PATH}/{image_file_name}.{FILETYPE_ENDING}")
    # numpy array with 4 channels shape: (10000, 10000, 4)
    image = jp2[:] 
    # convert to rgb
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

    # save converted file
    cv2.imwrite(f"{TMP_IMAGE_PATH}/{image_file_name}.png", image)
    
    # delete old 4 channel jp2 file
    os.remove(f"{TMP_IMAGE_PATH}/{image_file_name}.{FILETYPE_ENDING}")
    

def _save_resized_tile_image(image: np.array, image_file_name: str, municipal: str) -> None:
    cv2.imwrite(f"../data/exports/{municipal}/{image_file_name}.png", image)


def _crawl_images_data(image_file_name: str) -> None:
    '''
    Image format: 4 channel jp2 (JPEG2000)
    Incoming filename has no filetype ending.
    '''
    print("crawling image...")

    url: str = f"{BASE_URL}/{image_file_name}.{FILETYPE_ENDING}"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(f"{TMP_IMAGE_PATH}/{image_file_name}.{FILETYPE_ENDING}", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)    


def _create_dir_for_processed_images(municipal: str) -> None:
    directory = f"../data/exports/{municipal}"
    if not os.path.exists(directory):
        os.makedirs(directory)

def crawl_municipal_images(municipal: str, df_lookup_table: pd.DataFrame, resolution: int) -> None:
    '''
    Incoming dataframe with rows:
    Kachelname                   dop10rgbi_32_320_5648_1_nw
    Aktualitaet                                  2019-06-17
    Bildflugnummer                   1313/19 Erftkreis Köln
    Koordinatenursprung_East                         320000
    Koordinatenursprung_North                       5648000
    '''
    _create_dir_for_processed_images(municipal)

    i = 0
    for index, row in df_lookup_table.iterrows():
        try:
            file_name: str = row["Kachelname"]
            x: int = row["Koordinatenursprung_East"]
            y: int = row["Koordinatenursprung_North"]

            
            # tmp: Cologne (inner) city specific bounding box
            # BOUNDING_BOX_COLOGNE_CITY = (352568, 5640781, 360564, 5648837) -> # 64 images (out of 1092)
            if municipal == "Köln":
                if x < BOUNDING_BOX_COLOGNE_CITY[0] or x > BOUNDING_BOX_COLOGNE_CITY[2]:
                    continue
                if y < BOUNDING_BOX_COLOGNE_CITY[1] or y > BOUNDING_BOX_COLOGNE_CITY[3]:
                    continue

            print(i, file_name, x, y)
            i += 1
            
            _crawl_images_data(file_name)
            _save_rgb_image(file_name)
            _split_into_subimages(municipal, file_name, x, y, resolution)
            
            print("---")
        except Exception as e:
            pass  # print(f"Error at {index}: {file_name} - {e}")

        
