function getLocation(loc_type){
  var locId = document.getElementById(loc_type).value;
  reset_fields(loc_type) //Clears all data of children fields
  getData(locId, loc_type)
}

function reset_fields(loc_type){
  if (loc_type == "Building"){
    var locToDisable = ['#Floor', '#Room', '#Storage']
  }
  else if (loc_type == "Floor"){
    var locToDisable = ['#Room', '#Storage']
  }
  else if (loc_type == "Room"){
    var locToDisable = ['#Storage']
  }
  for(var i =0; i < locToDisable.length; i++){
    $(locToDisable[i]).children('.default').prop('selected', true);
    $(locToDisable[i]).prop('disabled', true);
  }
}

function getData(locId, locType){
  $.ajax({ //AJAX call to url "/getLocation/" to get location children
    url: "/locationData/",
    data: {locId : locId, locType : locType},
    type: "GET",
    success: function(data) {
      if (data['status'] === 'OK'){
        $('[name=' + data["objectType"] + ']').prop('disabled', false);
        var options = "<option class='default' value='*'>All " + data["objectType"] + "s</option>"
        for(var i = 0; i < data['locObject'].length; i++){
          if (data['objectType'] == "Floor"){
            options += '<option value="' + data['locObject'][i].fId  + '">' + data['locObject'][i].name + '</option>';
          }
          else if (data['objectType'] == "Room"){
            options += '<option value="' + data['locObject'][i].rId  + '">' + data['locObject'][i].name + '</option>';
        }
          else if (data['objectType'] == "Storage"){
            options += '<option value="' + data['locObject'][i].sId  + '">' + data['locObject'][i].name + '</option>';
          }
        }
        $("select#" + data["objectType"]).html(options);
      }
    }
  })
}

function enableFields(){
  //This enables all fields on form so they get submitted
  $('select:disabled').prop('disabled', false);
}
