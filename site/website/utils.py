from . import UPLOAD_FOLDER, Files
from flask_login import current_user

import imageio as io

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
GIF_EXTENSIONS = {'gif'}


def typecheck(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return "img"

    elif '.' in filename and filename.rsplit('.', 1)[1].lower() in GIF_EXTENSIONS:
        return "gif"

    else:
        return False

# def gif_from_images(filames):
    
