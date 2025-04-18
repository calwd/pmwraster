# pmwraster
A sample (simple) raster API using FastAPI and Rasterio.


## Notes
- This project currently contains two separate raster datasets that can be queried against: 
  - Nebraska 30m Soil Organic Carbon (SOC) raster dataset (EPSG:4326): `nebraska_30m_soc_4326`
  - Nebraska 30m Soil Organic Carbon (SOC) raster dataset with a different coordinate system (EPSG:3857): `nebraska_30m_soc`
This is done to demonstrate the API's ability to handle different coordinate systems and to show how the API can be extended to support multiple datasets.
  
- The folder structure of this project strays from the typical FastAPI project structure. This is intentional to keep the project simple and focused on the raster API functionality.
- Even though the assignment is to create a simple API for querying a single raster, the project is structured to allow for multiple raster datasets. This is done by creating a folder for each dataset and placing the raster files inside that folder. The API can be easily extended to support more datasets by adding more folders and updating the code accordingly.
- All pixel value queries use latitude / longitude values (assuming EPSG:4326). The API will convert the lat/lon values to the raster's coordinate system. This is done to ensure that the API can handle different raster datasets with different coordinate systems.
- The Endpoint paths for this project vary slightly from the assignment in order to facilitate multiple raster datasets in the future.
- Code was linted using ruff, type-checked using mypy, and formatted using isort and black
- Given time constraints, test coverage as not written for these endpoints. However, the groundwork for those tests was created and can be seen in the `conftest.py` file


## Installation Instructions

#### Clone the repository via SSH
```
git clone git@github.com:calwd/pmwraster.git

```

#### Change directory to the cloned repository`
```
cd pmwraster
```

#### Build the Docker image
```
docker build -t pmwraster .
```

#### Run the Docker image
```
docker run -p 8001:8001 pmwraster
```

#### View the API docs
http://localhost:8001/docs

#### Test the API

You can test the API using curl or any HTTP client of your choice. Here are some example curl commands:
- Query the Nebraska 30m SOC raster dataset (EPSG:4326) using latitude and longitude coordinates:
```
curl -X 'GET' \
  'http://127.0.0.1:8001/images/nebraska_30m_soc_4326/query?lat=41.94220050&lon=-97.91683807' \
  -H 'accept: application/json'
```

- Query the Nebraska 30m SOC raster dataset (EPSG:3857) using latitude and longitude coordinates:
```
curl -X 'GET' \
  'http://127.0.0.1:8001/images/nebraska_30m_soc/query?lat=41.94220050&lon=-97.91683807' \
  -H 'accept: application/json'
```


