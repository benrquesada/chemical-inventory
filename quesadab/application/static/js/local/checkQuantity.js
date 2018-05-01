function checkVals(groups) {
    /*Checks the input of capacity and quantity of container. If the container
    capacity is smaller than the amount of chemical that is entered, the form
    cannot be submitted. Values will be converted to a common unit of measurement
    for comparison.
    Also checking manual barcode against a RegExp*/
    var regex = new RegExp("^[a-zA-Z0-9-]*$");
    var barcode = document.getElementById('nullbarcodeId');
    // console.log(barcode, regex.test(barcode))
    if (regex.test(barcode.value) == false){
        barcode.parentElement.classList.add('has-error');
        document.getElementById("barcodeIdMessage").classList.remove('hidden');
        return false;
    }

    var quantityUnit = document.getElementById('currentQuantityUnit');
    quantityUnit = quantityUnit[quantityUnit.selectedIndex].text;
    var capacityUnit = document.getElementById('capacityUnit');
    capacityUnit = capacityUnit[capacityUnit.selectedIndex].text;
    var quantity = document.getElementById('currentQuantity').value;
    var capacity = document.getElementById('capacity').value;
    for (var i = 0; i < groups.length; i++){
        for (var x = 0; x < groups[i]['units'].length; x++){
            if (quantityUnit === groups[i]['units'][x]){
                var quantityMeasure = groups[i].measure;
            }
            if (capacityUnit === groups[i]['units'][x]){
                var capacityMeasure = groups[i].measure;
            }
        }
    }
    if (quantityMeasure === capacityMeasure){
        if (quantityMeasure === "Volume") {
            var convertTo = "milliliter (mL)"; //All volumes will be converted to milliliters
        } else {
            var convertTo = "gram (g)"; //All weights will be converted to grams
        }
        var convertedCapacity = window.conversionObject.functions.converter(capacityMeasure, capacityUnit, convertTo, capacity) //convert capacity to correct measurement
        var convertedQuanity = window.conversionObject.functions.converter(quantityMeasure, quantityUnit, convertTo, quantity) //convert quantity to correct measurment
      if (convertedCapacity >= convertedQuanity){
            return true; //No errors, the form can be submitted as is
        } else {
            removePreviousErrors();
            document.getElementById('capacityParent').classList.add('has-error');
            document.getElementById('capacityMessage').classList.remove('hidden');
            return false; //Quantity in container is more than the container can hold.
        }
    }else {
        removePreviousErrors();
        document.getElementById('capacityUnitParent').classList.add('has-error');
        document.getElementById('currentQuantityUnitParent').classList.add('has-error');
        document.getElementById('capacityUnitMessage').classList.remove('hidden');
        document.getElementById('currentQuantityUnitMessage').classList.remove('hidden');
        return false; //Measurements should be the same type (volume to volume, weight to weight)
    }
};

function removePreviousErrors() {
    $(".has-error").removeClass("has-error");
    $('.messages').addClass('hidden');
}


var quantityInput = document.getElementById('currentQuantity')
quantityInput.addEventListener('change', function() {
    var cap = document.getElementById('capacity')
    if (!cap.value) {
        cap.value = quantityInput.value;
    }
})

var quantityUnitSelect = document.getElementById('currentQuantityUnit')
quantityUnitSelect.addEventListener('change', function() {
    var capUnit = document.getElementById('capacityUnit')
    if (!capUnit.selectedIndex) {
        capUnit.selectedIndex = quantityUnitSelect.selectedIndex;
    }
})
