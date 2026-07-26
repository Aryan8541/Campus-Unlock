// Teacher Dashboard — minimal interactivity for the static stub.
// Only handles the mobile sidebar toggle; nothing here talks to the backend yet.
(function () {
  var toggle = document.getElementById('tdMenuToggle');
  var sidebar = document.getElementById('tdSidebar');
  if (!toggle || !sidebar) return;

  toggle.addEventListener('click', function () {
    var isOpen = sidebar.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  document.addEventListener('click', function (e) {
    if (!sidebar.classList.contains('is-open')) return;
    if (sidebar.contains(e.target) || toggle.contains(e.target)) return;
    sidebar.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  });
})();
