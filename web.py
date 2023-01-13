import main
import conf, re
from fabric import Connection
from paramiko.ssh_exception import AuthenticationException
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/config")
def config():
    return main.get_config()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_usage/<computer>/<user>")
def get_usage(computer, user):
    # todo - validate computer and user exist in config
    ssh = main.get_connection(computer)
    return main.get_usage(user, computer, ssh)


@app.route("/increase_time/<computer>/<user>/<seconds>")
def increase_time(computer, user, seconds):
    # todo - validate computer and user exist in config
    ssh = main.get_connection(computer)
    if main.increase_time(seconds, ssh, user):
        return "done"
    else:
        return "fail", 404


@app.route("/decrease_time/<computer>/<user>/<seconds>")
def decrease_time(computer, user, seconds):
    # todo - validate computer and user exist in config
    ssh = main.get_connection(computer)
    if main.decrease_time(seconds, ssh, user):
        return "done"
    else:
        return "fail", 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
