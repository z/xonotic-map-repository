importScripts('../vendor/lz-string/lz-string.min.js');
importScripts('../vendor/store.js/store+json2.min.js');

self.addEventListener('message', function(e) {

  console.log('message:' + e.data);
  console.log('worker-decompress');

  console.log(store);
  console.log(LZString);
  var tableData = store.get('tableData');
  console.log(tableData);
  var data = JSON.parse(LZString.decompress(tableData));
  console.log('data:' + data);
  self.postMessage(data);

}, false);


  var workerParser = cw({
    enities: function(data) {
      if (Object.keys(data)) {
        var str = "";
        $.each(data, function (key, value) {
          if (data[key].entities) {
            var manyMaps = (Object.keys(data).length > 1);
            if (manyMaps) {
              str += "<em>" + key + "</em><br>"
            }
            $.each(data[key].entities, function (k, v) {
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
      console.log(str);
    }
  });