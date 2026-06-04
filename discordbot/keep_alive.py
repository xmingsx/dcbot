from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Discord đang hoạt động!"

def run():
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False,
        use_reloader=False
    )

def keep_alive():
    server = Thread(target=run, daemon=True)
    server.start()
