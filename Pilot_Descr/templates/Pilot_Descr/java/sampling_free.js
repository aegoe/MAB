$('.no-sampling').click(function () {

    cart(this)
});

//prevent enter key from submitted the form
$(document).keypress(
    function (event) {
        if (event.which == '13') {
            event.preventDefault();
        }
    });