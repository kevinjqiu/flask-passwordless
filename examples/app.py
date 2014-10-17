import flask
from flask.ext.passwordless import Passwordless


app = flask.Flask("app")
app.config.from_object('settings')
passwordless = Passwordless(app)


@app.route('/login', methods=['post', 'get'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    elif flask.request.method == 'POST':
        email = flask.request.form.get('email')
        passwordless.request_token(email)
        return flask.render_template('login.html', email=email)


@app.route('/authenticate', endpoint="authenticate")
def authenticate():
    if passwordless.authenticate(flask.request):
        return "logged in"
    else:
        flask.abort(401)


app.run(debug=True)
