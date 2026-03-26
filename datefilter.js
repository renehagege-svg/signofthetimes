// datefilter.js - Override New Timepieces to show only watches added within 30 days
(function(){
  var origFetch = window.fetch;
  window.fetch = function(url, opts) {
    var result = origFetch.apply(this, arguments);
    if (typeof url === 'string' && url.indexOf('/api/watches') !== -1) {
      return result.then(function(response) {
        var clone = response.clone();
        return new Response(new ReadableStream({
          start: function(controller) {
            clone.json().then(function(watches) {
              var now = new Date();
              var filtered = watches.filter(function(w) {
                if (w.sold) return false;
                if (!w.dateAdded) return true;
                var d = new Date(w.dateAdded);
                return (now - d) < 30 * 24 * 60 * 60 * 1000;
              });
              var body = JSON.stringify(filtered);
              controller.enqueue(new TextEncoder().encode(body));
              controller.close();
            });
          }
        }), { headers: { 'Content-Type': 'application/json' } });
      });
    }
    return result;
  };
})();
