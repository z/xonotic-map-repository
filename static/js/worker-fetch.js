importScripts('../vendor/oboe/oboe-browser.min.js');

self.addEventListener('message', function (e) {

  var count = 0;

  oboe(e.data)
    .node('data.*', function( mapObject ) {

      if (count <= 2500) {
        self.postMessage(mapObject);
        count++;
      }

    })
    .done(function( mapData ) {
      
      self.postMessage( mapData );
      
    });

}, false);