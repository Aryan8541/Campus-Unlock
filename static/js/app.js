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
    compareSet: new Set(),
    favorites: new Set(JSON.parse(localStorage.getItem('favorites') || '[]')),
    bookmarks: new Set(JSON.parse(localStorage.getItem('bookmarks') || '[]')),
    recentlyViewed: JSON.parse(localStorage.getItem('recentlyViewed') || '[]'),
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
  }

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

  // ---------------------------------------------------------------------------
  // Compare — API-driven
  // ---------------------------------------------------------------------------
  const compareState = {
    controller: null,   // AbortController for in-flight /compare request
  };

  // Update "#compareSelected" using the local compareSet only.
  function _updateCompareStatus() {
    const sel = document.getElementById('compareSelected');
    if (!sel) return;
    const count = state.compareSet.size;
    if (!count) { sel.textContent = 'Selected: none'; return; }
    const names = [...state.compareSet].map(
      id => (appData.universities.find(u => u.id === id) || {}).name || ('#' + id)
    );
    sel.textContent = 'Selected (' + count + '/4): ' + names.join(' vs ');
  }

  // Write a message row into #compareBody (colspan 8 to span all columns).
  function _compareBodyMessage(html) {
    const body = document.getElementById('compareBody');
    if (body) body.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:#64748b;">' + html + '</td></tr>';
  }

  // Build one <tr> per university from the /compare API response.
  // Columns match the existing compare.html <thead>:
  //   University | NAAC Grade | NIRF | Popular Program | Duration | Starting Fee | EMI | Placement
  // Extra detail (city, state, established year, website, categories,
  // specializations, modes) is embedded inside the University cell so the
  // existing table layout and CSS are untouched.
  function _renderCompareRows(universities) {
    const body = document.getElementById('compareBody');
    if (!body) return;
    if (!universities.length) {
      _compareBodyMessage('No data returned from the server.');
      return;
    }

    body.innerHTML = universities.map(function(u) {
      var logoHtml = u.logo
        ? '<img src="' + u.logo + '" alt="' + u.name + ' logo" style="width:32px;height:32px;object-fit:cover;border-radius:6px;vertical-align:middle;margin-right:8px;">'
        : '<span style="display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:6px;background:#e0e7ff;font-weight:700;font-size:13px;color:#4f46e5;margin-right:8px;vertical-align:middle;">' + (u.avatar || '?') + '</span>';

      var location   = [u.city, u.state].filter(Boolean).join(', ') || '\u2014';
      var established = u.established_year ? 'Est. ' + u.established_year : '';
      var websiteHtml = u.website
        ? '<a href="' + u.website + '" target="_blank" rel="noopener noreferrer" style="color:#2563eb;font-size:11px;">' + u.website.replace(/^https?:\/\//, '') + '</a>'
        : '';
      var cats  = (u.categories      || []).join(', ') || '\u2014';
      var specs = (u.specializations || []).slice(0, 4).join(', ') || '\u2014';
      var modes = (u.modes           || []).join(', ') || '\u2014';

      var uniCell = '<td class="uni-cell"><div style="display:flex;align-items:flex-start;gap:4px;">'
        + logoHtml
        + '<div>'
        + '<div style="font-weight:600;font-size:14px;">' + u.name + '</div>'
        + '<div style="color:#64748b;font-size:11px;margin-top:2px;">' + location + (established ? ' \u00b7 ' + established : '') + '</div>'
        + (websiteHtml ? '<div style="margin-top:2px;">' + websiteHtml + '</div>' : '')
        + '<div style="color:#475569;font-size:11px;margin-top:4px;"><strong>Categories:</strong> ' + cats + '</div>'
        + '<div style="color:#475569;font-size:11px;"><strong>Specs:</strong> ' + specs + '</div>'
        + '<div style="color:#475569;font-size:11px;"><strong>Mode:</strong> ' + modes + '</div>'
        + '</div></div></td>';

      var naacCell     = '<td>' + (u.naac || '\u2014') + '</td>';
      var nirfCell     = '<td>' + (u.nirf != null ? '#' + u.nirf : '\u2014') + '</td>';
      var firstProg    = (u.programs && u.programs[0]) ? (u.programs[0].title || u.programs[0]) : '\u2014';
      var progCell     = '<td>' + firstProg + '</td>';
      var firstDur     = (u.programs && u.programs[0] && u.programs[0].duration) ? u.programs[0].duration : '\u2014';
      var durationCell = '<td>' + firstDur + '</td>';
      var feeCell      = '<td class="fee-cell">' + (u.min_fee != null ? inr(u.min_fee) + '/yr' : 'On request') + '</td>';
      var emiCell      = '<td>\u2014</td>';
      var placementCell = '<td>\u2014</td>';

      return '<tr>' + uniCell + naacCell + nirfCell + progCell + durationCell + feeCell + emiCell + placementCell + '</tr>';
    }).join('');
  }

  // Main compare entry point — validates selection, then calls
  // GET /compare?ids=… and populates #compareBody.
  function renderCompareTable() {
    _updateCompareStatus();

    var count = state.compareSet.size;

    // 0 selected — show default overview rows from already-hydrated appData
    if (count === 0) {
      var body = document.getElementById('compareBody');
      if (!body) return;
      var source = appData.universities.slice(0, 6);
      if (!source.length) {
        _compareBodyMessage('Select 2\u20134 universities from the results list to compare.');
        return;
      }
      body.innerHTML = source.map(function(u) {
        return '<tr>'
          + '<td class="uni-cell">' + u.name + '</td>'
          + '<td>' + (u.naac || '\u2014') + '</td>'
          + '<td>' + (u.nirf != null ? '#' + u.nirf : '\u2014') + '</td>'
          + '<td>' + ((u.programs && u.programs[0]) || '\u2014') + '</td>'
          + '<td>' + (u.duration || '\u2014') + '</td>'
          + '<td class="fee-cell">' + (u.fee != null ? inr(u.fee) + '/yr' : 'On request') + '</td>'
          + '<td>\u2014</td>'
          + '<td>\u2014</td>'
          + '</tr>';
      }).join('');
      return;
    }

    if (count < 2) {
      _compareBodyMessage('Please select at least two universities.');
      return;
    }

    if (count > 4) {
      _compareBodyMessage('You can compare a maximum of four universities.');
      return;
    }

    // Abort any in-flight request
    if (compareState.controller) compareState.controller.abort();
    var controller = new AbortController();
    compareState.controller = controller;

    var ids = [...state.compareSet].join(',');
    _compareBodyMessage('Loading comparison\u2026');

    fetch('/compare?ids=' + encodeURIComponent(ids), { signal: controller.signal })
      .then(function(res) {
        if (!res.ok) return res.json().then(function(err) { return Promise.reject(err); });
        return res.json();
      })
      .then(function(data) {
        compareState.controller = null;
        _renderCompareRows(Array.isArray(data.universities) ? data.universities : []);
      })
      .catch(function(err) {
        if (err && err.name === 'AbortError') return;
        compareState.controller = null;
        _compareBodyMessage((err && err.error) ? err.error : 'Failed to load comparison. Please try again.');
      });
  }

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
              <button class="action-btn action-light" data-compare="${u.id}">Compare</button>
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
    renderCompareTable();
    renderBlogs();
    setupFiltersMeta();
    renderResults();
    updateRecentlyViewedView();
    renderWizardSteps();

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
      Array.from(suggestionsBox.children).forEach((el, i) => {
        // Inline style only — no CSS file changes — so keyboard
        // navigation has a visible highlight regardless of stylesheet.
        el.style.background = (i === searchState.activeIndex) ? 'rgba(37,99,235,0.08)' : '';
      });
      const activeEl = suggestionsBox.children[searchState.activeIndex];
      if (activeEl && activeEl.scrollIntoView) activeEl.scrollIntoView({ block: 'nearest' });
    }

    function renderSearchResults(results) {
      searchState.results = results;
      searchState.activeIndex = -1;
      if (!results.length) {
        suggestionsBox.innerHTML = `<div class="suggestion-item" aria-disabled="true"><span>No matching universities or programs found.</span></div>`;
        suggestionsBox.classList.add('open');
        return;
      }
      suggestionsBox.innerHTML = results.map((r, i) => {
        const location = [r.university, r.city].filter(Boolean).join(', ');
        const meta = [location, r.duration, formatFee(r.fees)].filter(Boolean).join(' · ');
        const tag = [r.category, r.specialization].filter(Boolean).join(' · ') || 'Program';
        return `<div class="suggestion-item" data-sindex="${i}" role="option" tabindex="-1"><span>${r.program || r.university || ''}${meta ? ' — ' + meta : ''}</span><span class="suggestion-tag">${tag}</span></div>`;
      }).join('');
      suggestionsBox.classList.add('open');
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
        closeSearchSuggestions();
        return;
      }

      if (rawQuery === searchState.lastQuery && suggestionsBox.classList.contains('open')) {
        return; // identical to the last search already shown — skip duplicate request
      }

      searchState.lastQuery = rawQuery;
      debouncedSearch(rawQuery);
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
      $('#fSearch').value = heroSearchInput.value.trim();
      if (heroSearchBudget.value) $('#fBudget').value = heroSearchBudget.value;
      state.resultPage = 1;
      renderResults();
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

      const favBtn = e.target.closest('[data-fav]');
      if (favBtn) {
        const id = favBtn.dataset.fav;
        if (state.favorites.has(id)) state.favorites.delete(id); else state.favorites.add(id);
        saveLS(); renderResults();
      }

      const bmBtn = e.target.closest('[data-bookmark]');
      if (bmBtn) {
        const id = bmBtn.dataset.bookmark;
        if (state.bookmarks.has(id)) state.bookmarks.delete(id); else state.bookmarks.add(id);
        saveLS(); renderResults();
      }

      const cmpBtn = e.target.closest('[data-compare]');
      if (cmpBtn) {
        const id = cmpBtn.dataset.compare;
        if (state.compareSet.has(id)) state.compareSet.delete(id);
        else {
          if (state.compareSet.size >= 4) state.compareSet = new Set([...state.compareSet].slice(1));
          state.compareSet.add(id);
        }
        renderCompareTable();
      }

      const detailsBtn = e.target.closest('[data-detail]');
      if (detailsBtn) {
        const u = appData.universities.find(x => x.id === detailsBtn.dataset.detail);
        alert(`View Details\n\n${u.name}\nNAAC ${u.naac} · NIRF #${u.nirf}\nPrograms: ${u.programs.join(', ')}`);
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

  boot();
})();
