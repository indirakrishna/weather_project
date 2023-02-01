import click
from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

try:
    from .ingest import (
        generate_statistics,
        ingest_yld_data,
        ingest_wx_data,
    )
except Exception:
    from ingest import (
        generate_statistics,
        ingest_yld_data,
        ingest_wx_data,
    )


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example2.sqlite"
db = SQLAlchemy(app)


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(15))
    date = db.Column(db.String(8))
    maximum_temperature = db.Column(db.Integer)
    minimum_temperature = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            "station": self.station,
            "date": self.date,
            "maximum_temperature": self.maximum_temperature,
            "minimum_temperature": self.minimum_temperature,
            "precipitation": self.precipitation,
        }


class YieldData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(4))
    harvested_val = db.Column(db.Integer)

    @property
    def serialize(self):
        return {"year": self.year, "harvested_val": self.harvested_val}


class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(15))
    date = db.Column(db.String(8))
    final_maximum_temperature = db.Column(db.Integer)
    final_minimum_temperature = db.Column(db.Integer)
    final_precipitation = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            "station": self.station,
            "date": self.date,
            "final_maximum_temperature": self.final_maximum_temperature,
            "final_minimum_temperature": self.final_minimum_temperature,
            "final_precipitation": self.final_precipitation,
        }


@click.command(name="create")
def create():
    with app.app_context():
        db.drop_all()
        db.create_all()
        ingest_wx_data()
        ingest_yld_data()
        generate_statistics()


@app.route("/api/weather/", methods=["GET"])
def weather_main():
    page = request.args.get("page", type=int)
    date = request.args.get("date")
    station = request.args.get("station")
    result = WeatherData.query
    if date:
        result = result.filter(WeatherData.date == date)
    if station:
        result = result.filter(WeatherData.station == station)

    return jsonify([r.serialize for r in result.paginate(page=page, per_page=100)])


@app.route("/api/yield/", methods=["GET"])
def yield_main():
    page = request.args.get("page", type=int)
    return jsonify(
        [r.serialize for r in YieldData.query.paginate(page=page, per_page=100)]
    )


@app.route("/api/weather/stats/", methods=["GET"])
def stats():
    page = request.args.get("page", type=int)
    date = request.args.get("date")
    station = request.args.get("station")
    result = Statistic.query
    if date:
        result = result.filter(Statistic.date == date)
    if station:
        result = result.filter(Statistic.station == station)

    return jsonify([r.serialize for r in result.paginate(page=page, per_page=100)])


if __name__ == "__main__":
    app.run(debug=True)

app.cli.add_command(create)
