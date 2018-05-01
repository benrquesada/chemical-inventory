from application import app
from application.models.wasteContainersModel import *
from application.models.wasteContentsModel import *
from application.models.util import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser
from urllib import *

from flask import \
    render_template, \
    redirect, \
    request, \
    jsonify, \
    url_for, \
    flash, \
    abort

# PURPOSE: Add New Chemical to the database
@app.route('/AddWasteContents/<wID>/', methods = ['GET', 'POST'])
def AddWasteItem(wID):
        #function is what is run to render the right page, if GET, it shows the add waste contents view which allows a place to click to add chemicals
        #if Post, it redirects to waste chemicals page with a specific url conatining the waste container number.

  auth = AuthorizedUser()
  user = auth.getUser()
  userLevel = auth.userLevel()
  print user.username, userLevel

  if userLevel == "admin" or userLevel == "systemAdmin":
    if request.method == "GET":
        return render_template("views/AddWasteContentsView.html",
                               wID = wID,
                               authLevel = userLevel,
                               config = config,
                               wasteConfig = wasteConfig)


    return redirect(url_for('AddWasteChemical', wID = wID))

  else:
    abort(403)
