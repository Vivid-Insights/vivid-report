/* Vivid Insights research report: the little the page does at runtime.
   Theme toggle, contents highlighting, citation previews, maths, copy BibTeX, print.
   Everything degrades: without this script the report still reads in full. */
(function () {
  "use strict";
  var root = document.documentElement;

  /* theme */
  var themeBtn = document.querySelector("[data-vr-theme]");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var cur = root.getAttribute("data-theme") ||
      (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    var next = cur === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("vr-theme", next); } catch (e) {}
    notifyFrames(next);
  });
  /* interactive figures can follow the page theme by listening for this message */
  function notifyFrames(theme) {
    document.querySelectorAll(".vr-interactive iframe").forEach(function (f) {
      try { f.contentWindow.postMessage({ vividTheme: theme }, "*"); } catch (e) {}
    });
  }
  document.querySelectorAll(".vr-interactive iframe").forEach(function (f) {
    f.addEventListener("load", function () {
      var t = root.getAttribute("data-theme") ||
        (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      try { f.contentWindow.postMessage({ vividTheme: t }, "*"); } catch (e) {}
    });
  });

  /* print */
  var printBtn = document.querySelector("[data-vr-print]");
  if (printBtn) printBtn.addEventListener("click", function () { window.print(); });

  /* copy BibTeX */
  var copyBtn = document.querySelector("[data-vr-copy]");
  if (copyBtn) copyBtn.addEventListener("click", function () {
    var text = copyBtn.parentNode.querySelector("pre").textContent;
    var done = function () { copyBtn.textContent = "Copied"; setTimeout(function () { copyBtn.textContent = "Copy BibTeX"; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
  });

  /* maths: KaTeX is only loaded when the report has any */
  function renderMath() {
    if (!window.katex) return;
    document.querySelectorAll(".vr-tex").forEach(function (el) {
      try { katex.render(el.textContent, el, { displayMode: true, throwOnError: false }); } catch (e) {}
    });
    document.querySelectorAll(".math.inline").forEach(function (el) {
      try { katex.render(el.textContent, el, { displayMode: false, throwOnError: false }); } catch (e) {}
    });
  }
  if (document.querySelector(".vr-tex, .math.inline")) {
    if (window.katex) renderMath(); else window.addEventListener("load", renderMath);
  }

  /* contents: highlight the section being read */
  var links = Array.prototype.slice.call(document.querySelectorAll(".vr-toc a"));
  if (links.length && "IntersectionObserver" in window) {
    var byId = {};
    links.forEach(function (a) { byId[decodeURIComponent(a.getAttribute("href").slice(1))] = a; });
    var heads = Array.prototype.slice.call(document.querySelectorAll(".vr-body h2[id], .vr-body h3[id]"));
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
      var current = null;
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].getBoundingClientRect().top < window.innerHeight * 0.35) current = heads[i].id;
      }
      links.forEach(function (a) { a.classList.remove("active"); });
      if (current && byId[current]) byId[current].classList.add("active");
    }, { rootMargin: "0px 0px -60% 0px" });
    heads.forEach(function (h) { io.observe(h); });
  }

  /* citation previews: hover or focus a citation to see the reference */
  var pop = null;
  function hide() { if (pop) { pop.remove(); pop = null; } }
  function show(a) {
    hide();
    var ref = document.getElementById("ref-" + a.getAttribute("data-key"));
    if (!ref) return;
    pop = document.createElement("div");
    pop.className = "vr-pop";
    pop.innerHTML = ref.innerHTML;
    document.body.appendChild(pop);
    var r = a.getBoundingClientRect();
    var left = Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - pop.offsetWidth - 12);
    pop.style.left = Math.max(12, left) + "px";
    pop.style.top = (window.scrollY + r.bottom + 8) + "px";
  }
  document.querySelectorAll(".vr-cite").forEach(function (a) {
    a.addEventListener("mouseenter", function () { show(a); });
    a.addEventListener("focus", function () { show(a); });
    a.addEventListener("mouseleave", function () { setTimeout(function () { if (pop && !pop.matches(":hover")) hide(); }, 120); });
    a.addEventListener("blur", hide);
  });
  document.addEventListener("mouseover", function (e) {
    if (pop && !pop.contains(e.target) && !(e.target.closest && e.target.closest(".vr-cite"))) hide();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") hide(); });
})();
