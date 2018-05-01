function checkBar(formAction){
    var barInput = document.getElementById('barcodeId').value;
    if (barInput.length >= 4){ //Only runs after user has entered 8 digits into barcode field (all barcodes will be 8 digits)
        getData(barInput, formAction); //Fill enabled fields
    }else{
        changeForm(true); //Disable and clear fields when there are less than 8 digits in the field
    }
}

function changeForm(status){
    var inputList = document.getElementsByClassName("d");
    for (var i = 0; i < inputList.length; i++){ //For all elements with class "d"
        if (status == true){
           inputList[i].value = ''; //If status is true, change values of all fields to an empty string. When barcode is removed, values don't remain in text boxes.
        }
        inputList[i].disabled = status; //change disabled value to whatever is passed in. If true, they are disabled. If false, they are not.
    }
}

function getData(barcodeId, formAction){
    $.ajax({ //AJAX call to url "/checkInData/" to get info with barcodeId that is passed in from checkBar function
        url: "/checkInData/",
        data: {barId : barcodeId},
        type: "GET",
        success: function(data) { //fill values of elements: 'chemId', 'prevStorageId', and 'prevQuantity' with info from database
            if (data['status'] === 'OK') {
                if (formAction == 'checkOut') {
                    if (data['checkedOut'] == true){
                        changeForm(true);
                        alert("That container is already checked out.");
                        document.getElementById('submit').disabled = true;
                        return false;
                    };
                }else{
                    document.getElementById('currentQuantityUnit').value = data['unit'];
                };
                document.getElementById("chemId").value = data['chemName'];
                document.getElementById("primaryHazard").value = data['hazard']
                document.getElementById('prevStorageId').value = data['storage'];
                document.getElementById('prevQuantity').value = data['quantity'] + " " + data['unit'];
                document.getElementById('submit').disabled = false;
                changeForm(false); //Enable fields
            } else {
                changeForm(true); //Disable and clear fields when there are no containers with matching barcode
                console.log(data['status'])
            }
        },
        error: function() {
            console.log(data['status']) //TODO: change to write to a log file as well as console.
        }
    });
}

function manualBar(){
    var manualSel = document.getElementById('manualSel');
    var hiddenField = document.getElementById('nullbarcodeId');
    var autoField = document.getElementById('barcodeId');
    var barNum = document.getElementById('barcode');
    var migrated = document.getElementById('migrated');
    if (manualSel.checked) {
        migrated.value = 1
        //Hide the autopopulated barcode field and reveal the manual barcode entry field
        $(autoField).empty();
        autoField.setAttribute("name", "nullbarcodeId");
        hiddenField.setAttribute("name", "barcodeId");
        hiddenField.style.visibility = "visible";
        hiddenField.select();
    } else {
        //Clear value from manual barcode entry field, hide manual field, and reveal autopopulated field
        migrated.value = 0
        hiddenField.value = null;
        hiddenField.style.visibility = "hidden";
        hiddenField.setAttribute("name", "nullbarcodeId");
        autoField.setAttribute("name", "barcodeId");
        $.getScript("/static/js/local/createBarcode.js", function(){
            JsBarcode(barNum, autoField.value, {
                              height:30,
                              fontSize: 15
                             });
        })
    }
};

function spaceCheck(barcode){
    var regex = new RegExp("^[a-zA-Z0-9-]*$");
    if (!regex.test(barcode.value)) {
        barcode.parentElement.classList.add('has-error');
        document.getElementById("barcodeIdMessage").classList.remove('hidden');
    } else {
        barcode.parentElement.classList.remove('has-error');
        document.getElementById("barcodeIdMessage").classList.add('hidden');
    }
};
