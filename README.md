# Used Car Playground
![NY Average Points](ny.png "NY Average Points")

This is the repo for Used Car Playground project  

Used Car Playground project is a research project related to used car data

Map Data is obtained from [ArcGIS, shared by ESRI](https://www.arcgis.com/home/item.html?id=8d2012a2016e484dafaac0451f9aea24)

To run the scrapy spyder in usedcar folder, please read [the wiki page](https://github.com/lhy0807/used_car_playground/wiki/Used-Car-Data-Scrapper) and make sure you have followed the instructions before entering

```bash
scrapy crawl usedcar
```

To visualize the data, run the following in root directory:
```bash
jupyter notebook "Used Car Playground.ipynb"
```

~~To start bokeh application~~
```bash
chmod +x run_bokehapp.sh
./run_bokehapp.sh
```

To run Flask webapp, follow [the wiki instructions](https://github.com/lhy0807/used_car_playground/wiki/Flask)

`pip install Flask`

`pip install pymongo`

`pip install geopandas`