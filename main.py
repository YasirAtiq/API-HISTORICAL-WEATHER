## Importing
from flask import Flask, render_template
import pandas as pd

## Initiating the app
app = Flask(__name__)

## Adding the "stations.txt" file here
stations = pd.read_csv("data/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route("/")
def home():
    return render_template('home.html', data=stations.to_html())


@app.route("/api/<station>/<date>")
def data(station, date):
    ## Reading the data
    filename = f"data\\TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    ## Showing the API
    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/1/<station>")
def all_station_data(station):
    ## Reading the data
    filename = f"data\\TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df = df.loc[df["   TG"] != -9999]
    df["   TG"] = df["   TG"] / 10
    df = df[["    DATE", "   TG"]]
    ## Generating the API
    result_dict = df.to_dict(orient="records")
    ## Showing the API
    return result_dict

@app.route("/api/v1/yearly/<station>/<year>")
def all_station_data_annual(station, year):
    ## Reading the data
    filename = f"data\\TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df = df.loc[df["   TG"] != -9999]
    df["   TG"] = df["   TG"] / 10
    df["    DATE"] = df["    DATE"].astype(str)
    result_dict = df[df["    DATE"].str.startswith(str(year))].to_dict(
        orient="records")
    return result_dict

if __name__ == "__main__":
    app.run(debug=True)
