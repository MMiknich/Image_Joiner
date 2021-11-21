from flask import Blueprint, render_template, request, flash, jsonify, redirect, send_file, send_from_directory
from flask.helpers import url_for
from flask_login import login_required, current_user
from . import Files, User
from . import db
from .utils import typecheck, gif_from_images, gif_from_gif, gif_to_db

import os

views = Blueprint('views', __name__)

UPLOAD_FOLDER = './uploads'


def correct_filetype(filename):
    print(filename.rsplit('.', 1)[1].lower())
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/', methods=['GET', 'POST']) #//TODO
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            print(current_user)

    return render_template("home.html", user=current_user)


@views.route('/upload', methods=['GET', 'POST'])
# @login_required
def upload():
    if request.method == 'POST':
        # flash('No file part')
        gif_filename = request.form.get('filename')
        print(request.form.get('filename'))
        file_list = request.files.getlist('file')

        ftype = None
        for img in file_list:
            if not typecheck(img.filename):
                flash('At least one of the files in wrong type', category='error')
                return render_template("upload.html", user=current_user)
            if not(ftype is None or ftype == typecheck(img.filename)):
                flash('Different file types', category='error')
                return render_template("upload.html", user=current_user)
            ftype = typecheck(img.filename)

        file_list = sorted(file_list, key=lambda x: x.filename)

        if typecheck(file_list[0].filename) == 'gif':
            if request.form.get('download') is not None:
                flash('What the point of downloading?)')

            if request.form.get('share') is not None:
                url = gif_from_gif(file_list, gif_filename)
                gif_to_db(url, gif_filename)
                flash('File shared', category='success')
                redirect(url_for('share', url_gif = url))
                
        else:
            url = gif_from_images(file_list, gif_filename)
            print('gif made')
            if request.form.get('download') is not None:
                # not working
                print(url)
                send_file(url+".gif", as_attachment=True)
            if request.form.get('share') is not None:
                gif_to_db(url, gif_filename)
                flash('File shared', category='success')
                redirect(url_for('share', url_gif = url))
                # geturl()
                pass

        # make_gif()

        if request.form.get('share') is not None:
            # send_to_sql()
            # geturl()
            pass
        if request.form.get('download') is not None:
            pass
        # check for correct type and no files
        flash('No file part')
        flash('No selected file')
        # return redirect(url_for(''))

    return render_template("upload.html", user=current_user)
