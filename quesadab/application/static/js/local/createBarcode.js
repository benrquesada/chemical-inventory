function createBarcode(elementId, lastBar){
    var d = new Date(); //get the current date
    //Formatting date. Last two digits of year, two digit month, day is not needed.
    var year = d.getFullYear();
    var month = (d.getMonth()+1).toString();
    year = year.toString().substr(2,2);
    
    if (month.length == 1){
        month = "0" + month;
    }
    //Splitting barcode up into: two digit year, two digit month, and number of containers created in defined month.
    var barYear = lastBar.substr(0,2);
    var barMonth = lastBar.substr(2,2);
    var barNum = lastBar.substr(4,8);
    if (year == barYear){ //If the last barcode year and the current year match
        if (month == barMonth){ //If the last barcode month and the current month match
            barNum = (parseInt(barNum)+1).toString(); //Add one to the number of containers created for month
            barNum = checkbarNumLen(barNum); //Reformat number of containers to a 4 digit number with leading zeroes
            var newBar = year + month + barNum; //Concatenate current year, current, month, and formatted number of containers as the new barcode
        }else{
            var newBar = year + month + '0000';
        }
    }else{
        var newBar = year + month + '0000';
        //If the last barcode year or month don't both match the current year or month, new bar should be current year,
        //current month, and '0000' as no containers have been created in either the current year or current month
    }
    
    document.getElementById(elementId).value=newBar; //Set value of hidden barcode field to the new barcode
    return newBar
}

function checkbarNumLen(barNum){
    if (barNum.length == 4){ //If the new number of containers is 4, return it
        return barNum;
    }else{ //If the new number of containers is not 4, add a 0 to the front of the string and call this function again.
            return checkbarNumLen('0' + barNum);
        }
}
