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

# PURPOSE: CheckIn a container
@app.route('/CheckIn/', methods = ['GET', 'POST'])
def CheckIn():
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
            updateHistory(cont, "Checked In", data['storageId'], user.username) # updateHistory located in historiesModel.py
            changeLocation(cont, False, data, user.username) # changeLocation located in containersModel.py
            flash('Container Checked In','list-group-item list-group-item-success')
            # Move Try and Except to containersModel.py changeLocation()
            """try:
                data = request.form
                cont = Containers.get(Containers.barcodeId == data['barcodeId'])
                Histories.create(movedFrom = cont.storageId,
                               movedTo = data['storageId'],
                               containerId = cont.conId,
                               modUser = user.username,
                               action = "Checked In",
                               pastQuantity = "%s %s" %(cont.currentQuantity, cont.currentQuantityUnit))
                cont.storageId = data['storageId']
                cont.currentQuantity = data['currentQuantity']
                cont.currentQuantityUnit = data['currentQuantityUnit']
                cont.checkedOut = False
                cont.checkOutReason =''
                cont.forProf = ''
                cont.checkedOutBy = ''
                cont.save()
                flash(data['barcodeId']+" Successfully Checked-In")
            except:
                flash("Failed to Check-In "+ data['barcodeId'])"""
        return render_template("views/CheckInView.html",
                               config = config,
                               contConfig = contConfig,
                               container = None, #container = None is needed as a placeholder for the page before the barcode is entered.
                               buildingList = buildingList,
                               storageList = storageList,
                               pageConfig = checkInConfig,
                               authLevel = userLevel)
    else:
        # This will also be replaced for a specific checkin control for all other users
        abort(403)

@app.route('/checkInData/', methods = ['GET']) #Called by AJAX from getData()
def checkInData():
    try:
        barId = request.args.get('barId') #Gets the variable that was sent via the AJAX call
        container = Containers.select().where(Containers.barcodeId == barId).dicts().get() #Get a dictionary of the container with matching barcode
        chemical = Chemicals.get(Chemicals.chemId == container['chemId']) #Get the name of the chemical that this container refers to
        storage = Storages.get(Storages.sId == container['storageId']) #Get the storageId that this container refers to
        if storage.name != storage.roomId.name: #If the storage name is not the same as it's room name, show the building, room, and storage names
            location = storage.roomId.floorId.buildId.name + " Building, Room: " + storage.roomId.name + " (" + storage.name + ")"
        else: #If the storage name is the same as it's room name, only show building and room names
            location = storage.roomId.floorId.buildId.name + " Building, Room: " + storage.roomId.name
        if chemical is not None:
            return jsonify({'status':'OK',
                            'chemName' : chemical.name,
                            'hazard': chemical.primaryHazard,
                            'storage' : location,
                            'quantity' : container['currentQuantity'],
                            'unit' : container['currentQuantityUnit'],
                            'checkedOut' : container['checkedOut']})
            #Return all data as a JSON object
    except:
        return jsonify({'status':'Error: There are no containers with that barcode in the system.'})
