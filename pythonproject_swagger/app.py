from flask import Flask, render_template
from flask_smorest import Api
from resources.simpleapi import blp as SimpleAPIBlueprint
from resources.fileoperations import blp as FileOperationsBlueprint

app = Flask(__name__)

app.config["PROPOGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "File Upload REST API"
app.config["API_VERSION"] = "V1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config['UPLOAD_FOLDER'] = "/file/uploadfiles/"

api = Api(app)
api.register_blueprint(SimpleAPIBlueprint)
api.register_blueprint(FileOperationsBlueprint)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
