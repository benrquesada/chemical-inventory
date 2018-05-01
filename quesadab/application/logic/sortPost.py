import datetime
from unidecode import unidecode

def sortPost( data, model):
  # print "sortPost"
  # print data
  """
    Takes a dictionary and a model to replace empty strings with None.
    It also splits post data into two variable model_data and extra_data.
    Model data only has feilds present in the model, extra has all extra data.
    Requires that the name field in the html is the same as the model's field.

    Inputs:
      - data: form data to sort
      - model: the model related to the form data
    Returns:
    - model data (e.g., name) and extra data (anything that's not in input model, e.g., TimeSpentEatingLunchToday)
  """
  model_data = dict()
  extra_data = dict()
  for key in iter( data ):
    if data[key] == "":
      if hasattr( model, key ):
        # print (model, key)
        if getattr( model, key ).null is True:
          model_data[key] = None
        else:
          model_data[key] = data[key]
      else:
        extra_data[key] = data[key]

    elif hasattr( model, key ):
      instance = getattr(model, key)
      field_type = getattr(instance, "db_field")
      if field_type == "datetime":
        fixed_date = convert_to_datetime(data[key])
        model_data[key] = fixed_date
      elif field_type == bool:
        model_data[key] = bool(data[key])
      else:
        model_data[key] = unidecode(data[key])
    else:
     extra_data[key] = data[key]

  return ( model_data, extra_data )

def convert_to_datetime(dateString):
  return datetime.datetime.strptime(dateString, '%Y-%m-%d').date()
