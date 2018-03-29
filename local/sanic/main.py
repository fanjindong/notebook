from sanic import Blueprint, Sanic
from sanic.exceptions import NotFound, ServerError
from sanic.response import json, text

app = Sanic(__name__)


@app.route("/json")
def post_json(request):
    return json({"received": True, "message": request.json})


@app.post("/query_string")
def query_string(request):
    return json({"parsed": True,
                 "args": request.args,
                 "url": request.url,
                 "query_string": request.query_string,
                 "message": request.raw_args})


@app.route("/files")
def post_json(request):
    test_file = request.files.get('test')

    file_parameters = {
        'body': test_file.body,
        'name': test_file.name,
        'type': test_file.type,
    }

    return json({"received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters})


@app.route("/form")
def post_json(request):
    return json({"received": True, "form_data": request.form, "test": request.form.get('test')})


@app.route("/users", methods=["POST", ])
def create_user(request):
    return text("You are trying to create a user with the following POST: %s" % request.body)


bp = Blueprint('my_blueprint')


@app.route('/')
async def bp_root(request):
    if request.app.config['DEBUG']:
        return json({'status': 'debug'})
    else:
        return json({'status': 'production'})


bp = Blueprint('my_blueprint')


@bp.route('/blueprint')
async def bp_root(request):
    return json({'my': 'blueprint'})
app.blueprint(bp)
app.run(host="0.0.0.0", port=8000, debug=True)
