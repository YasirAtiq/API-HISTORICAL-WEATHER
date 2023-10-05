## Importing
from flask import Flask, render_template
import pandas as pd
import matplotlib as plot

## Initiating the app
app = Flask(__name__)



@app.route("/")
def home():
    return render_template('home.html')


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    ## Reading the data
    filename = f"data\\TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    ## Showing the API
    return {"station": station,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)
