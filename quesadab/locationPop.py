from application.models import classes
from application.config import *
from application.models import *
from application.models.staticModels.batchModel import *
from application.models.staticModels.mainModel import *
from application.models.staticModels.locatesModel import *
from application.models.chemicalsModel import *
from application.models.storagesModel import *
from application.models.historiesModel import *
from application.models.usersModel import *
import random
import datetime

def init_db():
    #Create the databases
    for database in config.databases.dynamic:
        filename = config.databases.dynamic[database].filename

        #Remove the DB
        if os.path.isfile(filename):
            os.remove(filename)

        #create an empty DB file
        open(filename, 'a').close()

    #Go through modules in models directory, and create a table for each one
    for c in classes:
        c.create_table(True)

    print 'Database Initialized'
    ####
    #Makes one building that the one floor is put in
    ####
    for building in addLocationConfig.buildings:
        print building.keys()
        currentBuildingId = buildingsModel.Buildings()
        currentBuildingId.name = building['name']
        currentBuildingId.numFloors = building['numFloors']
        currentBuildingId.address = building['address']
        currentBuildingId.save()
        for i in range(building['numFloors']):
            floorsModel.Floors(
                buildId = currentBuildingId.bId,
                name = i,
                level = i).save()
        for room in building['rooms']:
            Room = roomsModel.Rooms()
            Room.name = room['name']
            Room.floorId = room['floorId']
            Room.save()
            for storage in room['storages']:
                Storage = storagesModel.Storages()
                Storage.roomId = Room.rId
                Storage.name = storage['name']
                Storage.save()
   ####
    # Make all testing users
    ####
    usersModel.Users(
        username = "ballz",
        first_name = "Zach",
        last_name = "Ball",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()
 
    usersModel.Users(
        username = "hooverk",
        first_name = "Kye",
        last_name = "Hoover",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "heggens",
        first_name = "Scott",
        last_name = "Heggen",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "sagorj",
        first_name = "John",
        last_name = "Sagor",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "kaylorl",
        first_name = "Leslie",
        last_name = "Kaylor",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "morrism",
        first_name = "Mike",
        last_name = "Morris",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "saintilnordw",
        first_name = "Wesley",
        last_name = "Saintilnord",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "quesadab",
        first_name = "Ben",
        last_name = "Quesada",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "nandaa",
        first_name = "Asha",
        last_name = "Nanda",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "moranm",
        first_name = "Mike",
        last_name = "Morris",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "moorert",
        first_name = "Tiana",
        last_name = "Moorer",
        auth_level = "admin",
        emailadd = "test.berea.edu?",
        reportto = "test.berea.edu?",
        approve = True).save()

    usersModel.Users(
        username = "webbi",
        first_name = "Ivy",
        last_name = "Webb",
        auth_level = "admin",
        emailadd = "webbi@berea.edu",
        reportto = "Kye Hoover",
        approve = True).save()

print "Test Users were added to the database"

init_db()
