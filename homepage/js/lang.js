/* Workday Wake — language negotiation.
 * First visit only: redirect to the best language for the browser, with
 * English as fallback. A choice made here or via the language switch is
 * remembered; returning visitors are never redirected away from the page
 * they picked. URLs are content pages; text stays in the HTML (SEO-safe).
 */
(function () {
  'use strict';
  var KEY = 'ww-lang';

  function pageLang() {
    return document.documentElement.lang || 'en';
  }

  function norm(tag) {
    tag = (tag || '').toLowerCase();
    if (tag.indexOf('zh') === 0) {
      // Simplified vs Traditional: treat anything not explicitly Hant/HK/TW/MO as Hans
      return /hant|hk|tw|mo/.test(tag) ? null : 'zh-Hans';
    }
    if (tag.indexOf('de') === 0) return 'de';
    if (tag.indexOf('es') === 0) return 'es-419';
    if (tag.indexOf('fr') === 0) return 'fr';
    if (tag.indexOf('pt') === 0) return 'pt-BR';
    if (tag.indexOf('ja') === 0) return 'ja';
    if (tag.indexOf('en') === 0) return 'en';
    return null;
  }

  function bestFromNavigator() {
    var cands = [];
    if (navigator.languages) cands = cands.concat(navigator.languages);
    if (navigator.language) cands.push(navigator.language);
    for (var i = 0; i < cands.length; i++) {
      var m = norm(cands[i]);
      if (m) return m;
    }
    return null;
  }

  var current = pageLang();
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) { /* storage blocked */ }

  // Remember the page the visitor is on (also covers clicks on the switch).
  if (stored !== current) {
    try { localStorage.setItem(KEY, current); } catch (e) { /* ignore */ }
  }

  // Redirect only on first-ever visit, only from the EN default entry page,
  // and only when the browser prefers a language we actually have.
  if (stored === null && current === 'en') {
    var best = bestFromNavigator();
    var targets = {
      'de': 'de/index.html',
      'zh-Hans': 'zh-hans/index.html',
      'es-419': 'es-419/index.html',
      'fr': 'fr/index.html',
      'pt-BR': 'pt-br/index.html',
      'ja': 'ja/index.html'
    };
    if (best && targets[best] && document.body) {
      try { localStorage.setItem(KEY, best); } catch (e) { /* ignore */ }
      location.replace(targets[best]);
    }
  }
})();
