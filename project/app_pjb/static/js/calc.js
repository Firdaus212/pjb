$(document).ready(function(){
    $('#execInfo').hide();
    
    $('#calcBtn').click(function(){
        $.ajax({
            type: "POST",
            url: $(this).attr('data-url'),
            data: $('#inputForm').serialize(),
            dataType: "JSON",
            timeout: 1000*60*5,
            beforeSend: function(){
                $('#calcBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...');
                $('#execInfo').hide();
            },
            success: function (response) {
                $.each(response.data, function (key, value) { 
                    $('#'+key).text(value.toString()); 
                });
                $('#execInfo').show();
                $('#execInfo').html('Calculation time : '+response.exec_time+' s');
            },
            error: function(jqXHR, textStatus, errorThrown){
                $( "#resultTable tbody tr td" ).each(function( ) {
                    $(this).html('err');
                });
                bs4Toast.error('Error!', jqXHR.responseJSON.msg, {
                    delay : 1500,
                    bodyClasses : ['text-white', 'bg-danger'],
                    icon : {
                        type : 'fontawesome', 
                        class : 'fa-exclamation-circle'
                    }
                });
            },
            complete: function(){
                $('#calcBtn').prop('disabled', false).html('<i class="fas fa-calculator"></i> Calculate');
            }
        });
    });

    
});