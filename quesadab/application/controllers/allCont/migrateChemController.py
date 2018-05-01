from application import app
from application.models.staticModels.batchModel import *
from application.models.staticModels.mainModel import *
from application.models.staticModels.locatesModel import *
from application.models.chemicalsModel import *
from application.models.containersModel import *
from application.models.roomsModel import *
from application.models.storagesModel import *
from application.models.buildingsModel import *
from application.models.historiesModel import *
from application.config import *
from application.logic.getAuthUser import AuthorizedUser
from application.logic.sortPost import *


from flask import render_template, \
                          request, \
                          jsonify, \
                          redirect, \
                          url_for, \
                          flash

@app.route('/migrateChem/', methods = ['GET', 'POST'])
def migrateChem():
    auth = AuthorizedUser()
    user = auth.getUser()
    userLevel = auth.userLevel()
    print user.username, userLevel

    #locdict = Batch.select().dicts().get() This was used for datamodel testing
    if userLevel == 'admin' or userLevel == "systemAdmin":
        if request.method == "GET":
            return render_template("views/MigrateChem.html",
		    authLevel = userLevel,
                    config = config
                    )

        elif request.method == "POST":
           data = request.form
           if request.form['formName'] == "searchBcode":
               return renderCorrectTemplate(request.form['barcodeID'])

           elif request.form['formName'] == 'addCont':
                ###
                ##Process the form of adding a Container
                ###
                status, flashMessage, flashFormat, newChem = addContainer(data, user.username)
                flash(flashMessage, flashFormat)
                return redirect(url_for("migrateChem"))

           elif request.form['formName'] == 'addChem':
                data = request.form
                status, flashMessage, flashFormat, newChem = createChemical(request.form)
                flash(flashMessage, flashFormat)
                if status:
                    return renderCorrectTemplate(data['barcode'])

           return render_template('views/MigrateChem.html',
                    config = config,
                    authLevel = userLevel)

def renderCorrectTemplate(barcode):
                auth = AuthorizedUser()
                user = auth.getUser()
                userLevel = auth.userLevel()
                ########
                INIT = -1    #Inial start state(Not really needed but looks nice)
                MIGRATED = 0 #Both Chemical and Container already Migrated
                ONLYCHEM = 1 #Only Chemical has been Migrated. Container needs to be migrated
                NIETHER = 2  #Both Chemical and Container need to be migrated
                UNKNOWN = 3  #This container does not exist anywhere
                ########
                inputBar = barcode.upper()
                state = INIT
                containerObj = None
                chemObj = None
                #######
                if getContainer(inputBar):
                    flash("Container " + inputBar + " Already Migrated Into System", "list-group-item list-group-item-success")
                    state = MIGRATED
                #Try and Retrieve Container and Chemical Informatoin from CISPro
                if state != MIGRATED:
                    containerObj = getCisProContainer(inputBar)
                    print containerObj
                    if containerObj == False:
                        flash("Container " + inputBar + " Is Not In CISPro Database", "list-group-item list-group-item-danger")
                        state = UNKNOWN
                    if state != UNKNOWN:
                        ########
                        #If Continer in CISPro check if parent Chemical is Migrated
                        chemObj = getChemicalOldPK(containerObj.NameRaw_id)
                        if chemObj:
                            storageList = getStorages()
                            buildingList = getBuildings()
                            chemObj.remove = False #Make sure that the chemical will show in the UI
                            chemObj.save()
                            state = ONLYCHEM
                            return render_template("views/MigrateChem.html",
                                state = state,
                                container = containerObj,
                                chemInfo = chemObj,
                                inputBar = inputBar,
                                config = config,
                                contConfig = contConfig,
                                storageList = storageList,
                                buildingList = buildingList,
                                barcode = inputBar,
                                authLevel = userLevel,
                                migrated = 1)
                        else:
                            #Chemical is not yet in BCCIS
                            state = NIETHER
                            return render_template("views/MigrateChem.html",
                                state = state,
                                container = containerObj,
                                chemInfo = chemObj,
                                inputBar = inputBar,
                                config = config,
                                chemConfig = chemConfig,
                                authLevel = userLevel)

                return redirect(url_for("migrateChem"))
