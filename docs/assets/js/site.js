/* OSK-Keyboard site — language switch, size demo, copy buttons, reveal */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------------- language ---------------- */
  var KEY = 'osk-lang';
  var lang = 'zh';
  try { if (localStorage.getItem(KEY) === 'en') lang = 'en'; } catch (e) {}

  var nodes = $$('[data-en],[data-en-html]').map(function (el) {
    if (el.hasAttribute('data-en-html')) {
      if (!el.hasAttribute('data-zh-html')) el.setAttribute('data-zh-html', el.innerHTML);
    } else if (!el.hasAttribute('data-zh')) {
      el.setAttribute('data-zh', el.textContent);
    }
    return el;
  });

  function applyLang() {
    var en = lang === 'en';
    document.documentElement.setAttribute('lang', en ? 'en' : 'zh-CN');

    nodes.forEach(function (el) {
      if (el.hasAttribute('data-en-html')) {
        el.innerHTML = en ? el.getAttribute('data-en-html') : el.getAttribute('data-zh-html');
      } else {
        el.textContent = en ? el.getAttribute('data-en') : el.getAttribute('data-zh');
      }
    });

    var toggle = $('[data-lang-toggle]');
    if (toggle) {
      toggle.textContent = en ? '中文' : 'EN';
      toggle.setAttribute('aria-label', en ? '切换为中文' : 'Switch to English');
      toggle.setAttribute('lang', en ? 'zh-CN' : 'en');
    }

    var body = document.body;
    if (body.dataset.titleZh && body.dataset.titleEn) {
      document.title = en ? body.dataset.titleEn : body.dataset.titleZh;
    }

    document.dispatchEvent(new CustomEvent('langchange', { detail: { lang: lang } }));
  }

  var toggleBtn = $('[data-lang-toggle]');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      lang = lang === 'en' ? 'zh' : 'en';
      try { localStorage.setItem(KEY, lang); } catch (e) {}
      applyLang();
    });
  }

  /* ---------------- header shadow ---------------- */
  var header = $('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------------- sticky-nav offset for anchors ---------------- */
  (function () {
    if (!('scrollMarginTop' in document.documentElement.style)) return;
    $$('section[id]').forEach(function (sec) { sec.style.scrollMarginTop = '78px'; });
  })();

  /* ---------------- size demo ---------------- */
  var SIZES = {
    small:  { zh: '小', en: 'Small',  scale: '0.72', keyw: '46', panel: '927×349',   share: 55 },
    medium: { zh: '中', en: 'Medium', scale: '0.85', keyw: '54', panel: '1120×421',  share: 66 },
    large:  { zh: '大', en: 'Large',  scale: '0.99', keyw: '63', panel: '1295×491',  share: 76 }
  };
  var current = 'medium';
  var segs = $$('[data-size]');
  var imgs = $$('[data-size-img]');

  function fill(name, value, unit) {
    $$('[data-size-val="' + name + '"]').forEach(function (el) {
      el.textContent = value;
      if (unit) {
        var u = document.createElement('span');
        u.className = 'u';
        u.textContent = unit;
        el.appendChild(u);
      }
    });
  }

  function renderSize() {
    var s = SIZES[current];
    if (!s) return;
    imgs.forEach(function (img) { img.hidden = img.getAttribute('data-size-img') !== current; });
    segs.forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-size') === current)); });
    fill('name', lang === 'en' ? s.en : s.zh);
    fill('scale', s.scale);
    fill('keyw', s.keyw, 'px');
    fill('panel', s.panel, '· ' + s.share + ' %');
  }

  segs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      current = btn.getAttribute('data-size');
      renderSize();
    });
  });

  document.addEventListener('langchange', renderSize);
  if (segs.length) renderSize();

  /* ---------------- copy buttons ---------------- */
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); resolve(); } catch (err) { reject(err); }
      document.body.removeChild(ta);
    });
  }

  $$('.copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = $('pre', btn.parentNode);
      if (!code) return;
      copyText(code.innerText.replace(/\s+$/, '')).then(function () {
        btn.classList.add('done');
        setTimeout(function () { btn.classList.remove('done'); }, 1500);
      }).catch(function () {});
    });
  });

  /* ---------------- reveal on scroll ---------------- */
  var revealEls = $$('.reveal');
  revealEls.forEach(function (el) { el.classList.add('is-hidden'); });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------------- hero typewriter ---------------- */
  function typewriteHero() {
    var h1 = $('[data-typewriter]');
    if (!h1) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (h1.getAttribute('data-typing') === '1') return;
    h1.setAttribute('data-typing', '1');

    var chars = [];
    var walker = document.createTreeWalker(h1, NodeFilter.SHOW_TEXT, null);
    var textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);

    textNodes.forEach(function (node) {
      var frag = document.createDocumentFragment();
      var text = node.nodeValue;
      for (var i = 0; i < text.length; i++) {
        var ch = text.charAt(i);
        if (/\s/.test(ch)) { frag.appendChild(document.createTextNode(ch)); continue; }
        var s = document.createElement('span');
        s.className = 'tw-ch';
        s.textContent = ch;
        frag.appendChild(s);
        chars.push(s);
      }
      node.parentNode.replaceChild(frag, node);
    });
    if (!chars.length) return;

    var caret = document.createElement('span');
    caret.className = 'tw-caret';
    caret.setAttribute('aria-hidden', 'true');

    var idx = 0;
    function step() {
      if (idx >= chars.length) {
        setTimeout(function () { if (caret.parentNode) caret.parentNode.removeChild(caret); }, 1500);
        return;
      }
      var ch = chars[idx++];
      ch.classList.add('on');
      ch.parentNode.insertBefore(caret, ch.nextSibling);
      setTimeout(step, 42);
    }
    setTimeout(step, 240);
  }

  document.addEventListener('langchange', function () {
    var h1 = $('[data-typewriter]');
    if (h1) h1.removeAttribute('data-typing');
    typewriteHero();
  });

  /* ---------------- boot ---------------- */
  applyLang();
})();
