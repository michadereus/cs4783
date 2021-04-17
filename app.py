# %%
from routes.hello import hello_bp
from routes.properties import properties_bp
from routes.swagger import swagger_bp
from util.response_builder import response_builder
from flask import Flask, request
from flask_cors import CORS

# %%
app = Flask(__name__)
CORS(app)

app.register_blueprint(hello_bp)
app.register_blueprint(properties_bp)
app.register_blueprint(swagger_bp)


@app.route('/')
def index():
    return response_builder({"CS 4783 Project\nMichael DeReus\nwmi593"}, 200)


if __name__ == "__main__":
    app.run(ssl_context=("ssl\\cert.pem", "ssl\\key.pem"), port=8080, debug=True)
