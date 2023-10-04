## Importing
from flask import Flask, render_template

app = Flask("Website")


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/api/v1/<word>")
def about(word):
    temperature = 23
    return {"definition": word.upper(),
            "word": word}


if __name__ == "__main__":
    app.run(debug=True)
