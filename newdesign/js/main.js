/* University of Karachi — homepage interactions (vanilla JS) */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Sticky header shadow on scroll ---- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Mobile nav toggle ---- */
  var toggle = document.querySelector(".nav-toggle");
  var navLinks = document.querySelector(".nav-links");
  var backdrop = document.querySelector(".nav-backdrop");
  function closeNav() {
    if (!navLinks) return;
    navLinks.classList.remove("open");
    if (backdrop) backdrop.classList.remove("open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }
  function openNav() {
    navLinks.classList.add("open");
    if (backdrop) backdrop.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }
  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      open ? closeNav() : openNav();
    });
  }
  if (backdrop) backdrop.addEventListener("click", closeNav);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeNav();
  });

  /* ---- Dropdown panels (click / keyboard friendly, works on touch) ---- */
  var isMobile = function () { return window.matchMedia("(max-width: 1080px)").matches; };
  document.querySelectorAll(".nav-item.has-panel").forEach(function (item) {
    var btn = item.querySelector(".nav-link");
    var panel = item.querySelector(".nav-panel");
    if (!btn || !panel) return;
    btn.setAttribute("aria-expanded", "false");
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var open = btn.getAttribute("aria-expanded") === "true";
      // close siblings
      document.querySelectorAll(".nav-item.has-panel .nav-link").forEach(function (b) {
        if (b !== btn) { b.setAttribute("aria-expanded", "false"); b.parentElement.querySelector(".nav-panel").classList.remove("open"); }
      });
      btn.setAttribute("aria-expanded", String(!open));
      panel.classList.toggle("open", !open);
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav-item.has-panel") && !isMobile()) {
      document.querySelectorAll(".nav-item.has-panel .nav-link").forEach(function (b) {
        b.setAttribute("aria-expanded", "false");
        b.parentElement.querySelector(".nav-panel").classList.remove("open");
      });
    }
  });

  /* ---- Scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---- Count-up stats ---- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var decimals = (el.getAttribute("data-decimals") | 0);
    var dur = 1600;
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = target * eased;
      el.textContent = val.toLocaleString("en-US", {
        minimumFractionDigits: decimals, maximumFractionDigits: decimals
      });
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll("[data-count]");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    counters.forEach(function (el) {
      var d = (el.getAttribute("data-decimals") | 0);
      el.textContent = parseFloat(el.getAttribute("data-count")).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
    });
  } else {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { animateCount(entry.target); co.unobserve(entry.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* ---- Footer year ---- */
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();
