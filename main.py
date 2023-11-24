## Importing
from flask import Flask, render_template, jsonify
from dbutils.pooled_db import PooledDB
import pandas as pd
import sqlite3

def get_api_keys():
    connection = PooledDB(sqlite3, maxconnections=10, database="api_keys.sql").connection()
    cursor = connection.cursor()
    api_keys = []
    for row in cursor.execute("SELECT * FROM API_KEYS"):
        api_keys.append(row[1])
    cursor.close()
    connection.close()
    return api_keys

## Initiating the app
app = Flask(__name__)

## Adding the "stations.txt" file here
stations = pd.read_csv("data/stations.txt", skiprows=17)
stations["Station ID"] = stations["STAID"]
stations["Station"] = stations["STANAME                                 "]
stations = stations[["Station ID", "Station"]]

@app.route("/")
def home():
    return render_template('home.html', data=stations.to_html(index=False, justify="center"))


@app.route("/api/exact_date/<station>/<date>/api_key=<api_key>")
def data(station, date, api_key):
    api_keys = get_api_keys()
    if api_key in api_keys:
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
    else:
        return "API KEY INCORRECT!"

@app.route("/api/all_data_for_station/<station>/api_key=<api_key>")
def all_station_data(station, api_key):
    api_keys = get_api_keys()
    if api_key in api_keys:
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
    else:
        return "INCORRECT API KEY!"

@app.route("/api/all_data_for_station_annual/<station>/<year>/api_key=<api_key>")
def all_station_data_annual(station, year, api_key):
    api_keys = get_api_keys()
    if api_key in  api_keys:
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
    else:
        return "INCORRECT API KEY!"

if __name__ == "__main__":
    app.run(debug=False)
