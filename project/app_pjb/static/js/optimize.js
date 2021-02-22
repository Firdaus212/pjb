$(document).ready(function(){
    var empty_data = '<tr><td colspan="2" class="text-center">No Data</td></tr>';
    $('#execInfo').hide();

    var disableEnableCalcButton = function (status) { 
        var text = status === true ? '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...' : '<i class="fas fa-calculator"></i> Calculate';
        $('#calcBtn').prop('disabled', status).html(text);
    }

    var setTableData = function(row_data){
        $('#modalDataTable tbody').html(row_data);
    }

    setTableData(empty_data);

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
                setTableData(empty_data);
            },
            success: function (response) {
                $.each(response.data, function (key, value) { 
                    if(typeof(value) === 'object'){
                        var rows = '';
                        value.forEach((k, v) => { 
                            rows += '<tr>'+
                            '<td class="text-center">'+(v+1)+'</td>'+
                            '<td class="text-right">'+k.toFixed(4)+'</td>'+
                            '</tr>';
                        });
                        setTableData(rows);
                    }else{
                        $('.result-table #'+key+' .value').text(value.toFixed(2).toString()); 
                    }
                });
                $('#execInfo').show();
                $('#execInfo').html('Calculation time : '+response.exec_time.toFixed(2).toString()+' s');
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