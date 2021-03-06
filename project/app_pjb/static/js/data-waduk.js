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
                className: 'text-right'
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
                    bs4Toast.primary('Success!', 'File Updated. Page will reload in 3 seconds.', {
                        delay : 1500,
                        bodyClasses : ['text-white', 'bg-primary'],
                        icon : {
                            type : 'fontawesome', 
                            class : 'fa-check'
                        }
                    });

                    setTimeout(function(){
                        location.reload();
                    }, 3000)

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

    $('#emptyBtn').click(function (e) { 
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

    $('#table_id').on('click', 'button.delete-btn', function (e) { 
        var entity_id = $(this).attr('data-id');
        if(entity_id !== undefined){
            if(confirm('Are you sure want to delete the data?')){
                $.ajax({
                    type: "DELETE",
                    url: "/opt-data/delete-data-waduk/"+$('#table_id').attr('data-area')+"/"+entity_id,
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
            url = '/opt-data/edit-data-waduk/'+$('#table_id').attr('data-area')+'/'+$('#entity_id').val();
            var type = 'PATCH';
        }
        else if(action === 'add'){
            url = '/opt-data/add-data-waduk/'+$('#table_id').attr('data-area');
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
                        delay : 3000,
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
            $('#dataWadukModalLabel').text('Edit Data Waduk');
            var formData = $('#formData').find('input[type=number]');
            $(this).closest('tr').find('td').each(function(idx, td){
                $(formData[idx]).val($(td).text());
            });
            $('#entity_id').val(entity_id);
            $('#dataWadukModal').modal('show');
        }
    });

    $('#addBtn').on('click', function (e) { 
        action = 'add';
        $('#dataWadukModalLabel').text('Add Data Waduk');
        $('#formData').find('input[type=number]').each(function(idx, inp){
            $(inp).val('');
        });
        $('#dataWadukModal').modal('show');
    });

    $('#importBtn').on('click', function (e){
        $('#importDataWadukModal').modal('show');
    });

    $.ajax({
        type: "GET",
        url: "/opt-data/data-waduk-model/"+$('#table_id').attr('data-area'),
        dataType: "JSON",
        success: function (response) {
            $(".d-flex.justify-content-center").addClass('hide-spinner');
            $.each(response.data, function (idx, model) { 
                 var content = "";
                 content += "<b>"+model.modeltype+" :</b><br>";
                 content += "f(x) = "+model.formula+"<br>";
                 content += "<b>Coefficients :</b><br>";
                 $.each(model.coeffnames, function (i, name) { 
                        if(model.coeffvalues[i].charAt(0) == '-')
                            content += model.coeffnames[i]+" : "+model.coeffvalues[i]+"<br>";
                        else
                            content += model.coeffnames[i]+" : &nbsp;"+model.coeffvalues[i]+"<br>";
                 });
                 content += "<b>Figure :</b><br><br>";
                 content += "<img class='img-fluid' src='/static/images/"+idx+".png?"+performance.now()+"'>";
                 $('#'+idx).append(content);
            });
        },
        error: function(jqXHR, textStatus, errorThrown){
            $(".d-flex.justify-content-center").addClass('hide-spinner');
            bs4Toast.error('Error!', jqXHR.responseJSON.msg, {
                delay : 3000,
                bodyClasses : ['text-white', 'bg-danger'],
                icon : {
                    type : 'fontawesome', 
                    class : 'fa-exclamation-circle'
                }
            });
            disableEnableTrashButton(false);
        }
    });

} );