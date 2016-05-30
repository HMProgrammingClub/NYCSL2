var rows = document.querySelectorAll(".playerRow");
for (var i=0; i<rows.length; i++) {
    var className = rows[i].className;
    className = className.substr(className.indexOf(' ')+1);
    $('.playerRow.' + className).popup({
        popup:$('.gamePopup.' + className),
        hoverable:true,
        position : 'bottom right'
    });
}
