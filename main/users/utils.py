import secrets
import os
from PIL import Image
from main import mail
from flask_mail import Message
from flask import url_for, current_app



# create function to upload user photo

def save_photo(form_photo):
    hex_name = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_photo.filename)
    picture_fn = hex_name + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_photo)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



# create function to send token to reset password
def send_email_reset_pass(user):
    token = user.send_user_token()

    msg = Message('Password Reset Request',
                  sender='monasr79@yahoo.com',
                  recipients=['monasr79@yahoo.com'])

    msg.body = f"""To reset password, visit the following link:
{url_for('users.reset_password_page', token=token, _external=True)}
If you did not make that request then simply ignore that email
"""

    mail.send(msg)