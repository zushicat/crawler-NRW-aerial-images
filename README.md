# crawler-aerial-images
Crawl aerial images (published by Bezirksregierung NRW) of a selected areas in North Rhine-Westphalia and save tiles of those images on the fly with reduced resolution.     


### Update
Use the wms service by selecting a bounding box of an area to request (**recommended**). This area will be divided into 100 x 100 meter tiles and saved into a (by parameter) defined directory.
The file naming has following pattern:
```
<xmin>_<ymin>_<xmax>_<ymax>.png
```
Example for an area within the inner city of Cologne, Germany:
```
get_wms_images.py --xmin 353900 --ymin 5642000 --xmax 357400 --ymax 5647000 --name 2020_1 --resolution 400 --layer 2020
```

You can choose between current and historical images, where 2020 requests the current images and all other values request the layers of the wms service for historical images.    

Use the parameters as followed:
- xmin, ymin, xmax, ymax: the x,y values of the bounding box of 
- name: the name of the directory where the tile images are stored
- resolution: the resolution of the tiles
- layer: choose year for historical images

Regarding the layer parameter:
- 2020 requests current images
- The availability of images per year are defined as a so called layer. Please check http://www.wms.nrw.de/geobasis/wms_nw_hist_dop?VERSION=1.3.0&SERVICE=WMS&REQUEST=GetCapabilities for availability of a given year. 


See: 
- Overview service: https://www.bezreg-koeln.nrw.de/brk_internet/geobasis/webdienste/geodatendienste/ (under: Luftbildinformationen)
- Usage wms: https://www.bezreg-koeln.nrw.de/brk_internet/geobasis/webdienste/anleitung_capabilities.pdf

Please also check the comments in get_wms_images.py 

If an image for a specific request is not available (beside a real request error), the service will return a white (blank) image.


### Usage
Install python environment
```
$ pipenv install
```
and change into shell
```
$ pipenv shell
```
You can exit the shell with
```
$ exit
```
Then change into /src and request a) the webservice
```
$ cd src
$ python get_images.py
```
or b) the wms Service **recommended**
```
$ cd src
$ python get_wms_images.py --xmin 353900 --ymin 5642000 --xmax 357400 --ymax 5647000 --name 2020_1 --layer 2020
```


### If you want to use the webservice 
The original images have a tremendously high resolution (10cm per pixel resp. 10000x10000 pixel), which is far too high for many computer vision applications (i.e. object detection with machine learning techniques).    
Hence this little crawler to automatically create instantly useable imagesets.   

The default call requests "Köln" with a resolution of 400 (pixel width/height). You can specify these parameter:
```
$ python get_images.py --municipal Köln --resolution 400     
```
The --municipal parameter checks for substrings in the column "Bildflugnummer" in the [image_lookup_table.csv](https://github.com/zushicat/crawler-NRW-arial-images/tree/master/data/meta).    


Each 10000 x 10000 pixel image will coverted into RGB and cut into 100 tiles. Each tile will then be reduced to the passed resolution.    

The tiles are saved in /exports under a directory named as the passed municipal. The naming convention is    
x1_y1_x2_y2.png (i.e. 353000_5641000_353500_5641500.png)    

**Note**    
The covered area which falls under one "Bildflugnummer" is way bigger than you might be interested in. Right now (for my own purpose), I manually implemented a bounding box if municipal equals "Köln" to restrict incoming images.     
Please have a look at [_image_crawler.py](https://github.com/zushicat/crawler-NRW-aerial-images/blob/master/src/_image_crawler.py) to change / addapt these values (see: global variable BOUNDING_BOX_COLOGNE_CITY and function crawl_municipal_images)


### About original data
For the official product description of the image sets, please refer to the page [Digitale Orthophotos](https://www.bezreg-koeln.nrw.de/brk_internet/geobasis/luftbildinformationen/aktuell/digitale_orthophotos/index.html) by Bezirksregierung NRW.    

Usage and licensing of these images are defined on that page as followed:    
> Die digitalen Geobasisdaten werden nach Open Data-Prinzipien kostenfrei über automatisierte Abrufverfahren bereitgestellt. Es gelten die durch den IT-Planungsrat im Datenportal für Deutschland (GovData) veröffentlichten einheitlichen Lizenzbedingungen „Datenlizenz Deutschland – Zero“ (dl-de/zero-2-0). Jede Nutzung ist ohne Einschränkungen oder Bedingungen zulässig. Der Lizenztext ist unter www.govdata.de/dl-de/zero-2-0 abrufbar.


There are different bundles available:
- packaged by city / municipality: [Digitale Orthophotos (10-fache Kompression) - Paketierung: Gemeinden](https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/)
- single images, identifiable by file name (via lookup table): [Digitale Orthophotos (10-fache Kompression) - Paketierung: Einzelkacheln](https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10/)

The lookup table (resp. data description per image file) can be found here (zipped .csv):    
[Metadaten zum Datensatz](https://www.geoportal.nrw/suche?lang=de&searchTerm=56fb584b-10cf-4009-a405-0bef06bb3e00)

The reduced version of the lookup table and a short documentation can be found here [image_lookup_table.csv](https://github.com/zushicat/crawler-NRW-arial-images/tree/master/data/meta).
