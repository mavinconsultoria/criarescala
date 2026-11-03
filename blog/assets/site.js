// mavin. seguros — blog: tracking sutil de CTAs
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-cta="cotacao"]').forEach(function (el) {
    el.addEventListener('click', function () {
      if (typeof gtag === 'function') {
        gtag('event', 'gerar_lead', {
          event_category: 'blog',
          event_label: el.getAttribute('data-cta-label') || window.location.pathname
        });
      }
    });
  });

  // filtro de categorias na home do blog
  var pills = document.querySelectorAll('.filters .pill');
  var rows = document.querySelectorAll('.row-post');
  if (pills.length && rows.length) {
    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        pills.forEach(function (p) { p.classList.remove('active'); });
        pill.classList.add('active');
        var filter = pill.getAttribute('data-filter');
        rows.forEach(function (row) {
          var show = filter === 'todos' || row.getAttribute('data-category') === filter;
          row.hidden = !show;
        });
      });
    });
  }
});
