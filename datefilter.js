// datefilter.js - Re-render New Timepieces grid with 30-day filter
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    fetch('/api/watches')
      .then(function(r) { return r.json(); })
      .then(function(watches) {
        var now = new Date();
        var active = watches.filter(function(w) {
          if (w.sold) return false;
          if (!w.dateAdded) return true;
          var d = new Date(w.dateAdded);
          return (now - d) < 30 * 24 * 60 * 60 * 1000;
        }).slice(0, 4);
        var grid = document.getElementById('watchGrid');
        if (!grid) return;
        grid.innerHTML = active.map(function(w) {
          return '<div class="watch-card" onclick="location.href=\u0027watch.html?id=' + w.id + '\u0027">' +
            '<img src="images/' + w.img + '" loading="lazy" alt="' + w.brand + ' ' + w.name + '">' +
            '<div class="watch-info">' +
            '<p class="watch-brand">' + w.brand + '</p>' +
            '<p class="watch-year">' + (w.year || '') + '</p>' +
            '<h3 class="watch-name">' + w.name + '</h3>' +
            '<p class="watch-price">' + w.price + '</p></div></div>';
        }).join('');
      });
  }, 500);
});
