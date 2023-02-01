import pytest
import app

@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    client = app.app.test_client()
    with app.app.app_context():
        app.db.drop_all()
        app.db.create_all()
        weather_data = app.WeatherData(
            station="station_name",
            date="19850101",
            maximum_temperature=1,
            minimum_temperature=1,
            precipitation=10,
        )
        yield_data = app.YieldData(year="2014", harvested_val="20")
        app.db.session.add(yield_data)
        app.db.session.add(weather_data)
        app.db.session.commit()

    yield client


def test_weather_reports(client):
    response = client.get("/api/weather/")
    assert response.status_code == 200
    assert response.json == [
        {
            "date": "19850101",
            "maximum_temperature": 1,
            "minimum_temperature": 1,
            "precipitation": 10,
            "station": "station_name",
        }
    ]


def test_yield_reports(client):
    response = client.get("/api/yield/")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json == [{"harvested_val": 20, "year": "2014"}]
    assert response.json != "[]"
