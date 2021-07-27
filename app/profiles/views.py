from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user

from app.database import db
from app.models import FriendRequest
from app.models import User
from app.profiles.forms import FriendRequestForm
from app.profiles.forms import UpdateForm
from app.tools.check_auth import check_auth
from app.tools.format_dob import dob_string_to_datetime, calculate_age
from app.tools.nav_link_list import generate_nav_links
from app.tools.save_file import save_file

profiles_blueprint = Blueprint('profiles',
                               __name__,
                               template_folder='templates',
                               static_folder='static'
                               )


@profiles_blueprint.route('/')
@profiles_blueprint.route('/<username>', methods=['GET', 'POST'])
def list_people(username=None):
    """
    shows the list of all registered profiles
    if a username is specified, shows read-only data of a profile linked to the username
    """
    if username:
        friend_request_form = FriendRequestForm()
        incoming_requests = FriendRequest.query.filter_by(recipient_user=current_user.id, active=1).all()
        incoming_requests_ids = [r.id for r in incoming_requests]
        incoming_requests_senders = [r.sender_user for r in incoming_requests]
        incoming_requests = [incoming_requests_ids, incoming_requests_senders]

        user = User.find_by_username(username)
        friend_asked = FriendRequest.query.filter_by(recipient_user=user.id,
                                                     sender_user=current_user.id,
                                                     active=1).first()

        if request.method == 'POST':  # happens when sending a friend request or deleting an existing one
            sender = int(friend_request_form.sender_user.data)
            receiver = int(friend_request_form.receiving_user.data)

            if sender == current_user.id and receiver == user.id:
                if friend_request_form.submit_friend_request.data:
                    if not friend_asked:
                        new_friend_request = FriendRequest(sender_user=sender,
                                                           recipient_user=receiver)
                        db.session.add(new_friend_request)
                        db.session.commit()
                        return redirect(url_for('profiles.list_people', username=user.username))

                elif friend_request_form.undo_friend_request.data:
                    if friend_asked:
                        db.session.delete(friend_asked)
                        db.session.commit()
                        return redirect(url_for('profiles.list_people', username=user.username))


        return render_template('people_profile.html', pages=generate_nav_links(),
                               user=user,
                               friend_request_form=friend_request_form,
                               friend_asked=friend_asked,
                               incoming_requests=incoming_requests)

    else:
        people_list = User.query.all()
        return render_template('people.html', pages=generate_nav_links(), people_list=people_list)


@profiles_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    shows the profile of a signed-in user, lets them edit their data or log out
    """
    incoming_requests = FriendRequest.query.filter_by(recipient_user=current_user.id, active=1).all()
    request_sender_usernames = []
    if incoming_requests:
        for r in incoming_requests:
            request_sender_usernames.append(User.query.get(r.id).username)

    if request.method == 'POST':  # happens when editing own data
        form_update = UpdateForm()
        if current_user.check_password(form_update.password.data):
            formatted_date = dob_string_to_datetime(form_update.dob.data)
            if form_update.validate_on_submit():
                for x in set(form_update):

                    if x.name == 'dob':
                        x.data = formatted_date
                        setattr(current_user, 'age', calculate_age(x.data))

                    if x.data and x.data != '' and x.name in current_user.__table__.c:
                        if x.name == 'picture':
                            x.data = save_file(current_user.username, x.data,
                                               'profile_pictures')  # saves file to directory, returns filename

                        if x.name != 'password' and x.name != 'role':
                            setattr(current_user, x.name, x.data)
                            db.session.commit()
                flash('მონაცემები წარმატებით განახლდა', 'alert-green')
            else:
                flash('მონაცემები არასწორადაა შეყვანილი – მონაცემები არ განახლდა', 'alert-red')
        else:
            flash('პაროლი არასწორია – მონაცემები არ განახლდა', 'alert-red')

        return render_template('my_profile.html',
                               pages=generate_nav_links(),
                               form_update=UpdateForm(),
                               incoming_requests=incoming_requests,
                               request_sender_usernames=request_sender_usernames,
                               zip=zip)

    else:
        if check_auth():
            return render_template('my_profile.html',
                                   pages=generate_nav_links(),
                                   form_update=UpdateForm(),
                                   incoming_requests=incoming_requests,
                                   request_sender_usernames=request_sender_usernames,
                                   zip=zip)

    return redirect('/')


# @profiles_blueprint.route('/accept', methods=['POST'])
# def accept_request():
#
