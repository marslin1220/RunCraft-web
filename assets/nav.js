/* Nav behaviour shared by every page: globe language menu + mobile drawer.
   The drawer is cloned from .navlinks at runtime so each page keeps exactly
   one copy of its section links in the markup. */
(function () {
  var nav = document.querySelector("nav");
  if (!nav) return;

  var langBtn = nav.querySelector(".langbtn");
  var langMenu = nav.querySelector(".langmenu");
  var menuBtn = nav.querySelector(".menubtn");
  var links = nav.querySelector(".navlinks");

  // Remember the reader's choice so the root page can redirect next visit.
  Array.prototype.forEach.call(nav.querySelectorAll("a[data-lang]"), function (a) {
    a.addEventListener("click", function () {
      try { localStorage.setItem("rc-lang", a.getAttribute("data-lang")); } catch (e) {}
    });
  });

  var drawer = null;
  if (links) {
    drawer = document.createElement("div");
    drawer.className = "drawer";
    var panel = document.createElement("div");
    panel.className = "drawerpanel";
    // The nav sits under the scrim, so the drawer carries its own close control.
    var close = document.createElement("button");
    close.type = "button";
    close.className = "drawerclose";
    close.setAttribute("aria-label", menuBtn ? menuBtn.getAttribute("aria-label") : "Close");
    close.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="1.8" stroke-linecap="round" aria-hidden="true">' +
      '<path d="M6 6l12 12M18 6L6 18"/></svg>';
    close.addEventListener("click", function () { setDrawer(false); });
    panel.appendChild(close);
    panel.appendChild(links.cloneNode(true));
    drawer.appendChild(panel);
    document.body.appendChild(drawer);
  }

  function setLang(open) {
    if (!langMenu) return;
    langMenu.hidden = !open;
    langBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("noscroll", open);
    document.documentElement.classList.toggle("noscroll", open);
  }

  if (langBtn) {
    langBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = langMenu.hidden;
      setDrawer(false);
      setLang(open);
    });
  }

  if (menuBtn) {
    menuBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !drawer.classList.contains("open");
      setLang(false);
      setDrawer(open);
    });
  }

  if (drawer) {
    // Tapping the scrim closes; tapping a link closes and lets it navigate.
    drawer.addEventListener("click", function (e) {
      if (e.target === drawer || e.target.tagName === "A") setDrawer(false);
    });
  }

  document.addEventListener("click", function (e) {
    if (langMenu && !langMenu.hidden && !langMenu.contains(e.target)) setLang(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { setLang(false); setDrawer(false); }
  });

  // A resize past the breakpoint can leave the drawer open with no way out.
  window.addEventListener("resize", function () {
    if (window.innerWidth > 860) setDrawer(false);
  });
})();
