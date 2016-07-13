import flask
from init import app, db
import models


@app.route('/api/update-check', methods =['POST'])
def update_check():
    print(flask.request.form)

    if 'auth_user' not in flask.session:
        print('...')
        flask.abort(403)

    user_id = flask.session['auth_user']
    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        print('....')
        flask.abort(400)




