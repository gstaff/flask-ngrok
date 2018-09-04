# flask-ngrok
A simple way to demo Flask apps from your machine.
Makes your [Flask](http://flask.pocoo.org/) apps running on localhost available
 over the internet via the excellent [ngrok](https://ngrok.com/) tool.

## Compatability
Python 3.6+ is required.

## Installation
```bash
pip install Flask flask-ngrok
```

## Quickstart
1. Import with `from flask_ngrok import run_with_ngrok`
2. Add `run_with_ngrok(app)` to make your Flask app available upon running
```python
# flask_ngrok_example.py
from flask import Flask
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
```

```bash
python flask_ngrok_example.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Running on http://<random-address>.ngrok.io
 * Traffic stats available on http://127.0.0.1:4040 
```