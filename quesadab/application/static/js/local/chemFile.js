var table;
var cookie;
function createTable(){
    table = $('#chemtable').DataTable({
	    "columnDefs": [
		{
		    "targets": 'Barcodes',
		    "visible": false
		},
		{
		    "targets": 'nosort',
		    "searchable": false
		}
	                  ]
   });
  getCookie('savedSearch')
  addClearButton()
}

function cookieSaveAndRedirect(href) {

    //function to save the cookie held in the search bar as 'savedSearch' and then redirect to webpage
    //parameter is path in this case to a particular container

    var searchVal = document.getElementsByTagName("input")[0].value;
    setCookie("savedSearch",searchVal,600);
    window.location.href = href;
}

function addClearButton(){
    var x = document.getElementById('chemtable_filter');
    var button = document.createElement('button');
    button.className = 'btn btn-default CLEAR';
    button.onclick = function() {destroyCookie("savedSearch")};
    button.innerHTML = "Clear Search";
    x.append(button)
}



function getCookie(cname) {
    //function obtained from https://www.w3schools.com/js/js_cookies.asp
    //takes cookie name and returns the key value, else it returns an empty string
    var cookie_exist = find_cookie(cname);
    if (cookie_exist){
 	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	    for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
		    c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
		    cookie = c.substring(name.length, c.length);
            var el = document.getElementsByTagName("input")[0];
            el.value = cookie;
		    reload_table(cookie)
		    return true;
		}
 	    }
    }  
    return "";	
}

function find_cookie ( cookie_name ){
  //Used by getCookie function to find the cookie needed

  var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
  if ( results )
    return ( unescape ( results[2] ) );
  else
    return false;
}


function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}



function reload_table(cookie){
    table
         .search(cookie)
         .draw();

}

function destroyCookie(cookieKey){
   
   document.cookie = cookieKey+"=; expires=Fri, 5 July 2017 12:00:00 UTC; path=/";
   reload_table("");

}
