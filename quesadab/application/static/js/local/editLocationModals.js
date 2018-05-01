//Remove location modal
$(document).on('shown.bs.modal', '#removeModal', function (event) {
    var button = $(event.relatedTarget);
    var location = button.data('location'); // location, attribute, and name are all passed in with each button
    var attribute = button.data('attribute');
    var name = button.data('name');
    var modal = $(this);
    modal.find('.modal-title').text('Delete ' + location + ": " + name); // Change the title text of the modal
    document.getElementById('deleteButton').href = ('../delete/' + location + '/'+ attribute + '/'); // Change the URL for the yes button, so the correct building is deleted.
    document.getElementById('removeMessage').innerHTML = ("Are you sure you would like to remove this " + location + "?"); // Adds a message that changes based on location ie: 'Building' or 'Floor'
})

$(document).on('shown.bs.modal', '#editBuildingModal', function(event){
    var button = $(event.relatedTarget);
    var location = button.data('location');
    var attribute = button.data('attribute');
    var action = button.data('action');
    var name = button.data('name');
    var modal = $(this);
    console.log(action)
  if(action != "add"){
    modal.find('input[name="action"]').val(action);
    modal.find('.modal-title').text('Edit ' + location + ': ' + name);
    $.ajax({
        url: '/getBuildingData/',
        data: {bId : attribute},
        type: 'GET',
        success: function(data) {
            modal.find('input[id="name"]').val(data['name']);
            modal.find('input[id="id"]').val(attribute);
            document.getElementById('numFloors').value = data['numFloors'];
            document.getElementById('numFloors').disabled = true;
            document.getElementById('address').value = data['address'];
        },
        error: function() {
            console.log("Error")
        }
    });
  }
  else{
    modal.find('input[name="action"]').val(action);
    modal.find('.modal-title').text('Add Building');
    document.getElementById('numFloors').value = "";
    document.getElementById('address').value = "";
    document.getElementById('name').value = "";
    document.getElementById('numFloors').disabled = false;
  }
  document.getElementById('foreignKey').value = (attribute);
});

$(document).on('shown.bs.modal', '#editFloorModal', function(event) {
    var button = $(event.relatedTarget);
    var location = button.data('location');
    var attribute = button.data('attribute');
    var action = button.data('action');
    var parent = button.data('parent');
    var name = button.data('name');
    var modal = $(this);
    modal.find('input[name="action"]').val(action);
    if (action != 'add') {
        modal.find('.modal-title').text('Edit ' + location + ': ' + name);
        $.ajax({
            url: '/getFloorData/',
            data: {fId : attribute},
            type: 'GET',
            success: function(data){
                console.log(data);
                modal.find('input[id="name"]').val(data['name']);
                modal.find('input[id="id"]').val(attribute);
            },
            error: function(){
                console.log("Error")
            }
        });
    } else {
        modal.find('.modal-title').text('Add Floor');
        console.log(parent)
        modal.find('input[id="buildId"]').val(parent)
    }
});

$(document).on('shown.bs.modal', '#editRoomModal', function(event) {
    var button = $(event.relatedTarget);
    var location = button.data('location');
    var attribute = button.data('attribute');
    var action = button.data('action');
    var parent = button.data('parent')
    var name = button.data('name');
    var modal = $(this);
    modal.find('input[name="action"]').val(action);
    if (action != 'add') {
        modal.find('.modal-title').text('Edit ' + location + ': ' + name);
        $.ajax({
            url: '/getRoomData/',
            data: {rId : attribute},
            type: 'GET',
            success: function(data){
                modal.find('input[id="name"]').val(data['name']);
                modal.find('input[id="id"]').val(attribute);
            },
            error: function(){
                console.log("Error")
            }
        });
    } else {
        modal.find('.modal-title').text('Add Room');
        modal.find('input[id="floorId"]').val(parent);
    }
});

$(document).on('shown.bs.modal', '#editStorageModal', function(event) {
    var button = $(event.relatedTarget);
    var location = button.data('location');
    var attribute = button.data('attribute');
    var action = button.data('action');
    var parent = button.data('parent')
    var name = button.data('name');
    var modal = $(this);
    modal.find('input[name="action"]').val(action);
    if (action != 'add') {
        modal.find('.modal-title').text('Edit ' + location + ': ' + name);
        $.ajax({
            url: '/getStorageData/',
            data: {sId : attribute},
            type: 'GET',
            success: function(data){
              modal.find('input[id="name"]').val(data['name']);
              modal.find('input[id="id"]').val(attribute);
                for(var key in data){
                    if (data.hasOwnProperty(key)) {
                        if (key == "roomId" || key == "sId") {
                        }
                        else if(key == "name"){
                            modal.find('input[name="name"]').val(data[key]);
                        }
                        else {
                            var checkbox = document.getElementById(key);
                            if (data[key] == 'True') {
                                checkbox.checked = true;
                            }
                            else {
                                checkbox.checked = false;
                            }
                        }
                    }
                }
            },
            error: function(){
                console.log("Error")
            }
        });
    } else {
        modal.find('.modal-title').text("Add Storage Location");
        modal.find('input[name="roomId"]').val(parent);
    }
});
