from flask import Blueprint, session
from main import db
from flask import render_template, redirect, flash, url_for, request
from main.dbmodel import User
from flask_login import logout_user, login_user, login_required, current_user
from main.users.forms import RegisterForm, LoginForm, EditAccountForm, ResetPasswordForm, EmailResetForm
from main.users.utils import save_photo, send_email_reset_pass


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        print('ok')

        new_user = User(
            user_name= form.username.data,
            email = form.email.data,
            password_hash= form.password.data
        )


        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('you successfully registered, thank you')

        return redirect(url_for('tasks.task_page'))

    if form.errors != {}:
        for err in form.errors.values():
            flash(f"🙏: {err}", category='danger')

    return render_template('register.html', form=form)




@users.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()

        if attempted_user:
            if attempted_user.check_correct_password(attempted_password=form.password.data):
                login_user(attempted_user)

                flash(message=f'Welcome {current_user.user_name}: You Successfully logged In:', category='success')

                next = request.args.get('next')
                print(next)
                return redirect(next or url_for('tasks.personal_tasks'))

            else:
                flash(message='Password Is Wrong, Try again', category='fail')

        else:
            flash(message='Sorry, The Email IS Not Exist, You Should Register First', category='fail')
            return redirect(url_for('users.register_page'))

    return render_template('login.html', form=form)




@users.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home.home_page'))




@users.route('/account', methods=['GET', 'POST'])
@login_required
def account_page():
    form = EditAccountForm()
    print(users.root_path)
    if form.validate_on_submit():
        if form.photo.data:
            print('ok')
            print(type(form.photo.data))
            user_pic = save_photo(form.photo.data)
            current_user.profile_image = user_pic

        current_user.user_name = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash(message='Your account has been updated')
        return redirect(url_for('tasks.personal_tasks'))

    elif request.method == 'GET':
        form.username.data = current_user.user_name
        form.email.data = current_user.email

    image_file = url_for('static', filename='images/' + current_user.profile_image)
    return render_template('account.html', form=form, image_file=image_file)



# create Routes for send email reset password
@users.route('/msg-reset', methods=['GET', 'POST'])
def send_email_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = EmailResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        send_email_reset_pass(user)
        flash('please see an email has been sent to you')
        return redirect(url_for('users.login_page'))
    return render_template('send_email.html', form=form)



@users.route('/reset-pass/<token>', methods=['GET', 'POST'])
def reset_password_page(token):

    user = User.verify_user_token(token)
    if not user:
        flash('that is invalid or expired token')
        return redirect(url_for('users.send_email_page'))

    form = ResetPasswordForm()
    if form.validate_on_submit():

        user.password_hash = form.password.data

        db.session.commit()

        flash('you successfully changed your password, well done')

        return redirect(url_for('tasks.task_page'))

    return render_template('reset_pass.html', title='Reset Password', form=form)

















