function fillEditForm(chemId, config){
    $.ajax({ //AJAX call to get data from url "/getEditData" with chemId that is passed in from function call
        url: "/getEditData/",
        data: {chemId : chemId},
        type: "GET",
        success: function(data) {
            config = config.replace(/'/g, '"'); //JSON will not parse with single quotes, replacing them with double quotes
            config = config.replace(/u"/g, '"'); //Getting rid of all unicode leading characters.
            config = JSON.parse(config); //Turning string from config file into a JSON object
            for (var section in config){
                for (var element in config[section]){
                    var curElement = config[section][element];
                    if (curElement.type == "text" || curElement.type == "number"){
                        document.getElementById(curElement.id).value = data[curElement.id]; //Setting values of text and number fields to values from database
                    }
                    else if (curElement.type == "dropdown"){
                        // debugger
                        var dropdownList = document.getElementById(curElement.id);
                        dropdownList.value = data[curElement.id] //Setting selected values of dropdowns to values from database
                    }
                    else if (curElement.type == "checkbox"){
                      var checkbox = document.getElementById(curElement.id);
                      if (data[curElement.id] == 'True'){
                          checkbox.checked = true; //Setting selected boxes to true if they are set to true in database
                        }
                    }
                }
            }
        },
        error: function(){
            console.log("Error: Could not retrieve data for requested chemical"); //TODO: change this to write to a log file as well as console
        }
    });
}
