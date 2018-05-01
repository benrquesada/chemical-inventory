from application.models.util import *

class Roles (Model):
  uid           = PrimaryKeyField()
  username      = TextField()
  role          = TextField()

  class Meta:
    database = getDB("roles", "dynamic")

