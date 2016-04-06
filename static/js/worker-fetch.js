importScripts('../vendor/oboe/oboe-browser.min.js');

self.addEventListener('message', function (e) {

  var count = 0;

  oboe(e.data)
    .node('data.*', function( mapObject ) {

      if (count <= 1000) {
        self.postMessage(mapObject);
        count++;
      }

    })
    .done(function( mapData ) {
      
      self.postMessage( mapData );
      
    });

}, false);