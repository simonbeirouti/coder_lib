from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Online library under construction</h1>'