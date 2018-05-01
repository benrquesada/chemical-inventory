from application import app
from application.models.usersModel import *
from application.config import *
from application.logic.sortPost import *
from application.logic.getAuthUser import AuthorizedUser

from flask import \
    render_template, \
    request, \
    redirect, \
    url_for, \
    flash

# PURPOSE: superUser or Staff requesting for a student to have access to the system.
@app.route('/RequestUserAccess/', methods = ['GET', 'POST'])
def RequestUserAccess():
  # User authorization
  auth = AuthorizedUser()
  user = auth.getUser()
  userLevel = auth.userLevel()
  if userLevel == -1 or user == -1:
    abort(403)
  print user.username, userLevel

  if request.method == "POST":
    status, flashMessage, flashFormat = createUser(request.form, user.username, False)
    if status:
        flash("Success: Access for "+ user.first_name + " " + user.last_name + " was Requested", flashFormat)
    else:
        flash(flashMessage, flashFormat)
  return render_template("views/RequestUserAccessView.html",
                          config = config,
                          userConfig = userConfig,
                          authLevel = userLevel)




