function highlightTab(tabId) {
    clearPastStyles();
    var curTab = document.getElementById(tabId);
    clearPastStyles();
    if (curTab.classList.contains('panel-closed')){
            curTab.classList.remove("panel-closed");
            curTab.classList.add("panel-open");
        }
    else{
        curTab.classList.remove("panel-open");
        curTab.classList.add("panel-closed");
    }
}

function clearPastStyles() {
    //Get rid of all previous styles. Only highlight current tab
    var elementList = document.getElementsByClassName("panel-change");
    for (var i = 0; i < elementList.length; i++){
        elementList[i].classList.remove("panel-open");
        elementList[i].classList.add("panel-closed");
    }
}