function printBarcode(barId){
    var openWindow = window.open("", "", "width=800, height=700"); //Opens a window with specific dimensions
    var barcode = document.getElementById("barcodeDiv" + barId); //Get the entire div containing the correct barcode
    openWindow.document.write("<title>Print Barcode</title>"); //Set the title of the new window to Print Barcode
    openWindow.document.write(barcode.innerHTML); //Write the div with the barcode and all relevant information
    var barIMG = openWindow.document.getElementById("barcode" + barId); //Get the new div, relevant to the open window
    barIMG.style.width = '50%'; //Resize the barcode image (make it small enough to fit on the label)
    barIMG.style.height = 'auto';
    openWindow.focus();
    openWindow.print();
    openWindow.close();
}

$(document).ready(function(){ //Binding for all rows in container table, with the print glyphicon having a seperate action
    $('#containers tr').on('click', function(e){ //If anywhere in a row is clicked, pass in the event
        if ( $(e.target).is('span') ){ //If the glyphicon is clicked
            // console.log($(e.target.id).selector)
            printBarcode($(e.target.id).selector) //Calls the print function with the event's selector (barcode value)
        }
        else { //If anywhere else in the row was clicked
            var href = $(this).find("a").attr("href"); //Set the link to the correct one
            if(href){
                window.location = href; //And change the window location to that link
            }
        }
    })
});