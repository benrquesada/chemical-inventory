window.setTimeout(function() {
    $(".flashes").fadeTo(500, 0).slideUp(500, function(){
    $(this).remove();
    });
  }, 5000);
