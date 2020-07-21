# crawler-aerial-images
Crawl arial images (published by Bezirksregierung NRW) of a selected city in North Rhine-Westphalia and save those images on the fly with reduced resolution.     

The original images have a tremendously high resolution (10cm per pixel), which is far too high for many computer vision applications (i.e. object detection with machine learning techniques).    
Hence this little crawler to automatically create instantly useable imagesets.    



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
