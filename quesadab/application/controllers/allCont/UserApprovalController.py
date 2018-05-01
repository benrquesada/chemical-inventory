from application import app
from application.models.usersModel import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser
from application.logic.sortPost import *

from flask import \
    render_template, \
    request, \
    url_for, \
    abort, \
    flash

# PURPOSE: Approve and Deny Users
@app.route('/UserApproval/', methods = ['GET', 'POST'])
def UserApproval():
  # User authorization
  auth = AuthorizedUser()
  user = auth.getUser()
  userLevel = auth.userLevel()
  if userLevel == -1 or user == -1:
    abort(403)
  print user.username, userLevel

  if userLevel == "admin":
    if request.method == "POST":
      data = request.form
      usersList = request.form.getlist("users")
      # print usersList
      # print data
      if 'approveButton' in data:
        # print data['approveButton']
        for user in usersList:
          flashMessage, flashFormat = approveUsers(user)
          flash(flashMessage, flashFormat)
      elif 'denyButton' in data:
        #TODO: delete users that were denied
        print data['denyButton']
        for user in usersList:
          try:
            query = Users.delete().where(Users.userId == user)
            query.execute()
            flash("Success: User has been denied.", 'list-group-item list-group-item-success')
          except:
            flash("Error: User could not be removed.", 'list-group-item list-group-item-danger')
        pass
      else:
        #User was neither approved or denied? This should never happen...
        pass
    pendingUsers = Users.select().where(Users.approve == False)
    return render_template("views/UserApprovalView.html",
                          config = config,
                          userConfig = userConfig,
                          authLevel = userLevel,
                          pendingUsers = pendingUsers)
  else:
    abort(403)
