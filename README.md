# perennial-raster
Sample code submission for perennial



### Basic tests to ensure the API is working properly
```
curl -X 'GET' \
  'http://127.0.0.1:8001/images/nebraska_30m_soc_4326/query?lat=41.94220050&lon=-97.91683807' \
  -H 'accept: application/json'
```