$(document).ready(function() {

    // Setup - add a text input to each footer cell
    $('#maplist tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );

    var table = $('#maplist').DataTable( {
        "ajax": "data/maps.json",
        "lengthMenu": [[50, 100, 250, 500, 1000], [50, 100, 250, 500, 1000]],
        "pageLength": 500,
        "colReorder": true,
        "stateSave": true,
        "fixedHeader": true,
        "processing": true,
        "buttons": [
            'colvis'
        ],
        "dom": "<'row'<'col-sm-6'l><'col-sm-6'<'pull-right'B>>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-5'i><'col-sm-7'p>>",
        "columns": [
            { "data": "pk3" },
            { "data": "bsp[, ]" },
            { "data": "filesize" },
            { "data": "filesize" },
            { "data": "shasum" },
            { "data": "title" },
            { "data": "author" },
            { "data": "mapshot[, ]" },
            { "data": "gametypes[, ]" },
            { "data": "map" },
            { "data": "radar" },
            { "data": "waypoints" }
        ],
        "columnDefs": [
            {   // pk3
                "targets": 0,
                "render": function ( data, type, full, meta ) {
                  return type === 'display' && data.length > 40 ?
                    '<span title="'+data+'">'+data.substr( 0, 38 )+'...</span>' :
                    data;
                }
            },
            {   // bsp
                "targets": 1,
                "render": function ( data, type, full, meta ) {
                    if (data != false && data.length > 0) {
                        data = data.replace(/maps\//g,'');
            			if (data.length > 40 && data.indexOf(',') == -1) {
                            data = '<span title="'+data+'">'+data.substr( 0, 38 )+'...</span>';
        		    	}
        		    }
                    return data;
                }
            },
            {   // filesize
                "targets": 2,
                "orderData": 3,
                "render": function ( data, type, full, meta ) {
                    return(bytesToSize(data));
                }
            },
            {   // filesize for sorting
                "targets": 3,
                "visible": false,
                "searchable": false
            },
            {   // mapshot file
                "targets": 7,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            },
            {   // map file
                "targets": 9,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            },
            {   // radar file
                "targets": 10,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            },
            {   // waypoints file
                "targets": 11,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            }
        ]
    } );

    // Apply the search
    table.columns().every( function () {
        var that = this;
 
        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );

} );

function bytesToSize(bytes) {
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
   if (bytes == 0) return '0 Byte';
   var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
   return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
};

