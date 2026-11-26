from flask import Flask, jsonify, request

from config import Config
from app.controllers.application import Application

app = Flask(__name__, template_folder="app/views/html", static_folder="app/static")
app.config.from_object(Config)

ctl = Application(app.config)
app.add_template_filter(ctl.moeda, "moeda")


@app.get("/")
def index():
    return ctl.render("index")


@app.post("/pedido")
def pedido():
    corpo, status = ctl.criar_pedido(request.get_json(silent=True))
    return jsonify(corpo), status


@app.get("/healthz")
def healthz():
    return "ok", 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
