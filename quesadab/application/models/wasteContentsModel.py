from application.models.util import *
from application.logic.sortPost import *
from application.models.wasteContainersModel import Wastecontainers
from application.models.wasteChemicalsModel import Wastechemicals

class Wastecontents (Model):
    #model data to create table values and definitions to create rows in the table of waste contents
    wCID      =  PrimaryKeyField()
    wID          =  ForeignKeyField(Wastecontainers, related_name = 'container')
    wCHEMID      =  ForeignKeyField(Wastechemicals, related_name = 'chemical')
    rmWaste      =  BooleanField(default = False)

    class Meta:
        database = getDB("inventory", "dynamic")

def createWasteItem(data):
  """Creates chemical based on input from user."""
  try:
    modelData, extraData = sortPost(data, Wastecontents) #Only get relevant data for the current Model
    wItem = Wastecontents.create(**modelData)

    return(True, "Waste Item Created Successfully!", "list-group-item list-group-item-success", wItem)
  except Exception as e:
    print e
    return(False, "Waste Item Could Not Be Created.", "list-group-item list-group-item-danger", None)
