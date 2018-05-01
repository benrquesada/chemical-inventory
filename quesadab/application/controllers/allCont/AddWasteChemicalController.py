#



from application import app
from application.models.wasteContainersModel import *
from application.models.wasteContentsModel import *
from application.models.wasteChemicalsModel import *
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
@app.route('/AddWasteContents/<wID>/AddWasteChemical', methods = ['GET', 'POST'])
def AddWasteChemical(wID):
    #function is what is run to render the right page, if GET, it shows the create chemical view which allows form entry for chemicals
    #if Post, it creates a row entry to the database for waste chemicals as well as a row entry for contents to
    #show which container the chemical is in with a relevant message for success.
  auth = AuthorizedUser()
  user = auth.getUser()
  userLevel = auth.userLevel()
  print user.username, userLevel

  if userLevel == "admin" or userLevel == "systemAdmin":
    if request.method == "GET":
        return render_template("views/AddWasteChemicalView.html",
                               authLevel = userLevel,
                               config = config,
                               wasteConfig = wasteConfig)

    status, flashMessage, flashFormat, wChem = createWasteChemical(request.form) # Function located in wasteChemicalsModel.py
    flash(flashMessage, flashFormat)
    print(wID)
    contentData= {'wCHEMID':unicode(str(wChem.wCHEMID), "utf-8"),'wID':unicode(str(wID), "utf-8")}


    status, flashMessage, flashFormat, wCont = createWasteItem(contentData) # Function located in wasteContentsModel.py
    flash(flashMessage, flashFormat)


    return redirect(url_for('AddWasteItem', wID = wID))

  else:
    abort(403)
