/* ============================================================
   OlympicsAnalytics — main.js
   Global interactions: navbar scroll, counter animation,
   active nav links, smooth scroll helpers
   ============================================================ */

(function () {
  'use strict';

  /* ── 1. Navbar scroll effect ─────────────────────────────── */
  const navbar = document.getElementById('mainNav');
  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // run once on load
  }

  /* ── 2. Counter animation ────────────────────────────────── */
  const counters = document.querySelectorAll('.counter');

  const formatNumber = (n) => {
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000)    return Math.round(n).toLocaleString();
    return Math.round(n).toString();
  };

  const animateCounter = (el) => {
    const target = parseInt(el.getAttribute('data-target'), 10);
    if (isNaN(target) || target === 0) return;

    const duration = 1800; // ms
    const startTime = performance.now();

    const tick = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = formatNumber(Math.floor(eased * target));
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  // Trigger counters when they enter the viewport
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );
    counters.forEach((c) => observer.observe(c));
  } else {
    // Fallback: run immediately
    counters.forEach(animateCounter);
  }

  /* ── 3. Smooth scroll for anchor links ───────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const navbarHeight = navbar ? navbar.offsetHeight : 0;
        const targetY = target.getBoundingClientRect().top + window.scrollY - navbarHeight - 16;
        window.scrollTo({ top: targetY, behavior: 'smooth' });
      }
    });
  });

  /* ── 4. Fade-in animation (simple AOS-lite) ─────────────── */
  const fadeEls = document.querySelectorAll('[data-aos]');
  if (fadeEls.length && 'IntersectionObserver' in window) {
    // Inject minimal animation styles
    const style = document.createElement('style');
    style.textContent = `
      [data-aos] { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
      [data-aos].aos-in { opacity: 1; transform: translateY(0); }
      [data-aos="fade-left"]  { transform: translateX(24px); }
      [data-aos="fade-right"] { transform: translateX(-24px); }
      [data-aos="fade-left"].aos-in, [data-aos="fade-right"].aos-in { transform: translateX(0); }
    `;
    document.head.appendChild(style);

    const aosObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const delay = entry.target.getAttribute('data-aos-delay') || 0;
            setTimeout(() => entry.target.classList.add('aos-in'), parseInt(delay));
            aosObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    fadeEls.forEach((el) => aosObserver.observe(el));
  } else {
    // Fallback: show everything
    fadeEls.forEach((el) => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }

  /* ── 5. Active nav-link highlight based on current path ─── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('#mainNav .nav-link').forEach((link) => {
    const href = link.getAttribute('href');
    if (href && currentPath === href) {
      link.classList.add('active');
    }
  });

  /* ── 6. Collapse mobile nav on link click ────────────────── */
  document.querySelectorAll('#navbarMain .nav-link').forEach((link) => {
    link.addEventListener('click', () => {
      const collapse = document.getElementById('navbarMain');
      if (collapse && collapse.classList.contains('show')) {
        const bsCollapse = bootstrap.Collapse.getInstance(collapse);
        if (bsCollapse) bsCollapse.hide();
      }
    });
  });

  /* ── 7. Tooltip initialisation (Bootstrap) ───────────────── */
  const tooltipTriggers = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggers.forEach((el) => new bootstrap.Tooltip(el));

  /* ── 8. Global error boundary for fetch ─────────────────── */
  window.handleFetchError = (err, chartId) => {
    console.warn(`Chart ${chartId}: API unavailable —`, err.message || err);
    const canvas = document.getElementById(chartId);
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = 'rgba(255,255,255,0.15)';
      ctx.font = '13px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Data unavailable', canvas.width / 2, canvas.height / 2);
    }
  };

})();
