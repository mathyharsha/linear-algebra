(() => {
  const $ = (selector) => document.querySelector(selector);
  const theme = $('#theme-button');
  theme?.addEventListener('click', () => {
    const isDark = document.documentElement.dataset.theme === 'dark';
    if (isDark) delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = 'dark';
    try { localStorage.setItem('matrix-notes-theme', isDark ? 'light' : 'dark'); } catch (e) { /* local preview */ }
  });
  const menu = $('#menu-button');
  menu?.addEventListener('click', () => {
    const open = $('#mobile-nav')?.classList.toggle('open') ?? false;
    menu.setAttribute('aria-expanded', String(open));
  });
  $('#mobile-nav')?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    $('#mobile-nav')?.classList.remove('open');
    menu?.setAttribute('aria-expanded', 'false');
  }));
  const tocButton = $('#toc-collapse');
  tocButton?.addEventListener('click', () => {
    let collapsed = $('#chapter-sidebar .toc-list')?.classList.toggle('collapsed');
    tocButton.setAttribute('aria-expanded', String(!collapsed));
  });
  const progress = $('#reading-progress');
  const setProgress = () => {
    if (!progress) return;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    progress.style.width = Math.min(100, Math.max(0, scrollY / max * 100)) + '%';
  };
  addEventListener('scroll', setProgress, { passive:true });
  addEventListener('resize', setProgress, { passive:true });
  setProgress();
  const sectionLinks = [...document.querySelectorAll('.toc-link')];
  const headings = sectionLinks.map(a => document.getElementById(a.hash.slice(1))).filter(Boolean);
  if (headings.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const hits = entries.filter(e => e.isIntersecting).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (hits.length) {
        sectionLinks.forEach(a => a.classList.toggle('active', a.hash === '#' + hits[0].target.id));
      }
    }, {rootMargin:'-105px 0px -68% 0px', threshold:0});
    headings.forEach(h=>observer.observe(h));
  }
  const modal = $('#search-modal');
  const input = $('#search-input');
  const results = $('#search-results');
  const index = window.NOTES_SEARCH_INDEX || [];
  let oldFocus = null;
  const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const getBase = () => document.body.dataset.chapter === 'home' ? '' : '../';
  function search(query) {
    const term = query.trim().toLowerCase();
    if (!results) return;
    if (!term) { results.innerHTML = '<p>Type a term to search the chapters and section headings.</p>'; return; }
    const tokens = term.split(/\s+/).filter(Boolean);
    const found = index.map((entry) => {
      const t = `${entry.title} ${entry.keywords || ''}`.toLowerCase();
      const d = (entry.description || '').toLowerCase();
      const score = tokens.every(x => t.includes(x) || d.includes(x))
        ? tokens.reduce((s,x) => s + (entry.title.toLowerCase().includes(x) ? 6 : 0) + (t.includes(x) ? 2 : 0) + (d.includes(x) ? 1 : 0),0)
        : 0;
      return {...entry, score};
    }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,12);
    results.innerHTML = `<p class="search-count">${found.length} MATCH${found.length === 1 ? '' : 'ES'}</p>` +
      (found.length ? found.map(entry => `<a href="${getBase()}${encodeURI(entry.href)}"><strong>${escapeHTML(entry.title)}</strong><small>${escapeHTML(entry.description)}</small></a>`).join('') : '<p>No matching headings found. Try a broader term.</p>');
  }
  const openSearch = () => {
    if (!modal || !modal.hidden) return;
    oldFocus = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    input?.focus();
    search(input?.value || '');
  };
  const closeSearch = () => {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    document.body.style.overflow = '';
    oldFocus?.focus?.();
  };
  $('#search-button')?.addEventListener('click', openSearch);
  modal?.querySelectorAll('[data-close-search]').forEach(el=>el.addEventListener('click',closeSearch));
  input?.addEventListener('input', () => search(input.value));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSearch();
    if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey &&
      !['INPUT','TEXTAREA'].includes(document.activeElement?.tagName) && !document.activeElement?.isContentEditable) {
      e.preventDefault();openSearch();
    }
  });
  document.addEventListener('click', e => {
    const number = e.target.closest?.('.eq-number');
    if (!number) return;
    // Link itself is functional without JS; do not hijack navigation.
  });
})();
