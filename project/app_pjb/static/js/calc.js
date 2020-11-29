$(document).ready(function(){
    $('#execInfo').hide();

    $('#calcBtn').click(function(){
        $.ajax({
            type: "POST",
            url: CALC_URL,
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
                alert(jqXHR.responseJSON.msg);
            },
            complete: function(){
                $('#calcBtn').prop('disabled', false).html('Calculate');
            }
        });
    });
});