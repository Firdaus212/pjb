$(document).ready( function () {
    var columns = [];
    $( "#table_id thead tr th" ).each(function( ) {
        columns.push({data: $(this).attr('id')});
    });
    $('#table_id').DataTable({
        responsive: true,
        serverSide: true,
        ordering: false,
        ajax: {
            url: '/table_data/'+$("#table_id").attr('data-area'),
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
} );