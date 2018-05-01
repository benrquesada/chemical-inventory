from application.models.util import *
from application.logic.sortPost import *


class Buildings (Model):
  bId        = PrimaryKeyField()
  name       = TextField() #Sans "Building"
  numFloors  = FloatField()
  address    = TextField()

  class Meta:
    database = getDB("inventory", "dynamic")

def getBuilding(lId):
  try:
    return Buildings.get(Buildings.bId == lId)
  except Exception as e:
    return e

def getBuildings():
  try:
    return Buildings.select()
  except Exception as e:
    return e

def editBuilding(data):
  try:
    building = Buildings.get(Buildings.bId == data['id']) #Get building to be edited
    building.name = data['name'] #Change all information to what was in the form
    building.address = data['address']
    building.save()
    return(True, building.name + "Building was Successfully Modified", "list-group-item list-group-item-success", building)
  except Exception as e:
    return(False, building.name + "Building Could Not be Modified", "list-group-item list-group-item-danger", building)

def createBuilding(data):
  try:
    modelData, extraData = sortPost(data, Buildings)
    build = Buildings.create(**modelData)
    return(True, build.name + " Building was Successfully Added to System", "list-group-item list-group-item-success", build)
  except Exception as e:
    return (False, build.name + " Building Could Not Be Added to System", "list-group-item list-group-item-danger", none)

def deleteBuilding(bId):
  try:
    building = getBuilding(bId)
    building.delete_instance(recursive=True) # With recursive set to True, this will go through and delete the building and everything that is associated with it. ie: Floors, Rooms, and Storages
    return(True, building.name + " Building was Deleted From the System", "list-group-item list-group-item-success")
  except Exception as e:
    return (False, build.name + " Building Could Not Be Deleted From the System", "list-group-item list-group-item-danger")


