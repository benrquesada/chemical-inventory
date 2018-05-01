import os
from application import app
from application.config import *
from application.models import *
from application.models.floorsModel import *
from application.models.roomsModel import *
from application.models.storagesModel import *
from application.logic.getAuthUser import AuthorizedUser
from application.logic.excelMaker import *
from playhouse.shortcuts import model_to_dict, dict_to_model
#from absolutepath import getAbsolutePath


from flask import render_template, \
                  request, \
                  flash, \
                  redirect, \
                  url_for, \
                  jsonify, \
                  current_app, \
                  send_from_directory

@app.route('/Report/', methods = ['GET', 'POST'])
def report():
    auth = AuthorizedUser()
    user = auth.getUser()
    userLevel = auth.userLevel()
    if userLevel == 'admin' or userLevel == 'superUser' or userLevel == 'systemAdmin':
        if request.method == "GET":
            allBuild = getBuildings()
            inputs = [None] * len(reportConfig.ReportTypes.Inputs)
            for key in reportConfig.ReportTypes.Inputs:
                index = reportConfig.ReportTypes.Inputs[key]
                inputs[index] = key
            return render_template("views/ReportView.html",
                                   authLevel = userLevel,
                                   config = config,
                                   reportConfig = reportConfig,
                                   inputs = inputs,
                                   allBuild = allBuild)
        else:
            data = request.form 
            locData = genLocationReport(data)
            path = os.path.join(current_app.root_path, 'reports')
            #make the directory if it doesn't exist
            try:
                os.makedirs(path)
            except:
                pass
            reportName = exportExcel("Report", reportConfig["ReportTypes"]["LocationBased"]["LocationQuantity"]["row_title"], reportConfig["ReportTypes"]["LocationBased"]["LocationQuantity"]["queries"], locData, path)
            return redirect("/download/" + reportName)

@app.route('/download/<path:filename>', methods=["GET"])
def download(filename):
    ##Download file path
    reports = os.path.join(current_app.root_path, 'reports')
    return send_from_directory(directory=reports, filename=filename)

@app.route('/locationData/', methods = ['GET'])
def locationData():
    locId = request.args.get('locId')
    locType = request.args.get('locType')
    #print locType
    if locType == "Building":
        locObject = getFloors(locId)
        objectType = "Floor"
    elif locType == "Floor":
        locObject = getRooms(locId)
        objectType = "Room"
    elif locType == "Room":
        locObject = getStorages(locId)
        objectType = "Storage"
    locs = list()
    for loc in locObject:
        locs.append(model_to_dict(loc))
    return jsonify({'status':'OK',
                    'locObject' : locs,
                    'objectType' : objectType})
