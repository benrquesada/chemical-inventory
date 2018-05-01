$("ul.nav-tabs > li > a").on("shown.bs.tab", function(e){
   var id = $(this).attr("href");
   window.location.hash = id;
   });

var hash = window.location.hash;
$("#homeTab a[href='" + hash + "']").tab("show");

