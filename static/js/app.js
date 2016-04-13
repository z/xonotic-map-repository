$(document).ready(function () {

  // Config
  var preloadCount = 2500;
  var useCache = true;
  var cacheExpiration = 30000000;

  // Define Themes
  var themes = {
    'default': "//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css",
    'cerulean': "//bootswatch.com/cerulean/bootstrap.min.css",
    'cosmo': "//bootswatch.com/cosmo/bootstrap.min.css",
    'cyborg': "//bootswatch.com/cyborg/bootstrap.min.css",
    'darkly': "//bootswatch.com/darkly/bootstrap.min.css",
    'flatly': "//bootswatch.com/flatly/bootstrap.min.css",
    'journal': "//bootswatch.com/journal/bootstrap.min.css",
    'lumen': "//bootswatch.com/lumen/bootstrap.min.css",
    'paper': "//bootswatch.com/paper/bootstrap.min.css",
    'readable': "//bootswatch.com/readable/bootstrap.min.css",
    'sandstone': "//bootswatch.com/sandstone/bootstrap.min.css",
    'simplex': "//bootswatch.com/simplex/bootstrap.min.css",
    'slate': "//bootswatch.com/slate/bootstrap.min.css",
    'spacelab': "//bootswatch.com/spacelab/bootstrap.min.css",
    'superhero': "//bootswatch.com/superhero/bootstrap.min.css",
    'united': "//bootswatch.com/united/bootstrap.min.css",
    'yeti': "//bootswatch.com/yeti/bootstrap.min.css"
  };

  var userTheme = $.cookie('theme');
  //var userTheme = ($.cookie('theme')) ? $.cookie('theme') : 'default';
  
  // Jokes while you wait
  $.get('./resources/data/jokes.json', function(data) {
    var jokes = data.jokes;
    var random = jokes[Math.floor(Math.random()*jokes.length)].joke;
    $('#joke p').text(JSON.stringify(random));
  });

  
  /*
   * Tables
   */

  var table = $('#table-maplist').DataTable({
    data: {},
    lengthMenu: [25, 50, 100, 250],
    pageLength: 25,
    order: [[15, 'desc']],
    colReorder: true,
    stateSave: true,
    fixedHeader: {
      header: true,
      headerOffset: $('#main-nav').height()
    },
    processing: true,
    deferRender: true,
    language: {
      search: "",
      lengthMenu: '_MENU_',
      processing: '<h4 class="text-center">Processing a large file, this might take a second<br><br><i class="fa fa-spinner fa-pulse fa-3x"></i></h4>'
    },
    buttons: [
      {
        extend: 'csvHtml5',
        text: '<i class="fa fa-download" title="Download CSV"></i> CSV'
      },
      {
        extend: 'colvis',
        postfixButtons: ['colvisRestore'],
        text: '<i class="fa fa-eye" title="Toggle Column Visibility"></i> Columns'
      },
      {
        text: '<i class="fa fa-eraser" title="Reset Table State"></i> Reset',
        action: function (e, dt, node, config) {
          dt.state.clear();
          window.location.reload();
        }
      }
    ],
    dom: "<'#table-controls'lfB>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row footer-bar navbar-inverse'<'col-sm-5 navbar-brand'i><'col-sm-7'p>>",
    columns: [
      { // bsp
        data: 'bsp'
      },
      { // mapshot
        data: function (row, type, val, meta) {
          var arr = [];
          if (Object.keys(row.bsp)) {
            $.each(row.bsp, function (key, value) {
              if (row.bsp[key]['mapshot']) {
                var mapshot = row.bsp[key]['mapshot'].replace('.tga', '.jpg');
              } else {
                var mapshot = 'no_mapshot.png';
              }
              arr.push(mapshot);
            });
          }
          return arr;
        }
      },
      { // pk3
        data: 'pk3'
      },
      { // filesize
        data: 'filesize'
      },
       {// filesize
        data: 'filesize'
      },
      { // shasum
        data: 'shasum'
      },
      { // title
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // author
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // gametypes
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // gametypes
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // entities
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // map
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // radar
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // waypoints
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // license
        data: function (row, type, val, meta) {
          return row.bsp;
        }
      },
      { // date
        data: 'date'
      }
    ],
    columnDefs: [
      { // bsp
        targets: 0,
        render: function (data, type, full, meta) {
          if (data) {
            var bsps = Object.keys(data).join('<br>');
            if (bsps.length > 40 && bsps.indexOf('<br>') == -1) {
              bsps = '<span data-toggle="tooltip" title="' + bsps + '">' + bsps.substr(0, 38) + '...</span>';
            }
          }
          return bsps;
        }
      },
      { // mapshot file
        targets: 1,
        render: function (data, type, full, meta) {

          var api = $('#table-maplist').DataTable();
          var loadImages = (api.column(5).visible() === true) ? true : false;

          var string = "";

          data.forEach(function (value, index, array) {
            string += '<a class="btn mapshot-link" data-img="./resources/mapshots/' + value + '" href="./resources/mapshots/' + value + '" target="_blank">'
              + '<img src="./resources/mapshots/' + value + '" class="mapshot css-animated" />'
              + '<span>' + value + '</span>'
              + '</a>';
          });

          return string;
        }
      },
      { // pk3
        targets: 2,
        render: function (data, type, full, meta) {
          var pk3 = data;
          if (type === 'display' && data.length > 40) {
            data = '<span title="' + data + '">' + data.substr(0, 38) + '...</span>';
          }
          return '<a href="http://dl.xonotic.co/' + pk3 + '">' + data + '</a>';
        }
      },
      { // filesize
        targets: 3,
        orderData: 3,
        render: function (data, type, full, meta) {
          return bytesToSize(data);
        }
      },
      { // filesize (bytes)
        targets: 4,
        visible: false,
        searchable: false
      },
      { // shasum
        targets: 5,
        visible: false
      },
      { // title
        targets: 6,
        render: function (data, type, full, meta) {
          var str = "";
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              var manyMaps = (Object.keys(data).length > 1);
              if (manyMaps) {
                str += '<em>' + key + '</em><br>';
              }
              str += data[key]['title'] + '<br>';
              if (manyMaps) {
                str += '<br>';
              }
            });
          }
          return str;
        }
      },
      { // author
        targets: 7,
        render: function (data, type, full, meta) {
          var str = '';
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              var manyMaps = (Object.keys(data).length > 1);
              if (manyMaps) {
                str += '<em>' + key + '</em><br>'
              }
              str += data[key]['author'] + '<br>';
              if (manyMaps) {
                str += '<br>';
              }
            });
          }
          return str;
        }
      },
      { // gametypes (strings)
        targets: 8,
        visible: false,
        render: function (data, type, full, meta) {
          var str = "";
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              if (data[key]['gametypes'].length > 0) {
                var manyMaps = (Object.keys(data).length > 1);
                if (manyMaps) {
                  str += '<em>' + key + '</em><br>'
                }
                str += data[key]['gametypes'].join(', ') + '<br>';
                if (manyMaps) {
                  str += '<br>';
                }
              }
            });
          }
          return str;          
        }
      },
      { // gametypes
        targets: 9,
        //type: 'html',
        render: function (data, type, full, meta) {
          var str = "";
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              if (data[key]['gametypes'].length > 0) {
                var manyMaps = (Object.keys(data).length > 1);
                if (manyMaps) {
                  str += '<em>' + key + '</em><br>'
                }
                $.each(data[key]['gametypes'], function (k, v) {
                  str += '<i class="icon icon-gametype_' + v + '" data-toggle="tooltip" title="' + v + '"><b>' + v + '</b></i> ';
                });
                if (manyMaps) {
                  str += '<br><br>';
                }
              }
            });
          }
          return str;
        }
      },
      { // entities
        targets: 10,
        //type: 'html',
        render: function (data, type, full, meta) {
          // var response = workerParser.enities(data);
          // response.then(function(entities){
          //   return entities;
          // });
          if (Object.keys(data)) {
            var str = "";
            $.each(data, function (key, value) {
              if (data[key].entities) {
                var manyMaps = (Object.keys(data).length > 1);
                if (manyMaps) {
                  str += '<em>' + key + '</em><br>'
                }
                $.each(data[key].entities, function (k, v) {
                  str += '<i class="icon icon-' + k + '" data-toggle="tooltip" title="' + v + ' ' + k + '"><b>' + k + '</b></i> ';
                });
                if (manyMaps) {
                  str += '<br><br>';
                }
              }
            });
            return str;
          }
          return "";
        }
      },
      { // map file
        targets: 11,
        render: function (data, type, full, meta) {
          var str = "";
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              var manyMaps = (Object.keys(data).length > 1);
              if (manyMaps) {
                str += '<em>' + key + '</em><br>'
              }
              str += (data[key]['map']) ? 'yes' : 'no' + '<br>';
              if (manyMaps) {
                str += '<br><br>';
              }
            });
          }
          return str;
        },
        visible: false
      },
      { // radar file
        targets: 12,
        render: function (data, type, full, meta) {
          var str = "";
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              var manyMaps = (Object.keys(data).length > 1);
              if (manyMaps) {
                str += '<em>' + key + '</em><br>'
              }
              str += (data[key]['radar']) ? 'yes' : 'no' + '<br>';
              if (manyMaps) {
                str += '<br>';
              }
            });
          }
          return str;
        },
        visible: false
      },
      { // waypoints file
        targets: 13,
        render: function (data, type, full, meta) {
          var str = "";
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              var manyMaps = (Object.keys(data).length > 1);
              if (manyMaps) {
                str += '<em>' + key + '</em><br>'
              }
              str += (data[key]['waypoints']) ? 'yes' : 'no' + '<br>';
              if (manyMaps) {
                str += '<br>';
              }
            });
          }
          return str;
        },
        visible: false
      },
      { // license file
        targets: 14,
        render: function (data, type, full, meta) {
          var str = "";
          if (Object.keys(data)) {
            $.each(data, function (key, value) {
              if (data[key]['license']) {
                str += data[key]['license'] + ", ";
              }
            });
          }
          return (str) ? 'yes' : 'no';
        },
        visible: false
      },
      {
        // date
        targets: 15,
        render: function (data, type, full, meta) {
          var d = new Date(0);
          d.setUTCSeconds(data);
          return d.toISOString().slice(0, 10);
        }
      }
    ],
    initComplete: function (settings, json) {

      // clear filters on page load
      $('tfoot input').val('').trigger('change');
      $('tfoot select').val('').trigger('change');

      // Make the search more better ;)
      $('#table-maplist_filter')
        .addClass('pull-right')
        .css('position', 'relative')
        .append('<span id="search-clear" class="fa fa-times-circle-o hidden"></span>');
      $('#search-clear').click(function (e) {
        $('#table-maplist_filter input').val('');
        table.search('').draw();
      });

      // Put the controls in the navbar
      $('#table-controls').detach().appendTo('#nav-table-controls');

      // Style and show
      $('#table-maplist_length').addClass('pull-right');
      $('#table-controls .btn').addClass('btn-sm');
      $('#table-controls .dt-buttons').addClass('pull-right');
      $('#table-controls').show();

      if (userTheme) {
        setTheme(userTheme);
      }

      var searchTerm = $('#table-maplist_filter input').val();
      if (searchTerm) {
        $('#search-clear').removeClass('hidden');
      }

    },
    drawCallback: function (settings) {
      $('#table-controls').show();

      $('.mapshot').load(function(e) {
        $('tr .mapshot').hide().fadeIn();
      });

      $('body').trigger('scroll');
    }
  });

  table.on( 'draw.dt', function () {
    setTimeout(function() {
      table.fixedHeader.adjust();
    }, 10);
  });

  $(window).scroll( function() {
    $('tr').each(function () {

      var bottom_of_object = $(this).position().top + $(this).outerHeight();
      var bottom_of_window = $(window).scrollTop() + $(window).height();

      if ( bottom_of_window > bottom_of_object ) {
        $(this).animate({'opacity': '1'}, 500);
      }

    });
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
    $(this).html('<select class="form-control input-sm"><option value="">all (' + title + ' &amp; no ' + title + ')</option><option value="maps/">' + title + '</option><option value="no_mapshot.png">no ' + title + '</option></select>');
  });

  $('#table-maplist').on('page.dt', function() {
    $(document).scrollTop(0);
  });

  // To be shown by initComplete
  $('#table-controls').hide();

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
  if ( !useCache || store.isFake() || !store.get('expiration') || curTime > store.get('expiration') ) {

    var count = 0;
    var preloadMaps = [];
    var workerFetch = new Worker('static/js/worker-fetch.js');

    workerFetch.addEventListener('message', function(e) {

      if (e.data.hasOwnProperty('data') && useCache) {

        var mapData = e.data.data;
        mapData.splice(0, preloadCount);

        table.rows.add(mapData).draw();

        var string = JSON.stringify(mapData);
        var compressed = LZString.compressToUTF16(string);
        store.set('expiration', new Date().getTime() + cacheExpiration);
        store.set('tableData', compressed);
        store.set('preloadMaps', preloadMaps);

        $('#apology').fadeOut();
        $('.first-load-backdrop').remove();

      } else {

        var mapObjectData = e.data;
        
        // Preload?
        if (count < preloadCount) {
          preloadMaps.push(mapObjectData);
        } else if (preloadMaps.length == preloadCount) {
          table.rows.add(preloadMaps).draw();
        }

        count++;
      }

    }, false);

    workerFetch.postMessage('../../resources/data/maps.json');

  } else {

    var preloadMaps = store.get('preloadMaps');
    
    table.rows.add(preloadMaps).draw();

    var workerDecompress = cw({
      decompress: function(data) {
        importScripts('/static/vendor/lz-string/lz-string.min.js');
        importScripts('/static/vendor/store2/store2.min.js');
        var decompressed = JSON.parse(LZString.decompressFromUTF16(data));
        return decompressed;
      }
    });

    var response = workerDecompress.decompress(store.get('tableData'));

    response.then(function(data) {

      table.rows.add(data).draw();

      $('#apology').fadeOut();
      $('.first-load-backdrop').remove();

      workerDecompress.close();

    });

  }

  /*
   * Charts
   */

  var chartsDrawn = false;
  var allCharts = [];

  function drawCharts(data) {
    $('#charts').show();

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

    $('#loading-charts').hide();
  }

  function hideCharts() {
    // allCharts.forEach(function(value, index, array) {
    //   value.hide();
    // });
  }

  function showCharts() {
    $('#loading-charts').hide();
    $('#charts').show();
    // allCharts.forEach(function(value, index, array) {
    //  value.show();
    // });
  }

  // Need to hide datatables when changing tabs for fixedHeader
  var visible = true;
  var tableContainer = $(table.table().container());

  // Bootstrap tab shown event
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

    var currentTab = $('.nav li.active a').attr('href');

    switch (currentTab) {

      case "#maplist":

        visible = false;

        break;

      case "#statistics":

        $('#charts').hide();
        $('#loading-charts').show();

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

    $('#nav-table-controls').hide();

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
