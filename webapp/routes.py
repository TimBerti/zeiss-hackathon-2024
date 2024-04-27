from flask import Flask, request, render_template

from . import database

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def jsonifyexceptions(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            return {
                "status": "error",
                "message": str(ex),
            }

    return wrapper


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/statusmask", methods=["GET"])
def statusmask_get():
    return {
        "status": "success",
        "data": database.get_status_mask(),
    }

@app.route("/statusmask", methods=["POST"])
def statusmask_post():
    try:
        mask = request.get_json()["data"]
    except Exception as ex:
        return {
            "status": "error",
            "message": str(ex),
        }
    database.set_status_mask(mask)
    return {"status": "success"}


@app.route("/reserve/<int:desk_id>")
def reserve(desk_id: int):
    try:
        database.make_reservation(desk_id)
    except Exception as ex:
        return {
            "status": "error",
            "message": str(ex),
        }
    return {"status": "success"}
