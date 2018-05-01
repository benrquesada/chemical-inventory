from application.models.util import *
from application.models.storagesModel import Storages
from application.models.containersModel import Containers 
import datetime

class Histories (Model):
  hId          = PrimaryKeyField()
  ##Foreign Keys
  movedFrom     = ForeignKeyField(Storages, related_name="movedFrom", null = True)
  movedTo       = ForeignKeyField(Storages, related_name="movedTo")
  containerId   = ForeignKeyField(Containers, related_name = "containers")
  ##
  modUser       = TextField(null = True) # This should probably eventually be a foreign key to the users table.
  ##
  action        = CharField()
  pastQuantity  = CharField()# This holds both the quantity and unit as a string. Since it won't be changed, the two fields could be combined
  modDate       = DateTimeField(default = datetime.datetime.now) #If a history instance is made, and the call doesn't specify the date, the default will take care of it

  class Meta:
    database = getDB("inventory", "dynamic")

def updateHistory(container, action, location, modifiedBy):
  """Creates a new history instance everytime a container is moved

  Args:
      container (Containers): the container to be changed
      action (str): 'Checked In' -OR- 'Checked Out' -OR- 'Created'
      location (Storages): Specific storage location that the container is being moved to
      modifiedBy (str): Username of user that accessed the page that called this function
  Returns:
      Nothing
  """ #should return something for unit testing later
  try:
    Histories.create(movedFrom = container.storageId,
                  movedTo = location,
                  containerId = container.conId,
                  modUser = modifiedBy,
                  action = action,
                  pastQuantity = "%s %s" %(container.currentQuantity, container.currentQuantityUnit))
    return "History updated"
  except:
    return "History failed to update"

def getContainerHistory(containerId):
  """Gets all history objects of a specific container

  Args:
      containerId (str): Unique identifier for one container
  Returns:
      All history objects of a specific container"""
  try:
    return Histories.select().where(Histories.containerId == containerId)
  except Exception as e:
    return e
