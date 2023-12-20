from flask import redirect, url_for
from flask_login import logout_user, login_required
from . import auth



@auth.route('/logout')
@login_required
def logout():
    """ Logout the user """
    logout_user()
    return redirect(url_for('views.index'))