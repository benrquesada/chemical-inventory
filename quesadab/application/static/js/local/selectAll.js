$("#selectAll").click(function(event) {
    if(this.checked) {
        $('.selectUser').each(function() {
            this.checked = true;
        });
    } else {
        $('.selectUser').each(function() {
            this.checked = false;
        })
    }
});