from flask import Flask
import os

from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app, '<YOUR AUTH TOKEN HERE>')  # Start ngrok when app is run


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
