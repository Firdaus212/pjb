$(document).ready(function () {
    $('.upload-ref').on('click', function () { 
        var area = $(this).attr('data-area');
        var filename = $(this).attr('data-name');
        
        $('#upload-card').show();
        $('#upload-card .card-header').html('Update file <b>'+filename+'</b> ('+area+')');
        $('[name="area"]').val(area);
        $('[name="filename"]').val(filename);
    });

    $('#cancelBtn').on('click', function () { 
        $('#upload-form')[0].reset();
        $('#upload-card').hide();
    });
});