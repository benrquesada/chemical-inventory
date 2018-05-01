function pictSelect(element) //Is called when a hazard pictogram is clicked
{
    if (document.getElementById(element).class == 'selectedPict'){
        document.getElementById(element).removeClass('selectedPict'); //If pictogram was selected, remove select styling
    }else{
        document.getElementById(element).addClass('selectedPict'); //If pictogram was not selected, add select styling
    }
}
window.onload=function(){
  document.getElementById('primaryHazard').onchange=function(){
    var hazard = this.value;
    if (hazard == "Oxidizer"){
      document.getElementById('oxidizerPict').checked = true; 
    }
    else{
     document.getElementById('oxidizerPict').checked = false; 
    }
  }
  document.getElementById('state').onchange=function(){
    var state = this.value;
    if (state == "Gas"){
      document.getElementById('gcPict').checked = true; 
    }
    else{
      document.getElementById('gcPict').checked = false; 
    }
  }
}
