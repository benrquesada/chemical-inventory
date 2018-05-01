function loadDependencies() {
    var datefield = document.createElement("input")
    datefield.setAttribute("type", "date")
    if (datefield.type != "date") {
        document.write('<link href="http://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css" rel="stylesheet"/>\n')
        document.write('<script src="https://code.jquery.com/jquery-1.12.4.js"><\/script>\n')
        document.write('<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"><\/script>\n')
        $(function(){
          $('#end_date').datepicker({
                changeMonth: true,
                changeYear: true,
                minDate: "-0D",
                maxDate: "+2Y" 
            });
        });
    }
}

loadDependencies();
