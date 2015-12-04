$(document).ready(function() {
    $('#maplist').DataTable( {
        "ajax": "data/maps.json",
        "lengthMenu": [[50, 100, 250, 500], [50, 100, 250, 500]],
        "pageLength": 100,
        "columns": [
            { "data": "pk3" },
            { "data": "bsp" },
            { "data": "filesize" },
            { "data": "shasum" },
            { "data": "title" },
            { "data": "author" },
            { "data": "mapshot" },
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
            {   // pk3
                "targets": 1,
                "render": function ( data, type, full, meta ) {
                    if (data != false) {
                        return data.replace('maps/','');
                    } else {
                        return data;
                    }
                }
            },
            {   // filesize
                "targets": 2,
                "render": function ( data, type, full, meta ) {
                    return(bytesToSize(data));
                }
            },
            {   // mapshot file
                "targets": 5,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            },
            {   // map file
                "targets": 6,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            },
            {   // radar file
                "targets": 7,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            },
            {   // waypoints file
                "targets": 8,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? true : false;
                }
            }
        ]
    } );

} );

function bytesToSize(bytes) {
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
   if (bytes == 0) return '0 Byte';
   var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
   return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
};
