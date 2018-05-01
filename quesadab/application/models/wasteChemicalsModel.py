from application.models.util import *
from application.logic.sortPost import *


class Wastechemicals (Model):
    #model data to create table values and definition to create rows in the table of waste chemicals
    wCHEMID = PrimaryKeyField()
    wName   = CharField(null = False)
    wCasNo  = CharField(null = True)
    wFlam   = BooleanField(default = False)
    wCorr   = BooleanField(default = False)
    wTox    = BooleanField(default = False)
    wReact  = BooleanField(default = False)
    wBio    = BooleanField(default = False)
    wRadio  = BooleanField(default = False)
    wHealth = BooleanField(default = False)
    wPlist  = BooleanField(default = False)

    class Meta:
        database = getDB("inventory", "dynamic")

def createWasteChemical(data):
  """Creates chemical based on input from user."""
  try:
    modelData, extraData = sortPost(data, Wastechemicals) #Only get relevant data for the current Model
    wCont = Wastechemicals.create(**modelData)

    return(True, "Waste Chemical Created Successfully!", "list-group-item list-group-item-success", wCont)
  except Exception as e:
    print e
    return(False, "Waste Chemical Could Not Be Created.", "list-group-item list-group-item-danger", None)
