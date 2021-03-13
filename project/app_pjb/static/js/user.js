$(document).ready( function () {
    var columns = [];
    var action_column = {};
    var action = '';
    
    $( "#table_id thead tr th" ).each(function( ) {
        var id = $(this).attr('id');
        if(id !== undefined)
            if(id === 'id')
                action_column = {
                    data: id,
                    className: "text-center",
                    render: function ( data, type, row, meta ) {
                        return '<button class="btn btn-sm btn-info edit-btn" data-id="'+data+'"><i class="fa fa-edit"></i></button>'+
                            '<button class="btn btn-sm btn-danger delete-btn" data-id="'+data+'"><i class="fa fa-trash-alt"></i></button>';
                    }
                };
            else
                columns.push({data: id});
    });

    columns.push(action_column);

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
                className: 'text-left'
            }
          ]
    });

    var disableEnableTrashButton = function (status) { 
        $('#actionMenu').prop('disabled', status);
    }

    $("#updateBtn").click(function (e) { 
        e.preventDefault();
        if(confirm("Do you want to update data waduk excel file?")) {
            $.ajax({
                type: "GET",
                url: '/opt-data/update-excel-file/'+$('#table_id').attr('data-area'),
                dataType: "JSON",
                beforeSend: function(){
                    disableEnableTrashButton(true);
                },
                success: function (response) {
                    bs4Toast.primary('Success!', 'File Updated', {
                        delay : 1500,
                        bodyClasses : ['text-white', 'bg-primary'],
                        icon : {
                            type : 'fontawesome', 
                            class : 'fa-check'
                        }
                    });
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

    $('#table_id').on('click', 'button.delete-btn', function (e) { 
        var entity_id = $(this).attr('data-id');
        if(entity_id !== undefined){
            if(confirm('Are you sure want to delete the data?')){
                $.ajax({
                    type: "DELETE",
                    url: "/delete-user/"+entity_id,
                    dataType: "JSON",
                    success: function (response) {
                        table.ajax.reload();
                    }
                });
            }
        }
    });

    $('#saveBtn').on('click', function (e) { 
        var url = '';
        if(action === 'edit'){
            url = '/edit-user/'+$('#entity_id').val();
            var type = 'PATCH';
        }
        else if(action === 'add'){
            url = '/add-user';
            var type = 'POST';
        }
        if(url !== ''){
            $.ajax({
                type: type,
                url: url,
                data: $('#formData').serialize(),
                dataType: "JSON",
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
                }
            });
        }
        $('#dataWadukModal').modal('hide');
    });

    $('#table_id').on('click', 'button.edit-btn', function (e) { 
        action = 'edit';
        var entity_id = $(this).attr('data-id');
        if(entity_id !== undefined){
            $('#dataWadukModalLabel').text('Edit User Data');
            var formData = $('#formData').find('input[type=text], select');
            $(this).closest('tr').find('td').each(function(idx, td){
                if(idx === 2){
                    $(formData[2]).val($(td).text());
                }
                else if(idx < 3){
                    $(formData[idx]).val($(td).text());
                }
            });
            $('#entity_id').val(entity_id);
            $('#dataWadukModal').modal('show');
            $('#dataWadukModal #email').attr('readonly', true);
            $('#dataWadukModal #password').val('');
            $('.password-div').hide();
        }
    });

    $('#addBtn').on('click', function (e) { 
        action = 'add';
        $('#dataWadukModalLabel').text('Add New User');
        $('#dataWadukModal #email').attr('readonly', false);
        $('.password-div').show();
        $('#formData').find('input[type=text], input[type=password], select').each(function(idx, inp){
            $(inp).val('');
        });
        $('#dataWadukModal').modal('show');
        
    });

} );