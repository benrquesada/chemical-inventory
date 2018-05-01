from application.models.util import *
from application.models.staticModels.locatesModel import *
from application.models.staticModels.mainModel import *

class Batch(Model):
   NameSorted         = PrimaryKeyField()
   NameRaw            = ForeignKeyField(Main)
   UniqueContainerID1 = TextField()
   Id                 = ForeignKeyField(Locates)
   """
   IsSupplyItem       = TextField()
   Quantity           = TextField()
   Size_Description   = TextField()
   NewLocationID      = TextField()
   ChangeDate         = TextField()
   NewLocation        = TextField()
   """
   UniqueContainerID  = TextField()
   """
   Rollbac_           = TextField()
   InitialDate        = TextField()
   InitialTimeSeconds = TextField()
   InitialTimeMinutes = TextField()
   InitialTimeHours   = TextField()
   DecayedRate        = TextField()
   ReservedNumber     = TextField()
   ReservedText       = TextField()
   ReservedInt        = TextField()
   ReservedDate       = TextField()
   DateLastUpdated    = TextField()
   WhoLastUpdated     = TextField()
   ParentContainerID  = TextField()
   ContNotes          = TextField()
   LastRibm           = TextField()
   ContainerStatus    = TextField()
   ParentBatchID      = TextField()
   ParentBarcode      = TextField()
   RETEST_date        = TextField()
   LASTTEST_date      = TextField()
   ALT_CONTAINERID    = TextField()
   alt_locationid     = TextField()
   usert1             = TextField()
   usert2             = TextField()
   userd1             = TextField()
   userd2             = TextField()
   usern1             = TextField()
   usern2             = TextField()
   AccessMode         = TextField()
   StorPress          = TextField()
   StorTemp           = TextField()
   UseType            = TextField()
   ContDescript       = TextField()
   open_date          = TextField()
   DateLastScanned    = TextField()
   """
   class Meta:
       database = getDB("cispro", "static")

def getCisProContainer(barcode):
    try:
        return Batch.select()\
                .join(Main, on=(Batch.NameRaw_id == Main.NameSorted))\
                .join(Locates, on=(Batch.Id_id == Locates.Location))\
                .where((Batch.UniqueContainerID == barcode)|(Batch.UniqueContainerID == str(barcode).upper())).get()
    except Exception as e:
        print e
        return False


