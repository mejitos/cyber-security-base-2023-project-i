# VISP - Vulnerable Image Sharing Platform.
#
# Project for Cyber Security Base -course.
#   https://cybersecuritybase.mooc.fi/
import bcrypt
import functools
import os
import subprocess
import time
import urllib
import uuid
from flask import (
    Flask, request, redirect, url_for, render_template,
    jsonify, make_response, session
)
from visp_database import load_database, save_database, create_database

# FIX Flaw 6: Security Logging and Monitoring Failures
#
# UNCOMMENT
#
# import logging as log
# log.basicConfig(
#     filename='visp.log',
#     filemode='w',
#     format='[%(asctime)s][%(levelname)s] %(message)s',
#     datefmt='%d-%b-%y %H:%M:%S')


app = Flask(__name__)

# FIX Flaw 4: Security Misconfiguration
#
# REPLACE
#
# app.config['SECRET_KEY']  = os.environ['SECRET_KEY']
# app.config['DEBUG']       = os.environ.get('DEBUG') in {'1', 'true', 'True'}

app.config['SECRET_KEY'] = 'supersekret'
app.config['DEBUG'] = True


# FIX Flaw 5: Identification and Authentication Failure
#
# UNCOMMENT
#
# # Global maximum login attempts
# MAX_LOGIN_ATTEMPTS = 5
# # <ip, number of tries>
# login_attempts = {}
# # set of banned ip addresses
# jail = set()


def authentication_required(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        if session.get('user', None) is None:
            # FIX Flaw 6: Security Logging and Monitoring Failures
            #
            # UNCOMMENT
            #
            # log.error(f'[{request.remote_addr}] Attempting unauthorized access')
            return make_response('Unauthorized', 401)

        return handler(*args, **kwargs)
    return inner


@app.get('/')
def index():
    user = session.get('user', None)

    if user is None:
        return redirect(url_for('login'))

    return render_template('index.html', user=user)


valid_credentials = lambda a, b: a['username'] == b['username'] and \
    bcrypt.checkpw(a['password'].encode(), b['password'].encode())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # FIX Flaw 5: Identification and Authentication Failure
        #
        # UNCOMMENT
        #
        # if request.remote_addr in jail:
        #     return make_response('Forbidden', 403)

        try:
            credentials = {
                'username': request.form['username'],
                'password': request.form['password'],
            }
        except KeyError:
            return 'Bad request', 400

        for user in database['users'].values():
            if valid_credentials(credentials, user):
                session['user'] = {'id': user['id'], 'name': user['username']}
                # FIX Flaw 5: Identification and Authentication Failure
                #
                # UNCOMMENT
                #
                # login_attempts[request.remote_addr] = 0
                return redirect(url_for('index'))

        # FIX Flaw 5: Identification and Authentication Failure
        #
        # UNCOMMENT
        #
        # login_attempts[request.remote_addr] = \
        #     login_attempts.get(request.remote_addr, -1) + 1
        # if login_attempts[request.remote_addr] >= MAX_LOGIN_ATTEMPTS:
        #     jail.add(request.remote_addr)
        #     return make_response('Forbidden', 403)

        # FIX Flaw 6: Security Logging and Monitoring Failures
        #
        # UNCOMMENT
        #
        # if login_attempts[request.remote_addr] == MAX_LOGIN_ATTEMPTS - 1:
        #     log.warning(f'[{request.remote_addr}] Invalid username or password. About to send client to jail')
        # else:
        #     log.info(f'[{request.remote_addr}] Invalid username or passowrd')

        return redirect(url_for('login'))

    # If user is already logged in, redirect in
    if session.get('user', None) is not None:
        return redirect(url_for('index'))

    return render_template('login.html')


@app.post('/logout')
def logout():
    if session.get('user', None) is None:
        return redirect(url_for('index'))

    session.pop('user')
    return redirect(url_for('login'))


@app.get('/api/images')
@authentication_required
def get_images():
    user = session.get('user')
    images = list(database['images'].values())
    images = list(filter(lambda img: img['owner'] == user['id'], images))

    return jsonify(images), 200


@app.post('/api/images')
@authentication_required
def add_image():
    try:
        image = request.files['image']
    except KeyError:
        return 'Bad request', 400

    # Decode the URL encoding to get the actual filename
    image_filename = urllib.parse.unquote(image.filename)

    # If the filename has '..' components, it is a possible path injection
    if '..' in image_filename:
        # FIX Flaw 6: Security Logging and Monitoring Failures
        #
        # UNCOMMENT
        #
        # log.error(f'[{request.remote_addr}] Possible path injection detected')
        return 'Bad request', 400

    # Save the image for inspection
    image_path = app.root_path + '/static/images/' + image.filename
    image.save(image_path)

    # FIX Flaw 3: Injection
    #
    # REPLACE
    #
    result = subprocess.run(
        ['file', image_path], shell=False,
        timeout=15, stdout=subprocess.PIPE
    ).stdout.decode()

    # Ensure that the file is JPEG/PNG with `file` command
    # result = subprocess.run(
    #     f'file {image_path}', shell=True,
    #     timeout=15, stdout=subprocess.PIPE
    # ).stdout.decode()

    # If the file was not JPEG/PNG, remove it and return error
    if not ('PNG image data' in result or 'JPEG image data' in result):
        # FIX Flaw 6: Security Logging and Monitoring Failures
        #
        # UNCOMMENT
        #
        # log.warning(f'[{request.remote_addr}] Attempt to upload a file with non-supported file type')
        try:
            os.remove(image_path)
        except FileNotFoundError:
            return 'Not found', 404

        return 'Bad request', 400

    try:
        new_image = {
            'id': str(uuid.uuid4()),
            'timestamp': int(time.time()),
            'title': request.form['title'],
            'description': request.form['description'],
            'filename': image.filename,
            'shared': 'shared' in request.form and request.form['shared'] == '1',
            'owner': session.get('user')['id'],
        }
        database['images'][new_image['id']] = new_image
        save_database(database)
    except KeyError:
        return 'Missing required data', 400

    return jsonify(new_image), 201


@app.patch('/api/images/<image_id>')
@authentication_required
def share_image(image_id):
    for image in database['images'].values():
        if image['id'] == image_id:
            # FIX Flaw 1: Broken Access Control:
            #
            # UNCOMMENT
            #
            # if image['owner'] != session.get('user')['id']:
            #     return 'Forbidden', 403

            image['shared'] = not image['shared']
            save_database(database)
            return '', 200

    # FIX Flaw 6: Security Logging and Monitoring Failures
    #
    # UNCOMMENT
    #
    # log.info(f'[{request.remote_addr}] User {session.get("user")["id"]} tried to share non-existing image {image_id}')

    return 'Not found', 404


@app.delete('/api/images/<image_id>')
@authentication_required
def delete_image(image_id):
    for image in database['images'].values():
        if image['id'] == image_id:
            # FIX Flaw 1 Broken Access Control
            #
            # UNCOMMENT
            #
            # if image['owner'] != session.get('user')['id']:
            #     return 'Forbidden', 403

            image_path = app.root_path + '/static/images/' + image['filename']

            try:
                os.remove(image_path)
            except FileNotFoundError:
                return 'Not found', 404

            database['images'].pop(image['id'])
            save_database(database)
            return '', 204

    # FIX Flaw 6: Security Logging and Monitoring Failures
    #
    # UNCOMMENT
    #
    # log.info(f'[{request.remote_addr}] User {session.get("user")["id"]} tried to remove non-existing image {image_id}')

    return 'Not found', 404


@app.get('/api/images/shared')
@authentication_required
def get_shared_images():
    images = database['images'].values()
    shared_images = [
        {
            **image,
            'owner': database['users'][image['owner']]['username']
        }
        for image in images if image['shared']
    ]

    return jsonify(shared_images), 200


if __name__ == '__main__':
    database = load_database()

    if database is None:
        database = create_database()

    # FIX Flaw 2: Cryptographic Failures
    #
    # REPLACE
    #
    # app.run(ssl_context='adhoc')
    #
    # OR, if using self signed certificates
    #
    # app.run(ssl_context=('/path/to/cert.pem', '/path/to/key.pem'))

    app.run()
