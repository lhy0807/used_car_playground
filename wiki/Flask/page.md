# System Requirement

You operating system has to be either:
- Ubuntu 16.04 LTS (“Xenial”)
- Ubuntu 18.04 LTS (“Bionic”)

Other operating systems may also work, but those have not been tested yet.

# Pull the Git Repo

`git pull https://github.com/lhy0807/used_car_playground.git`

# Installation for Flask, PyMongo, and GeoPandas

Flask is a micro web framework written in Python

`pip install Flask`

PyMongo is a Python distribution containing tools for working with MongoDB

`pip install pymongo`

GeoPandas extends the datatypes used by pandas to allow spatial operations on geometric types.

`pip install geopandas`

You should have no problem installing these packages.

# atlas_db.py

navigate to **gpdapp** folder

`cd gpdapp`

* If you are a team member of the Used Car Playground project, you should ask for a created **atlas_db.py** with connection info of the project database

* Otherwise, create a file under gpdapp directory called **atlas_db.py**. Inside the file, paste and assign your MongoDB connection info to variable **atlas**, such as `atlas = 'mongodb://localhost:27017'`

# Run **save_geojson.py**

Before running, create a folder

`mkdir geojson`


Currently, we have our data analysis module in **save_geojson.py**. Running this file would create a **ny.geojson** which contains the map info of New York and several json files containing calculated *Points* and *Quantity* of each car model.

`python save_geojson.py`

Now, you should run Flask webapp successfully

`python main.py`

Note that the webapp will be hosted on port **5100**