from application.models.util import *
from application.models.roomsModel import Rooms

class Storages(Model):
  sId           = PrimaryKeyField()
  roomId        = ForeignKeyField(Rooms, related_name="stor") # When creating a container, select room first, then populate dropdown with all storages with matching roomId.
  oldPK         = IntegerField(null = True)
  name          = TextField() # Name of the specific storage unit ex: "Flammable Cabinet"
  # Booleans of true are what the storage is allowed to hold
  flammable     = BooleanField(default = False)
  healthHazard  = BooleanField(default = False)
  oxidizer      = BooleanField(default = False)
  orgAcid       = BooleanField(default = False)
  inorgAcid     = BooleanField(default = False)
  base          = BooleanField(default = False)
  peroxide      = BooleanField(default = False)
  pressure      = BooleanField(default = False)
  # refridgerated = BooleanField(default = False) # Do we need to check if a storage is refridgerated?

  class Meta:
    database = getDB("inventory", "dynamic")

def getStorages(room = None):
  if room == None:
    try:
      return Storages.select()
    except Exception as e:
      return e
  else:
    try:
      return Storages.select().where(Storages.roomId == room)
    except Exception as e:
      return e

def addStorage():
    #Needs to be filled in with query and return status message
    return 0

def editStorage():
    #Needes to be filled in with Query and return status message
    return 0

def deleteStorage(storage_id):
  try:
    storage = Storages.get(Storages.sId == storage_id)
    storage.delete_instance(recursive=True)
    return(True, str(storage.name) + " Storage was Successfully Removed", "list-group-item list-group-item-success")
  except Exception as e:
    return(False, str(storage.name) + " Storage was Successfully Removed", "list-group-item list-group-item-danger")

