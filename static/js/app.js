$(document).ready(function () {

  var preloadCount = 1000;
  var useCache = true;
  var cacheExpiration = 30000000;

  // Define Themes
  var themes = {
    "default": "//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css",
    "cerulean": "//bootswatch.com/cerulean/bootstrap.min.css",
    "cosmo": "//bootswatch.com/cosmo/bootstrap.min.css",
    "cyborg": "//bootswatch.com/cyborg/bootstrap.min.css",
    "darkly": "//bootswatch.com/darkly/bootstrap.min.css",
    "flatly": "//bootswatch.com/flatly/bootstrap.min.css",
    "journal": "//bootswatch.com/journal/bootstrap.min.css",
    "lumen": "//bootswatch.com/lumen/bootstrap.min.css",
    "paper": "//bootswatch.com/paper/bootstrap.min.css",
    "readable": "//bootswatch.com/readable/bootstrap.min.css",
    "sandstone": "//bootswatch.com/sandstone/bootstrap.min.css",
    "simplex": "//bootswatch.com/simplex/bootstrap.min.css",
    "slate": "//bootswatch.com/slate/bootstrap.min.css",
    "spacelab": "//bootswatch.com/spacelab/bootstrap.min.css",
    "superhero": "//bootswatch.com/superhero/bootstrap.min.css",
    "united": "//bootswatch.com/united/bootstrap.min.css",
    "yeti": "//bootswatch.com/yeti/bootstrap.min.css"
  };

  var userTheme = $.cookie('theme');
  //var userTheme = ($.cookie('theme')) ? $.cookie('theme') : 'default';


  /*
   * Tables
   */
  
  var table = $('#table-maplist').DataTable({
    "data": {},
    "lengthMenu": [[50, 100, 250, 500, 1000], [50, 100, 250, 500, 1000]],
    "pageLength": 50,
    "order": [[15, 'desc']],
    "colReorder": true,
    "stateSave": true,
    "fixedHeader": {
      "header": true,
      "headerOffset": $('#main-nav').height()
    },
    "processing": true,
    "deferRender": true,
    "language": {
      "search": "",
      "lengthMenu": "_MENU_",
      "processing": '<h4 class="text-center">Processing a large file, this might take a second<br><br><i class="fa fa-spinner fa-pulse fa-3x"></i></h4>'
    },
    "buttons": [
      {
        "extend": "csvHtml5",
        "text": '<i class="fa fa-download" title="Download CSV"></i> CSV'
      },
      {
        "extend": "colvis",
        "postfixButtons": ['colvisRestore'],
        "text": '<i class="fa fa-eye" title="Toggle Column Visibility"></i> Columns'
      },
      {
        "text": '<i class="fa fa-eraser" title="Reset Table State"></i> Reset',
        "action": function (e, dt, node, config) {
          dt.state.clear();
          window.location.reload();
        }
      }
    ],
    "dom": "<'#table-controls'lfB>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row footer-bar navbar-inverse'<'col-sm-5 navbar-brand'i><'col-sm-7'p>>",
    "columns": [
      { // pk3
        "data": "pk3"
      },
      { // bsp
        "data": function (row, type, val, meta) {
          return (row.bsp) ? Object.keys(row.bsp).join("<br>") : "";
        }
      },
      { // filesize
        "data": "filesize"
      },
       {// filesize
        "data": "filesize"
      },
      { // shasum
        "data": "shasum"
      },
      { // mapshot
        "data": function (row, type, val, meta) {
          var arr = [];
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              if (row.bsp[key]['mapshot']) {
                arr.push(row.bsp[key]['mapshot'].replace('.tga', '.jpg'));
              }
            });
          }
          return arr;
        }
      },
      { // title
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              var manyMaps = (Object.keys(row.bsp).length > 1);
              if (manyMaps) {
                str += "<em>" + key + "</em><br>";
              }
              str += row.bsp[key]['title'] + "<br>";
              if (manyMaps) {
                str += "<br>";
              }
            });
          }
          return str;
        }
      },
      { // author
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              var manyMaps = (Object.keys(row.bsp).length > 1);
              if (manyMaps) {
                str += "<em>" + key + "</em><br>"
              }
              str += row.bsp[key]['author'] + "<br>";
              if (manyMaps) {
                str += "<br>";
              }
            });
          }
          return str;
        }
      },
      { // gametypes
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              if (row.bsp[key]['gametypes'].length > 0) {
                var manyMaps = (Object.keys(row.bsp).length > 1);
                if (manyMaps) {
                  str += "<em>" + key + "</em><br>"
                }
                str += row.bsp[key]['gametypes'].join(', ') + "<br>";
                if (manyMaps) {
                  str += "<br>";
                }
              }
            });
          }
          return str;
        }
      },
      { // gametypes
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              if (row.bsp[key]['gametypes'].length > 0) {
                var manyMaps = (Object.keys(row.bsp).length > 1);
                if (manyMaps) {
                  str += "<em>" + key + "</em><br>"
                }
                $.each(row.bsp[key]['gametypes'], function (k, v) {
                  str += '<i class="icon icon-gametype_' + v + '" data-toggle="tooltip" title="' + v + '"><b>' + v + '</b></i> ';
                });
                if (manyMaps) {
                  str += "<br><br>";
                }
              }
            });
          }
          return str;
        }
      },
      { // entities
        "data": function (row, type, val, meta) {
          if (Object.keys(row.bsp)) {
            var str = "";
            $.each(row.bsp, function (key, value) {
              if (row.bsp[key].entities) {
                var manyMaps = (Object.keys(row.bsp).length > 1);
                if (manyMaps) {
                  str += "<em>" + key + "</em><br>"
                }
                $.each(row.bsp[key].entities, function (k, v) {
                  str += '<i class="icon icon-' + k + '" data-toggle="tooltip" title="' + v + ' ' + k + '"><b>' + k + '</b></i> ';
                });
                if (manyMaps) {
                  str += "<br><br>";
                }
              }
            });
            return str;
          } else {
            return "";
          }
        }
      },
      { // map
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              var manyMaps = (Object.keys(row.bsp).length > 1);
              if (manyMaps) {
                str += "<em>" + key + "</em><br>"
              }
              str += (row.bsp[key]['map']) ? "yes" : "no" + "<br>";
              if (manyMaps) {
                str += "<br><br>";
              }
            });
          }
          return str;
        }
      },
      { // radar
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              var manyMaps = (Object.keys(row.bsp).length > 1);
              if (manyMaps) {
                str += "<em>" + key + "</em><br>"
              }
              str += (row.bsp[key]['radar']) ? "yes" : "no" + "<br>";
              if (manyMaps) {
                str += "<br>";
              }
            });
          }
          return str;
        }
      },
      { // waypoints
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              var manyMaps = (Object.keys(row.bsp).length > 1);
              if (manyMaps) {
                str += "<em>" + key + "</em><br>"
              }
              str += (row.bsp[key]['waypoints']) ? "yes" : "no" + "<br>";
              if (manyMaps) {
                str += "<br>";
              }
            });
          }
          return str;
        }
      },
      { // license
        "data": function (row, type, val, meta) {
          var str = "";
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              if (row.bsp[key]['license']) {
                str = +row.bsp[key]['license'] + ", ";
              }
            });
          }
          return str;
        }
      },
      { // date
        "data": "date"
      }
    ],
    "columnDefs": [
      { // pk3
        "targets": 0,
        "render": function (data, type, full, meta) {
          var pk3 = data;
          if (type === 'display' && data.length > 40) {
            data = '<span title="' + data + '">' + data.substr(0, 38) + '...</span>';
          }
          return '<a href="http://dl.xonotic.co/' + pk3 + '">' + data + '</a>';
        }
      },
      { // bsp
        "targets": 1,
        "render": function (data, type, full, meta) {
          if (data != false && data.length > 0) {
            if (data.length > 40 && data.indexOf('<br>') == -1) {
              data = '<span data-toggle="tooltip" title="' + data + '">' + data.substr(0, 38) + '...</span>';
            }
          }
          return data;
        }
      },
      { // filesize
        "targets": 2,
        "orderData": 3,
        "render": function (data, type, full, meta) {
          return (bytesToSize(data));
        }
      },
      { // filesize (bytes)
        "targets": 3,
        "visible": false,
        "searchable": false
      },
      { // shasum
        "targets": 4,
        "visible": false
      },
      { // mapshot file
        "targets": 5,
        "render": function (data, type, full, meta) {
          var api = $('#table-maplist').DataTable();
          var loadImages = (api.column(5).visible() === true ? true : false);
          var string = "___no_mapshot___";
          if (data.length > 0) {
            string = "";
            data.forEach(function (value, index, array) {
              if (value != "" && loadImages) {
                string += '<a class="btn mapshot-link" data-img="./resources/mapshots/' + value + '" href="./resources/mapshots/' + value + '" target="_blank">'
                  + '<img src="./resources/mapshots/' + value + '" class="mapshot css-animated" />'
                  + '<span>' + value + '</span>'
                  + '</a>';
              } else {
                string += '';
              }
            });
          }
          return string;
        }
      },
      { // title
        "targets": 6,
        "render": function (data, type, full, meta) {
          return (data != false) ? data : "";
        }
      },
      { // author
        "targets": 7,
        "render": function (data, type, full, meta) {
          return (data != false) ? data : "";
        }
      },
      { // gametypes (strings)
        "targets": 8,
        "visible": false
      },
      { // gametypes
        "targets": 9,
        "type": "html"
      },
      { // entities
        "targets": 10,
        "type": "html"
      },
      { // map file
        "targets": 11,
        "render": function (data, type, full, meta) {
          return data;
        },
        "visible": false
      },
      { // radar file
        "targets": 12,
        "render": function (data, type, full, meta) {
          return data;
        },
        "visible": false
      },
      { // waypoints file
        "targets": 13,
        "render": function (data, type, full, meta) {
          return data;
        },
        "visible": false
      },
      { // license file
        "targets": 14,
        "render": function (data, type, full, meta) {
          return (data != false) ? "yes" : "no";
        },
        "visible": false
      },
      {
        // date
        "targets": 15,
        "render": function (data, type, full, meta) {
          d = new Date(0);
          d.setUTCSeconds(data);
          return d.toISOString().slice(0, 10);
        }
      }
    ],
    "initComplete": function (settings, json) {
      // clear filters on page load
      $("tfoot input").val('').trigger('change');
      $("tfoot select").val('').trigger('change');
      // Hacky way to put the controls in the navbar
      $("#table-controls .btn").addClass("btn-sm");
      $("#table-maplist_length").addClass("pull-right");
      $("#table-maplist_filter")
        .addClass("pull-right")
        .css('position', 'relative')
        .append('<span id="search-clear" class="fa fa-times-circle-o hidden"></span>');
      $('#search-clear').click(function (e) {
        $("#table-maplist_filter input").val('');
        table.search('').draw();
      });
      $("#table-controls").detach().appendTo('#nav-table-controls');
      $("#table-controls .dt-buttons").addClass("pull-right");
      $("#table-controls").show();
      if (userTheme) {
        setTheme(userTheme);
      }
      //$('[data-toggle="tooltip"]').tooltip();
      var searchTerm = $("#table-maplist_filter input").val();
      if (searchTerm) {
        $('#search-clear').removeClass('hidden');
      }
    },
    "drawCallback": function (settings) {
      $("#table-controls").show();
      $(".mapshot").load(function(e){
          $(".mapshot").hide().fadeIn();
      });
    }
  });

  table.on('search.dt', function () {
    if (table.search() == "") {
      $('#search-clear').addClass('hidden');
    } else {
      $('#search-clear').removeClass('hidden');
    }
  });

  // Setup - add a text input to filtesearch footers
  $('#table-maplist tfoot th.filtersearch').each(function () {
    var title = $(this).text();
    $(this).html('<input type="text" placeholder="filter ' + title + '" class="form-control input-sm" />');
  });

  // Setup - add a dropdown to dropdownsearch footers
  $('#table-maplist tfoot th.dropdownsearch').each(function () {
    var title = $(this).text();
    $(this).html('<select class="form-control input-sm"><option value="">all (' + title + ' &amp; no ' + title + ')</option><option value="yes">' + title + '</option><option value="no">no ' + title + '</option></select>');
  });

  // Setup - add a dropdown to dropdownsearch footers
  $('#table-maplist tfoot th.dropdownsearch-mapshot').each(function () {
    var title = $(this).text();
    $(this).html('<select class="form-control input-sm"><option value="">all (' + title + ' &amp; no ' + title + ')</option><option value="maps/">' + title + '</option><option value="___no_mapshot___">no ' + title + '</option></select>');
  });

  $('#table-maplist').on('page.dt', function() {
    $(document).scrollTop(0);
  });

  // To be shown by initComplete
  $("#table-controls").hide();

  // Apply filtersearch and dropdownsearch
  table.columns().every(function () {
    var that = this;

    $('input', this.footer()).on('keyup change', function () {
      if (that.search() !== this.value) {
        that
          .search(this.value)
          .draw();
      }
    });

    $('select', this.footer()).on('change', function () {
      if (that.search() !== this.value) {
        that
          .search(this.value)
          .draw();
      }
    });

  });

  var curTime = new Date().getTime();
  var userAgent = navigator.userAgent.toLowerCase();

  // if no cache exists or browser doesn't support it
  if ( !useCache || store.isFake() || !store.get('expiration') || curTime > store.get('expiration') || /firefox/.test(userAgent) ) {
    
    var worker = new Worker('static/js/worker.js');

    worker.addEventListener('message', function(e) {

      var mapData = e.data.data;
      table.rows.add(mapData).draw();

      if (useCache) {
        var string = JSON.stringify(mapData);
        var compressed = LZString.compress(string);
        store.set('expiration', new Date().getTime() + cacheExpiration);
        store.set('tableData', compressed);
      }
      
      $('#apology').fadeOut();
      
    }, false);

    worker.postMessage('../../resources/data/maps.json');

  } else {

    var worker = cw({
      decompress: function(data) {
        importScripts('/static/vendor/lz-string/lz-string.min.js');
        importScripts('/static/vendor/store2/store2.min.js');
        var decompressed = JSON.parse(LZString.decompress(data));
        return decompressed;
      }
    });

    var response = worker.decompress(store.get('tableData'));

    response.then(function(data) {

      // var preload = data.splice(0, preloadCount);
      // var maps = data;
      //
      // table.rows.add(preload).draw();
      // table.rows.add(maps).draw();

      table.rows.add(data).draw();

      $('#apology').fadeOut();

      worker.close();

    });


    // var workerDecompress = new Worker('static/js/worker-decompress.js');
    //
    // workerDecompress.addEventListener('message', function(e) {
    //   console.log('done decompressing');
    //   console.log(e.data);
    // }, false);
    //
    // workerDecompress.postMessage('test');
    
    // Object.defineProperty(Array.prototype, 'chunk', {value: function(n) {
    //     return Array.from(Array(Math.ceil(this.length/n)), (_,i)=>this.slice(i*n,i*n+n));
    // }});
    //
    // var chunks = data.chunk(100);
    //
    // function drawIt(value) {
    //   table.rows.add(value).draw(false);
    //   console.log('adding');
    // }
    //
    // $.each(chunks, function(index, value) {
    //   drawIt(value);
    //   setTimeout(function() {
    //     console.log('waiting');
    //   }, 4000);
    // });
    //
    // setTimeout(function() {
    //   console.log('drawing');
    //   table.draw();
    //   $('#apology').fadeOut();
    // }, 1000);

  }

  /*
   * Charts
   */

  var chartsDrawn = false;
  var allCharts = [];

  function drawCharts(data) {
    $("#charts").show();

    // Pie
    allCharts[0] = c3.generate(data.mapinfos);
    allCharts[1] = c3.generate(data.mapshots);
    allCharts[2] = c3.generate(data.maps);
    allCharts[3] = c3.generate(data.radars);
    allCharts[4] = c3.generate(data.waypoints);
    allCharts[5] = c3.generate(data.licenses);

    // Bar Chart
    var filesizes = {
      tooltip: {
        format: {
          title: function (x) {
            return;
          },
          name: function (name, ratio, id, index) {
            return "map count";
          },
          value: function (value, ratio, id, index) {
            return value;
          }
        }
      }
    };

    $.extend(filesizes, data.filesizes);
    allCharts[6] = c3.generate(filesizes);

    // Line
    allCharts[7] = c3.generate(data.mapsbyyear);

    // Donut
    allCharts[8] = c3.generate(data.gametypes);
    allCharts[9] = c3.generate(data.shacount);

    // Stacked Area
    allCharts[10] = c3.generate(data.filesbyyear);

    // Donut
    allCharts[11] = c3.generate(data.entityappearance);

    // Donut
    allCharts[12] = c3.generate(data.entitycount);

    $("#loading-charts").hide();
  }

  function hideCharts() {
    // allCharts.forEach(function(value, index, array) {
    //   value.hide();
    // });
  }

  function showCharts() {
    $("#loading-charts").hide();
    $("#charts").show();
    // allCharts.forEach(function(value, index, array) {
    //  value.show();
    // });
  }

  // Need to hide datatables when changing tabs for fixedHeader
  var visible = true;
  var tableContainer = $(table.table().container());

  // Bootstrap tab shown event
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

    var currentTab = $(".nav li.active a").attr("href");

    switch (currentTab) {

      case "#maplist":

        visible = false;

        break;

      case "#statistics":

        $("#charts").hide();
        $("#loading-charts").show();

        if (!chartsDrawn) {
          $.get('./resources/data/charts.json', function (data) {
            drawCharts(data);
            chartsDrawn = true;
          });
        } else {
          showCharts();
        }

      case "#about":

      default:

        visible = false;

    }

    $("#nav-table-controls").hide();

    table.fixedHeader.adjust();
    hideCharts();

    // decide whether to show the table or not
    if (visible) { // hide table
      tableContainer.css('display', 'none');
    } else { // show table
      tableContainer.css('display', 'block');
    }

  });

  $('[href=#maplist]').click(function() {
    setTimeout(function() {
      $('#nav-table-controls').show();
    }, 10);
  });


  /*
   * Theme Switcher
   */

  function themeSwitcher() {

    // Setup menu

    var themeMenu = '<li id="theme-switcher-wrapper" class="navbar-btn"><div class="dropdown btn-group">' +
      '<a class="btn btn-sm btn-default dropdown-toggle" data-toggle="dropdown" href="#">' +
      '<span>Theme</span> ' +
      '<i class="caret"></i>' +
      '</a>' +
      '<ul id="theme-switcher" class="dropdown-menu"></ul>' +
      '</div></li>';

    $('.navbar-right').append(themeMenu);

    $.each(themes, function (index, value) {
      var title = index.charAt(0).toUpperCase() + index.substr(1);
      $('#theme-switcher').append('<li><a href="#" data-theme="' + index + '">' + title + '</a></li>');
    });

    $('#theme-switcher li a').click(function () {
      var theme = $(this).attr('data-theme');
      setTheme(theme);
    });

  }

  function setTheme(theme) {
    var themeurl = themes[theme];
    $.cookie('theme', theme)
    $('#theme-switcher li').removeClass('active');
    $('#theme').attr('href', themeurl);
    $('#theme-custom').attr('href', './static/css/themes/' + theme + '/custom.css');
    $('#theme-switcher li a[data-theme=' + theme + ']').parent().addClass('active');
    $('#theme-switcher-wrapper span').text('Theme: ' + theme);
    // table.fixedHeader.adjust();
  }

  new Konami(function () {
    themeSwitcher();
  });

});

function bytesToSize(bytes) {
  var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  if (bytes == 0) return '0 Byte';
  var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
  return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
}
