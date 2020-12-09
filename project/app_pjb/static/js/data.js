$(document).ready( function () {
    $('#table_id').DataTable({
        responsive: true,
        serverSide: true,
        ordering: false,
        ajax: {
            url: '/elevation_data',
            type: 'POST'
        },
        columnDefs: [
            {
                targets: '_all',
                className: 'text-right'
            }
          ]
    });
} );