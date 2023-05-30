import os
import secrets
from PIL import Image
from flask import url_for, current_app

def save_file_cover_letter(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/cover_letters', file_fn)
    form_file.save(file_path, buffer_size=16384)
    form_file.close()
    return file_fn

def save_file_resume(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/resume_application_files', file_fn)
    form_file.save(file_path, buffer_size=16384)
    form_file.close()
    return file_fn