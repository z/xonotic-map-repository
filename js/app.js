$(document).ready(function() {

    /*
     * Data Tables
     */

    // Setup - add a text input to filtesearch footers
    $('#table-maplist tfoot th.filtersearch').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="filter '+title+'" />' );
    } );

    // Setup - add a dropdown to dropdownsearch footers
    $('#table-maplist tfoot th.dropdownsearch').each( function () {
        var title = $(this).text();
        $(this).html( '<select><option value=""></option><option value="yes">' + title + '</option><option value="no">no ' + title + '</option></select>' );
    } );

    var table = $('#table-maplist').DataTable( {
        "ajax": "data/maps.json",
        "lengthMenu": [[50, 100, 250, 500, 1000], [50, 100, 250, 500, 1000]],
        "pageLength": 250,
        "colReorder": true,
        "stateSave": true,
        "fixedHeader": {
            "header": true,
            "headerOffset": $('#main-nav').height()
        },
        "processing": true,
        "deferRender": true,
        "language": {
            "lengthMenu": "_MENU_",
            "processing": '<h4 class="text-center">Processing a large file, this might take a second<br><br><i class="fa fa-spinner fa-pulse fa-3x"></i></h4>'
        },
        "buttons": [
            {
                "extend": "csvHtml5",
                "text": '<i class="fa fa-download" title="Download CSV"></i>',
            },
            {
                "extend": "colvis",
                "postfixButtons": [ 'colvisRestore' ],
                "text": '<i class="fa fa-eye" title="Toggle Columns"></i>'
            }
        ],
        "dom": "<'#table-controls'lB>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-5'i><'col-sm-7'p>>",
        "columns": [
            { "data": "pk3" },
            { "data": "bsp[<br> ]" },
            { "data": "filesize" },
            { "data": "filesize" },
            { "data": "shasum" },
            { "data": "mapshot" },
            { "data": "title" },
            { "data": "author" },
            { "data": "gametypes[, ]" },
            { "data": "map[, ]" },
            { "data": "radar[, ]" },
            { "data": "waypoints[, ]" },
            { "data": "license" },
            { "data": "date" }
        ],
        "columnDefs": [
            {   // pk3
                "targets": 0,
                "render": function ( data, type, full, meta ) {
                    var pk3 = data;
                    if (type === 'display' && data.length > 40) {
                        data = '<span title="'+data+'">'+data.substr( 0, 38 )+'...</span>';
                    }
                    return '<a href="http://dl.xonotic.co/' + pk3 + '">' + data + '</a>';
                }
            },
            {   // bsp
                "targets": 1,
                "render": function ( data, type, full, meta ) {
                    if (data != false && data.length > 0) {
            			if (data.length > 40 && data.indexOf('<br>') == -1) {
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
            {   // filesize (bytes)
                "targets": 3,
                "visible": false,
                "searchable": false
            },
            {   // shasum
                "targets": 4,
                "visible": false,
            },
            {   // mapshot file
                "targets": 5,
                "render": function ( data, type, full, meta ) {
                    var string = "";
                    if (data.length > 0) {
                        data.forEach(function(value, index, array) {
                            string += '<a class="btn" rel="popover" data-placement="auto bottom" data-img="mapshots/' + value + '" href="mapshots/' + value + '" target="_blank"><i class="fa fa-picture-o"></i></a>';
                        });
                    }
                    return string;
                }
            },
            {   // title
                "targets": 6,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? data : "";
                }
            },
            {   // author
                "targets": 7,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? data : "";
                }
            },
            {   // map file
                "targets": 9,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? "yes" : "no";
                }
            },
            {   // radar file
                "targets": 10,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? "yes" : "no";
                }
            },
            {   // waypoints file
                "targets": 11,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? "yes" : "no";
                }
            },
            {   // license file
                "targets": 12,
                "render": function ( data, type, full, meta ) {
                    return (data != false) ? "yes" : "no";
                }
            },
            {
                // date
                "targets": 13,
                "render": function ( data, type, full, meta ) {
                    d = new Date(0);
                    d.setUTCSeconds(data);
                    return d.toISOString().slice(0,10);
                }
            }
        ],
        "initComplete": function( settings, json ) {
            // clear filters on page load
            $("tfoot input").val('').trigger('change');
            $("tfoot select").val('').trigger('change');
            // Hacky way to put the controls in the navbar
            $("#table-controls .btn").addClass("btn-sm");
            $("#table-maplist_length").addClass("pull-right");
            $("#table-controls").detach().appendTo('#nav-table-controls');
            initPopovers();
        }
    } );

    // Reorder callback
    table.on( 'column-reorder', function ( e, settings, details ) {
        initPopovers();
    });

    // Popover image previews
    function initPopovers() {
        $('a[rel=popover]').popover({                            
            html: true,                                          
            trigger: 'hover',                                    
            content: function () {                               
                return '<img src="'+$(this).data('img') + '" />';
            }                                                    
        });                                                      
    }

    // Apply filtersearch and dropdownsearch
    table.columns().every( function () {
        var that = this;
 
        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );

        $( 'select', this.footer() ).on( 'change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );

    } );

    /*
     * Charts
     */

    var chartData;

    function drawCharts(data) {
            $("#charts").show();

            // Pie
            c3.generate(data.mapinfos);
            c3.generate(data.mapshots);
            c3.generate(data.maps);
            c3.generate(data.radars);
            c3.generate(data.waypoints);
            c3.generate(data.licenses);

            // Scatter
            var filesizes = {
                axis: { x: { show: false }, rotated: true },
                tooltip: {
                    format: {
                        title: function (x) { return; },
                        name: function (name, ratio, id, index) { return "size"; },
                        value: function (value, ratio, id, index) { return bytesToSize(value); }
                    }
                }
            };

            $.extend(filesizes, data.filesizes);
            c3.generate(filesizes);

            // Line
            c3.generate(data.mapsbyyear);

            $("#loading-charts").hide();
    }

    // Need to hide datatables when changing tabs for fixedHeader
    var visible = true;
    var tableContainer = $(table.table().container());

    // Bootstrap tab shown event
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

        // decide whether to show the table or not
        if (visible) {
            $("#nav-table-controls").hide();
            tableContainer.css('display', 'none');
        } else { 
            $("#nav-table-controls").show();
            tableContainer.css('display', 'block');
        }

        table.fixedHeader.adjust();
 
        visible = ! visible;

        $("#charts").hide();
        $("#loading-charts").show();

        if (!chartData) {
            $.get('data/charts.json', function(data) {
                drawCharts(data);
                chartData = data;
            });
        } else {
            drawCharts(chartData);
        }

    });

} );

function bytesToSize(bytes) {
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
   if (bytes == 0) return '0 Byte';
   var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
   return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
};

