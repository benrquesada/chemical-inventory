from application import app
from application.models.containersModel import *
from application.models.chemicalsModel import *
from application.models.storagesModel import *
from application.models.buildingsModel import *
from application.models.historiesModel import *
from application.models.containersModel import *
from application.models import *
from application.models.containersModel import *
from application.models.historiesModel import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser
from application.logic.sortPost import *
import datetime

from flask import \
    render_template, \
    request, \
    redirect, \
    url_for, \
    abort,  \
    flash

# PURPOSE: CheckOut a container
@app.route('/ContainerInfo/<chemId>/<barcodeId>/', methods = ['GET', 'POST'])
def maContainerInfo(chemId, barcodeId):
  auth = AuthorizedUser()
  user = auth.getUser()
  userLevel = auth.userLevel()
  print user.username, userLevel

  if userLevel == "admin" or userLevel == "systemAdmin":
    chemical = getChemical(chemId)
    if chemical.remove == True:
      return redirect('/ChemTable')
    container = getContainer(barcodeId)
    if container.disposalDate is not None:
      return redirect('/ChemTable')
    storageList = getStorages()
    buildingList = getBuildings()
    histories = getContainerHistory(container.conId)
    if request.method =="POST":
      data = request.form
      cont = getContainer(barcodeId)
      if data['formName'] == 'checkOutForm':
        updateHistory(cont, "Checked Out", data['storageId'], user)
        changeLocation(cont, True, data, user.username)
      else:
        updateHistory(cont, "Checked In", data['storageId'], user)
        changeLocation(cont, False, data, user.username)
      return redirect('/ViewChemical/%s/' %(chemId))
    else: #It is a GET
      return render_template("views/ContainerInfoView.html",
                         config = config,
                         contConfig = contConfig,
                         pageConfig = checkInConfig,
                         container = container,
                         chemical = chemical,
                         storageList = storageList,
                         buildingList = buildingList,
                         histories = histories,
                         authLevel = userLevel)
  else:
    abort(403)


@app.route('/ContainerInfo/<chemId>/<barcodeId>/dispose/', methods = ['GET', 'POST'])
def maContainerDispose(chemId, barcodeId):
  status, flashMessage, flashFormat = disposeContainer(barcodeId)
  flash(flashMessage, flashFormat)
  if status: #Container disposed successfully
    return redirect('/ViewChemical/%s/' %(chemId))
  else:
    return redirect('/ContainerInfo/%s/%s/' %(chemId, barcodeId))
