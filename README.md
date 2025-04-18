# pmwraster
A sample (simple) raster API using FastAPI and Rasterio.
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
```
curl -X 'GET' \
  'http://127.0.0.1:8001/images/nebraska_30m_soc_4326/query?lat=41.94220050&lon=-97.91683807' \
  -H 'accept: application/json'
```