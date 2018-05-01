from application.models.chemicalsModel import *
from application.models.containersModel import Containers
from application.models.roomsModel import Rooms
from application.models.storagesModel import Storages
from application.models.floorsModel import Floors
from application.models.buildingsModel import Buildings
from application.models.buildingsModel import *
from application.models.historiesModel import *

def getChemInLoc(loc_data):
    ##Returns all containers, chem in Storages and rooms and floors in build
    loc_cons = {"Building":"Buildings.bId == loc_data['Building']", "Floor":"Floors.fId == loc_data['Floor']", "Room":"Rooms.rId == loc_data['Room']", "Storage":"Storages.sId == loc_data['Storage']"}
    haz_cons = {"reactive":"Chemicals.primaryHazard == 'Reactive'", "hh":"Chemicals.primaryHazard == 'Health Hazard'", "base":"Chemicals.primaryHazard == 'Base'", "oxi":"Chemicals.primaryHazard == 'Oxidizer'", "flam":"Chemicals.primaryHazard == 'Flammable'", "inorg_acid":"Chemicals.primaryHazard == 'Inorganic Acid'", "flam_solid":"Chemicals.primaryHazard == 'Flammable Solid'", "org_acid":"Chemicals.primaryHazard == 'Organic Acid'", "gen_haz":"Chemicals.primaryHazard == 'General Hazard'", "pres":"Chemicals.pressureFormer == True", "per":"Chemicals.peroxideFormer == True", "req_stab":"Chemicals.reqStabalizer == True", "tox_form":"Chemicals.toxicFormation == True", "p_list":"Chemicals.pListAcute == True"}
    ##The ifs are to instanciate the where, not sure how else to do it
    if loc_data["Building"] != "*":
        wheres = eval(loc_cons["Building"])
    else:
        wheres = Buildings.name == Buildings.name
    haz_where = eval("Chemicals.primaryHazard == 'Nothing'") #Does nothing but instanciate object
    for value in loc_data:
        if (loc_data[value] != "*") and (value in loc_cons):
            wheres &= eval(loc_cons[value])
        elif value in haz_cons: 
            haz_where |= eval(haz_cons[value])
        else:
            #No conditional provided
            pass
    if len(loc_data) > 4:
        wheres &= haz_where

    conts = (Containers.select() \
                .join(Chemicals, on = (Containers.chemId == Chemicals.chemId)) \
                .join(Storages, on = (Containers.storageId == Storages.sId)) \
                .join(Rooms, on = (Rooms.rId == Storages.roomId)) \
                .join(Floors, on = (Floors.fId == Rooms.floorId)) \
                .join(Buildings, on = (Buildings.bId == Floors.buildId)) \
                .where(wheres)\
                .switch(Containers))
    return conts

def getChemInStor(s_id):
    ##Done cont.storageId.roomId.floorId.buildId.name
    conts = (Containers.select() \
                .where(Containers.storageId == s_id))
    return conts

def getChemInRoom(r_id):
    ##Done
    ##Return all chemicals in Room
    conts = (Containers.select() \
                .join(Storages, on = (Containers.storageId == Storages.sId)) \
                .join(Rooms, on = (Rooms.rId == Storages.roomId)) \
                .where(Rooms.rId == r_id)
                .switch(Containers))
    return conts

def getChemInFloor(f_id):
    ##Done
    ##Return all containers, chem, in Storages and rooms on Floor
    conts = (Containers.select() \
                .join(Storages, on = (Containers.storageId == Storages.sId)) \
                .join(Rooms, on = (Rooms.rId == Storages.roomId)) \
                .join(Floors, on = (Floors.fId == Rooms.floorId)) \
                .where(Floors.fId == f_id) \
                .switch(Containers))
    return conts

def getChemInBuild(b_id):
    ##Returns all containers, chem in Storages and rooms and floors in build
    conts = (Containers.select() \
                .join(Storages, on = (Containers.storageId == Storages.sId)) \
                .join(Rooms, on = (Rooms.rId == Storages.roomId)) \
                .join(Floors, on = (Floors.fId == Rooms.floorId)) \
                .join(Buildings, on = (Buildings.bId == Floors.buildId)) \
                .where(Buildings.bId == b_id) \
                .switch(Containers))
    return conts

def getIAFlamLiquids():
    allIAFlam = (Containers.select() \
                    .join(Chemicals, on = (Containers.chemId == Chemicals.chemId)) \
                    .where((Chemicals.flashPoint < 73) & (Chemicals.boilPoint < 100))) \
                    .switch(Containers)
    return allIAFlam

