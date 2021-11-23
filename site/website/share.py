from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user
from . import UPLOAD_FOLDER
from .utils import get_gif_name

share = Blueprint('share', __name__)


@share.route('/share/<url_gif>')
def share_url(url_gif): 
    gif_name, author_name = get_gif_name(url=url_gif)
    if gif_name:
        return render_template("share.html", url_gif=url_gif, author_name=author_name, gif_name = gif_name, user=current_user)
    else:
        return redirect(url_for('views.home'))

@share.route('static/<filename>')
def display(filename):
    return redirect(url_for('static', filename= 'uploads/' + filename ), code=301)
    