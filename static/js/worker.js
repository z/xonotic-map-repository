// TODO: Figure out how to use libs in web workers
//   // Lazy load tabledata
//   var count = 0;
//   oboe('./resources/data/maps.json')
//     .node('data.*', function( mapObject ) {
//
//       if (count % preloadCount == 0) {
//         setTimeout(function () {
//           table.draw('page');
//         }, 25);
//       }
//
//       table.row.add(mapObject);
//       count++;
//
//     })
//     .done(function(mapData) {
//
//
//       table.draw(false);
//       $('#apology').fadeOut();
//
//     });

self.addEventListener('message', function (e) {

  fetch(e.data, function (xhr) {
    var result = xhr.responseText;
    var object = JSON.parse(result);
    self.postMessage(object);
  });

}, false);

//simple XHR request in pure raw JavaScript
function fetch(url, callback) {
  var xhr;

  if (typeof XMLHttpRequest !== 'undefined') {
    xhr = new XMLHttpRequest();
  } else {
    var versions = ["MSXML2.XmlHttp.5.0",
      "MSXML2.XmlHttp.4.0",
      "MSXML2.XmlHttp.3.0",
      "MSXML2.XmlHttp.2.0",
      "Microsoft.XmlHttp"];

    for (var i = 0, len = versions.length; i < len; i++) {
      try {
        xhr = new ActiveXObject(versions[i]);
        break;
      }
      catch (e) {
      }
    } // end for
  }

  xhr.onreadystatechange = ensureReadiness;

  function ensureReadiness() {
    if (xhr.readyState < 4) {
      return;
    }

    if (xhr.status !== 200) {
      return;
    }

    // all is well
    if (xhr.readyState === 4) {
      callback(xhr);
    }
  }

  xhr.open('GET', url, true);
  xhr.send('');
}