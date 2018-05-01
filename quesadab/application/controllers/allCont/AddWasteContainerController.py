from application import app
from application.models.wasteContainersModel import *
from application.models.util import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser

from flask import \
    render_template, \
    redirect, \
    request, \
    jsonify, \
    url_for, \
    flash, \
    abort

# PURPOSE: Add New Chemical to the database
@app.route('/AddWasteContainer/', methods = ['GET', 'POST'])
def AddWaste():
    #function is what is run to render the right page, if GET, it shows the create container view which allows form entry for container
    #if Post, it creates a row entry to the database for waste containers with a relevant message for success.
  auth = AuthorizedUser()
  user = auth.getUser()
  userLevel = auth.userLevel()
  print user.username, userLevel

  if userLevel == "admin" or userLevel == "systemAdmin":
    if request.method == "GET":
        return render_template("views/AddWasteContainerView.html",
                               authLevel = userLevel,
                               config = config,
                               chemConfig = chemConfig,
                               wasteConfig = wasteConfig)

    status, flashMessage, flashFormat, wCont = createWaste(request.form) # Function located in wasteContainersModel.py
    flash(flashMessage, flashFormat)
    print wCont.wID
    #if status: # Chemical created successfully
    #  return redirect(url_for('ViewChemical', chemId = newChem.chemId)) #Redirect to the new chemical page
    #else:
    return redirect(url_for('AddWasteItem', wID = wCont.wID))

  else:
    abort(403)
