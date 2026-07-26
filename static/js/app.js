(function () {
  'use strict';

  const appData = {
    // programs / universities are no longer hardcoded here — they are
    // hydrated from the server-rendered JSON payload (see hydrateAppData()
    // below), which is populated from SQLAlchemy objects by Flask.
    programs: [],
    universities: [],
    blogs: [
      { id:'b1', title:"UGC-DEB vs UGC-Regular: what's the real difference?", category:'Guide', read:'6 min', updated:'Jul 2026', cover:'🎓' },
      { id:'b2', title:'How EMI plans for online degrees actually work', category:'Finance', read:'4 min', updated:'Jun 2026', cover:'💰' },
      { id:'b3', title:'Is an online MBA valued the same by employers?', category:'Careers', read:'7 min', updated:'Jun 2026', cover:'📈' },
      { id:'b4', title:'Best online MCA specializations in 2026', category:'Guide', read:'5 min', updated:'May 2026', cover:'💻' }
    ]
  };

  const state = {
    favorites: new Set(JSON.parse(localStorage.getItem('favorites') || '[]')),
    bookmarks: new Set(JSON.parse(localStorage.getItem('bookmarks') || '[]')),
    recentlyViewed: JSON.parse(localStorage.getItem('recentlyViewed') || '[]'),
    recentSearches: JSON.parse(localStorage.getItem('recentSearches') || '[]'),
    // compareSet: persisted in localStorage so selections survive page reloads.
    // IDs are stored as strings to match dataset.compare (always a string).
    compareSet: new Set(JSON.parse(localStorage.getItem('compareSet') || '[]').map(String)),
    resultPage: 1,
    pageSize: 4,
    blogCategory: 'all',
    wizardStep: 0
  };

  const $ = (s, p=document) => p.querySelector(s);
  const $$ = (s, p=document) => Array.from(p.querySelectorAll(s));
  const inr = n => '₹' + Number(n).toLocaleString('en-IN');

  // Populates appData.programs / appData.universities from the JSON payload
  // Flask renders into a <script type="application/json" id="campus-data">
  // tag (see index.html). This replaces the old hardcoded arrays with real
  // SQLAlchemy-backed data, without changing how any of the functions below
  // consume appData.
  function hydrateAppData() {
    const dataEl = document.getElementById('campus-data');
    if (!dataEl) return;
    try {
      const parsed = JSON.parse(dataEl.textContent || '{}');
      appData.programs = Array.isArray(parsed.programs) ? parsed.programs : [];
      appData.universities = Array.isArray(parsed.universities) ? parsed.universities : [];
    } catch (err) {
      appData.programs = [];
      appData.universities = [];
    }
  }

  function saveLS() {
    localStorage.setItem('favorites', JSON.stringify([...state.favorites]));
    localStorage.setItem('bookmarks', JSON.stringify([...state.bookmarks]));
    localStorage.setItem('recentlyViewed', JSON.stringify(state.recentlyViewed.slice(0, 10)));
    // FIX: compareSet is now persisted like every other selection state.
    // The Remove handler already calls saveLS(), so removals now actually stick.
    localStorage.setItem('compareSet', JSON.stringify([...state.compareSet]));
  }

  // FIX: the university-card compare/save buttons are server-rendered HTML
  // (Flask/Jinja), not JS-generated like the search-results cards, so they
  // never got the usual re-render that shows selection state. Without this,
  // clicking Compare/Save on a university card silently updated state but
  // gave zero visual feedback — looked completely broken. This directly
  // toggles .is-active on every button for a given id (there may be more
  // than one instance of the same university's buttons on a page) and is
  // called both on every click and once on boot to restore state saved in
  // localStorage from a previous visit.
  function syncAllQuickActionButtons() {
    document.querySelectorAll('[data-compare]').forEach(btn => {
      const id = String(btn.dataset.compare);
      btn.classList.toggle('is-active', state.compareSet.has(id));
    });
    document.querySelectorAll('[data-fav]').forEach(btn => {
      const id = String(btn.dataset.fav);
      btn.classList.toggle('is-active', state.favorites.has(id));
    });
  }

  // Curated static list — no backend call, purely a UI convenience shown
  // in the idle/empty search dropdown alongside the person's own recent terms.
  const POPULAR_SEARCHES = ['Online MBA', 'Online MCA', 'NAAC A+ Universities', 'Under ₹50,000/yr', 'Executive MBA'];

  // Records a submitted/selected search query (deduped, most-recent-first,
  // capped at 5) — display-only convenience layered on top of the existing
  // /search flow; does not affect what the backend returns.
  function pushRecentSearch(query) {
    const q = (query || '').trim();
    if (!q) return;
    state.recentSearches = [q, ...state.recentSearches.filter(x => x.toLowerCase() !== q.toLowerCase())].slice(0, 5);
    localStorage.setItem('recentSearches', JSON.stringify(state.recentSearches));
  }

  // Escapes regex metacharacters so a user-typed query can be safely used
  // inside a RegExp when highlighting matches.
  function escapeRegex(s) {
    return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // Wraps the first case-insensitive match of `query` inside `text` with a
  // <mark> tag for visual emphasis in the suggestions dropdown.
  function highlightMatch(text, query) {
    const t = String(text == null ? '' : text);
    const q = (query || '').trim();
    if (!q) return t;
    try {
      const re = new RegExp('(' + escapeRegex(q) + ')', 'ig');
      return t.replace(re, '<mark class="suggestion-mark">$1</mark>');
    } catch (err) {
      return t;
    }
  }

  // ── Compare V2 ──────────────────────────────────────────────────────────
  // Self-contained. Uses state.compareSet (declared above) and saveLS().
  // Two entry points used externally:
  //   renderCompareTable()  — called on page load + after every selection change
  //   (data-compare / data-remove-compare handlers wired in boot())

  const compareState = { controller: null };

  // Build the card HTML for one university using either API or local fields.
  function _compareCardHtml(u) {
    const id    = String(u.id);
    const logo  = u.logo
      ? `<img src="${u.logo}" alt="${u.name}" style="width:100%;height:100%;object-fit:cover;border-radius:inherit;">`
      : `<span class="cmp-avatar-initials">${u.avatar || u.name.slice(0, 2).toUpperCase()}</span>`;
    const loc   = [u.city, u.state].filter(Boolean).join(', ');
    const fee   = u.min_fee != null ? inr(u.min_fee) + '/yr'
                : u.fee    != null ? inr(u.fee)    + '/yr'
                : 'On request';
    const isSelected = state.compareSet.has(id);

    return `<div class="cmp-card" data-cmp-id="${id}">
      <div class="cmp-card-top">
        <div class="cmp-card-logo">${logo}</div>
        ${u.rating ? `<span class="cmp-card-rating">★ ${Number(u.rating).toFixed(1)}</span>` : ''}
      </div>
      <div class="cmp-card-body">
        <div class="cmp-card-name" title="${u.name}">${u.name}</div>
        ${loc ? `<div class="cmp-card-loc">📍 ${loc}</div>` : ''}
        <div class="cmp-card-fee">${fee}</div>
        <div class="cmp-card-actions">
          <button class="cmp-btn cmp-btn-detail" data-detail="${id}">View Details</button>
          ${isSelected
            ? `<button class="cmp-btn cmp-btn-remove" data-remove-compare="${id}">Remove</button>`
            : `<button class="cmp-btn cmp-btn-add" data-compare="${id}">+ Compare</button>`}
        </div>
      </div>
    </div>`;
  }

  // Build the attribute rows table for selected universities.
  function _renderCompareTable(universities) {
    const wrap = document.getElementById('cmpTableWrap');
    if (!wrap) return;
    if (!universities || !universities.length) { wrap.innerHTML = ''; return; }

    const attrs = [
      { label: 'NAAC Grade',      fn: u => u.naac || '—' },
      { label: 'NIRF Rank',       fn: u => u.nirf != null ? '#' + u.nirf : '—' },
      { label: 'Location',        fn: u => [u.city, u.state].filter(Boolean).join(', ') || '—' },
      { label: 'Popular Program', fn: u => (u.programs && u.programs[0]) ? (u.programs[0].title || u.programs[0]) : '—' },
      { label: 'Duration',        fn: u => (u.programs && u.programs[0] && u.programs[0].duration) ? u.programs[0].duration : '—' },
      { label: 'Starting Fee',    fn: u => u.min_fee != null ? inr(u.min_fee) + '/yr' : u.fee != null ? inr(u.fee) + '/yr' : 'On request' },
      { label: 'Modes',           fn: u => (u.modes || []).join(', ') || '—' },
      { label: 'Specializations', fn: u => (u.specializations || []).slice(0, 3).join(', ') || '—' },
      { label: 'EMI',             fn: () => '—' },
      { label: 'Placement',       fn: () => '—' },
    ];

    const thead = `<tr><th class="cmp-attr-col">Attribute</th>${universities.map(u => `<th>${u.name}</th>`).join('')}</tr>`;
    const tbody = attrs.map(a =>
      `<tr><td class="cmp-attr-label">${a.label}</td>${universities.map(u => `<td>${a.fn(u)}</td>`).join('')}</tr>`
    ).join('');

    wrap.innerHTML = `<table class="cmp-table"><thead>${thead}</thead><tbody>${tbody}</tbody></table>`;
    wrap.style.display = 'block';
  }

  // Render cards into #cmpSelectedCards. Used for the 2-4 selected (API) path.
  function _renderSelectedCards(universities) {
    const grid = document.getElementById('cmpSelectedCards');
    if (!grid) return;
    grid.innerHTML = universities.map(_compareCardHtml).join('');
  }

  // Render all-universities sidebar list.
  function _renderSidebar() {
    const list = document.getElementById('cmpSidebarList');
    if (!list) return;
    const unis = appData.universities;
    if (!unis || !unis.length) {
      list.innerHTML = '<li class="cmp-sidebar-empty">No universities found.</li>';
      return;
    }
    list.innerHTML = unis.map(u => {
      const id = String(u.id);
      const isSelected = state.compareSet.has(id);
      const logo = u.logo
        ? `<img src="${u.logo}" alt="" class="cmp-sidebar-logo">`
        : `<span class="cmp-sidebar-initials">${(u.avatar || u.name.slice(0,2)).toUpperCase()}</span>`;
      return `<li class="cmp-sidebar-item ${isSelected ? 'is-selected' : ''}" data-cmp-sid="${id}">
        ${logo}
        <span class="cmp-sidebar-name">${u.name}</span>
        <button class="cmp-sidebar-toggle" data-${isSelected ? 'remove-compare' : 'compare'}="${id}" aria-label="${isSelected ? 'Remove' : 'Add'} ${u.name}">
          ${isSelected ? '✕' : '+'}
        </button>
      </li>`;
    }).join('');
  }

  // Update the selection counter badge.
  function _updateCmpCounter() {
    const badge = document.getElementById('cmpCounter');
    if (badge) badge.textContent = state.compareSet.size + ' / 4 selected';
    const compareBtn = document.getElementById('cmpCompareBtn');
    if (compareBtn) compareBtn.disabled = state.compareSet.size < 2;
  }

  // Main entry point — renders everything on the compare page.
  function renderCompareTable() {
    const page = document.getElementById('cmpPage');
    if (!page) return; // not on compare page

    _renderSidebar();
    _updateCmpCounter();

    const count = state.compareSet.size;
    const status = document.getElementById('cmpStatus');
    const tableWrap = document.getElementById('cmpTableWrap');

    if (count === 0) {
      // Show all universities as browseable cards (no selection yet).
      const grid = document.getElementById('cmpSelectedCards');
      if (grid) grid.innerHTML = appData.universities.map(_compareCardHtml).join('');
      if (status) status.textContent = 'Select 2–4 universities to compare side by side.';
      if (tableWrap) tableWrap.innerHTML = '';
      return;
    }

    if (count === 1) {
      const grid = document.getElementById('cmpSelectedCards');
      if (grid) {
        const id = [...state.compareSet][0];
        const u  = appData.universities.find(x => String(x.id) === id);
        if (u) grid.innerHTML = _compareCardHtml(u);
      }
      if (status) status.textContent = 'Select one more university to start comparing.';
      if (tableWrap) tableWrap.innerHTML = '';
      return;
    }

    // 2–4 selected — fetch from API.
    if (compareState.controller) compareState.controller.abort();
    const controller = new AbortController();
    compareState.controller = controller;

    const grid = document.getElementById('cmpSelectedCards');
    if (grid) grid.innerHTML = '<div class="cmp-loading">Loading comparison…</div>';
    if (status) status.textContent = 'Loading…';
    if (tableWrap) tableWrap.innerHTML = '';

    const ids = [...state.compareSet].join(',');
    fetch('/compare?ids=' + encodeURIComponent(ids), { signal: controller.signal })
      .then(res => { if (!res.ok) return res.json().then(e => Promise.reject(e)); return res.json(); })
      .then(data => {
        compareState.controller = null;
        const unis = Array.isArray(data.universities) ? data.universities : [];
        _renderSelectedCards(unis);
        _renderCompareTable(unis);
        if (status) status.textContent = unis.length + ' universities compared.';
      })
      .catch(err => {
        if (err && err.name === 'AbortError') return;
        compareState.controller = null;
        if (grid) grid.innerHTML = `<div class="cmp-error">${(err && err.error) ? err.error : 'Failed to load. Please try again.'}</div>`;
        if (status) status.textContent = '';
      });
  }
  // ── End Compare V2 ──────────────────────────────────────────────────────

  function renderPrograms() {
    // #progGrid is now rendered server-side by Flask/Jinja from real
    // Program rows — see templates/includes/programs.html. This function
    // now only keeps the dependent <select> dropdowns in sync with the
    // same (DB-backed) program list.
    const leadProgram = $('#leadProgram');
    const fProgram = $('#fProgram');
    if (!leadProgram || !fProgram) return;
    leadProgram.innerHTML = '<option value="">Select a program</option>' + appData.programs.map(p => `<option>${p.name}</option>`).join('') + '<option>Not sure yet</option>';
    fProgram.innerHTML = '<option value="">Any</option>' + appData.programs.map(p => `<option>${p.name}</option>`).join('');
  }

  // renderUniversities() previously overwrote #uniGrid with hardcoded
  // appData.universities. #uniGrid is now rendered server-side by Flask/
  // Jinja from real University rows — see templates/includes/universities.html.
  // No client-side rendering is needed for it anymore.

  
  function renderBlogs() {
    const grid = $('#blogGrid');
    if (!grid) return;
    const query = ($('#blogSearchInput')?.value || '').toLowerCase().trim();
    let blogs = appData.blogs.filter(b => (state.blogCategory === 'all' || b.category === state.blogCategory) && b.title.toLowerCase().includes(query));
    const filterInfo = $('#blogFilterInfo');
    if (filterInfo) filterInfo.textContent = `Showing ${blogs.length} blog post(s)${state.blogCategory !== 'all' ? ` in ${state.blogCategory}` : ''}.`;
    grid.innerHTML = blogs.map((b, i) => `
      <div class="blog-card reveal reveal-stagger" style="--d:${i*80}ms" tabindex="0" role="button" data-blog-id="${b.id}" aria-label="Read: ${b.title}">
        <div class="blog-cover">${b.cover}</div>
        <div class="blog-body">
          <div class="blog-tag">${b.category}</div>
          <div class="blog-title">${b.title}</div>
          <div class="blog-meta">${b.read} read · Updated ${b.updated}</div>
        </div>
      </div>
    `).join('') || `<div class="tool-result">No blogs found.</div>`;
  }

  function setupFiltersMeta() {
    if (!$('#fState') || !$('#fCity')) return;
    const states = [...new Set(appData.universities.map(u => u.state))];
    const cities = [...new Set(appData.universities.map(u => u.city))];
    $('#fState').innerHTML = '<option value="">Any</option>' + states.map(s => `<option>${s}</option>`).join('');
    $('#fCity').innerHTML = '<option value="">Any</option>' + cities.map(c => `<option>${c}</option>`).join('');
  }

  // ---------------------------------------------------------------------------
  // Server-driven filter state
  // ---------------------------------------------------------------------------
  const filterState = {
    controller: null,   // AbortController for in-flight /filter request
    debounceTimer: null,
    totalPages: 1,
  };

  // Build a URLSearchParams from the current filter controls.
  // Human labels for the filter fields that _buildFilterParams actually
  // sends to /filter — used only to render removable "active filter" badges.
  const FILTER_LABELS = {
    fSearch: 'Search', fDegree: 'Degree', fProgram: 'Program', fBudget: 'Budget',
    fNaac: 'NAAC', fNirf: 'NIRF', fDuration: 'Duration', fState: 'State',
    fCity: 'City', fMode: 'Mode', fSpec: 'Specialization'
  };

  function _ensureActiveFilterBadgesContainer() {
    let el = document.getElementById('activeFilterBadges');
    if (el) return el;
    const anchor = document.getElementById('resultCards');
    if (!anchor || !anchor.parentNode) return null;
    el = document.createElement('div');
    el.id = 'activeFilterBadges';
    el.className = 'active-filters';
    anchor.parentNode.insertBefore(el, anchor);
    el.addEventListener('click', (e) => {
      const clearBtn = e.target.closest('[data-clear-filter]');
      if (clearBtn) {
        const input = document.getElementById(clearBtn.dataset.clearFilter);
        if (input) { input.value = ''; state.resultPage = 1; renderResults(); }
        return;
      }
      if (e.target.closest('#clearAllFiltersBadge')) {
        Object.keys(FILTER_LABELS).forEach(id => { const input = document.getElementById(id); if (input) input.value = ''; });
        state.resultPage = 1;
        renderResults();
      }
    });
    return el;
  }

  // Renders removable badges for every currently-set filter — a purely
  // display-layer reflection of the same fields _buildFilterParams reads.
  // Clearing a badge just blanks that field and calls renderResults(),
  // identical to what #resetFiltersBtn already does for all fields at once.
  function renderActiveFilterBadges() {
    const container = _ensureActiveFilterBadgesContainer();
    if (!container) return;
    const active = Object.keys(FILTER_LABELS).map(id => {
      const el = document.getElementById(id);
      return (el && el.value.trim()) ? { id, label: FILTER_LABELS[id], value: el.value.trim() } : null;
    }).filter(Boolean);
    if (!active.length) {
      container.innerHTML = '';
      container.classList.remove('has-badges');
      return;
    }
    container.classList.add('has-badges');
    container.innerHTML = active.map(f => `
      <button type="button" class="active-filter-badge" data-clear-filter="${f.id}">
        ${f.label}: ${f.value} <span aria-hidden="true">×</span>
      </button>`).join('') + `<button type="button" class="active-filter-clear-all" id="clearAllFiltersBadge">Clear all</button>`;
  }

  function _buildFilterParams() {
    const params = new URLSearchParams();
    const add = (key, id) => { const v = ($(id) ? $(id).value : '').trim(); if (v) params.set(key, v); };
    add('search',   '#fSearch');
    add('degree',   '#fDegree');
    add('program',  '#fProgram');
    add('budget',   '#fBudget');
    add('naac',     '#fNaac');
    add('nirf',     '#fNirf');
    add('duration', '#fDuration');
    add('state',    '#fState');
    add('city',     '#fCity');
    add('mode',     '#fMode');
    add('spec',     '#fSpec');
    add('sort',     '#sortBy');
    params.set('page',      String(state.resultPage));
    params.set('page_size', String(state.pageSize));
    return params;
  }

  // Render university cards from a /filter JSON response payload.
  function _renderFilterResponse(data) {
    const rows = Array.isArray(data.universities) ? data.universities : [];
    filterState.totalPages = data.total_pages || 1;

    $('#resultCount').textContent = `${data.total || 0} result(s)`;
    renderActiveFilterBadges();

    $('#resultCards').innerHTML = rows.length
      ? rows.map(u => `
          <article class="result-card" data-id="${u.id}">
            <div class="uni-top">
              <div class="uni-avatar">${u.avatar}</div>
              <div><div class="uni-name">${u.name}</div><div class="uni-naac">NAAC ${u.naac || '—'} · NIRF #${u.nirf || '—'} · ${u.city || '—'}</div></div>
              <div class="uni-rating">${u.rating != null ? '★ ' + u.rating : ''}</div>
            </div>
            <div class="uni-chips">${(u.programs || []).map(p => `<span class="uni-chip">${p.replace('Online ','')}</span>`).join('')}</div>
            <div class="uni-fee">From ${u.fee != null ? inr(u.fee) + '/yr' : 'Fees on request'}${u.placement != null ? ' · Placement ' + u.placement + '%' : ''}${u.emi != null ? ' · EMI ' + u.emi : ''}</div>
            <div class="result-actions">
              <button class="action-btn action-light" data-fav="${u.id}">${state.favorites.has(u.id) ? '★ Favorited' : '☆ Favorite'}</button>
              <button class="action-btn action-light" data-bookmark="${u.id}">${state.bookmarks.has(u.id) ? '🔖 Bookmarked' : '🔖 Bookmark'}</button>
              <!-- FIX: String(u.id) keeps this id in the same format compareSet
                   uses everywhere else, so add/remove/has() never disagree. -->
              <button class="action-btn action-light" data-compare="${String(u.id)}">Compare</button>
              <button class="action-btn action-light" data-detail="${u.id}">View Details</button>
              <button class="action-btn action-apply" data-apply="${u.id}">Apply</button>
              <button class="action-btn action-light" data-brochure="${u.id}">Download Brochure</button>
            </div>
          </article>
        `).join('')
      : `<div class="tool-result">No programs match your selected filters.</div>`;

    const totalPages = filterState.totalPages;
    $('#pagination').innerHTML = Array.from({ length: totalPages }, (_, i) => `
      <button class="${state.resultPage === i + 1 ? 'active' : ''}" data-page="${i + 1}">${i + 1}</button>
    `).join('');
  }

  // Abort any in-flight request, then fire a new debounced /filter fetch.
  function fetchFilteredResults() {
    if (!$('#resultCards')) return;
    if (filterState.controller) {
      filterState.controller.abort();
    }
    clearTimeout(filterState.debounceTimer);

    filterState.debounceTimer = setTimeout(() => {
      const controller = new AbortController();
      filterState.controller = controller;

      const params = _buildFilterParams();

      fetch(`/filter?${params.toString()}`, { signal: controller.signal })
        .then(res => (res.ok ? res.json() : { total: 0, page: 1, page_size: state.pageSize, total_pages: 1, universities: [] }))
        .then(data => {
          filterState.controller = null;
          _renderFilterResponse(data);
        })
        .catch(err => {
          if (err && err.name === 'AbortError') return; // superseded — ignore
          filterState.controller = null;
          _renderFilterResponse({ total: 0, page: 1, page_size: state.pageSize, total_pages: 1, universities: [] });
        });
    }, 280); // 280 ms debounce — fast enough to feel live, avoids hammering on every keystroke
  }

  // Kept as a thin alias so every existing internal call to renderResults()
  // (pagination click, fav toggle, bookmark toggle, wizard, etc.) automatically
  // goes through the server-driven path without any other changes.
  function renderResults() {
    fetchFilteredResults();
  }

  function updateRecentlyViewedView() {
    if (!state.recentlyViewed.length) {
      $('#recentlyViewed').textContent = 'None yet.';
      return;
    }
    $('#recentlyViewed').innerHTML = state.recentlyViewed.map(id => appData.universities.find(u => u.id===id)).filter(Boolean).map(u => `${u.name}`).join(' · ');
  }

  function renderWizardSteps() {
    const labels = ['Qualification','Degree','Specialization','Budget','Career Goal','Recommendation'];
    $('#wizardSteps').innerHTML = labels.map((l,i)=> `<span class="wizard-step ${i===state.wizardStep?'active':''}">${i+1}. ${l}</span>`).join('');
  }

  function suggestionsFor(q) {
    const query = q.toLowerCase();
    if (!query) return [];
    const uni = appData.universities.filter(u => u.name.toLowerCase().includes(query)).map(u => ({type:'University', label:u.name, action:() => { $('#fSearch').value = u.name; state.resultPage = 1; renderResults(); document.getElementById('results').scrollIntoView({behavior:'smooth'}); }}));
    const prog = appData.programs.filter(p => p.name.toLowerCase().includes(query)).map(p => ({type:'Course', label:p.name, action:() => { $('#fProgram').value = p.name; state.resultPage = 1; renderResults(); document.getElementById('results').scrollIntoView({behavior:'smooth'}); }}));
    const blog = appData.blogs.filter(b => b.title.toLowerCase().includes(query)).map(b => ({type:'Blog', label:b.title, action:() => { $('#blogSearchInput').value = b.title; renderBlogs(); document.getElementById('blog').scrollIntoView({behavior:'smooth'}); }}));
    return [...uni, ...prog, ...blog].slice(0, 8);
  }

  function boot() {
    hydrateAppData();
    renderPrograms();
    renderBlogs();
    setupFiltersMeta();
    renderResults();
    updateRecentlyViewedView();
    renderWizardSteps();
    renderCompareTable(); // Compare V2 — no-op on pages without #cmpPage
    syncAllQuickActionButtons(); // restore compare/save state on server-rendered cards (e.g. #uniGrid)

    const hamburger = $('#hamburger');
    const navLinks = $('#navLinks');
    const header = $('#siteHeader');

    function setMenu(open) {
      navLinks.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
      hamburger.classList.toggle('is-active', open);
    }

    hamburger.addEventListener('click', () => setMenu(!navLinks.classList.contains('open')));
    navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
    document.addEventListener('click', (e) => { if (window.innerWidth <= 960 && !navLinks.contains(e.target) && !hamburger.contains(e.target)) setMenu(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

    window.addEventListener('scroll', () => header.classList.toggle('scrolled', window.scrollY > 8), { passive: true });

    const sections = ['programs','universities','compare','scholarships','blog'].map(id => document.getElementById(id)).filter(Boolean);
    const navAnchors = Array.from(navLinks.querySelectorAll('a[data-section]'));
    const spyObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => { if (entry.isIntersecting) { const id = entry.target.id; navAnchors.forEach(a => a.classList.toggle('active', a.dataset.section === id)); } });
    }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });
    sections.forEach(sec => spyObserver.observe(sec));

    $$('[data-scroll-to]').forEach(btn => btn.addEventListener('click', () => {
      const target = document.getElementById(btn.dataset.scrollTo);
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    }));

    const revealObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in-view'); obs.unobserve(entry.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    $$('.reveal').forEach(el => revealObserver.observe(el));

    const statEls = $$('.stat-num[data-count]');
    function animateCount(el) {
      const target = parseInt(el.dataset.count, 10), suffix = el.dataset.suffix || '', duration = 1400, start = performance.now();
      function tick(now) {
        const progress = Math.min((now - start) / duration, 1), eased = 1 - Math.pow(1 - progress, 3), value = Math.floor(eased * target);
        el.textContent = value.toLocaleString('en-IN') + suffix;
        if (progress < 1) requestAnimationFrame(tick);
        else el.textContent = target.toLocaleString('en-IN') + suffix;
      }
      requestAnimationFrame(tick);
    }
    const statObserver = new IntersectionObserver((entries, obs) => { entries.forEach(entry => { if (entry.isIntersecting) { animateCount(entry.target); obs.unobserve(entry.target); } }); }, { threshold: 0.5 });
    statEls.forEach(el => statObserver.observe(el));

    // Detail, account and admin pages share the header but not the landing
    // page controls below. Keeping the shared navigation active prevents
    // absent homepage elements from creating runtime errors on those pages.
    if (!document.getElementById('heroSearch')) return;

    const heroSearch = $('#heroSearch');
    const heroSearchInput = $('#heroSearchInput');
    const heroSearchBudget = $('#heroSearchBudget');
    const suggestionsBox = $('#searchSuggestions');

    // --- Live search: hero box wired to the real /search API ---
    // Replaces the old client-side suggestionsFor() lookup with a
    // debounced fetch to the server search endpoint. The dropdown
    // reuses the exact same DOM shape/classes (.suggestion-item /
    // .suggestion-tag on #searchSuggestions) so no CSS changes are
    // needed and the existing open/close styling still applies.
    const searchState = {
      controller: null,
      lastQuery: null,
      results: [],
      activeIndex: -1,
    };

    function closeSearchSuggestions() {
      suggestionsBox.classList.remove('open');
      suggestionsBox.innerHTML = '';
      searchState.results = [];
      searchState.activeIndex = -1;
    }

    function formatFee(fees) {
      return (fees === null || fees === undefined) ? 'Fees on request' : (inr(fees) + '/yr');
    }

    function updateActiveSuggestion() {
      const items = Array.from(suggestionsBox.querySelectorAll('.suggestion-item[data-sindex]'));
      items.forEach(el => {
        el.classList.toggle('is-active', Number(el.dataset.sindex) === searchState.activeIndex);
      });
      const activeEl = items[searchState.activeIndex];
      if (activeEl && activeEl.scrollIntoView) activeEl.scrollIntoView({ block: 'nearest' });
    }

    function renderSearchResults(results) {
      // Stable-group by category so the dropdown reads as clusters
      // ("MBA", "MCA", ...) instead of one flat list. This only reorders
      // for display — nothing is added, removed, or re-filtered.
      const groupOf = r => (r.category || 'More results');
      const groups = [];
      const seen = new Map();
      results.forEach(r => {
        const key = groupOf(r);
        if (!seen.has(key)) { seen.set(key, []); groups.push(key); }
        seen.get(key).push(r);
      });
      const grouped = groups.flatMap(key => seen.get(key));

      searchState.results = grouped;
      searchState.activeIndex = -1;

      if (!grouped.length) {
        suggestionsBox.innerHTML = `<div class="suggestion-item" aria-disabled="true"><span>No matching universities or programs found.</span></div>`;
        suggestionsBox.classList.add('open');
        return;
      }

      const query = searchState.lastQuery || '';
      let idx = 0;
      suggestionsBox.innerHTML = groups.map(key => {
        const rows = seen.get(key).map(r => {
          const i = idx++;
          const location = [r.university, r.city].filter(Boolean).join(', ');
          const meta = [location, r.duration, formatFee(r.fees)].filter(Boolean).join(' · ');
          const tag = [r.category, r.specialization].filter(Boolean).join(' · ') || 'Program';
          const label = r.program || r.university || '';
          return `<div class="suggestion-item" data-sindex="${i}" role="option" tabindex="-1" style="--stagger:${i}"><span>${highlightMatch(label, query)}${meta ? ' — ' + highlightMatch(meta, query) : ''}</span><span class="suggestion-tag">${tag}</span></div>`;
        }).join('');
        return `<div class="suggestion-group"><div class="suggestion-group-label">${key}</div>${rows}</div>`;
      }).join('');
      suggestionsBox.classList.add('open');
    }

    // Shown when the search box is focused but empty — surfaces the
    // person's own recent queries plus a static list of popular ones.
    // Purely a UI convenience; selecting a chip just re-runs the same
    // /search flow used for typed queries.
    function renderSearchIdle() {
      const recent = state.recentSearches;
      const recentBlock = recent.length ? `
        <div class="search-idle-section">
          <div class="search-idle-label">Recent searches</div>
          <div class="search-chip-row">${recent.map(q => `<button type="button" class="search-chip" data-search-chip="${q}">${q}</button>`).join('')}</div>
        </div>` : '';
      const popularBlock = `
        <div class="search-idle-section">
          <div class="search-idle-label">Popular searches</div>
          <div class="search-chip-row">${POPULAR_SEARCHES.map(q => `<button type="button" class="search-chip" data-search-chip="${q}">${q}</button>`).join('')}</div>
        </div>`;
      suggestionsBox.innerHTML = recentBlock + popularBlock;
      suggestionsBox.classList.add('open');
      searchState.results = [];
      searchState.activeIndex = -1;
    }

    function selectSearchResult(result) {
      if (!result) return;
      // No standalone program/university detail pages exist yet, so
      // "opening the appropriate page" means jumping to the live
      // Results section pre-filtered to this result — the same pattern
      // the rest of the app already uses for search/filter deep-links.
      if (result.university) $('#fSearch').value = result.university;
      if (result.program) $('#fProgram').value = result.program;
      state.resultPage = 1;
      renderResults();
      heroSearchInput.value = result.program || result.university || heroSearchInput.value;
      pushRecentSearch(heroSearchInput.value);
      closeSearchSuggestions();
      document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
    }

    function runSearch(query) {
      if (searchState.controller) searchState.controller.abort();
      const controller = new AbortController();
      searchState.controller = controller;

      fetch(`/search?q=${encodeURIComponent(query)}`, { signal: controller.signal })
        .then(res => (res.ok ? res.json() : []))
        .then(data => {
          if (searchState.lastQuery !== query) return; // stale response, ignore
          renderSearchResults(Array.isArray(data) ? data.slice(0, 10) : []);
        })
        .catch(err => {
          if (err && err.name === 'AbortError') return;
          renderSearchResults([]);
        });
    }

    const debouncedSearch = (() => {
      let timer = null;
      return (query) => {
        clearTimeout(timer);
        timer = setTimeout(() => runSearch(query), 300);
      };
    })();

    heroSearchInput.addEventListener('input', () => {
      const rawQuery = heroSearchInput.value.trim();

      // live highlight across program cards (unchanged local behaviour)
      const q = rawQuery.toLowerCase();
      $$('#progGrid .prog-card').forEach(card => {
        const match = !q || (card.dataset.name || '').toLowerCase().includes(q);
        card.classList.toggle('is-match', !!q && match);
        card.classList.toggle('no-match', !!q && !match);
      });

      if (rawQuery.length < 2) {
        if (searchState.controller) searchState.controller.abort();
        searchState.lastQuery = null;
        if (!rawQuery) renderSearchIdle(); else closeSearchSuggestions();
        return;
      }

      if (rawQuery === searchState.lastQuery && suggestionsBox.classList.contains('open')) {
        return; // identical to the last search already shown — skip duplicate request
      }

      searchState.lastQuery = rawQuery;
      debouncedSearch(rawQuery);
    });

    heroSearchInput.addEventListener('focus', () => {
      if (!heroSearchInput.value.trim()) renderSearchIdle();
    });

    heroSearchInput.addEventListener('keydown', (e) => {
      if (!suggestionsBox.classList.contains('open') || !searchState.results.length) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        searchState.activeIndex = Math.min(searchState.activeIndex + 1, searchState.results.length - 1);
        updateActiveSuggestion();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        searchState.activeIndex = Math.max(searchState.activeIndex - 1, 0);
        updateActiveSuggestion();
      } else if (e.key === 'Enter' && searchState.activeIndex >= 0) {
        e.preventDefault();
        selectSearchResult(searchState.results[searchState.activeIndex]);
      }
    });

    suggestionsBox.addEventListener('click', (e) => {
      const chip = e.target.closest('[data-search-chip]');
      if (chip) {
        const q = chip.dataset.searchChip;
        heroSearchInput.value = q;
        heroSearchInput.focus();
        searchState.lastQuery = q;
        pushRecentSearch(q);
        debouncedSearch(q);
        return;
      }
      const item = e.target.closest('.suggestion-item');
      if (!item || item.hasAttribute('aria-disabled')) return;
      const idx = Number(item.dataset.sindex);
      selectSearchResult(searchState.results[idx]);
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.hero-search-wrap')) closeSearchSuggestions();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && suggestionsBox.classList.contains('open')) {
        closeSearchSuggestions();
      }
    });

    heroSearch.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = heroSearchInput.value.trim();
      $('#fSearch').value = q;
      if (heroSearchBudget.value) $('#fBudget').value = heroSearchBudget.value;
      if (q) pushRecentSearch(q);
      state.resultPage = 1;
      renderResults();
      closeSearchSuggestions();
      document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
    });

    const backToTop = $('#backToTop');
    window.addEventListener('scroll', () => backToTop.classList.toggle('show', window.scrollY > 600), { passive: true });
    backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

    const stickyCtaBar = $('#stickyCtaBar');
    const heroEl = $('.hero');
    if (stickyCtaBar && heroEl) {
      const heroObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => stickyCtaBar.classList.toggle('show', !entry.isIntersecting && window.innerWidth <= 960));
      }, { threshold: 0 });
      heroObserver.observe(heroEl);
    }

    const modalOverlay = $('#modalOverlay'), modalClose = $('#modalClose'), modalFormView = $('#modalFormView'), modalSuccessView = $('#modalSuccessView'), leadForm = $('#leadForm');
    let lastFocusedEl = null;
    function openModal() {
      lastFocusedEl = document.activeElement;
      modalFormView.style.display = 'block';
      modalSuccessView.style.display = 'none';
      leadForm.reset();
      $$('.form-error').forEach(e => { e.classList.remove('show'); });
      $$('.form-group input, .form-group select').forEach(i => i.classList.remove('valid', 'invalid'));
      const uniField = $('#leadUniversity');
      if (uniField) uniField.value = '';
      modalOverlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      setTimeout(() => $('#leadName').focus(), 250);
    }
    function closeModal() { modalOverlay.classList.remove('open'); document.body.style.overflow = ''; if (lastFocusedEl) lastFocusedEl.focus(); }

    $$('[data-open-modal], .nav-cta, #navCtaBtn').forEach(el => el.addEventListener('click', (e) => { e.preventDefault(); openModal(); }));
    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) closeModal(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modalOverlay.classList.contains('open')) closeModal(); });

    const nameInput = $('#leadName'), phoneInput = $('#leadPhone'), emailInput = $('#leadEmail'), programSelect = $('#leadProgram');
    function showError(input, show, msg) {
      const errorEl = $('#err-' + input.id);
      if (msg) errorEl.textContent = '⚠ ' + msg;
      errorEl.classList.toggle('show', show);
      input.classList.toggle('invalid', show);
      input.classList.toggle('valid', !show && (input.value || '').trim().length > 0);
    }
    function showServerError(msg) {
      const el = $('#err-leadServer');
      if (!el) return;
      el.textContent = msg ? '⚠ ' + msg : '';
      el.classList.toggle('show', !!msg);
    }
    function validateName() { const ok = nameInput.value.trim().length >= 2; showError(nameInput, !ok); return ok; }
    function validatePhone() { const digits = phoneInput.value.replace(/\D/g, ''); const ok = digits.length === 10; showError(phoneInput, !ok); return ok; }
    function validateEmail() { const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim()); showError(emailInput, !ok); return ok; }
    function validateProgram() { const ok = !!(programSelect && programSelect.value.trim()); if (programSelect) { const el = $('#err-leadProgram'); if (el) el.classList.toggle('show', !ok); programSelect.classList.toggle('invalid', !ok); programSelect.classList.toggle('valid', ok); } return ok; }
    nameInput.addEventListener('input', () => { if (nameInput.classList.contains('invalid')) validateName(); });
    phoneInput.addEventListener('input', () => { if (phoneInput.classList.contains('invalid')) validatePhone(); });
    emailInput.addEventListener('input', () => { if (emailInput.classList.contains('invalid')) validateEmail(); });
    if (programSelect) programSelect.addEventListener('change', () => { if (programSelect.classList.contains('invalid')) validateProgram(); });
    nameInput.addEventListener('blur', validateName); phoneInput.addEventListener('blur', validatePhone); emailInput.addEventListener('blur', validateEmail);

    leadForm.addEventListener('submit', (e) => {
      e.preventDefault();
      showServerError('');
      const nameOk = validateName(), phoneOk = validatePhone(), emailOk = validateEmail(), programOk = validateProgram();
      if (!nameOk || !phoneOk || !emailOk || !programOk) return;

      const submitBtn = leadForm.querySelector('.form-submit');
      submitBtn.disabled = true; submitBtn.textContent = 'Submitting…';

      const payload = {
        name:       nameInput.value.trim(),
        phone:      phoneInput.value.replace(/\D/g, ''),
        email:      emailInput.value.trim(),
        program:    programSelect ? programSelect.value.trim() : '',
        university: ($('#leadUniversity') || {}).value || '',
      };

      fetch('/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        body: JSON.stringify(payload),
      })
        .then(res => res.json().then(data => ({ ok: res.ok, status: res.status, data })))
        .then(({ ok, data }) => {
          submitBtn.disabled = false; submitBtn.textContent = 'Request a callback';
          if (ok) {
            modalFormView.style.display = 'none';
            modalSuccessView.style.display = 'block';
            setTimeout(closeModal, 1800);
          } else {
            // Server-side validation or duplicate — surface the error inline
            const msg = (data && data.error) ? data.error : 'Something went wrong. Please try again.';
            showServerError(msg);
          }
        })
        .catch(() => {
          submitBtn.disabled = false; submitBtn.textContent = 'Request a callback';
          showServerError('Network error. Please check your connection and try again.');
        });
    });

    document.body.addEventListener('click', (e) => {
      const uniCard = e.target.closest('.uni-card');
      if (uniCard && uniCard.dataset.id) {
        const id = uniCard.dataset.id;
        state.recentlyViewed = [id, ...state.recentlyViewed.filter(x => x !== id)].slice(0, 10);
        saveLS(); updateRecentlyViewedView();

        // Navigate to the university details page. Guarded so clicks on
        // any interactive element inside the card (favourite, bookmark,
        // compare, apply, brochure, view-details, or any other link/button)
        // are left alone for their own handlers below — only a click on
        // the card itself triggers navigation.
        const hitInteractive = e.target.closest(
          '[data-fav], [data-bookmark], [data-compare], [data-detail], [data-apply], [data-brochure], a, button'
        );
        if (!hitInteractive && uniCard.dataset.slug) {
          window.location.href = '/university/' + uniCard.dataset.slug;
          return;
        }
      }

      // ── data-remove-compare ────────────────────────────────────────────
      const removeBtn = e.target.closest('[data-remove-compare]');
      if (removeBtn) {
        const id = String(removeBtn.dataset.removeCompare);
        state.compareSet.delete(id);
        saveLS(); renderCompareTable(); return;
      }

      // ── data-compare (add / toggle) ─────────────────────────────────────
      const cmpBtn = e.target.closest('[data-compare]');
      if (cmpBtn) {
        const id = String(cmpBtn.dataset.compare);
        if (state.compareSet.has(id)) {
          state.compareSet.delete(id);
        } else {
          if (state.compareSet.size >= 4) state.compareSet.delete([...state.compareSet][0]);
          state.compareSet.add(id);
        }
        saveLS(); renderCompareTable(); syncAllQuickActionButtons(); return;
      }

      const favBtn = e.target.closest('[data-fav]');
      if (favBtn) {
        const id = favBtn.dataset.fav;
        if (state.favorites.has(id)) state.favorites.delete(id); else state.favorites.add(id);
        saveLS(); renderResults(); syncAllQuickActionButtons();
      }

      const bmBtn = e.target.closest('[data-bookmark]');
      if (bmBtn) {
        const id = bmBtn.dataset.bookmark;
        if (state.bookmarks.has(id)) state.bookmarks.delete(id); else state.bookmarks.add(id);
        saveLS(); renderResults();
      }

      const detailsBtn = e.target.closest('[data-detail]');
      if (detailsBtn) {
        // data-detail carries the university id as a string; u.id may be a number.
        // Try appData first (fast), fall back to slug embedded in dataset.
        const detailId = String(detailsBtn.dataset.detail);
        const u = appData.universities.find(x => String(x.id) === detailId);
        if (u && u.slug) {
          window.location.href = '/university/' + u.slug;
        } else if (detailsBtn.dataset.slug) {
          window.location.href = '/university/' + detailsBtn.dataset.slug;
        }
      }

      const applyBtn = e.target.closest('[data-apply]');
      if (applyBtn) {
        const u = appData.universities.find(x => x.id === applyBtn.dataset.apply);
        if (u) {
          $('#leadProgram').value = u.programs[0] || '';
          const uniField = $('#leadUniversity');
          if (uniField) uniField.value = u.name || '';
        }
        openModal();
      }

      // Server-rendered cards (homepage uni grid, uni details page, program details page)
      // embed context directly as data attributes — no appData lookup needed.
      // data-apply-uni="<university name>"  (optional on program-only buttons)
      // data-apply-program="<program name>" (optional on uni-only buttons)
      const applyCtxBtn = e.target.closest('[data-apply-uni],[data-apply-program]');
      if (applyCtxBtn && !applyBtn) {
        const uniName  = applyCtxBtn.dataset.applyUni     || '';
        const progName = applyCtxBtn.dataset.applyProgram || '';
        const uniField = $('#leadUniversity');
        if (uniField) uniField.value = uniName;
        if (progName && programSelect) {
          // Try to match an existing <option>; if not found leave select at current value.
          const opt = Array.from(programSelect.options).find(o => o.value === progName || o.text === progName);
          if (opt) programSelect.value = opt.value;
        }
        openModal();
      }

      const brochureBtn = e.target.closest('[data-brochure]');
      if (brochureBtn) {
        const u = appData.universities.find(x => x.id === brochureBtn.dataset.brochure);
        alert(`Brochure download started for ${u.name} (demo action).`);
      }

      const pageBtn = e.target.closest('[data-page]');
      if (pageBtn) { state.resultPage = Number(pageBtn.dataset.page); renderResults(); }
    });

    ['#fSearch','#fDegree','#fProgram','#fBudget','#fNaac','#fNirf','#fPlacement','#fEmi','#fDuration','#fState','#fCity','#fMode','#fSpec','#sortBy'].forEach(sel => {
      $(sel).addEventListener('input', () => { state.resultPage = 1; renderResults(); });
      $(sel).addEventListener('change', () => { state.resultPage = 1; renderResults(); });
    });
    $('#resetFiltersBtn').addEventListener('click', () => {
      ['fSearch','fDegree','fProgram','fBudget','fNaac','fNirf','fPlacement','fEmi','fDuration','fState','fCity','fMode','fSpec'].forEach(id => $('#'+id).value = '');
      $('#sortBy').value = 'rating-desc';
      state.resultPage = 1;
      renderResults();
    });

    const wizardInputs = ['cfQualification','cfDegree','cfSpec','cfBudget','cfCareer'];
    function applyWizardVisibility() {
      wizardInputs.forEach((id, i) => $('#'+id).closest('.form-group').style.display = (i === state.wizardStep ? 'block' : 'none'));
      $('#cfPrev').style.display = state.wizardStep === 0 ? 'none' : 'inline-block';
      $('#cfNext').style.display = state.wizardStep >= 4 ? 'none' : 'inline-block';
      $('#cfRun').style.display = state.wizardStep === 5 ? 'inline-block' : 'none';
      renderWizardSteps();
    }
    applyWizardVisibility();
    $('#cfNext').addEventListener('click', () => { state.wizardStep = Math.min(5, state.wizardStep + 1); applyWizardVisibility(); });
    $('#cfPrev').addEventListener('click', () => { state.wizardStep = Math.max(0, state.wizardStep - 1); applyWizardVisibility(); });
    $('#cfRun').addEventListener('click', () => {
      const degree = $('#cfDegree').value, budget = Number($('#cfBudget').value || 0), spec = $('#cfSpec').value.toLowerCase();
      const recs = appData.universities.filter(u => (!degree || u.degree.includes(degree)) && (!budget || u.fee <= budget) && (!spec || u.specs.join(' ').toLowerCase().includes(spec))).slice(0,3);
      $('#cfResult').innerHTML = recs.length ? `Recommended: <strong>${recs.map(r=>r.name).join('</strong>, <strong>')}</strong>` : 'No perfect match. Try increasing budget or broader specialization.';
    });

    $('#eligibilityBtn').addEventListener('click', () => {
      const q = $('#elQual').value, m = Number($('#elMarks').value || 0), a = Number($('#elAge').value || 0), c = $('#elCourse').value;
      let ok = true, reasons = [];
      if (['Online MBA','Online MCA','Executive MBA'].includes(c) && q === '12th') { ok = false; reasons.push('Graduation required'); }
      if (m < 45) { ok = false; reasons.push('Minimum 45% marks suggested'); }
      if (a < 17) { ok = false; reasons.push('Minimum age 17'); }
      $('#eligibilityResult').innerHTML = ok ? `✅ Eligible for ${c}.` : `❌ Not eligible: ${reasons.join(', ')}.`;
    });

    $('#emiCalcBtn').addEventListener('click', () => {
      const P = Number($('#emiFees').value || 0), annual = Number($('#emiInterest').value || 0), n = Number($('#emiMonths').value || 0);
      if (!P || !n) return $('#emiResult').textContent = 'Please enter valid fees and months.';
      const r = annual / 12 / 100;
      const emi = r ? (P * r * Math.pow(1+r, n)) / (Math.pow(1+r, n)-1) : P / n;
      $('#emiResult').innerHTML = `Estimated Monthly EMI: <strong>${inr(Math.round(emi))}</strong>`;
    });

    $('#scholarshipBtn').addEventListener('click', () => {
      const income = Number($('#scIncome').value || 0), cat = $('#scCategory').value, g = $('#scGender').value, marks = Number($('#scMarks').value || 0);
      let score = 0;
      if (income <= 800000) score += 1;
      if (['SC','ST','OBC','EWS'].includes(cat)) score += 1;
      if (g === 'Female') score += 1;
      if (marks >= 75) score += 1;
      const map = ['Not eligible', 'Possible 5%', 'Likely 10%', 'Likely 15%', 'Likely 20%'];
      $('#scholarshipResult').innerHTML = `Scholarship result: <strong>${map[score]}</strong>`;
    });

    $('#blogSearchInput').addEventListener('input', renderBlogs);
    $$('[data-blog-filter]').forEach(btn => btn.addEventListener('click', () => {
      state.blogCategory = btn.dataset.blogFilter;
      renderBlogs();
    }));
    document.body.addEventListener('click', (e) => {
      const blog = e.target.closest('[data-blog-id]');
      if (blog) alert('Opening blog details (demo).');
    });

    $$('#faqWrap .faq-q').forEach(q => q.addEventListener('click', () => {
      const item = q.closest('.faq-item');
      item.classList.toggle('open');
      q.querySelector('span').textContent = item.classList.contains('open') ? '−' : '+';
    }));

    $$('#progGrid .prog-card').forEach(card => {
      card.addEventListener('click', () => {
        $('#fProgram').value = card.dataset.name;
        state.resultPage = 1;
        renderResults();
        document.getElementById('results').scrollIntoView({behavior:'smooth'});
      });
    });

    $$('a[href="#"]:not([data-section]):not(.nav-cta)').forEach(a => a.addEventListener('click', e => e.preventDefault()));

    /* ===== Phase 8E ===== */
    // Enhances the existing menu handlers without replacing their navigation logic.
    let menuTrigger = null;
    let resizeTimer = null;
    const syncMenuAccessibility = () => {
      const isOpen = navLinks.classList.contains('open');
      document.body.classList.toggle('nav-menu-open', isOpen && window.innerWidth <= 960);
      navLinks.setAttribute('aria-hidden', window.innerWidth > 960 || isOpen ? 'false' : 'true');

      if (isOpen) {
        menuTrigger = document.activeElement === hamburger ? hamburger : menuTrigger;
        const firstLink = navLinks.querySelector('a');
        if (firstLink && document.activeElement === hamburger) firstLink.focus();
      } else if (menuTrigger === hamburger && document.activeElement && navLinks.contains(document.activeElement)) {
        hamburger.focus();
      }
    };

    const closeMenu = () => {
      if (navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
        hamburger.classList.remove('is-active');
        hamburger.setAttribute('aria-expanded', 'false');
      }
      syncMenuAccessibility();
    };

    // Existing handlers run first; queueing this keeps one source of truth for state.
    hamburger.addEventListener('click', () => requestAnimationFrame(syncMenuAccessibility));
    navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', () => requestAnimationFrame(syncMenuAccessibility)));
    document.addEventListener('click', event => {
      if (window.innerWidth <= 960 && !navLinks.contains(event.target) && !hamburger.contains(event.target)) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeMenu();
    });
    window.addEventListener('resize', () => {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(() => {
        if (window.innerWidth > 960) closeMenu();
        else syncMenuAccessibility();
      }, 150);
    }, { passive: true });
    syncMenuAccessibility();

    // A rAF-throttled scroll pass adds a scroll state while avoiding layout work per event.
    let scrollQueued = false;
    window.addEventListener('scroll', () => {
      if (scrollQueued) return;
      scrollQueued = true;
      window.requestAnimationFrame(() => {
        document.documentElement.classList.toggle('is-scrolled', window.scrollY > 8);
        scrollQueued = false;
      });
    }, { passive: true });

    // Make reveal reusable for content rendered after initial observer setup.
    const phase8eReveal = element => {
      if (!element || element.classList.contains('in-view')) return;
      element.classList.add('reveal', 'phase-8e-reveal');
      revealObserver.observe(element);
    };
    const revealRoots = ['#blogGrid', '#resultsGrid', '#recentGrid'];
    revealRoots.forEach(selector => {
      const root = $(selector);
      if (!root || !window.MutationObserver) return;
      new MutationObserver(records => records.forEach(record => record.addedNodes.forEach(node => {
        if (node.nodeType !== 1) return;
        if (node.matches('.reveal')) revealObserver.observe(node);
        else if (node.matches('.blog-card, .result-card, .uni-card, .prog-card')) phase8eReveal(node);
      }))).observe(root, { childList: true });
    });
  }

  // boot() wires up homepage-only widgets (#backToTop, #modalOverlay, the
  // search grid, etc.). On pages that don't have those elements — like
  // auth.html — several of those calls hit null and throw. Left unguarded,
  // that exception used to kill the REST of this script file (a single
  // uncaught error in one top-level IIFE stops every statement after it,
  // including the auth page's password show/hide toggle further down),
  // which is why "Show password" silently did nothing on the login/register
  // page even though its own code was correct. try/catch here contains
  // boot() to its own page instead of taking the whole file down with it.
  try {
    boot();
  } catch (err) {
    console.error('boot() failed (likely a non-homepage page missing some elements):', err);
  }
})();

// ---------------------------------------------------------------------------
// Auth page (login.html) — tab switch, password visibility, role shortcuts.
// Guarded so this is a no-op on every other page.
// ---------------------------------------------------------------------------
(function () {
  const form = document.getElementById('authForm');
  if (!form) return;

  const tabs = document.querySelectorAll('.auth-tab');
  const loginModeInput = document.getElementById('authLoginMode');
  const emailInput = document.getElementById('email');
  const emailLabel = document.getElementById('authEmailLabel');

  const TAB_COPY = {
    universal: { label: 'Email or Username', placeholder: 'name@campus.edu' },
    institutional: { label: 'Institutional Email or ID', placeholder: 'name@institution.edu' },
  };

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => { t.classList.remove('is-active'); t.setAttribute('aria-selected', 'false'); });
      tab.classList.add('is-active');
      tab.setAttribute('aria-selected', 'true');

      const mode = tab.dataset.authTab;
      if (loginModeInput) loginModeInput.value = mode;
      const copy = TAB_COPY[mode];
      if (copy) {
        if (emailLabel) emailLabel.textContent = copy.label;
        if (emailInput) emailInput.placeholder = copy.placeholder;
      }
    });
  });

  // Password show/hide toggle.
  const eyeToggle = document.getElementById('authEyeToggle');
  const passwordInput = document.getElementById('password');
  if (eyeToggle && passwordInput) {
    eyeToggle.addEventListener('click', () => {
      const showing = passwordInput.type === 'text';
      passwordInput.type = showing ? 'password' : 'text';
      eyeToggle.setAttribute('aria-pressed', showing ? 'false' : 'true');
      eyeToggle.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
    });
  }

  // Same toggle, generalized for the register panel's two password fields
  // (Password / Confirm Password), each pointing at its own input via
  // data-eye-target so one handler covers both.
  document.querySelectorAll('.auth-eye-toggle[data-eye-target]').forEach(btn => {
    const target = document.getElementById(btn.dataset.eyeTarget);
    if (!target) return;
    btn.addEventListener('click', () => {
      const showing = target.type === 'text';
      target.type = showing ? 'password' : 'text';
      btn.setAttribute('aria-pressed', showing ? 'false' : 'true');
      btn.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
    });
  });

  // Role shortcuts — sets a hint field and focuses the email input with a
  // role-appropriate placeholder. The actual post-login destination is
  // still decided server-side from the authenticated user's real role;
  // this is a convenience shortcut, not a way to select what you log in as.
  const roleButtons = document.querySelectorAll('.auth-role-btn');
  const roleHintInput = document.getElementById('authRoleHint');
  const ROLE_PLACEHOLDER = {
    student: 'name@campus.edu',
    teacher: 'name@faculty.campus.edu',
    admin: 'name@admin.campus.edu',
  };

  roleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      roleButtons.forEach(b => b.classList.remove('is-active'));
      btn.classList.add('is-active');

      const role = btn.dataset.role;
      if (roleHintInput) roleHintInput.value = role;
      if (emailInput) {
        emailInput.placeholder = ROLE_PLACEHOLDER[role] || emailInput.placeholder;
        emailInput.focus();
      }
    });
  });
})();

// ---------------------------------------------------------------------------
// Unified auth page (auth.html) — Task 1: Login and Register live in one
// page/container. Clicking "Apply for Access" / "Already have an account?"
// cross-fades + slides the login card into the register card (and back)
// in place, instead of navigating to a second page/modal. Real form
// submissions still POST and reload normally — this only animates the
// toggle between the two idle forms. Guarded so it's a no-op elsewhere.
// ---------------------------------------------------------------------------
(function () {
  const stage = document.getElementById('authStage');
  if (!stage) return;

  const body = document.body;
  const panels = {
    login: document.getElementById('authPanelLogin'),
    register: document.getElementById('authPanelRegister'),
  };
  const eyebrowEl = document.getElementById('authEyebrow');
  const titleEl = document.getElementById('authTitle');
  const subtitleEl = document.getElementById('authSubtitle');
  const footEl = document.getElementById('authFoot');

  const COPY = {
    login: {
      title: 'Log In | Campus Unlock',
      eyebrow: 'Welcome back',
      heading: 'Log in to your account',
      subtitle: 'Pick up right where you left off.',
      foot: 'Don\u2019t have an account? <a href="/register" id="authToRegister">Apply for Access</a>',
      url: '/login',
    },
    register: {
      title: 'Apply for Access | Campus Unlock',
      eyebrow: 'Get started',
      heading: 'Create your account',
      subtitle: 'Compare, shortlist and apply \u2014 all in one place.',
      foot: 'Already have an account? <a href="/login" id="authToLogin">Log In</a>',
      url: '/register',
    },
  };

  const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ANIM_MS = prefersReduced ? 0 : 340;
  let animating = false;

  function focusFirstField(panel) {
    const field = panel.querySelector('input:not([type="hidden"])');
    if (field) field.focus({ preventScroll: true });
  }

  function bindFootLink() {
    const link = document.getElementById('authToRegister') || document.getElementById('authToLogin');
    if (link) link.addEventListener('click', onToggleClick);
  }

  function applyCopy(mode) {
    const c = COPY[mode];
    if (!c) return;
    document.title = c.title;
    if (eyebrowEl) eyebrowEl.textContent = c.eyebrow;
    if (titleEl) titleEl.textContent = c.heading;
    if (subtitleEl) subtitleEl.textContent = c.subtitle;
    if (footEl) footEl.innerHTML = c.foot;
    bindFootLink();
  }

  function switchTo(mode, pushState) {
    if (animating || body.dataset.authMode === mode || !panels[mode]) return;
    const from = panels[body.dataset.authMode];
    const to = panels[mode];
    if (!from || !to) return;

    animating = true;
    const goingForward = mode === 'register';

    if (prefersReduced) {
      from.hidden = true;
      to.hidden = false;
      body.dataset.authMode = mode;
      applyCopy(mode);
      focusFirstField(to);
      if (pushState !== false) history.pushState({ authMode: mode }, '', COPY[mode].url);
      animating = false;
      return;
    }

    const fromH = from.offsetHeight;
    stage.style.height = fromH + 'px';

    from.classList.add('auth-panel--stacked', goingForward ? 'auth-panel--out-to-left' : 'auth-panel--out-to-right');

    to.hidden = false;
    to.classList.add('auth-panel--stacked', goingForward ? 'auth-panel--in-from-right' : 'auth-panel--in-from-left');

    // Force a layout flush so the "incoming" start position is painted
    // before we flip it to settled below — otherwise both writes get
    // coalesced into one frame and it never visibly animates.
    void to.offsetHeight;

    requestAnimationFrame(() => {
      stage.style.height = to.scrollHeight + 'px';
      from.classList.remove('auth-panel--out-to-left', 'auth-panel--out-to-right');
      to.classList.remove('auth-panel--in-from-right', 'auth-panel--in-from-left');
      to.classList.add('auth-panel--settled');
    });

    setTimeout(() => {
      from.hidden = true;
      from.classList.remove('auth-panel--stacked', 'auth-panel--settled', 'auth-panel--out-to-left', 'auth-panel--out-to-right');
      to.classList.remove('auth-panel--stacked', 'auth-panel--settled');
      stage.style.height = '';
      animating = false;
    }, ANIM_MS + 20);

    body.dataset.authMode = mode;
    applyCopy(mode);
    focusFirstField(to);

    if (pushState !== false) {
      history.pushState({ authMode: mode }, '', COPY[mode].url);
    }
  }

  function onToggleClick(e) {
    e.preventDefault();
    switchTo(this.id === 'authToRegister' ? 'register' : 'login');
  }

  bindFootLink();

  window.addEventListener('popstate', (e) => {
    const fallback = location.pathname.indexOf('register') !== -1 ? 'register' : 'login';
    switchTo((e.state && e.state.authMode) || fallback, false);
  });
})();
