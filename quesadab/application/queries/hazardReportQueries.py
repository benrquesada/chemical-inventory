from application.models.chemicalsModel import *
from application.models.containersModel import Containers
from application.models.roomsModel import Rooms
from application.models.storagesModel import Storages
from application.models.floorsModel import Floors
from application.models.buildingsModel import Buildings
from application.models.buildingsModel import *
from application.models.historiesModel import *
###
# Flammable Liquids
###

def getIAFlamLiquids():
    ##Done
    IAFlam = (Containers.select() \
                .join(Chemicals, on = (Containers.chemId == Chemicals.chemId)) \
                .where((Chemicals.flashPoint < 73) & (Chemicals.boilPoint < 100))) \
                .switch(Containers)
    return IAFlam

def getIBFlamLiquids():
    ##Done
    IBFlam = (Containers.select() \
                .join(Chemicals, on = (Containers.chemId == Chemicals.chemId)) \
                .where((Chemicals.flashPoint < 73) & (Chemicals.boilPoint >= 100))) \
                .switch(Containers)
    return IBFlam

def getICFlamLiquids():
    ICFlam = (Containers.select() \
                .join(Chemicals, on = (Containers.chemId == Chemicals.chemId)) \
                .where((Chemicals.flashPoint >= 73) & (Chemicals.boilPoint < 100))) \
                .switch(Containers)
    return ICFlam

###
#Combustable Liquids
###
def getIIFlamLiquids():
    allIIFlam = (Chemical.select().where
    ((Chemical.flash_point > 100) & (Chemical.boil_point < 140)))

    if allIIFlam.exists():
        allChemicals = []
        for chem in allIIFlam:
            allChemicals.append(chem)
        return allChemicals
    else:
        return None

def getIIAFlamLiquids():
    allIIAFlam = (Chemical.select().where
    ((Chemical.flash_point >= 140) & (Chemical.boil_point < 200)))

    if allIIAFlam.exists():
        allChemicals = []
        for chem in allIIAFlam:
            allChemicals.append(chem)
        return allChemicals
    else:
        return None

def getIIBFlamLiquids():
    allIIBFlam = (Chemical.select().where
    (Chemical.flash_point > 200))

    if allIIBFlam.exists():
        allChemicals = []
        for chem in allIIBFlam:
            allChemicals.append(chem)
        return allChemicals
    else:
        return None

###
#Cryogenics
###

def getCryogenics():
    allCryogenics = (Chemical.select().where
    (Chemical.boil_point < -238))

    if allCryogenics.exists():
        allChemicals = []
        for chem in allCryogenics:
            allChemicals.append(chem)
        return allChemicals
    else:
        return None

###
#Flammable Solids
###

def getFlamSolids():
    allFlamSolids = (Chemical.select().where
    (Chemical.primary_hazard == "Flammable Solid"))

    if allFlamSolids.exists():
        allChemicals = []
        for chem in allFlamSolids:
            allChemicals.append(chem)
        return allChemicals
    else:
        return None

###
#Corrosive
###

def getCorrosives():
    allCorrosives = (Chemical.select().where
    (Chemical.corrosive_pict == True))

    if allCorrosives.exists():
        allChemicals = []
        for chem in allCorrosives:
            allChemicals.append(chem)
        return allChemicals
    else:
        return Nonene

###
#Water Reactive
###

def getWaterReactive():
    allWaterReactives = (Chemical.select().where
    (Checmical.wr_pict == True))

    if allWaterReactives.exists():
        allChemicals = []
        for chem in allWaterReactives:
            allChemicals.append(chem)
        return allChemicals
    else:
        return None

###
#Oxidizer
###
#This needs to be fixed because of classes
def getOxidizer(class_num):
    allOxidizers = (Chemical.select().where
    (Chemical.oxidizer_pict == True))

    if allOxidizers.exists():
        allChemicals = []
        for chem in allOxidizers:
            if chem.oxidizer_class == class_num:
                allChemicals.append(chem)
        return allChemicals
    else:
        return None
