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
        ]
    } );
} );
