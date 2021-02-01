$(document).ready(function(){
    $('#execInfo').hide();

    var disableEnableCalcButton = function (status) { 
        var text = status === true ? '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...' : '<i class="fas fa-calculator"></i> Calculate';
        $('#calcBtn').prop('disabled', status).html(text);
    }

    $(':input[type="number"]').change(function () { 
        var h0 = parseFloat($(this).val());
        var min = parseFloat($(this).attr('min'));
        var max = parseFloat($(this).attr('max'));
        if(h0 > max){
            $(this).val(max);
        }else if(h0 < min){
            $(this).val(min);
        }
    });

    $('#calcBtn').click(function(){
        $.ajax({
            type: "POST",
            url: $(this).attr('data-url'),
            data: $('#inputForm').serialize(),
            dataType: "JSON",
            timeout: 1000*60*10,
            beforeSend: function(){
                disableEnableCalcButton(true);
                $('#execInfo').hide();
            },
            success: function (response) {
                $.each(response.data, function (key, value) { 
                    $('#resultTable #'+key+' .value').text(value.toFixed(2).toString()); 
                });
                $('#execInfo').show();
                $('#execInfo').html('Calculation time : '+response.exec_time+' s');
            },
            error: function(jqXHR, textStatus, errorThrown){
                $( "#resultTable tbody tr td .value" ).each(function( ) {
                    $(this).html('<span class="text-danger">err</span>');
                });
                disableEnableCalcButton(false);
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
                disableEnableCalcButton(false);
            }
        });
    });

    
});