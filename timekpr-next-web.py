import functools
import os
from datetime import timedelta

import conf
import main
from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Pflichtwerte aus conf.py
if not getattr(conf, "secret_key", None):
    raise RuntimeError("Missing 'secret_key' in conf.py")

if not getattr(conf, "pin_hash", None):
    raise RuntimeError("Missing 'pin_hash' in conf.py")

app.config["SECRET_KEY"] = conf.secret_key
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def validate_request(computer, user):
    if computer not in conf.trackme:
        return {"result": "fail", "message": "computer not in config"}

    if user not in conf.trackme[computer]:
        return {"result": "fail", "message": "user not in computer in config"}

    return {"result": "success", "message": "valid user and computer"}


def pin_required(view_func):
    @functools.wraps(view_func)
    def wrapped(*args, **kwargs):
        if session.get("pin_ok") is True:
            return view_func(*args, **kwargs)

        return redirect(url_for("login"))
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        pin = request.form.get("pin", "")

        if check_password_hash(conf.pin_hash, pin):
            session.clear()
            session["pin_ok"] = True
            session.permanent = True

            next_url = request.args.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)

            return redirect(url_for("index"))

        error = "Falsche PIN"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/config")
@pin_required
def config():
    return main.get_config()


@app.route("/")
@pin_required
def index():
    return render_template("index.html")


@app.route("/get_usage/<computer>/<user>")
@pin_required
def get_usage(computer, user):
    valid = validate_request(computer, user)
    if valid["result"] == "fail":
        return valid, 500

    ssh = main.get_connection(computer)
    usage = main.get_usage(user, computer, ssh)
    return {
        "result": usage["result"],
        "time_left": usage["time_left"],
        "time_spent": usage["time_spent"],
    }, 200


@app.route("/increase_time/<computer>/<user>/<seconds>")
@pin_required
def increase_time(computer, user, seconds):
    valid = validate_request(computer, user)
    if valid["result"] == "fail":
        return valid, 500

    ssh = main.get_connection(computer)
    if main.increase_time(seconds, ssh, user, computer):
        usage = main.get_usage(user, computer, ssh)
        return {
            "result": "success",
            "time_left": usage["time_left"],
            "time_spent": usage["time_spent"],
        }, 200

    return {"result": "fail"}, 500


@app.route("/decrease_time/<computer>/<user>/<seconds>")
@pin_required
def decrease_time(computer, user, seconds):
    valid = validate_request(computer, user)
    if valid["result"] == "fail":
        return valid, 500

    ssh = main.get_connection(computer)
    if main.decrease_time(seconds, ssh, user, computer):
        usage = main.get_usage(user, computer, ssh)
        return {
            "result": "success",
            "time_left": usage["time_left"],
            "time_spent": usage["time_spent"],
        }, 200

    return {"result": "fail"}, 500


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
