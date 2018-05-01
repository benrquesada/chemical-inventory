from application.models.util import *

class Locates(Model):
	Location          = PrimaryKeyField()
	NameSorted        = TextField()
	NameRaw           = TextField()
	UniqueContainerID = TextField()
	Id                = TextField()
	CASNo             = TextField()
	StructuralFormula = IntegerField()
	IsSupplyItem      = IntegerField()
	Quantity          = IntegerField()
	Size_Description  = IntegerField()
	NoFlamables       = IntegerField()
	KeepDesicated     = IntegerField()
	KeepFrozen        = IntegerField()
	KeepRefrigerated  = IntegerField()
	NoOxidizers       = IntegerField()
	LastUpdated       = IntegerField()
	StorPress         = TextField()
	StorTemp          = TextField()
	UseStorType       = IntegerField()

	class Meta:
		database = getDB("cispro", "static")
