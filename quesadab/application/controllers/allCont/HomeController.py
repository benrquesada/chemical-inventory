from application import app
from application.models.buildingsModel import *
from application.models.floorsModel import *
from application.models.roomsModel import *
from application.models.storagesModel import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser

from flask import \
    render_template, \
    redirect, \
    request, \
    jsonify, \
    flash, \
    url_for

####################################################
@app.route("/")
def homeRedr():
    return redirect('/Home/')
####################################################


# PURPOSE: Edit, delete, and add buildings
@app.route('/Home/', methods = ['GET', 'POST'])
# 'admin')
def adminHome():
    auth = AuthorizedUser()
    user = auth.getUser()
    userLevel = auth.userLevel()
    if user == -1:
        render_template("views/UnathorizedView.html")
    print user.username, userLevel

    if userLevel == "admin" or userLevel == "systemAdmin":
        buildings = getBuildings()
        floors = {}
        rooms = {}
        storages = {}
        if request.method == "POST":
            data = request.form #If a form is posted to the page
            if data['location'] == "Building": #If the form is editing a building
                if data['action'] == 'edit':
                    status, flashMessage, flashFormat, editBuild = editBuilding(data)
                elif data['action'] == 'add':
                    status, flashMessage, flashFormat, newBuild = createBuilding(data)
                    if status:
                        for value in range(int(data['numFloors'])):
                            createFloor({'buildId': str(newBuild.bId), 'name':"Level " + str(value), 'level': str(value) })
                    flash(flashMessage, flashFormat)
            elif data['location'] == "Floor": #If the form is editing a floor
                status, flashMessage, flashFormat, editedFloor = editFloor(data)
                flash(flashMessage, flashFormat)
            elif data['location'] == "Room": #If the form is editing a room
                if data['action'] == 'edit':
                    status, flashMessage, flashFormat, editedRoom = editRoom(data)
                    flash(flashMessage, flashFormat)
                elif data['action'] == 'add':
                    status, flashMessage, flashFormat, editedRoom = createRoom(data)
                    flash(flashMessage, flashFormat)
            elif data['location'] == "Storage": #If the form is editing a storage
                if data['action'] == 'edit':
                    print data
                    storage = Storages.get(Storages.sId == data['id']) #Get storage location to be edited and change all information to what was in form
                    for i in data:
                        setattr(storage, i, data[i])
                    storage.save()
                elif data['action'] == 'add':
                    modelData, extraData = sortPost(data, Storages)
                    Storages.create(**modelData)
            return redirect(url_for("adminHome"))

        for building in buildings: #Set floor dictionary with key of current building, and value of all floors that reference that building
            floors[building.bId] = getFloors(building.bId)
            for floor in floors[building.bId]: #Set room dictionary with key of current floor, and value of all rooms that reference that floor
                rooms[floor.fId] = Rooms.select().where(Rooms.floorId == floor.fId).order_by(+Rooms.name)
                for room in rooms[floor.fId]: #Set storage dictionary with key of current room, and value of all storages that reference that room
                    storages[room.rId] = Storages.select().where(Storages.roomId == room.rId)

        return render_template("views/HomeView.html",
                               config = config,
                               locationConfig = locationConfig,
                               buildings = buildings,
                               floors = floors,
                               rooms = rooms,
                               storages = storages,
                               authLevel = userLevel)

    else:
        return redirect("/ChemTable")

@app.route("/getBuildingData/", methods = ['GET'])
def getBuildingData():
    bId = request.args.get('bId')
    building = Buildings.select().where(Buildings.bId == bId).dicts().get()
    for key in building:
        building[key] = str(building[key])
    return jsonify(building)

@app.route("/getFloorData/", methods = ['GET'])
def getFloorData():
    fId = request.args.get('fId')
    floor = Floors.select().where(Floors.fId == fId).dicts().get()
    for key in floor:
        floor[key] = str(floor[key])
    return jsonify(floor)

@app.route("/getRoomData/", methods = ['GET'])
def getRoomData():
    rId = request.args.get('rId')
    room = Rooms.select().where(Rooms.rId == rId).dicts().get()
    for key in room:
        room[key] = str(room[key])
    return jsonify(room)

@app.route("/getStorageData/", methods = ['GET'])
def getStorageData():
    sId = request.args.get('sId')
    storage = Storages.select().where(Storages.sId == sId).dicts().get()
    for key in storage:
        storage[key] = str(storage[key])
    return jsonify(storage)
