/* =========================================================
   CLUB AURORA — interactions
   ========================================================= */
(() => {
  'use strict';

  /* ---- enable JS-only enhancements (reveal hides only when JS present) ---- */
  document.documentElement.classList.add('js');

  /* ---- header scrolled state ---- */
  const header = document.getElementById('siteHeader');
  const onScroll = () => {
    if (!header) return;
    header.classList.toggle('scrolled', window.scrollY > 40);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- mobile nav ---- */
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('mainNav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => document.body.classList.toggle('nav-open'));
    nav.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => document.body.classList.remove('nav-open')));
  }

  /* ---- reveal on scroll ---- */
  const reveals = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(el => io.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('in'));
  }

  /* ---- progressively enhance with real images when present ---- */
  // Hero still is set directly in CSS; just hide the CSS fallback scene.
  document.querySelector('.hero__scene')?.style.setProperty('display', 'none');

  // Hero video rotation: play each clip once, then crossfade to the next (cycle).
  const clips = Array.from(document.querySelectorAll('.hero__video'));
  if (clips.length && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let cur = -1;
    const playClip = (i) => {
      cur = i;
      const v = clips[i];
      try { v.currentTime = 0; } catch (e) {}
      clips.forEach((c, idx) => c.classList.toggle('on', idx === i));
      v.play?.().catch(() => {});
    };
    clips.forEach((v, i) => {
      v.addEventListener('ended', () => playClip((i + 1) % clips.length));
      v.addEventListener('error', () => { if (i === cur) playClip((i + 1) % clips.length); });
    });
    const start = () => { if (cur === -1) playClip(0); };
    if (clips[0].readyState >= 3) start();
    else {
      clips[0].addEventListener('canplay', start, { once: true });
      clips[0].addEventListener('loadeddata', start, { once: true });
    }
  } else if (clips.length) {
    clips[0].classList.add('on'); // reduced motion: hold first clip's still
  }
  // Any element flagged with data-img -> set as background when the file loads
  document.querySelectorAll('[data-img]').forEach(el => {
    const src = el.getAttribute('data-img');
    if (!src) return;
    const probe = new Image();
    probe.onload = () => { el.style.backgroundImage = `url('${src}')`; };
    probe.src = src;
  });

  /* ---- gentle parallax on hero photo ---- */
  const hp = document.getElementById('heroPhoto');
  if (hp && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    window.addEventListener('scroll', () => {
      const y = Math.min(window.scrollY, 700);
      hp.style.transform = `translateY(${y * 0.12}px) scale(1.04)`;
    }, { passive: true });
  }

  /* ---- active nav link by current file ---- */
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.main-nav a').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (href === page) a.classList.add('active');
  });
})();
