# views.py handles the home page and note management 

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import  login_required, current_user
from .models import Note
from . import db
import json
import os
import pandas as pd
from werkzeug.utils import secure_filename

# creates a new blueprint called views, which is related to the main functionality
# which is viewing and managing notes
views = Blueprint('views', __name__)

# first creates the home route (which is just /), and handles both get and post requests
# the post requests include creating notes. 
@views.route('/', methods=['GET', 'POST'])

# only logged in users can access this route
@login_required
def home():
    # if its a post request, get the note from the form
    if request.method=='POST':
        note = request.form.get('note')
        # flash an error if the note is nothing. 
        if len(note) < 1:
            flash("Note is too short.", category = 'error')
        # otherwise create a new note using the note class from the models.py file
        # and add the note to the database and flash a success message. 
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added.", category = 'success')
    # otherwise return just the home page defined in home.html
    return render_template("home.html", user=current_user)

# allows users to delete notes; only a post request -- there is no default delete note page.
@views.route('/delete-note', methods=['POST'])

def delete_note():
    # receives a JSON payload from the client, and parses it
    note = json.loads(request.data)
    # extracts the noteID from the parsed data.
    noteId = note['noteId']
    # obtains the note using the noteID
    note = Note.query.get(noteId)
    # if the note exists and belongs to the user, then delete it. 
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    # otherwise return an empty json repsonse
    return jsonify({})
