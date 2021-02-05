$(document).ready( function () {
    var columns = [];
    
    $( "#table_id thead tr th" ).each(function( ) {
        columns.push({data: $(this).attr('id')});
    });

    var table = $('#table_id').DataTable({
        responsive: true,
        serverSide: true,
        ordering: false,
        ajax: {
            url: $("#table_id").attr('data-url'),
            type: 'POST'
        },
        columns: columns,
        columnDefs: [
            {
                targets: '_all',
                className: 'text-right'
            }
          ]
    });

    var disableEnableTrashButton = function (status) { 
        $('#emptyBtn').prop('disabled', status);
    }

    $("#emptyBtn").click(function (e) { 
        e.preventDefault();
        if(confirm("Are you sure want to delete all data?")) {
            $.ajax({
                type: "GET",
                url: $("#table_id").attr('data-empty-url'),
                dataType: "JSON",
                beforeSend: function(){
                    disableEnableTrashButton(true);
                },
                success: function (response) {
                    table.ajax.reload();
                },
                error: function(jqXHR, textStatus, errorThrown){
                    bs4Toast.error('Error!', jqXHR.responseJSON.msg, {
                        delay : 1500,
                        bodyClasses : ['text-white', 'bg-danger'],
                        icon : {
                            type : 'fontawesome', 
                            class : 'fa-exclamation-circle'
                        }
                    });
                    disableEnableTrashButton(false);
                },
                complete: function(){
                    disableEnableTrashButton(false);
                }
            });  
        } 
        
    });
} );