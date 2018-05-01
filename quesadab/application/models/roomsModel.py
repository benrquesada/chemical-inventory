import application
from application.models.util import *
from application.models.floorsModel import Floors
from application.logic.sortPost import *

class Rooms (Model):
  rId        = PrimaryKeyField()
  floorId    = ForeignKeyField(Floors, related_name = "floor")
  name       = TextField() #Room number. It is a text field to account for rooms like '13c'

  class Meta:
    database = getDB("inventory", "dynamic")

def editRoom(data):
  try:
    room = Rooms.get(Rooms.rId == data['id']) #Get room to be edited and change all information to what was in form
    room.name = data['name']
    room.save()
    return(True, room.name + " was Successfully Modified", "list-group-item list-group-item-success", room)
  except Exception as e:
    return(False, "Room could not be Modified", "list-group-item list-group-item-danger", None)

def createRoom(data):
  try:
    modelData, extraData = sortPost(data, Rooms)
    room = Rooms.create(**modelData)
    lastRoomId = Rooms.select().order_by(-Rooms.rId).get().rId
    application.models.storagesModel.Storages.create(roomId = lastRoomId, # This isn't letting me import Storages or storagesModel. I think it is because that file in turn imports this one.
                    name = modelData['name'],
                    flammable = True,
                    healthHazard = True,
                    oxidizer = True,
                    orgAcid = True,
                    inorgAcid = True,
                    base = True,
                    peroxide = True,
                    pressure = True)
    return(True, room.name + " was Successfully Added to System", "list-group-item list-group-item-success", room)
  except Exception as e:
    return(False, "Room could not be Added to System", "list-group-item list-group-item-danger", None)

def getRooms(floor):
  try:
    return Rooms.select().where(Rooms.floorId == floor)
  except Exception as e:
    return e

def deleteRoom(room):
  try:
    room = Rooms.get(Rooms.rId == room)
    room.delete_instance(recursive=True)
    return(True, room.name + " was Successfully Removed From System", "list-group-item list-group-item-success")
  except Exception as e:
    return(False, "Room could not be Removed to System", "list-group-item list-group-item-danger")


