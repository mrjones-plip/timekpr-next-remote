import main
import conf, re
from fabric import Connection
from paramiko.ssh_exception import AuthenticationException
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/config")
def config():
    return main.get_config()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)