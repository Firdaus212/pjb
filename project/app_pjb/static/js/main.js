$(document).ready(function () {
    let url = $(location).attr('href');

    $('.nav-item').each( function () { 
        if ($(this).find('.nav-link').first().prop('href') == url){
            $(this).addClass('active');
        }
    });
});