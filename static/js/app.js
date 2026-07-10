(function () {
  'use strict';

  const appData = {
    programs: [
      { id:'p1', name:'Online MBA', degree:'Master', duration:'2 Years', tag:'#1 Choice', spec:['Marketing','Finance','HR'], emoji:'🎓' },
      { id:'p2', name:'Online MCA', degree:'Master', duration:'2 Years', tag:'Trending', spec:['AI','Cyber Security','Cloud'], emoji:'💻' },
      { id:'p3', name:'Online BBA', degree:'Bachelor', duration:'3 Years', tag:'Popular', spec:['Business Analytics','Marketing'], emoji:'📊' },
      { id:'p4', name:'1-Year MBA', degree:'Master', duration:'1 Year', tag:'Fast Track', spec:['General Management'], emoji:'⚡' },
      { id:'p5', name:'Dual MBA', degree:'Master', duration:'2 Years', tag:'New', spec:['Dual Specialization'], emoji:'🔗' },
      { id:'p6', name:'Online BCA', degree:'Bachelor', duration:'3 Years', tag:'Tech', spec:['Programming','Data Science'], emoji:'🖥️' },
      { id:'p7', name:'Executive MBA', degree:'Master', duration:'1 Year', tag:'Premium', spec:['Leadership','Strategy'], emoji:'🏛️' },
      { id:'p8', name:'Online M.Tech', degree:'Master', duration:'2 Years', tag:'New', spec:['CS','AI'], emoji:'⚙️' },
      { id:'p9', name:'Online M.Com', degree:'Master', duration:'2 Years', tag:'Affordable', spec:['Finance','Accounting'], emoji:'📈' }
    ],
    universities: [
      { id:'u1', name:'Amity University Online', naac:'A+', nirf:35, rating:4.8, fee:65000, emi:'Yes', placement:88, duration:'2 Years', state:'Uttar Pradesh', city:'Noida', mode:'Online', programs:['Online MBA','Online MCA','Online BBA'], specs:['Marketing','Finance','AI'], degree:['Bachelor','Master'], avatar:'AM' },
      { id:'u2', name:'NMIMS Online', naac:'A++', nirf:21, rating:4.9, fee:100000, emi:'Yes', placement:92, duration:'2 Years', state:'Maharashtra', city:'Mumbai', mode:'Online', programs:['Online MBA','Online BBA','Executive MBA'], specs:['Finance','Leadership'], degree:['Bachelor','Master'], avatar:'NM' },
      { id:'u3', name:'Manipal University Online', naac:'A++', nirf:43, rating:4.7, fee:70000, emi:'Yes', placement:86, duration:'2 Years', state:'Karnataka', city:'Manipal', mode:'Online', programs:['Online MBA','Online MCA','Online M.Com'], specs:['Cloud','Cyber Security','Accounting'], degree:['Master'], avatar:'MP' },
      { id:'u4', name:'LPU Online', naac:'A+', nirf:46, rating:4.6, fee:45000, emi:'Yes', placement:82, duration:'3 Years', state:'Punjab', city:'Jalandhar', mode:'Online', programs:['Online MBA','Online BCA','Online BBA'], specs:['Programming','Marketing'], degree:['Bachelor','Master'], avatar:'LP' },
      { id:'u5', name:'Jain University Online', naac:'A++', nirf:68, rating:4.7, fee:55000, emi:'Yes', placement:85, duration:'2 Years', state:'Karnataka', city:'Bengaluru', mode:'Online', programs:['Online MBA','Online MCA','Online BBA'], specs:['AI','Business Analytics'], degree:['Bachelor','Master'], avatar:'JN' },
      { id:'u6', name:'Chandigarh University', naac:'A+', nirf:45, rating:4.5, fee:40000, emi:'Yes', placement:80, duration:'2 Years', state:'Punjab', city:'Mohali', mode:'Online', programs:['Online MBA','Online MCA'], specs:['Cyber Security','HR'], degree:['Master'], avatar:'CU' },
      { id:'u7', name:'Symbiosis Centre for Distance Learning', naac:'A', nirf:88, rating:4.4, fee:52000, emi:'No', placement:78, duration:'2 Years', state:'Maharashtra', city:'Pune', mode:'Hybrid', programs:['Online MBA','Online BBA'], specs:['Operations','Marketing'], degree:['Bachelor','Master'], avatar:'SY' },
      { id:'u8', name:'UPES Online', naac:'A', nirf:61, rating:4.3, fee:85000, emi:'Yes', placement:84, duration:'2 Years', state:'Uttarakhand', city:'Dehradun', mode:'Online', programs:['Online MBA','Online BCA','Online M.Tech'], specs:['AI','Energy Management'], degree:['Bachelor','Master'], avatar:'UP' }
    ],
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

  function saveLS() {
    localStorage.setItem('favorites', JSON.stringify([...state.favorites]));
    localStorage.setItem('bookmarks', JSON.stringify([...state.bookmarks]));
    localStorage.setItem('recentlyViewed', JSON.stringify(state.recentlyViewed.slice(0, 10)));
  }

  function renderPrograms() {
    const grid = $('#progGrid');
    grid.innerHTML = appData.programs.map((p, i) => `
      <div class="prog-card reveal reveal-stagger" style="--d:${i*40}ms" data-name="${p.name}" data-program-id="${p.id}">
        <div class="prog-icon">${p.emoji}</div>
        <div>
          <div class="prog-name">${p.name}</div>
          <div class="prog-meta">${p.duration} · ${p.spec.join(', ')}</div>
          <div class="prog-tag">${p.tag}</div>
        </div>
      </div>
    `).join('');
    const leadProgram = $('#leadProgram');
    leadProgram.innerHTML = '<option value="">Select a program</option>' + appData.programs.map(p => `<option>${p.name}</option>`).join('') + '<option>Not sure yet</option>';
    const fProgram = $('#fProgram');
    fProgram.innerHTML = '<option value="">Any</option>' + appData.programs.map(p => `<option>${p.name}</option>`).join('');
  }

  function renderUniversities() {
    const grid = $('#uniGrid');
    grid.innerHTML = appData.universities.slice(0, 6).map((u, i) => `
      <div class="uni-card reveal reveal-stagger" style="--d:${i*60}ms" data-id="${u.id}">
        <div class="uni-top">
          <div class="uni-avatar">${u.avatar}</div>
          <div><div class="uni-name">${u.name}</div><div class="uni-naac">NAAC ${u.naac} · NIRF #${u.nirf}</div></div>
          <div class="uni-rating">★ ${u.rating}</div>
        </div>
        <div class="uni-chips">${u.programs.slice(0,4).map(p=>`<span class="uni-chip">${p.replace('Online ','')}</span>`).join('')}</div>
        <div class="uni-fee">From ${inr(u.fee)}/yr</div>
      </div>
    `).join('');
  }

  function renderCompareTable() {
    const body = $('#compareBody');
    const source = state.compareSet.size === 2 ? appData.universities.filter(u => state.compareSet.has(u.id)) : appData.universities.slice(0,6);
    body.innerHTML = source.map(u => `
      <tr>
        <td class="uni-cell">${u.name}</td>
        <td>${u.naac}</td>
        <td>#${u.nirf}</td>
        <td>${u.programs[0]}</td>
        <td>${u.duration}</td>
        <td class="fee-cell">${inr(u.fee)}/yr</td>
        <td>${u.emi}</td>
        <td>${u.placement}%</td>
      </tr>
    `).join('');
    $('#compareSelected').textContent = state.compareSet.size ? `Selected: ${[...state.compareSet].map(id => appData.universities.find(u => u.id===id)?.name).join(' vs ')}` : 'Selected: none';
  }

  function renderBlogs() {
    const grid = $('#blogGrid');
    const query = ($('#blogSearchInput')?.value || '').toLowerCase().trim();
    let blogs = appData.blogs.filter(b => (state.blogCategory === 'all' || b.category === state.blogCategory) && b.title.toLowerCase().includes(query));
    $('#blogFilterInfo').textContent = `Showing ${blogs.length} blog post(s)${state.blogCategory !== 'all' ? ` in ${state.blogCategory}` : ''}.`;
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
    const states = [...new Set(appData.universities.map(u => u.state))];
    const cities = [...new Set(appData.universities.map(u => u.city))];
    $('#fState').innerHTML = '<option value="">Any</option>' + states.map(s => `<option>${s}</option>`).join('');
    $('#fCity').innerHTML = '<option value="">Any</option>' + cities.map(c => `<option>${c}</option>`).join('');
  }

  function getFilteredUniversities() {
    const f = {
      search: $('#fSearch').value.toLowerCase().trim(),
      degree: $('#fDegree').value,
      program: $('#fProgram').value,
      budget: Number($('#fBudget').value || 0),
      naac: $('#fNaac').value,
      nirf: Number($('#fNirf').value || 0),
      placement: Number($('#fPlacement').value || 0),
      emi: $('#fEmi').value,
      duration: $('#fDuration').value,
      state: $('#fState').value,
      city: $('#fCity').value,
      mode: $('#fMode').value,
      spec: $('#fSpec').value.toLowerCase().trim()
    };

    return appData.universities.filter(u => {
      const hitSearch = !f.search || [u.name, u.city, u.state, u.mode, u.naac, ...u.programs, ...u.specs].join(' ').toLowerCase().includes(f.search);
      const hitDegree = !f.degree || u.degree.includes(f.degree);
      const hitProgram = !f.program || u.programs.includes(f.program);
      const hitBudget = !f.budget || u.fee <= f.budget;
      const hitNaac = !f.naac || u.naac === f.naac;
      const hitNirf = !f.nirf || u.nirf <= f.nirf;
      const hitPlacement = !f.placement || u.placement >= f.placement;
      const hitEmi = !f.emi || u.emi === f.emi;
      const hitDuration = !f.duration || u.duration === f.duration;
      const hitState = !f.state || u.state === f.state;
      const hitCity = !f.city || u.city === f.city;
      const hitMode = !f.mode || u.mode === f.mode;
      const hitSpec = !f.spec || u.specs.join(' ').toLowerCase().includes(f.spec);
      return hitSearch && hitDegree && hitProgram && hitBudget && hitNaac && hitNirf && hitPlacement && hitEmi && hitDuration && hitState && hitCity && hitMode && hitSpec;
    });
  }

  function sortUniversities(list) {
    const sort = $('#sortBy').value;
    const arr = [...list];
    if (sort === 'rating-desc') arr.sort((a,b) => b.rating-a.rating);
    if (sort === 'fee-asc') arr.sort((a,b) => a.fee-b.fee);
    if (sort === 'fee-desc') arr.sort((a,b) => b.fee-a.fee);
    if (sort === 'nirf-asc') arr.sort((a,b) => a.nirf-b.nirf);
    return arr;
  }

  function renderResults() {
    let rows = sortUniversities(getFilteredUniversities());
    $('#resultCount').textContent = `${rows.length} result(s)`;
    const totalPages = Math.max(1, Math.ceil(rows.length / state.pageSize));
    if (state.resultPage > totalPages) state.resultPage = totalPages;
    const start = (state.resultPage - 1) * state.pageSize;
    const pageRows = rows.slice(start, start + state.pageSize);

    $('#resultCards').innerHTML = pageRows.map(u => `
      <article class="result-card" data-id="${u.id}">
        <div class="uni-top">
          <div class="uni-avatar">${u.avatar}</div>
          <div><div class="uni-name">${u.name}</div><div class="uni-naac">NAAC ${u.naac} · NIRF #${u.nirf} · ${u.city}</div></div>
          <div class="uni-rating">★ ${u.rating}</div>
        </div>
        <div class="uni-chips">${u.programs.map(p=>`<span class="uni-chip">${p.replace('Online ','')}</span>`).join('')}</div>
        <div class="uni-fee">From ${inr(u.fee)}/yr · Placement ${u.placement}% · EMI ${u.emi}</div>
        <div class="result-actions">
          <button class="action-btn action-light" data-fav="${u.id}">${state.favorites.has(u.id) ? '★ Favorited' : '☆ Favorite'}</button>
          <button class="action-btn action-light" data-bookmark="${u.id}">${state.bookmarks.has(u.id) ? '🔖 Bookmarked' : '🔖 Bookmark'}</button>
          <button class="action-btn action-light" data-compare="${u.id}">Compare</button>
          <button class="action-btn action-light" data-detail="${u.id}">View Details</button>
          <button class="action-btn action-apply" data-apply="${u.id}">Apply</button>
          <button class="action-btn action-light" data-brochure="${u.id}">Download Brochure</button>
        </div>
      </article>
    `).join('') || `<div class="tool-result">No universities match your filters.</div>`;

    $('#pagination').innerHTML = Array.from({length: totalPages}, (_,i) => `
      <button class="${state.resultPage === i+1 ? 'active' : ''}" data-page="${i+1}">${i+1}</button>
    `).join('');
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
    renderPrograms();
    renderUniversities();
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

    const heroSearch = $('#heroSearch');
    const heroSearchInput = $('#heroSearchInput');
    const heroSearchBudget = $('#heroSearchBudget');
    const suggestionsBox = $('#searchSuggestions');

    heroSearchInput.addEventListener('input', () => {
      const list = suggestionsFor(heroSearchInput.value);
      suggestionsBox.innerHTML = list.map((s, i) => `<div class="suggestion-item" data-sindex="${i}"><span>${s.label}</span><span class="suggestion-tag">${s.type}</span></div>`).join('');
      suggestionsBox.classList.toggle('open', list.length > 0);
      suggestionsBox.dataset.payload = JSON.stringify(list.map(s => ({type:s.type,label:s.label})));
      suggestionsBox._actions = list.map(s => s.action);
      // live search across cards
      const q = heroSearchInput.value.trim().toLowerCase();
      $$('#progGrid .prog-card').forEach(card => {
        const match = !q || (card.dataset.name || '').toLowerCase().includes(q);
        card.classList.toggle('is-match', !!q && match);
        card.classList.toggle('no-match', !!q && !match);
      });
    });

    suggestionsBox.addEventListener('click', (e) => {
      const item = e.target.closest('.suggestion-item');
      if (!item) return;
      const idx = Number(item.dataset.sindex);
      const fn = suggestionsBox._actions?.[idx];
      if (fn) fn();
      suggestionsBox.classList.remove('open');
      heroSearchInput.value = item.firstElementChild.textContent;
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.hero-search-wrap')) suggestionsBox.classList.remove('open');
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
      $$('.form-error').forEach(e => e.classList.remove('show'));
      $$('.form-group input').forEach(i => i.classList.remove('valid', 'invalid'));
      modalOverlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      setTimeout(() => $('#leadName').focus(), 250);
    }
    function closeModal() { modalOverlay.classList.remove('open'); document.body.style.overflow = ''; if (lastFocusedEl) lastFocusedEl.focus(); }

    $$('[data-open-modal], .nav-cta, #navCtaBtn').forEach(el => el.addEventListener('click', (e) => { e.preventDefault(); openModal(); }));
    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) closeModal(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modalOverlay.classList.contains('open')) closeModal(); });

    const nameInput = $('#leadName'), phoneInput = $('#leadPhone'), emailInput = $('#leadEmail');
    function showError(input, show) {
      const errorEl = $('#err-' + input.id);
      errorEl.classList.toggle('show', show);
      input.classList.toggle('invalid', show);
      input.classList.toggle('valid', !show && input.value.trim().length > 0);
    }
    function validateName() { const ok = nameInput.value.trim().length >= 2; showError(nameInput, !ok); return ok; }
    function validatePhone() { const digits = phoneInput.value.replace(/\D/g, ''); const ok = digits.length === 10; showError(phoneInput, !ok); return ok; }
    function validateEmail() { const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim()); showError(emailInput, !ok); return ok; }
    nameInput.addEventListener('input', () => { if (nameInput.classList.contains('invalid')) validateName(); });
    phoneInput.addEventListener('input', () => { if (phoneInput.classList.contains('invalid')) validatePhone(); });
    emailInput.addEventListener('input', () => { if (emailInput.classList.contains('invalid')) validateEmail(); });
    nameInput.addEventListener('blur', validateName); phoneInput.addEventListener('blur', validatePhone); emailInput.addEventListener('blur', validateEmail);

    leadForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!validateName() || !validatePhone() || !validateEmail()) return;
      const submitBtn = leadForm.querySelector('.form-submit');
      submitBtn.disabled = true; submitBtn.textContent = 'Submitting…';
      setTimeout(() => {
        modalFormView.style.display = 'none';
        modalSuccessView.style.display = 'block';
        submitBtn.disabled = false; submitBtn.textContent = 'Request a callback';
        setTimeout(closeModal, 1800);
      }, 450);
    });

    document.body.addEventListener('click', (e) => {
      const uniCard = e.target.closest('.uni-card');
      if (uniCard && uniCard.dataset.id) {
        const id = uniCard.dataset.id;
        state.recentlyViewed = [id, ...state.recentlyViewed.filter(x => x !== id)].slice(0, 10);
        saveLS(); updateRecentlyViewedView();
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
          if (state.compareSet.size >= 2) state.compareSet = new Set([...state.compareSet].slice(1));
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
        $('#leadProgram').value = u.programs[0] || '';
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
  }

  boot();
})();