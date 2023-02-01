# Weather API

This API allows you to access weather and yield data for various locations and years. The data can be filtered by date and location. The API also provides statistical information on the weather data.

## Features
- Retrieve weather data for a specific date and location
- Retrieve yield data for a specific year
- Retrieve statistical information on the weather data, including the maximum, minimum, and total precipitation for a specific date and location



# Installation

>Install the required packages:
```base
pip install -r requirements.txt
```

## Usage

- Run the following command to create the database and populate it with data:

```bash
python -m flask create
```

- Start the API server
```bash
 python -m flask run
```
- The API can now be accessed at http://localhost:5000.

### Endpoints
##### Weather data
```
GET /api/weather/
```
This endpoint returns a paginated list of weather records. You can filter the results by date and station using query parameters:
```
GET /api/weather/?date=19850103&station=USC00257715
```
##### Yield data
```
GET /api/yield/
```
This endpoint returns a paginated list of yield records
##### Statistics
```
GET /api/weather/stats/

```
This endpoint returns statistical information about the weather data. You can filter the results by date and station using query parameters, in the same way as the /api/weather/ endpoint.

### Example Request

``` bash
 curl -X GET "http://localhost:5000/api/weather?date=19850103&station=USC00257715"
```
### Example Response
```json
[{"date":"19850103","maximum_temperature":22,"minimum_temperature":-111,"precipitation":0,"station":"USC00257715"}]
```


# Testing

## Run the tests

```bash
pytest -v
```