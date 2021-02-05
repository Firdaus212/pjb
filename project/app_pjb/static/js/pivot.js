$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: $('#pgrid').attr('data-source-url'),
        dataType: "JSON",
        success: function (response) {
            // data source
            var data = response.data;

            // pivot grid options
            var config = {
                dataSource: data,
                dataHeadersLocation: 'columns',
                theme: 'blue',
                toolbar: {
                    visible: false
                },
                grandTotal: {
                    rowsvisible: false,
                    columnsvisible: false
                },
                subTotal: {
                    visible: false,
                    collapsed: false
                },
                fields: [
                    { name: '0', caption: 'H', sort: { order: 'asc' } },
                    { name: '1', caption: 'P', sort: { order: 'asc' } },
                    { name: '2', caption: 'Q' }
                ],
                rows    : [ 'H' ],
                columns : [ 'P' ],
                data    : [ 'Q' ],
                width: 1280,
                height: 800
            };

            // instantiate and show the pivot grid
            new orb.pgridwidget(config).render(document.getElementById('pgrid'));
                }
            });
});