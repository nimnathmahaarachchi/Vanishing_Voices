
(async () => { 
  'use strict';
  // Inline the SVG so map controls can access its markers.
  await Promise.all(Array.from(document.querySelectorAll('[data-map-src]')).map(async placeholder => {
    try {
      const response = await fetch(placeholder.dataset.mapSrc); // Read the SVG address
      if (!response.ok) return;
      const documentWithMap = new DOMParser().parseFromString(await response.text(), 'image/svg+xml'); // Turn downloaded SVG text into elements the browser could work with that
      const map = documentWithMap.documentElement;
      if (map.localName === 'svg') placeholder.replaceWith(document.importNode(map, true)); // Replace the fallback only when the downloaded document is an SVG.
    } catch (_) {
      // Leave the object fallback visible if inline loading fails.
    }
  }));
  const node = document.getElementById('atlas-data');
  if (!node) return;
  // Index records by slug to connect controls with the matching animal.
  const { animals, animal: activeAnimal, page } = JSON.parse(node.textContent); // Unpack the page's JSON; animal is renamed activeAnimal in this script.
  const bySlug = Object.fromEntries(animals.map(a => [a.slug, a])); // A lookup table: bySlug['tiger'] gives the tiger record.
  const find = (selector, root = document) => root.querySelector(selector); // Find one matching element; use the whole page unless a smaller root is supplied.
  const findAll = (selector, root = document) => Array.from(root.querySelectorAll(selector)); // Collect matching elements into an array so we can loop through them.
  const SLIDE_INTERVAL = 3000; //  3 seconds between photographs.
  document.documentElement.style.setProperty('--slide-time', `${SLIDE_INTERVAL}ms`);
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; // Check whether the visitor has asked their device to reduce animation.
  const icon = type => `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${type === 'play' ? '<path d="m8 4 12 8-12 8Z"/>' : '<path d="M9 5v14M15 5v14"/>'}</svg>`;
  const statusName = a => a.status === 'CR' ? 'Critically endangered' : 'Endangered';
  // Escape text before inserting it into search results and tooltips.
  const escapeText = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let toastTimer;
  function toast(message) {
    const element = find('.toast');
    element.textContent = message;
    element.classList.add('show');
    clearTimeout(toastTimer); // Cancel the old hide timer so it does not dismiss a newer message too early.
    toastTimer = setTimeout(() => element.classList.remove('show'), 4500);
  }

  // One slideshow controller serves both hero and profile photographs.
  function slideshow(slides, { pause, next, previous, tabs = [], onChange, progress }) {
    if (!slides.length) return;
    // Respect reduced motion and pause timers while the tab is hidden.
    let current = 0, timer = null, userPaused = reducedMotion;
    // Decode photographs before starting the crossfade.
    const ready = Promise.all(slides.map(async slide => { // Wait until every slide has finished loading or reported an error.
      const image = find('img', slide);
      if (!image) return;
      try {
        if (!image.complete) await new Promise(resolve => {
          image.addEventListener('load', resolve, {once:true}); // once removes this listener after it runs the first time.
          image.addEventListener('error', resolve, {once:true});
        });
        if (image.naturalWidth && image.decode) await image.decode();
      } catch (_) { /* Keep the current photo if decoding fails. */ }
    }));
    const canRun = () => !userPaused && !document.hidden; // Advance only if the visitor has not paused and the browser tab is visible.
    function restartProgress() {
      if (!progress) return;
      progress.classList.remove('running');
      void progress.offsetWidth; // Restart the CSS progress animation.
      if (canRun()) progress.classList.add('running');
    }
    function setPauseLabel() {
      if (!pause) return;
      pause.innerHTML = icon(userPaused ? 'play' : 'pause');
      pause.setAttribute('aria-label', `${userPaused ? 'Play' : 'Pause'} ${page === 'home' ? 'background' : 'photo'} slideshow`);
      pause.setAttribute('aria-pressed', String(userPaused));
    }
    function stop() { clearInterval(timer); timer = null; }
    function start() {
      stop();
      if (canRun()) timer = setInterval(() => show((current + 1) % slides.length, false), SLIDE_INTERVAL);
      restartProgress();
    }
    function show(index, restart = true) {
      index = (index + slides.length) % slides.length; // Wrap around: after the last photo comes the first; before the first comes the last.
      const photo = find('img', slides[index]);
      if (photo && (!photo.complete || !photo.naturalWidth)) return; // Do not switch to a photograph that is still loading or failed to load.
      const outgoing = current;
      current = index;
      slides.forEach((slide, i) => {
        slide.classList.toggle('previous', i === outgoing && outgoing !== current);
        slide.classList.toggle('active', i === current);
        slide.setAttribute('aria-hidden', String(i !== current));
      });
      tabs.forEach((tab, i) => tab.setAttribute('aria-pressed', String(i === current)));
      onChange?.(current); // Call the caption update only if this slideshow was given one.
      if (restart) start(); else restartProgress();
    }
    pause?.addEventListener('click', () => { userPaused = !userPaused; setPauseLabel(); start(); });
    next?.addEventListener('click', () => show(current + 1));
    previous?.addEventListener('click', () => show(current - 1));
    tabs.forEach((tab, i) => tab.addEventListener('click', () => show(i)));
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); else start(); });
    setPauseLabel();
    slides.forEach((slide, i) => slide.setAttribute('aria-hidden', String(i !== 0)));
    ready.then(start);
  }

  // Keep captions and photo credits matched to the active slide.
  const heroSlides = findAll('.hero-slide');
  if (heroSlides.length) slideshow(heroSlides, {
    pause: find('#hero-pause'), tabs: findAll('.hero-thumb'),
    onChange(index) {
      const a = bySlug[heroSlides[index].dataset.slug];
      find('#hero-name').textContent = a.name;
      find('#hero-region').textContent = a.region;
      find('#hero-sub').textContent = `${a.scientific} · ${statusName(a)}`;
      find('#hero-feature').href = `/animals/${a.slug}-page.html`;
      find('#hero-index').textContent = String(index + 1).padStart(2, '0'); // Show a two-digit slide number, e.g. index 0 becomes 01.
    }
  });
  if (activeAnimal) {
    const a = bySlug[activeAnimal];
    slideshow(findAll('.photo-slide'), {
      pause: find('#gallery-pause'), next: find('#gallery-next'), previous: find('#gallery-prev'), progress: find('.gallery-progress'),
      onChange(index) {
        find('#gallery-index').textContent = String(index + 1).padStart(2, '0');
        const p = a.photos[index];
        const credit = find('#gallery-credit');
        credit.replaceChildren(document.createTextNode(`Photo: ${p.credit} · `));
        const link = document.createElement('a');
        link.href = p.source;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = `${p.license} ↗`;
        credit.append(link);
      }
    });
  }

  // Share the selected animal between map markers and the preview card.
  let selectedSlug = 'amur-leopard';
  function previewAnimal(a) {
    if (!find('#preview-image')) return;
    selectedSlug = a.slug;
    const photo = find('#preview-image');
    photo.src = a.photos[0].src;
    photo.alt = a.name;
    find('#preview-name').textContent = a.name;
    find('#preview-location').textContent = a.location;
    find('#preview-population').textContent = a.population;
    find('#preview-unit').textContent = a.unit;
    find('#preview-link').href = `/animals/${a.slug}-page.html`;
    const pill = find('#preview-status .pill'); // The small label showing endangered or critically endangered.
    pill.className = `pill ${a.status.toLowerCase()}`;
    pill.textContent = statusName(a);
    findAll('.map-pin').forEach(p => p.classList.toggle('selected', p.dataset.slug === a.slug));
  }
  const mapPanel = find('.map-panel');
  const map = mapPanel && find('.world-map', mapPanel);
  const tooltip = mapPanel && find('.map-tooltip', mapPanel);
  if (mapPanel && map && tooltip) {
    const pins = findAll('.map-pin', map);
    function showTooltip(pin) {
      const a = bySlug[pin.dataset.slug]; previewAnimal(a);
      tooltip.innerHTML = `<img src="${escapeText(a.photos[0].src)}" alt=""><span>${escapeText(a.name)}<small>${escapeText(a.region)} · View profile</small></span>`;
      tooltip.style.display = 'flex';
      const panel = mapPanel.getBoundingClientRect(); // Get the map panel's position and size in browser pixels.
      const point = find('.pin-core', pin).getBoundingClientRect();
      const half = tooltip.offsetWidth / 2; // Half the tooltip width lets us keep both edges inside the panel.
      tooltip.style.left = `${Math.min(panel.width - half - 8, Math.max(half + 8, point.x + point.width / 2 - panel.x))}px`;
      tooltip.style.top = `${Math.max(60, point.y - panel.y - 7)}px`;
    }
    pins.forEach(pin => {
      pin.addEventListener('mouseenter', () => showTooltip(pin));
      pin.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
      pin.addEventListener('focus', () => showTooltip(pin));
      pin.addEventListener('blur', () => { tooltip.style.display = 'none'; });
    });
    let zoom = 1, centerX = 500, centerY = 262.5, drag = null; // Start at normal scale with the map centred; drag is empty until a pointer press.
    // Clamp the viewBox so dragging stays inside the map bounds.
    function applyZoom() {
      const width = 1000 / zoom, height = 415 / zoom; // A smaller SVG viewing area makes the map look larger.
      centerX = Math.max(width / 2, Math.min(1000 - width / 2, centerX));
      centerY = Math.max(55 + height / 2, Math.min(470 - height / 2, centerY));
      map.setAttribute('viewBox', `${centerX-width/2} ${centerY-height/2} ${width} ${height}`);
      find('#zoom-in').disabled = zoom >= 2.5; find('#zoom-out').disabled = zoom <= 1;
      map.style.cursor = zoom > 1 ? 'grab' : '';
      tooltip.style.display = 'none';
    }
    find('#zoom-in').addEventListener('click', () => { zoom = Math.min(2.5, zoom + .5); applyZoom(); });
    find('#zoom-out').addEventListener('click', () => { zoom = Math.max(1, zoom - .5); applyZoom(); });
    find('#zoom-reset').addEventListener('click', () => { zoom = 1; centerX = 500; centerY = 262.5; applyZoom(); });
    map.addEventListener('pointerdown', event => {
      if (zoom <= 1 || event.target.closest('.map-pin')) return; // Drag only when zoomed in, and leave marker clicks free to open profiles.
      drag = {x:event.clientX, y:event.clientY, cx:centerX, cy:centerY}; // Remember where the pointer and map centre were when dragging began.
      map.setPointerCapture(event.pointerId); map.style.cursor = 'grabbing'; // Keep receiving pointer events even if the pointer leaves the map.
    });
    map.addEventListener('pointermove', event => {
      if (!drag) return;
      const box = map.getBoundingClientRect();
      centerX = drag.cx - (event.clientX - drag.x) / box.width * (1000 / zoom); // Convert the horizontal movement from screen pixels into SVG map units.
      centerY = drag.cy - (event.clientY - drag.y) / box.height * (415 / zoom);
      applyZoom();
    });
    const endDrag = () => { drag = null; if (zoom > 1) map.style.cursor = 'grab'; };
    map.addEventListener('pointerup', endDrag); map.addEventListener('pointercancel', endDrag);
    applyZoom();
  }

  let filter = 'All';
  const animalCards = findAll('.animal-card');
  const grid = find('.species-grid');
  function searchMatches(a, value) {
    return [a.name, a.scientific, a.region, a.location, a.habitat].join(' ').toLowerCase().includes(value.toLowerCase().trim());
  }
  // Apply the same region and search filters to cards and map markers.
  function filterSpecies() {
    const value = find('#species-search')?.value || '';
    const visible = animals.filter(a => (filter === 'All' || a.region === filter) && searchMatches(a, value));
    const ids = new Set(visible.map(a => a.slug)); // Store matching slugs in a Set for quick membership checks.
    animalCards.forEach(card => { card.hidden = !ids.has(card.dataset.slug); }); // Hide cards whose slugs are missing from the matching set.
    findAll('.map-panel .map-pin').forEach(pin => pin.classList.toggle('dimmed', !ids.has(pin.dataset.slug)));
    if (find('#species-count')) find('#species-count').textContent = String(visible.length).padStart(2, '0');
    if (find('.grid-empty')) find('.grid-empty').hidden = visible.length !== 0;
    if (visible.length && !ids.has(selectedSlug)) previewAnimal(visible[0]); // If the selected animal was filtered out, preview the first matching one.
    if (tooltip) tooltip.style.display = 'none';
  }
  findAll('.filter-button').forEach(button => button.addEventListener('click', () => {
    filter = button.dataset.filter;
    findAll('.filter-button').forEach(b => {
      b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button));
    });
    filterSpecies();
  }));
  find('#species-search')?.addEventListener('input', filterSpecies);
  find('#species-sort')?.addEventListener('change', event => {
    const mode = event.target.value;
    const cards = [...animalCards].sort((a, b) => { // Sort a copy so the original card array is still available.
      const x = bySlug[a.dataset.slug], y = bySlug[b.dataset.slug];
      if (mode === 'name') return x.name.localeCompare(y.name);
      if (mode === 'status') return x.status.localeCompare(y.status) || x.name.localeCompare(y.name); // CR sorts before EN; animals with the same status are sorted by name.
      return animals.indexOf(x) - animals.indexOf(y); // For featured order, use the order in the original animals list.
    });
    cards.forEach(card => grid.append(card)); // Move the existing cards into the new order; this does not create duplicates.
  });

  const menuToggle = find('.menu-toggle');
  const mobileNav = find('.mobile-nav');

  // Keep navigation visibility and accessibility labels in sync.
  function setMenu(open) {
    mobileNav.classList.toggle('open', open);
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  }
  menuToggle?.addEventListener('click', () => {
    setMenu(!mobileNav.classList.contains('open'));
  });
  findAll('.mobile-nav a').forEach(link => {
    link.addEventListener('click', () => setMenu(false));
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mobileNav?.classList.contains('open')) {
      setMenu(false);
      menuToggle.focus(); // Return keyboard focus to the menu button after Escape closes navigation.
    }
  });

  // Search all species from the shared navigation dialog.
  const dialog = find('.search-dialog'), search = find('#global-search');
  function renderSearch() {
    const matches = animals.filter(a => searchMatches(a, search.value));
    find('.search-results').innerHTML = matches.length ? matches.map(a => `<a class="search-result" href="/animals/${a.slug}-page.html"><img src="${escapeText(a.photos[0].src)}" alt=""><span>${escapeText(a.name)}<small>${escapeText(a.location)}</small></span><span style="margin-left:auto" aria-hidden="true">↗</span></a>`).join('') : '<p style="color:#7e8b70;font-size:12px">No matching animals. Enter another name or region.</p>';
  }
  findAll('.search-toggle').forEach(button => button.addEventListener('click', () => { dialog.showModal(); renderSearch(); search.focus(); }));
  find('.dialog-close')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
  search?.addEventListener('input', renderSearch);

  // Update matching fields and show the source-check status.
  function applyPopulation(record) {
    if (!record || !bySlug[record.slug]) return; // Ignore missing results or results for an animal this page does not know.
    const a = bySlug[record.slug];
    if (record.population) {
      a.population = record.population;
      findAll(`[data-population="${record.slug}"]`).forEach(el => { el.textContent = record.population; });
      if (selectedSlug === record.slug && find('#preview-population')) find('#preview-population').textContent = record.population;
    }
    if (record.estimate_date) findAll(`[data-estimate-date="${record.slug}"]`).forEach(el => { el.textContent = record.estimate_date; });
    findAll(`[data-check="${record.slug}"]`).forEach(el => {
      const time = record.checked_at ? new Intl.DateTimeFormat('en-GB', {day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(record.checked_at)) : '';
      const states = {
        verified: `Source checked ${time}${record.cached ? ' · cached check' : ''}`,
        unavailable: 'Saved estimate · source unavailable',
        review_required: 'Saved estimate · source needs review'
      };
      el.textContent = states[record.verification] || 'Saved published estimate';
      el.classList.toggle('verified', record.verification === 'verified');
      el.title = record.message || '';
    });
  }
  // Request one species or all sources, with a 35-second browser timeout.
  async function fetchPopulation(slug, force = false) {
    const parameters = new URLSearchParams(); // Build the query string safely, e.g. species=tiger&refresh=1.
    if (slug) parameters.set('species', slug);
    if (force) parameters.set('refresh', '1');
    const response = await fetch(`/api/populations?${parameters}`, {headers:{'Accept':'application/json'}, signal:AbortSignal.timeout(35000)});
    if (!response.ok) throw new Error('Source check unavailable');
    const data = await response.json(); // Turn the server's JSON response into a JavaScript object.
    if (!Array.isArray(data.records)) throw new Error('Unexpected data response');
    data.records.forEach(applyPopulation); // Send each returned animal record to the function that updates the page.
    return data.records;
  }
  // Disable refresh controls while their source checks are running.
  findAll('[data-refresh]').forEach(button => button.addEventListener('click', async () => {
    button.disabled = true; button.classList.add('busy'); const span = find('span', button); span.textContent = 'Checking source…';
    try {
      const records = await fetchPopulation(button.dataset.refresh, true);
      const verified = records[0]?.verification === 'verified'; // Check the first returned record; ?. also handles an empty results list.
      toast(verified ? 'Source checked. The published estimate is displayed.' : 'Source verification failed. The saved estimate remains visible.');
    } catch (_) { toast('Source check unavailable. The saved estimate remains visible.'); }
    finally { button.disabled = false; button.classList.remove('busy'); span.textContent = 'Check this source'; } // Restore the refresh button whether the check succeeds or fails.
  }));
  find('#refresh-all')?.addEventListener('click', async event => {
    const button = event.currentTarget; button.disabled = true; find('span',button).textContent = 'Checking sources…';
    const summary = find('#refresh-summary');
    summary.textContent = `Checking ${animals.length} linked sources…`;
    try {
      const records = await fetchPopulation(null, true);
      const count = records.filter(r => r.verification === 'verified').length;
      summary.textContent = `${count} of ${animals.length} linked sources verified. ${animals.length-count ? 'Other records retain their saved estimates; their source status is shown below.' : 'Dates and counting methods remain attached to each record.'}`;
    } catch (_) { summary.textContent = 'The source check is unavailable. All saved estimates and original source links remain available.'; }
    finally { button.disabled = false; find('span',button).textContent = 'Check all sources'; }
  });
  // Check sources after the page loads; failures leave the displayed figures.
  if (activeAnimal) setTimeout(() => fetchPopulation(activeAnimal).catch(() => {}), 900);
  else if (page === 'home') setTimeout(() => fetchPopulation().catch(() => {}), 1800);
})();
