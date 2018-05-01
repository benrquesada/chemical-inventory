from application.models.util import *
from application.logic.sortPost import *
from application.config import *

class Chemicals (Model):
  chemId          = PrimaryKeyField()
  oldPK           = IntegerField(null = True)
  ## General Information
  name            = CharField(null = True, unique = True)
  casNum          = CharField(null = True)
  primaryHazard   = CharField(null = False)
  formula         = CharField(null = True)
  state           = CharField(null = False)
  structure       = CharField(null = False) # Organic or Inorganic
  flashPoint      = DecimalField(null = True)
  boilPoint       = DecimalField(null = True)
  molecularWeight = DecimalField(null = True)
  storageTemp     = DecimalField(null = True)
  sdsLink         = CharField(null = True)
  description     = CharField(default = "")
  remove          = BooleanField(default = False)
  deleteDate      = DateTimeField(null = True)
  ## NFPA "Fire Diamond"
  healthHazard    = CharField(null = True) # 0-4
  flammable       = CharField(null = True) # 0-4
  reactive        = CharField(null = True) # 0-4
  other           = CharField(null = True)
  ## NFPA "Fire Diamond" DATABASE DOES NOT SUPPORT THESE YET!
  #simpleAsphyxiant= BooleanField(default = False) # Simple Asphyxiant
  #oxidizer        = BooleanField(default = False) # Oxidizer
  waterReactive   = BooleanField(default = False) # Water Reactive
  ## HMIS Color Bar
  hmisHealth      = CharField(null = True) # 0-4
  hmisFlammable   = CharField(null = True) # 0-4
  hmisPhysical    = CharField(null = True) # 0-4
  hmisPPE         = CharField(default = "A") # "A, B, C, D, E, H"
  # Ask the user which pictograms a chemical should have
  hhPict          = BooleanField(default = False) # Health Hazard Pictogram
  flamePict       = BooleanField(default = False) # Flammmable Pictogram
  emPict          = BooleanField(default = False) # Exclamation Mark Pictogram
  gcPict          = BooleanField(default = False) # Gas Cylinder Pictogram
  corrosivePict   = BooleanField(default = False) # Corrosive Pictogram
  expPict         = BooleanField(default = False) # Explosive Pictogram
  oxidizerPict    = BooleanField(default = False) # Oxidizer Pictogram
  oxidizerClass   = CharField(default = '4')      # Only if it is an oxidizer
  envPict         = BooleanField(default = False) # Environmental Hazard
  toxicPict       = BooleanField(default = False) # Acute Toxicity
  peroxideFormer  = BooleanField(default = False)
  pressureFormer  = BooleanField(default = False)
  reqStabalizer   = BooleanField(default = False) # If chemical timesensitive because it requires stablizer
  toxicFormation  = BooleanField(default = False) # If the chemical forms a toxic gas/liquid over time
  carcinogen      = BooleanField(default = False) # If carcinogenic
  pListAcute      = BooleanField(default = False) # If defined as Acutely Toxic in 40CFR 266.31

  class Meta:
    database = getDB("inventory", "dynamic")

def createChemical(data):
  """Creates chemical based on input from user."""
  try:
    modelData, extraData = sortPost(data, Chemicals) #Only get relevant data for the current Model
    if modelData['sdsLink'] == None:
      modelData['sdsLink'] = 'https://msdsmanagement.msdsonline.com/af807f3c-b6be-4bd0-873b-f464c8378daa/ebinder/?SearchTerm=%s' %(modelData['casNum'])
    elif modelData['sdsLink'][0:8] != 'https://' and  modelData['sdsLink'][0:7] != 'http://':
	    modelData['sdsLink'] = 'https://' + modelData['sdsLink']
    modelData['name'] = modelData['name'].upper()
    try:
      newChem = (Chemicals.get(name = modelData['name']), True) #True because it could get the chemical
    except:
      newChem = (Chemicals.create(**modelData), False) #Create instance of Chemical with mapped info in modelData False, because it couldn't get the chemical
    if newChem[1]:
      print modelData
      Chemicals.update(**modelData).where(Chemicals.name == newChem[0].name).execute()
      newChem[0].remove = False
      newChem[0].save()
    return(True, "Chemical Created Successfully!", "list-group-item list-group-item-success", newChem[0])
  except Exception as e:
    print e
    return(False, "Chemical Could Not Be Created.", "list-group-item list-group-item-danger", None)

def deleteChemical(chemId):
    """Deletes a Chemical from the database"""
    try:
        chem = Chemicals.get(Chemicals.chemId == chemId)
        chem.deleteDate = datetime.date.today()
        chem.remove = True
        chem.save()
        return(True, "Successfully Deleted " + chem.name + " From the System", "list-group-item list-group-item-success", chem)
    except Exception as e:
        return(False, "Failed to Delete " + chem.name + " From the System", "list-group-item list-group-item-danger", None)

def getChemicalOldPK(oldpk):
    try:
        return Chemicals.select().where(Chemicals.oldPK == oldpk).get()
    except Exception as e:
        return False

def getChemical(chemId):
  try:
    return Chemicals.get(Chemicals.chemId == chemId)
  except Exception as e:
    return e

def getChemicals():
  try:
    return Chemicals.select()
  except Exception as e:
    return e

def getChemicalHazards(chemId):
  pictList = []
  try:
    chem = Chemicals.get(Chemicals.chemId == chemId)
    if chem:
      for hazardPict in chemConfig['pictograms']:
        if getattr(chem, hazardPict['id']):
          pictList.append((hazardPict['pict'], hazardPict['alt']))
      return pictList
  except Exception as e:
    return e
