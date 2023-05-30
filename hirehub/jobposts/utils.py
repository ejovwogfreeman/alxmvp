import os
import secrets
from PIL import Image
from flask import url_for, current_app
def save_image_flyer(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/job_desc_images', picture_fn)

    # output_size = (125, 125)
    i = Image.open(form_picture)
    # i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



def save_job_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/job_flyers', file_fn)
    form_file.save(file_path, buffer_size=16384)
    form_file.close()
    return file_fn