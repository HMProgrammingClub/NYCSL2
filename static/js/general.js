$("#sidebarBtn").click(function(e) {
    e.preventDefault();
    $('.ui.sidebar').sidebar('toggle');
    return false;
});

$('#accountBtn').popup({
    popup: '.special.popup',
    hoverable: true,
    position : 'bottom center'
});
