from flask import Blueprint, render_template, request, flash, redirect
from flask.helpers import url_for
from flask_login import login_required, current_user
from . import UPLOAD_FOLDER
from .utils import typecheck, gif_from_images, gif_from_gif, gif_to_db, get_rand_gif

from os import path

views = Blueprint('views', __name__)

UPLOAD_FOLDER = './uploads'


@views.route('/', methods=['GET', 'POST'])
def home():
    gifs = get_rand_gif(12)
        
    if len(gifs) < 12:
        return render_template("home.html", user=current_user, gifs=None) 
    gifs_new = []
    for i in range(4):
        gifs_new.append([gifs[0+i*3], gifs[1+i*3], gifs[2+i*3]])
    
    return render_template("home.html", user=current_user, gifs=gifs_new)


@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        gif_filename = request.form.get('filename')
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
            url = gif_from_gif(file_list, gif_filename)
            if request.form.get('type') == 'download':
                flash('What the point of downloading?)')

            if request.form.get('type') ==  'share':
                gif_to_db(url, gif_filename, current_user.id)
                flash('File shared', category='success')
                return redirect(url_for('share.share_url', url_gif = url))
                
        else:
            url = gif_from_images(file_list, gif_filename, int(request.form.get('fps')))
            if request.form.get('type') == 'download':
                flash(path.join(UPLOAD_FOLDER,url+".gif"))
                return redirect(url_for('share.display', filename = url+".gif"))
            
            if request.form.get('type') ==  'share':
                gif_to_db(url, gif_filename, current_user.id)
                flash('File shared', category='success')
                return redirect(url_for('share.share_url', url_gif = url))

    return render_template("upload.html", user=current_user)
