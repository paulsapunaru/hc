import json

from bson import json_util
from flask import Flask, request, Response, jsonify

from common import service
from common.api_exception import BadRequestException

app = Flask(__name__)


@app.errorhandler(BadRequestException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/items")
def get_items():
    subreddit_param = request.args.get("subreddit")
    from_param = request.args.get("from")
    to_param = request.args.get("to")
    keyword = request.args.get("keyword")

    # Retrieve filtered items
    items = service.retrieve_items(subreddit_param, from_param, to_param,
                                   keyword)
    # Build the response
    resp_json = {"status": "success", "count": len(items), "data": items}
    js = json.dumps(resp_json, default=json_util.default)
    resp = Response(js, status=200, mimetype="application/json")

    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
