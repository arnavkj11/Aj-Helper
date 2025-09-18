from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080) # Use port 8080 or another suitable port

def keep_alive():
    t = Thread(target=run)
    t.start()