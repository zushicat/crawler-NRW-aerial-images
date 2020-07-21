This dataset dop_nw.csv is a very reduced version of [Metadaten zum Datensatz](https://www.geoportal.nrw/suche?lang=de&searchTerm=56fb584b-10cf-4009-a405-0bef06bb3e00), used as a lookup table
- {city name} -> {image file name} for image crawling
- {image file name} -> {east/north coordinates} for application after crawling

The following columns are available in this reducced dataset:
- Kachelname (i.e. dop10rgbi_32_442_5764_1_nw)
- Aktualitaet (i.e. 2017-03-25)
- Bildflugnummer (i.e. 1255/17 Münster-Warendorf)
- Koordinatenursprung_East (i.e. 442000)
- Koordinatenursprung_North (i.e. 5764000)


**Note**    
All of the images have a value of 10000 both for Anzahl_Spalten and Anzahl_Zeilen (in the original dataset), which equals a 10000 x 10000 pixel resolution for each image.
