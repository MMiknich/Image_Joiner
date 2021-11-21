from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
# from .models import Note
from . import UPLOAD_FOLDER
# import json

share = Blueprint('share', __name__)


@share.route('/share/<url_gif>')
def share(url_gif):
    
    return render_template("share.html", user=current_user, gif_path = UPLOAD_FOLDER+url_gif, gif_name = )
    

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
