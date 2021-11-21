import types
from . import UPLOAD_FOLDER, Files
from flask_login import current_user
import pickle
from base64 import urlsafe_b64encode

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


def gif_from_images(files, gifname):

    writer = []
    for file in files:
        image = iio.imread(file.read(), '.'+typecheck(file.filename))
        writer.append(image)
    iio.mimsave(UPLOAD_FOLDER + gifname+'.gif', writer, fps=5)
    print(hashnbigu(str(writer)+gifname))
    # with open('data.pickle', 'wb') as f:
    #     pickle.dump(data, f)
    return UPLOAD_FOLDER + gifname + '.gif'

# def get_rundom_gifs():

# def generate_url(filename, gifname):
def hashnbigu(word):
    return urlsafe_b64encode(str(hash(word)).encode('utf-8')).decode("utf8").rstrip("=")
    
