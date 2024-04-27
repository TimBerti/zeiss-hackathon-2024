from datetime import datetime
from functools import update_wrapper, wraps
from flask import Flask, make_response, request, render_template

from . import database

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def jsonifyexceptions(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            return {
                "status": "error",
                "message": f"{type(ex).__name__} {ex}",
            }

    return wrapper


def nocache(view):

    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route("/")
@nocache
def home():
    return render_template("index.html")

@app.route("/statusmask", methods=["GET"])
@nocache
def statusmask_get():
    return {
        "status": "success",
        "data": database.get_status_mask(),
    }

@app.route("/statusmask", methods=["POST"])
@jsonifyexceptions
def statusmask_post():
    mask = request.get_json()["data"]
    database.set_status_mask(mask)
    return {"status": "success"}


@app.route("/reserve/<int:desk_id>")
@nocache
@jsonifyexceptions
def reserve(desk_id: int):
    database.make_reservation(desk_id)
    return {"status": "success"}
