import types
from . import UPLOAD_FOLDER, db
from .models import User, Files
import random
from base64 import urlsafe_b64encode

from  sqlalchemy.sql.expression import func

import imageio as iio
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
GIF_EXTENSIONS = {'gif'}


def typecheck(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return filename.rsplit('.', 1)[1].lower()

    elif '.' in filename and filename.rsplit('.', 1)[1].lower() in GIF_EXTENSIONS:
        return "gif"

    else:
        return False
    

def correct_filetype(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gif_from_images(files, gifname, fps):

    writer = []
    for file in files:
        image = iio.imread(file.read(), '.'+typecheck(file.filename))
        writer.append(image)
    url = hashnbigu(str(writer)+str(random.getrandbits(8))+gifname)
    iio.mimsave(UPLOAD_FOLDER + url+'.gif', writer, fps=fps)
    return url

def gif_from_gif(files, gifname):
    writer = [iio.imread(files[0].read(), '.'+typecheck(files[0].filename))]
    url = hashnbigu(str(writer)+str(random.getrandbits(8))+gifname)
    iio.mimsave(UPLOAD_FOLDER + url+'.gif', writer, fps=5)
    return url

# def get_rundom_gifs():


def hashnbigu(word):
    return urlsafe_b64encode(str(hash(word)).encode('utf-8')).decode("utf8").rstrip("=")

def gif_to_db(url, name,  user_id):
        new_gif = Files(gif_url=url, gif_name=name, user_id=user_id)
        db.session.add(new_gif)
        db.session.commit()
        return url
    
def get_gif_name(url):
    gif = Files.query.filter_by(gif_url=url).first()
    if gif:
        return gif.gif_name, User.query.filter_by(id=gif.user_id).first().first_name
    else:
        return None,None
    
def get_rand_gif(n):
    gifs = Files.query.order_by(func.random()).all()
    return [x.gif_url for x in gifs[:min(n, len(gifs))]]
