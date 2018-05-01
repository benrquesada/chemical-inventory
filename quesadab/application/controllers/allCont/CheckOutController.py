from application import app
from application.models.chemicalsModel import *
from application.models.containersModel import *
from application.models.storagesModel import *
from application.models.buildingsModel import *
from application.models.historiesModel import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser

from flask import \
    render_template, \
    request, \
    jsonify, \
    url_for, \
    flash, \
    abort
    
# PURPOSE: Check out a container
@app.route('/CheckOut/', methods=['GET', 'POST'])
def CheckOut():
    auth = AuthorizedUser()
    user = auth.getUser()
    userLevel = auth.userLevel()
    print user.username, userLevel
    
    if userLevel == "admin" or userLevel == "systemAdmin":
        storageList = getStorages()
        buildingList = getBuildings()
        if request.method == "POST":
            data = request.form
            cont = getContainer(data['barcodeId'])
            updateHistory(cont, "Checked Out", data['storageId'], user.username)
            changeLocation(cont, True, data, user.username)
            flash('Container Checked Out','list-group-item list-group-item-success')
        return render_template("views/CheckOutView.html",
                               config = config,
                               contConfig = contConfig,
                               container = None, #container = None is needed as a placeholder for the page before the barcode is entered.
                               buildingList = buildingList,
                               storageList = storageList,
                               pageConfig = checkOutConfig,
                               authLevel = userLevel,
                               user = user)
    else:
        # This will later have a slightly different render_template. To allow for all other users to access a specific checkout page.
        abort(403)
