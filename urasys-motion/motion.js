// Urasys × Pera PDKS — hareket yardımcıları (bağımlılık yok)
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Logo intro: harfleri ayır ve oynat
  const intro = $('#intro');
  const word = $('.wordmark', intro);
  word.innerHTML =
    [...'urasys'].map((c, i) => `<span class="ch" style="--i:${i}">${c}</span>`).join('') +
    '<span class="dot">.</span>';
  const playIntro = () => {
    intro.classList.remove('play');
    void intro.offsetWidth; // animasyonu sıfırla
    intro.classList.add('play');
  };
  $('#replay-intro').addEventListener('click', playIntro);

  // Scroll-reveal + sayaç + panel canlandırma
  const countUp = (el) => {
    const end = +el.dataset.to, suffix = el.dataset.suffix || '', dur = 1400, t0 = performance.now();
    const tick = (t) => {
      const p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))).toLocaleString('tr-TR') + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      $$('[data-to]', e.target).forEach(countUp);
      if (e.target.matches('#intro')) playIntro();
      if (e.target.matches('.dash')) e.target.classList.add('live');
      io.unobserve(e.target);
    });
  }, { threshold: 0.25 });
  $$('.reveal, .dash, #intro').forEach((el) => io.observe(el));

  // Kartlarda imleci izleyen ışık
  $$('.card').forEach((card) =>
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', e.clientX - r.left + 'px');
      card.style.setProperty('--my', e.clientY - r.top + 'px');
    })
  );
  $('#replay-dash').addEventListener('click', () => {
    const d = $('.dash');
    d.classList.remove('live');
    void d.offsetWidth;
    d.classList.add('live');
  });

  // Sosyal medya sahneleri: zaman çizelgesi
  const stage = $('#social');
  const scenes = $$('.scene', stage);
  const bar = $('.progress', stage);
  bar.innerHTML = scenes.map(() => '<i></i>').join('');
  const segs = $$('i', bar);
  const DUR = [3200, 4200, 3800, 3200];
  let idx = -1, timer;
  const show = (n) => {
    clearTimeout(timer);
    scenes.forEach((s, i) => {
      s.classList.remove('active', 'leaving');
      if (i === idx && n !== idx) s.classList.add('leaving');
    });
    idx = n;
    scenes[idx].classList.add('active');
    segs.forEach((s, i) => {
      s.className = i < idx ? 'done' : i === idx ? 'cur start' : '';
    });
    stage.style.setProperty('--scene-dur', DUR[idx] + 'ms');
    requestAnimationFrame(() => requestAnimationFrame(() => segs[idx].classList.remove('start')));
    timer = setTimeout(() => show((idx + 1) % scenes.length), DUR[idx]);
  };
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) show(0); else scenes[0].classList.add('active');
  $('#replay-social').addEventListener('click', () => { idx = -1; show(0); });
  // Kayıt için dışarıdan sahne sıfırlama: window.restartSocial()
  window.restartSocial = () => { idx = -1; show(0); };
})();
