## Importing
from flask import Flask, render_template, jsonify
import pandas as pd

## Initiating the app
app = Flask(__name__)

## Adding the "stations.txt" file here
stations = pd.read_csv("data/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route("/")
def home():
    return render_template('home.html', data=stations.to_html())


@app.route("/api/exact_date/<station>/<date>")
def data(station, date):
    try:
        ## Reading the data
        filename = f"data\\TG_STAID{str(station).zfill(6)}.txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        try:
            temperature = float(df.loc[df["    DATE"] == date, "   TG"].squeeze() / 10)
        except TypeError:
            return "Record Not Found!"
        date
        ## Showing the API
        record = {"station ID": station,
                "date": date,
                "temperature": temperature}
        record = jsonify(record)
        return record
    except FileNotFoundError:
        return "Record Not Found!"

@app.route("/api/all_data_for_station/<station>")
def all_station_data(station):
    try:
        ## Reading the data
        filename = f"data\\TG_STAID{str(station).zfill(6)}.txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        df = df.loc[df["   TG"] != -9999, ["   TG", "    DATE"]]
        df["temperature"] = df["   TG"] / 10
        df["date"] = df["    DATE"].astype(str)
        df = df[["date", "temperature"]]
        ## Generating the API
        result_dict = df.to_dict(orient="records")
        ## Showing the API
        return result_dict
    except FileNotFoundError:
        return "Record not found!"

@app.route("/api/all_data_for_station_annual/<station>/<year>")
def all_station_data_annual(station, year):
    try:
        ## Reading the data
        filename = f"data\\TG_STAID{str(station).zfill(6)}.txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        df = df.loc[df["   TG"] != -9999, ["   TG", "    DATE"]]
        df["temperature"] = df["   TG"] / 10
        df["date"] = df["    DATE"].astype(str)
        df = df[["date", "temperature"]]
        result_dict = df.loc[df["date"].str.startswith(str(year))].to_dict(
            orient="records")
        result_dict = jsonify(result_dict)
        return result_dict
    except FileNotFoundError:
        return "Record Not Found!"

if __name__ == "__main__":
    app.run(debug=False)
