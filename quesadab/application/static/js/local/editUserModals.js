$(document).on('shown.bs.modal', '#editUserModal', function (event) {
    var button = $(event.relatedTarget);
    var name = button.data('username');
    var authorization = button.data('authlevel');
    var modal = $(this);
    modal.find('.modal-title').text('Edit User, '+ name);
    modal.find("#auth_level").val(authorization);
    modal.find("#username").val(name);
});

$(document).on('shown.bs.modal', '#deleteUserModal', function (event) {
    var button = $(event.relatedTarget);
    var username = button.data('username');
    var modal = $(this);
    modal.find('.modal-title').text('Remove User, ' + username);
    modal.find('.modal-body').text('Are you sure you want to remove ' + username + ' from the system?');
    modal.find('#username').val(username);
})