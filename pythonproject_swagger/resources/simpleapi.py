from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort

blp = Blueprint("simpleapi", __name__, description="This is Simple API for Demo")

@blp.route("/simpleapi/")
class SimpleAPI(MethodView):
    def get(self):
        try:
            return "Hello World!"
        except:
            abort(404, "Error In Execution")

    def delete(self):
        try:
            return "Record Deleted!!"
        except:
            abort(404, "Error In Execution")