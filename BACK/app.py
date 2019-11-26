# все импорты
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import mapper, relationship

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:admin@localhost/backmass'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
UPLOAD_FOLDER = 'D:/Coding/FULL/BACK/static/img/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config["IMAGE_UPLOADS"] = r'D:/Coding/FULL/BACK/static/img/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)


# def init_db():
#    metadata.create_all(bind=engine)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(40), nullable=False)
    country = db.Column('country', db.String(32), nullable=False)
    #photos = db.relationship('Photo', backref='user_id', lazy=True)

    def __init__(self, name, country):
        self.name = name.strip()
        self.country = country.strip()


class Photo(db.Model):
    # __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    it = db.Column(db.String, nullable=False)
   # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, it=None):
        self.it = it

    # def __repr__(self):
    #    return str('<Photo %r>' % (self.it))


db.create_all()


@app.route("/enter", methods=['GET', 'POST'])
def enter():
    return render_template('enter.html')


@app.route("/add_users", methods=['POST'])
def add_users():
    name = request.form['mam']
    country = request.form['country']
    db.session.add(Users(name, country))
    db.session.commit()
    return redirect(url_for('data_user'))


@app.route("/data_user", methods=['GET', 'POST'])
def data_user():
    return render_template('data_user.html', users=Users.query.order_by(Users.id.desc()).limit(1).all()[::-1],
                           photo=Photo.query.order_by(Photo.it.desc()).limit(1).all()[::-1])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/load", methods=['GET', 'POST'])
def load():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        img = request.files['img']
        # if user does not select file, browser also
        # submit an empty part without filename
        if img.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if img and allowed_file(img.filename):
            img = request.files['img']

            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            it = Photo(os.path.join(app.config['UPLOAD_FOLDER'] + filename))
            # image = str(img)
            db.session.add(it)
            db.session.commit()
            Photo.query.all()

            return redirect(url_for('enter',
                                    filename=filename))

    return render_template('load.html')


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/profile", methods=['GET'])
def profile():
    return render_template('profile.html')


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True)
