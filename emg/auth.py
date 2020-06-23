from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user
from .models import User, Personne, Signing, Watcher
from . import db
import os
from .backend import face_cropper

auth = Blueprint('auth', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/new_user', methods=['POST'])
def new_user():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.users'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@auth.route('/personnes')
def personnes():
    personnes = Personne.query.all()
    return render_template('personne.html', personnes=personnes)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@auth.route('/new_personne', methods=['POST'])
def new_personne():
    if 'img' not in request.files:
        flash('No file part')
        return redirect(url_for('auth.personnes'))

    email = request.form.get('email')
    name = request.form.get('name')
    first_name = request.form.get('first_name')
    addresse = request.form.get('addresse')
    telephone = request.form.get('telephone')
    _file = request.files['img']

    if _file.filename == '':
        flash('No selected file')
        return redirect(url_for('auth.personnes'))

    personne = Personne.query.filter_by(email=email).first()

    if personne:
        flash('Email address already exists')
        return redirect(url_for('auth.personnes'))

    if _file and allowed_file(_file.filename):
        filename = secure_filename(_file.filename)
        CASCADE_PATH = "/home/jordy/EMG/emg/backend/haarcascade_frontalface_default.xml"
        detecter = face_cropper.FaceCropper(CASCADE_PATH)
        img_path = detecter.generate(_file, name, first_name)

    new_personne = Personne(name=name, first_name=first_name, email=email, addresse=addresse, telephone=telephone, img_path=img_path)
    watcher = Watcher.query.filter_by(db_name='personne').first()
    watcher.revision = watcher.revision + 1

    db.session.add(new_personne)
    db.session.add(watcher)
    db.session.commit()

    return redirect(url_for('auth.personnes'))

@auth.route('/delete_personne/<req_id>', methods=['GET'])
def delete_personne(req_id):
    id = req_id
    personne = Personne.query.filter_by(id=id).first()
    db.session.delete(personne)
    db.session.commit()

    return redirect(url_for('auth.personnes'))

@auth.route('/signing')
def signing():
    signings = db.session.query(Signing).join(Personne).all()
    return render_template('signing.html', signings=signings)