from application.models.util import *
from application.models.chemicalsModel import Chemicals
from application.models.storagesModel import Storages
from application.models.roomsModel import *
import datetime

class Containers (Model):
  conId              = PrimaryKeyField()
  ##Foreign Keys
  chemId             = ForeignKeyField(Chemicals, related_name = 'chemical')
  storageId          = ForeignKeyField(Storages, related_name = 'storage')
  ##
  barcodeId          = CharField(null = False, unique = True)
  currentQuantityUnit= TextField() # units of chemical
  currentQuantity    = FloatField()# amount of chemical currently in container
  receiveDate        = DateTimeField(default = datetime.date.today)
  disposalDate       = DateTimeField(null = True)
  conType            = CharField(default = "")
  manufacturer       = CharField(null = True)
  capacityUnit       = CharField(default = "") # units container is initially measured in
  capacity           = FloatField(null = False)# amount of units that the container can hold
  checkedOut         = BooleanField(default = False) # set to True upon checkout
  checkOutReason     = CharField(null = True)
  forProf            = CharField(null = True)
  checkedOutBy       = CharField(null = True) # Will be filled in with users username upon checkout
  migrated           = IntegerField(null = True) # If the container was migrated from CISPro
  waste              = BooleanField(default = False) # If the container is in waste
  removalDate        = DateTimeField(null = True) # This will be for when waste is disposed
  peroxideCheckDate  = DateTimeField(null = True)

  class Meta:
    database = getDB("inventory", "dynamic")

def getContainer(barcode):
  """Returns a Containers object with the given barcode"""
  try:
    return Containers.get((Containers.barcodeId == barcode)|(Containers.barcodeId == str(barcode).upper()))
  except:
    return False

def addContainer(data, user):
    """Used to add a new container

    Args:
        data (dict): From data input by user
        user (str): User creating container
    Returns:
        Array containing status details (Bool, Str, Str, Object_Created)
        """
    try:
        modelData, extraData = sortPost(data, Containers)
        cont = Containers.create(**modelData)
        application.models.historiesModel.updateHistory(cont, "Created", data['storageId'], user)
        return (True, "Container Created Successfully!", "list-group-item list-group-item-success", cont)
    except Exception as e:
        print e
        return (False, "Container Could Not Be Created!", "list-group-item list-group-item-danger", None)
    return Containers.get(Containers.barcodeId == barcode)

def changeLocation(cont, status, data, user):
  """Used to check containers in and out

  Args:
      container (Containers): the container to be changed
      status (bool): True if container is being checked out, False if checked in
      data (dict): Form data from user.
  Returns:
      Nothing
  """ #should return something for unit testing later
  print data
  if status: # True if checking out
    try:
      cont.storageId = data['storageId']
      cont.checkedOut = status
      cont.checkOutReason = data['forClass']
      cont.forProf = data['forProf']
      cont.checkedOutBy = user
      cont.save()
    except Exception as e:
      return e
  else: # Checking in
    try:
      cont.storageId = data['storageId']
      cont.currentQuantity = data['currentQuantity']
      cont.currentQuantityUnit = data['currentQuantityUnit']
      cont.checkedOut = status
      cont.checkOutReason = ''
      cont.forProf = ''
      cont.checkedOutBy = ''
      cont.save()
    except Exception as e:
      return e

def contCount(chemicals):
  """Gets a count of how many containers are currently checked in and not disposed of for each chemical

  Args:
      chemicals (list): a list of all chemicals in the database
  Returns:
      dict: a dictionary with keys of every chemical name, and values of how many containers are available for checkout
  """
  contDict = {} #Set up a dictionary for all containers
  for chemical in chemicals: #For each chemical
    try:
      contDict[chemical.name] = ((((Containers
                                .select())
                                .join(Chemicals))
                                .where(
                                  (Containers.disposalDate == None) &
                                  (Containers.chemId == chemical.chemId) &
                                  (Chemicals.remove == False))))
    except:
      contDict[chemical.name] = "n/a"
  return contDict

def getContainers(storage):
  try:
    Containers.get(Containers.storageId == storage,
                   Containers.disposalDate == None)
  except Exception as e:
    return False 

def disposeContainer(bId):
    try:
        cont = getContainer(bId)
        cont.disposalDate = datetime.date.today()
        cont.save()
        return (True, "Container "+ bId +" was removed successfully!", "list-group-item list-group-item-success")
    except Exception as e:
        return (False, "Container "+ bId +" was could not be removed!", "list-group-item list-group-item-danger")

