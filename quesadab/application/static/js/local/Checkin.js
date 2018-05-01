function CheckInModal(name,barcode,lastroom,newQuantity,newroom){
   var list = [name,barcode,lastroom,newQuantity,newroom];
   var check = checkValues(list);
   if (check == true) {
     printdata(name,barcode,lastroom,newQuantity,newroom);
   }
}

function checkValues(list){
  for (x = 0; x < list.length; x++){
    var string = list[x];
    var val = document.getElementById(string).value;
    if (val == "" || val == null){
      return false;
    }
  }
  return true;
}

function printdata(name,barcode,lastroom,newQuantity,newroom){
     var Name = $("#" + name).val();
     var Barcode =$("#" + barcode).val();
     var Lastroom = $("#" + lastroom).val();
     var Quantity = $("#" + newQuantity).val();
     var newroomy = $("#" + newroom).val();
      $('.chemdata').append("<li>Name: "+ Name +"</li>");
      $('.chemdata').append("<li>Barcode: " + Barcode + "</li>");
      $('.chemdata').append("<li>Lastroom: " + Lastroom + "</li>");
      $('.chemdata').append("<li>NewQuantity: " +Quantity+ "</li>")
      $('.chemdata').append("<li>NewRoom:" +newroomy+"</li>")
      $("#myModal").modal('show');
}
