$(document).ready(function() {
    $('#maplist').DataTable( {
        "ajax": "data/maps.json",
        "columns": [
            { "data": "title" },
            { "data": "author" },
            { "data": "bsp" },
            { "data": "map" },
            { "data": "radar" },
            { "data": "waypoints" },
            { "data": "shasum" },
            { "data": "pk3" }
        ],
        "columnDefs": [
            {
                "targets": 4,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            },
            {
                "targets": 7,
                "render": function ( data, type, full, meta ) {
                  return type === 'display' && data.length > 40 ?
                    '<span title="'+data+'">'+data.substr( 0, 38 )+'...</span>' :
                    data;
                }
            }
        ]
    } );
} );
