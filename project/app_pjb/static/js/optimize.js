$(document).ready(function(){
    $('#execInfo').hide();
    
    var disableCalcBtn = function(){
        $('#calcBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...');
    }

    var enableCalcBtn = function(){
        $('#calcBtn').prop('disabled', false).html('<i class="fas fa-calculator"></i> Calculate');
    }

    $('#calcBtn').click(function(){
        $.ajax({
            type: "POST",
            url: $(this).attr('data-url'),
            data: $('#inputForm').serialize(),
            dataType: "JSON",
            timeout: 1000*60*10,
            beforeSend: function(){
                disableCalcBtn();
                $('#execInfo').hide();
            },
            success: function (response) {
                $.each(response.data, function (key, value) { 
                    $('#resultTable #'+key).text(value.toFixed(2).toString()); 
                });
                $('#execInfo').show();
                $('#execInfo').html('Calculation time : '+response.exec_time+' s');
            },
            error: function(jqXHR, textStatus, errorThrown){
                $( "#resultTable tbody tr td" ).each(function( ) {
                    $(this).html('err');
                });
                $('#calcBtn').prop('disabled', false).html('<i class="fas fa-calculator"></i> Calculate');
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
                enableCalcBtn();
            }
        });
    });

    
});