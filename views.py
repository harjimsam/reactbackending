import os
import base64
import flask
import bcrypt
import datetime
from init import app, db
import models
from sqlalchemy import desc
from math import ceil

#Note: Test PER_PAGE, need to change to 25
PER_PAGE = 25


@app.before_request
def setup_csrf():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


@app.before_request
def setup_user():
    if 'auth_user' in flask.session and flask.session['auth_user'] is not None:
        user = models.User.query.get(flask.session['auth_user'])
        flask.g.user = user
def checkAuth():
    if flask.session['auth_user'] is None:
        return flask.redirect('/')


@app.route('/')
def index():

    flask.session['auth_user'] = None
    return flask.render_template('index.html')


@app.route('/login', methods=['POST'])
def login():


    #if the user and password is filled out,
    if flask.request.form['password'] and flask.request.form['username']:
        p = flask.request.form['password']
        u = flask.request.form['username']



        #see if the user already exists
        user = models.User.query.filter_by(username=u).first()

        if user:
            #if they do, take them to the homepage

            password = bcrypt.hashpw(p.encode('utf8'), user.password)


            if password == user.password:

                flask.session['auth_user'] = user.id
                return flask.redirect('/home/')


        else:
            #if they dont, send them back
            flask.flash('Invalid user name or password')
            return flask.redirect('/')

    else:
        flask.flash('Invalid user name or password')
        return flask.redirect('/')


@app.route('/createNewUser', methods=['POST'])
def createNewUser():
    #if the user and password is filled out,
    if flask.request.form['password'] and flask.request.form['username'] and flask.request.form['confirmpw']:
        if flask.request.form['password'] != flask.request.form['confirmpw']:
            flask.flash('Password not confirmed')
            return flask.redirect('/')
        else:



            # check to see if the user name is already taken.
            p = flask.request.form['password']
            u = flask.request.form['username']

            user = models.User.query.filter_by(username=u).first()

            if not user:

                newUser = models.User(p,u)
                newUser.username = u
                # newUser.password = bcrypt.hashpw(p.encode('utf8'), bcrypt.gensalt(15))


                print("in ",p)

                print("out ", newUser.password)
                print("size ", len(newUser.password))


                db.session.add(newUser)
                db.session.commit()
                flask.session['auth_user'] = newUser.id


                return flask.redirect('/home')
            else:
                flask.flash('That username is already taken. ')
                return flask.redirect('/')

    else:
        flask.flash('Fill out all fields.')
        return flask.redirect('/')


@app.route('/home/', defaults={'page': 0})
@app.route('/home/<int:page>')
def home(page):
    checkAuth()
    message = 'man, you might ahve made it. '
    user = models.User.query.get(flask.session['auth_user'])
    return flask.render_template('home.html', user =user )




def url_for_other_page(page):
    args = flask.request.view_args.copy()
    args['page'] = page
    return flask.url_for(flask.request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route('/logout')
def logout():
    return flask.redirect('/')

