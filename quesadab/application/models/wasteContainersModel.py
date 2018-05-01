from application.models.util import *
from application.logic.sortPost import *
import  datetime

class Wastecontainers (Model):
    #model data to create table values and definition to create rows in the table of waste containers
    wID              = PrimaryKeyField()
    wQuant           = FloatField(null = False)
    wQuantUnit       = CharField(default = "")
    wState           = CharField(default = "")
    wStorageDate     = DateTimeField(default = datetime.date.today)
    wProf            = CharField(default = "")
    wCourse          = CharField(default = "")
    wDept            = CharField(default = "")
    wBldg            = CharField(default = "")
    wRoom            = CharField(default = "")
    wSemester        = CharField(default = "")

    class Meta:
        database = getDB("inventory", "dynamic")

def createWaste(data):
  """Creates chemical based on input from user."""
  try:
    modelData, extraData = sortPost(data, Wastecontainers) #Only get relevant data for the current Model
    wCont = Wastecontainers.create(**modelData)

    return(True, "Waste Container Created Successfully!", "list-group-item list-group-item-success", wCont)
  except Exception as e:
    print e
    return(False, "Waste Container Could Not Be Created.", "list-group-item list-group-item-danger", None)
