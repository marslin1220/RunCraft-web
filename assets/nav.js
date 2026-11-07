/* Shared language disclosure and accessible mobile navigation. */
(function () {
  var nav = document.querySelector('nav');
  if (!nav) return;
  var langBtn = nav.querySelector('.langbtn');
  var langMenu = nav.querySelector('.langmenu');
  var menuBtn = nav.querySelector('.menubtn');
  var links = nav.querySelector('.navlinks');
  var drawer, closeButton, previousInert = [];
  var closeLabels = { en: 'Close menu', 'zh-Hant': '關閉選單', 'zh-Hans': '关闭菜单', ja: 'メニューを閉じる', ko: '메뉴 닫기' };

  nav.querySelectorAll('a[data-lang]').forEach(function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('rc-lang', a.getAttribute('data-lang')); } catch (e) {}
    });
  });

  if (langBtn && langMenu) {
    langMenu.id = langMenu.id || 'languages';
    langBtn.setAttribute('aria-controls', langMenu.id);
    // This is an ordinary disclosure of links, not an ARIA menu widget.
    langBtn.removeAttribute('aria-haspopup');
  }

  if (links && menuBtn) {
    drawer = document.createElement('div');
    drawer.id = 'mobile-navigation';
    drawer.className = 'drawer';
    drawer.hidden = true;
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('aria-label', menuBtn.getAttribute('aria-label'));
    menuBtn.setAttribute('aria-controls', drawer.id);
    var panel = document.createElement('div');
    panel.className = 'drawerpanel';
    closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'drawerclose';
    closeButton.setAttribute('aria-label', menuBtn.dataset.closeLabel || closeLabels[document.documentElement.lang] || closeLabels.en);
    closeButton.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    closeButton.addEventListener('click', function () { setDrawer(false); });
    panel.appendChild(closeButton);
    var clonedLinks = links.cloneNode(true);
    clonedLinks.querySelectorAll('[id]').forEach(function (element) { element.removeAttribute('id'); });
    panel.appendChild(clonedLinks);
    drawer.appendChild(panel);
    document.body.appendChild(drawer);
  }

  function setLang(open, restoreFocus) {
    if (!langMenu || !langBtn) return;
    var wasOpen = !langMenu.hidden;
    langMenu.hidden = !open;
    langBtn.setAttribute('aria-expanded', String(open));
    if (wasOpen && !open && restoreFocus) langBtn.focus();
  }

  function setDrawer(open, restoreFocus) {
    if (!drawer || drawer.hidden === !open) return;
    drawer.hidden = !open;
    drawer.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('noscroll', open);
    document.documentElement.classList.toggle('noscroll', open);
    if (open) {
      previousInert = [];
      Array.prototype.forEach.call(document.body.children, function (element) {
        if (element === drawer || element.tagName === 'SCRIPT') return;
        previousInert.push([element, element.inert]);
        element.inert = true;
      });
      closeButton.focus();
    } else {
      previousInert.forEach(function (entry) { entry[0].inert = entry[1]; });
      previousInert = [];
      if (restoreFocus !== false) menuBtn.focus();
    }
  }

  if (langBtn && langMenu) langBtn.addEventListener('click', function (event) {
    event.stopPropagation();
    setDrawer(false, false);
    setLang(langMenu.hidden);
  });

  if (menuBtn && drawer) menuBtn.addEventListener('click', function () {
    setLang(false);
    setDrawer(drawer.hidden);
  });

  if (drawer) drawer.addEventListener('click', function (event) {
    var link = event.target.closest('a');
    if (event.target === drawer) setDrawer(false);
    else if (link) {
      setDrawer(false, false);
      var url = new URL(link.href);
      if (url.pathname === location.pathname && url.hash) {
        var target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
        if (target) {
          target.setAttribute('tabindex', '-1');
          target.focus({ preventScroll: true });
        }
      }
    }
  });

  document.addEventListener('click', function (event) {
    if (langMenu && !langMenu.hidden && !langMenu.contains(event.target) && event.target !== langBtn) setLang(false);
  });

  document.addEventListener('focusin', function (event) {
    if (langMenu && !langMenu.hidden && !langMenu.contains(event.target) && event.target !== langBtn) setLang(false);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      setLang(false, true);
      setDrawer(false);
    }
    if (event.key === 'Tab' && drawer && !drawer.hidden) {
      var focusable = drawer.querySelectorAll('button, a[href]');
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 860 && drawer && !drawer.hidden) {
      setDrawer(false, false);
      nav.querySelector('.brand').focus();
    }
  });
})();
