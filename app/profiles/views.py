from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user

from app.models import User
from app.profiles.forms import RegisterForm
from app.tools.check_auth import check_auth
from app.tools.format_dob import dob_string_to_datetime, calculate_age
from app.tools.nav_link_list import generate_nav_links
from app.tools.save_file import save_file

profiles_blueprint = Blueprint('profiles',
                               __name__,
                               template_folder='templates'
                               )


# server:port/blueprint_prefix/add
@profiles_blueprint.route('/')
@profiles_blueprint.route('/<username>')
def list_people(username=None):
    """
    shows the list of all registered profiles
    if a username is specified, shows read-only data of a profile linked to the username
    """
    if username:
        user = User.find_by_username(username)
        return render_template('people_profile.html', pages=generate_nav_links(), user=user)

    else:
        people_list = User.query.all()
        return render_template('people.html', pages=generate_nav_links(), people_list=people_list)


# server:port/blueprint_prefix/add
@profiles_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    shows the profile of a signed-in user, lets them edit their data or log out
    """

    if request.method == 'POST':  # happens when editing own data
        form_register = RegisterForm()
        if current_user.check_password(form_register.password.data):
            from app.database import db
            formatted_date = dob_string_to_datetime(form_register.dob.data)

            for x in set(form_register):

                if x.name == 'dob':
                    x.data = formatted_date
                    setattr(current_user, 'age', calculate_age(x.data))

                if x.data and x.data != '' and x.name in current_user.__table__.c:
                    if x.name == 'picture':
                        x.data = save_file(current_user.username, x.data, 'profile_pictures')  # saves file to directory, returns filename

                    if x.name != 'password' and x.name != 'role':
                        setattr(current_user, x.name, x.data)
                        db.session.commit()
            flash('მონაცემები წარმატებით განახლდა', 'alert-green')

        else:
            flash('პაროლი არასწორია – მონაცემები არ განახლდა', 'alert-red')

        return render_template('my_profile.html', pages=generate_nav_links(), form_register=RegisterForm())

    else:
        if check_auth():
            return render_template('my_profile.html', pages=generate_nav_links(), form_register=RegisterForm())

    return redirect('/')
