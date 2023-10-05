## Importing
from flask import Flask
from flask import render_template
import pandas as pd

app = Flask("Website")


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/api/<word>")
def about(word):
    global definition
    df = pd.read_csv("dictionary.csv")
    definition = df.loc[df["word"] == word]["definition"].squeeze()
    return {"definition": definition, "word": word}


if __name__ == "__main__":
    app.run(port=1234)
