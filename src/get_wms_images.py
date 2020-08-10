'''
More convenient method of requesting georeferenced images tiles by wms services
See: 
- Overview service: https://www.bezreg-koeln.nrw.de/brk_internet/geobasis/webdienste/geodatendienste/ (Luftbildinformationen)
- Usage wms: https://www.bezreg-koeln.nrw.de/brk_internet/geobasis/webdienste/anleitung_capabilities.pdf

Script call example (bigger area of Cologne, Germany):
$python get_wms_images.py --xmin 352568 --ymin 5640781 --xmax 360564 --ymax 5648837 --resolution 100

Request NRW Geoportal webservice
Current version:
https://www.wms.nrw.de/geobasis/wms_nw_dop?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&LAYERS=nw_dop_rgb&STYLES=&CRS=EPSG:25832&WIDTH=400&HEIGHT=400&BBOX=354000,5642300,354100,5642400

Historical:
https://www.wms.nrw.de/geobasis/wms_nw_hist_dop?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&LAYERS=nw_hist_dop_2016&STYLES=&CRS=EPSG:25832&WIDTH=400&HEIGHT=400&BBOX=354000,5642300,354100,5642400

Available Layer: 1998, 2003 (lower resolution!), 2007, 2010, 2013, 2016 (winter?)

Get request 100 x 100 meter tiles from bounding box area.
'''
import os
import shutil
from typing import Any, Dict, List

import click
import cv2
import numpy as np
import requests


BASE_URL = "../data/exports"
FILETYPE_ENDING = "png"


def _show_image(image: np.array) -> None:
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _request_wms(bounding_box: List[int], resolution: int, layer_year: str, collection_name: str) -> None:
    '''
    Choose wms by layer_year: 2020 is current, everthing else is historic
    '''
    xmin = bounding_box[0]
    ymin = bounding_box[1]
    xmax = bounding_box[2]
    ymax = bounding_box[3]

    file_name = f"{xmin}_{ymin}_{xmax}_{ymax}.{FILETYPE_ENDING}"
    
    enhance_image = False
    if layer_year == "2020":  # wms for current images
        url = f"https://www.wms.nrw.de/geobasis/wms_nw_dop?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&LAYERS=nw_dop_rgb&STYLES=&CRS=EPSG:25832&WIDTH={resolution}&HEIGHT={resolution}&BBOX={xmin},{ymin},{xmax},{ymax}"
    else:  # wms for historic images; choose layer with layer_year 
        url = f"https://www.wms.nrw.de/geobasis/wms_nw_hist_dop?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&LAYERS=nw_hist_dop_{layer_year}&STYLES=&CRS=EPSG:25832&WIDTH={resolution}&HEIGHT={resolution}&BBOX={xmin},{ymin},{xmax},{ymax}"

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        image = np.asarray(bytearray(r.raw.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite(f"{BASE_URL}/{collection_name}/{file_name}", image)


def _create_tile_bounds(xmin: int, ymin: int, xmax: int, ymax: int) -> List[int]:
    '''
    Devide the area into <steps> x <steps> m tiles and return upper left / lower right bounding box x,y of each tile
    '''
    step = 100  # 100 meter
    tiles_bounding_boxes: List[int] = []
    new_xmin = xmin  # i.e. 353900 -> 357400

    while (new_xmin+step) < xmax + step:  
        current_xmin = new_xmin
        new_xmin = new_xmin+step
        
        new_ymin = ymin  # i.e. 564200 -> 564700new_ymin = ymin  # i.e. 564200 -> 564700
        while (new_ymin+step) < ymax + step:  
            current_ymin = new_ymin
            new_ymin = new_ymin+step
            tiles_bounding_boxes.append([current_xmin, current_ymin, new_xmin, new_ymin])
        
    return tiles_bounding_boxes


def _create_collection_dir(collection_name: str) -> None:
    directory = f"{BASE_URL}/{collection_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)


@click.command()
@click.option('--xmin', default=None, help="upper left x", type=int)
@click.option('--ymin', default=None, help="upper left y", type=int)
@click.option('--xmax', default=None, help="lower right x", type=int)
@click.option('--ymax', default=None, help="lower right y", type=int)
@click.option('--resolution', default=400,  help="Height and width pixel resolution (Default: 400)", type=int)
@click.option('--name', default="default", help="Name of the collection", type=str)
@click.option('--layer', default=None, help="Available layer for years: 1998, 2003, 2007, 2010, 2013, 2016, 2020", type=str)
def request_images(xmin, ymin, xmax, ymax, resolution, name, layer) -> None:
    '''
    Area of interest:
    get_wms_images.py --xmin 353900 --ymin 5642000 --xmax 357400 --ymax 5647000 --name 2020_1 --layer 2020
    get_wms_images.py --xmin 354870 --ymin 5645440 --xmax 355220 --ymax 5645880 --name 2020_stadtgarten --layer 2020
    '''
    try:
        # print(xmin, ymin, xmax, ymax, name, resolution, layer)
        if layer is None:
            raise Exception

        _create_collection_dir(name)

        tiles_bounding_boxes = _create_tile_bounds(xmin, ymin, xmax, ymax)
        for tile_bounding_box in tiles_bounding_boxes:
            _request_wms(tile_bounding_box, resolution, layer, name)
    except Exception as e:
        print(f"ERROR! {e}")
    
    
if __name__ == "__main__":
    request_images()