from application import app
from application.models.buildingsModel import *
from application.models.floorsModel import *
from application.models.roomsModel import *
from application.models.storagesModel import *
from application.models.containersModel import *
from application.models.util import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser
from application.logic.sortPost import *

from flask import \
    redirect, \
    request, \
    flash, \
    url_for, \
    abort

@app.route('/delete/<location>/<lId>/', methods = ['GET', 'POST']) #Called from delete location modals
def maDelete(location, lId):
    auth = AuthorizedUser()
    user = auth.getUser()
    userLevel = auth.userLevel()
    if userLevel == -1 or user == -1:
        abort(403)
    print user.username, userLevel
    if userLevel == "admin":
        state = 0
        if request.method == "GET": #Calls delete queries based on what type of location is being deleted.
            if location == "Building":
                floors = getFloors(lId) #All floors of the current building
                for floor in floors:
                    rooms = getRooms(floor) #All rooms of current floor
                    for room in rooms:
                        storages = getStorages(room) #All storage locations of current room
                        for storage in storages:
                            if getContainers(storage) != False:# Try to get any containers related to this storage, they do not need to be saved as their mere existence prohibits this building from being deleted.
                                state = 1
                if state != 1:
                    status, flashMessage, flashStatus = deleteBuilding(lId)
                    flash(flashMessage, flashStatus)
                else:
                    flash("This building could not be deleted, as there are 1 or more containers still assigned to it.",  "list-group-item list-group-item-danger")
            elif location == "Room":
                storages = getStorages(lId)
                for storage in storages:
                     if getContainers(storage) != False:# Try to get any containers related to this storage, they do not need to be saved as their mere existence prohibits this building from being deleted.
                        state = 1
                if state != 1:
                    status, flashMessage, flashStatus = deleteRoom(lId)
                    flash(flashMessage, flashStatus)
                else:
                    flash("This room could not be deleted, as there are 1 or more containers still assigned to it.", "list-group-item list-group-item-danger")
            elif location == "Storage":
                if getContainers(lId) != False:# Try to get any containers related to this storage, they do not need to be saved as their mere existence prohibits this building from being deleted.
                    state = 1
                if state != 1:
                    status, flashMessage, flashStatus = deleteStorage(lId)
                    flash(flashMessage, flashStatus)
                else:
                    flash("This storage location could not be deleted, as there are 1 or more containers still assigned to it.", "list-group-item list-group-item-danger")
        return redirect(url_for("adminHome")) #need some js to handle this and edit in order to reload the page on the location tab
    else:
        abort(403)
