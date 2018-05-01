from application import app
from application.models.chemicalsModel import *
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
@app.route('/AddChemical/', methods = ['GET', 'POST'])
def AddChemical():
  auth = AuthorizedUser()
  user = auth.getUser()
  userLevel = auth.userLevel()
  print user.username, userLevel

  if userLevel == "admin" or userLevel == "systemAdmin":
    if request.method == "GET":
        return render_template("views/AddChemicalView.html",
                               authLevel = userLevel,
                               config = config,
                               chemConfig = chemConfig)

    status, flashMessage, flashFormat, newChem = createChemical(request.form) # Function located in chemicalsModel.py
    flash(flashMessage, flashFormat)
    if status: # Chemical created successfully
      return redirect(url_for('ViewChemical', chemId = newChem.chemId)) #Redirect to the new chemical page
    else:
      return render_template("views/AddChemicalView.html",
                             authLevel = userLevel,
                             config = config,
                             chemConfig = chemConfig)

  else:
    abort(403)

@app.route('/checkName/', methods=['GET'])
def checkName():
  nameVal = request.args.get('value')
  try:
    chemical = chemicalsModel.Chemicals.get(chemicalsModel.Chemicals.name == nameVal)
    if chemical is not None:
      return jsonify({'required':True}) #Build the json dict for a success
  except:
    print "This should log something..."
    return jsonify({'required':False})
