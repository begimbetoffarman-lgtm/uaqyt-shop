# -*- coding: utf-8 -*-
"""FAQ / order rules block, pair-name fields in the product modal, compact 2-column mobile grids."""
from i18n_blocks import bi

_ITEMS = [
    ("Как проходит заказ?",
     "Тапсырыс қалай өтеді?",
     "1. Выбираете модель и пишете нам в WhatsApp, что нанести на циферблат. 2. Вносите предоплату. 3. Мы готовим дизайн, согласуем его с вами и передаём в производство. 4. Когда часы готовы, отправляем вам фото-отчёт. 5. После вашего подтверждения по фото часы упаковываются и отправляются.",
     "1. Үлгіні таңдап, циферблатқа не жазылатынын WhatsApp-қа жазасыз. 2. Алдын ала төлем жасайсыз. 3. Біз дизайн дайындап, сізбен келісіп, өндіріске береміз. 4. Сағат дайын болғанда фото-есеп жібереміз. 5. Фотоны растағаннан кейін ғана сағат оралып, жолға шығады."),
    ("Как работает бонус 1+1?",
     "1+1 бонусы қалай жұмыс істейді?",
     "При покупке любых часов от 25 900 ₸ вторые часы вы получаете в подарок. Подробности и выбор бонусных часов уточните в WhatsApp.",
     "25 900 ₸-ден бастап кез келген сағатты алсаңыз, екінші сағат сыйлыққа беріледі. Бонус сағатты таңдау мен толық шарттарды WhatsApp-та нақтылаңыз."),
    ("Сколько времени делают часы?",
     "Сағат қанша уақытта жасалады?",
     "2–3 рабочих дня после предоплаты и утверждения дизайна. Каждое изделие собирается вручную. Срочный заказ можно сделать ускоренно, за 1 день: уточняйте в WhatsApp.",
     "Алдын ала төлем түсіп, дизайн бекітілгеннен кейін 2–3 жұмыс күні. Әр бұйым қолмен құрастырылады. Шұғыл тапсырысты жеделдетіп, 1 күнде жасауға болады: WhatsApp-та нақтылаңыз."),
    ("Можно ли обменять или вернуть часы?",
     "Сағатты ауыстыруға немесе қайтаруға бола ма?",
     "Нет. Часы именные и делаются только для вас, поэтому обмен и возврат не предусмотрены. Чтобы не ошибиться, перед отправкой мы присылаем фото готовых часов, и вы подтверждаете их.",
     "Жоқ. Сағат жеке тапсырыспен, тек сіз үшін жасалатындықтан, ауыстыру да, қайтару да жоқ. Қателеспеу үшін жібермес бұрын дайын сағаттың фотосын жібереміз, сіз оны растайсыз."),
    ("Какая гарантия?",
     "Кепілдік қандай?",
     "Гарантия 6–12 месяцев, в зависимости от модели. Срок указан в карточке каждой модели.",
     "Кепілдік модельге байланысты 6–12 ай. Мерзімі әр модельдің карточкасында көрсетілген."),
    ("Как оплатить и как доставляете?",
     "Қалай төлеуге және жеткізуге болады?",
     "Оплата: Kaspi Red (рассрочка 0-0-12) и Halyk. По Казахстану доставляем бесплатно почтой или автобусом, курьером за отдельную плату. Можно забрать самому в шоуруме в Алматы.",
     "Төлем: Kaspi Red (0-0-12 бөліп төлеу) және Halyk. Қазақстан бойынша пошта немесе автобуспен тегін, курьермен бөлек ақыға жеткіземіз. Алматыдағы шоурумнан өзіңіз алып кете аласыз."),
    ("Когда вы работаете?",
     "Сіз қашан жұмыс істейсіз?",
     "Понедельник – суббота, с 10:00 до 20:00. Воскресенье выходной. Пишите в WhatsApp в любое время, ответим в рабочие часы.",
     "Дүйсенбі – сенбі, 10:00 – 20:00. Жексенбі демалыс. WhatsApp-қа кез келген уақытта жазыңыз, жұмыс уақытында жауап береміз."),
]

_rows = "\n".join(
    f'<details class="faq-item">'
    f'<summary>{bi(qr, qk)}</summary>'
    f'<p>{bi(ar, ak)}</p></details>'
    for qr, qk, ar, ak in _ITEMS)

FAQ_SECTION = f'''<section class="faq-section" id="faq">
    <div class="holiday-head">
      {bi("Как заказать: сроки, оплата, возврат", "Қалай тапсырыс беру: мерзім, төлем, қайтару", "h2", "picker-title")}
      {bi("Все часы делаются под заказ. Здесь ответы на частые вопросы перед покупкой.", "Барлық сағат тапсырыспен жасалады. Сатып алар алдындағы жиі сұрақтардың жауаптары.", "p", "picker-sub")}
    </div>
    <div class="faq-list">
{_rows}
    </div>
  </section>'''

CSS_FAQ = '''
    /* ───────── FAQ ───────── */
    .faq-section { padding: 64px 32px 8px; max-width: 820px; margin: 0 auto; }
    .faq-list { display: flex; flex-direction: column; gap: 10px; }
    .faq-item { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 0 18px; }
    .faq-item[open] { border-color: var(--accent-gold); }
    .faq-item summary { cursor: pointer; list-style: none; padding: 16px 0; font-weight: 700; font-size: 16px; color: var(--text); display: flex; justify-content: space-between; gap: 12px; align-items: center; }
    .faq-item summary::-webkit-details-marker { display: none; }
    .faq-item summary::after { content: "+"; color: var(--accent-gold); font-size: 22px; line-height: 1; }
    .faq-item[open] summary::after { content: "–"; }
    .faq-item p { margin: 0; padding: 0 0 16px; color: var(--text-muted); font-size: 15px; line-height: 1.6; }
    @media (max-width: 768px) {
      .faq-section { padding: 44px 16px 4px; }
      .faq-item summary { font-size: 15px; }
      .products-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
      .product-card { border-radius: 14px; }
      .product-card .card-body { padding: 10px; }
      .product-card .card-category-tag, .product-card .card-desc, .product-card .zoom-hint { display: none; }
      .product-card .card-title { font-size: 14px; margin-bottom: 6px; }
      .product-card .installment-pill { font-size: 11px; padding: 4px 6px; }
      .product-card .card-footer { flex-direction: column; align-items: stretch; gap: 6px; }
      .product-card .card-price { font-size: 16px; }
      .product-card .btn-card-action { width: 100%; justify-content: center; padding: 9px 6px; font-size: 13px; }
      .product-card .card-badge { font-size: 10px; padding: 3px 7px; max-width: 90%; }
      .reviews-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
      .review-card { border-radius: 14px; }
      /* phones: no sideways scroll in the constructor, comfortable tap targets */
      .simulator-section { padding-left: 12px !important; padding-right: 12px !important; }
      .sim-grid { grid-template-columns: minmax(0, 1fr) !important; }
      .dial-display-card { padding: 10px !important; max-width: 100%; }
      .sim-controls-form, .sim-controls-form .form-group, .form-input { max-width: 100%; min-width: 0; box-sizing: border-box; }
      .price-chip { min-height: 40px; }
      .lang-btn { min-height: 34px; padding: 7px 12px; }
      .product-card .btn-card-action { min-height: 40px; }
    }
'''

JS_FAQ = '''
    // always open at the very top, even if the link carried a #section (e.g. copied after clicking the menu)
    (function () {
      const top = () => window.scrollTo(0, 0);
      if (location.hash) { try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {} }
      top(); window.addEventListener('load', () => { top(); setTimeout(top, 250); setTimeout(top, 900); });
    })();
    // dynamic chip counts: price buckets follow the active category and search
    (function () {
      const origFilter = filterCatalog;
      filterCatalog = function () {
        origFilter();
        try {
          const q = (document.getElementById('catalogSearch').value || '').toLowerCase().trim();
          const b = [0, 0, 0, 0];
          document.querySelectorAll('.product-card').forEach(card => {
            const cat = card.getAttribute('data-category') || '';
            if (activeFilter !== 'all') { const ok = activeFilter === 'mens' ? (cat.includes('mens') && !cat.includes('couples')) : cat.includes(activeFilter); if (!ok) return; }
            if (q) { const t = (card.querySelector('.card-title').textContent + ' ' + card.querySelector('.card-desc').textContent + ' ' + card.querySelector('.card-category-tag').textContent).toLowerCase(); if (!t.includes(q)) return; }
            const pr = parseInt(card.getAttribute('data-price')); if (!(pr < 999999)) return;
            b[pr < 30000 ? 0 : pr < 40000 ? 1 : pr < 55000 ? 2 : 3]++;
          });
          document.querySelectorAll('.price-chip').forEach((c, i) => { if (i > 0) c.textContent = c.textContent.replace(/\\(\\d+\\)/, '(' + b[i - 1] + ')'); });
        } catch (e) {}
      };
    })();
    // ═════════ gift reveal + bonus picker inside the order modal ═════════
    (function () {
      const BT = {
        ru: { h1: 'Отличный выбор! Вторые часы дарим мы', h2: 'Листайте и выберите подарок: 14 женских моделей', pick: 'Выберите подарок', ok: 'Ваш подарок: модель №', chg: 'Нажмите на другую модель, чтобы поменять', ribbon: '+1 в подарок' },
        kk: { h1: 'Тамаша таңдау! Екінші сағатты біз сыйлаймыз', h2: 'Сырғытып, сыйлықты таңдаңыз: 14 әйелдер моделі', pick: 'Сыйлықты таңдаңыз', ok: 'Сіздің сыйлығыңыз: №', chg: 'Ауыстыру үшін басқа модельді басыңыз', ribbon: '+1 сыйлыққа' }
      };
      window.bonusChoice = null;
      const eligible = p => p && !p.is_price_on_request && p.price >= 25900 && !/couples/.test(p.cat);
      const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

      function confetti(host) {
        if (reduce) return;
        const em = ['🎉', '✨', '🎁', '⭐', '💛'];
        for (let i = 0; i < 14; i++) {
          const el = document.createElement('span'); el.className = 'gift-conf'; el.textContent = em[i % em.length];
          el.style.setProperty('--dx', (Math.random() * 220 - 110).toFixed(0) + 'px');
          el.style.setProperty('--dy', (-60 - Math.random() * 90).toFixed(0) + 'px');
          el.style.setProperty('--rot', (Math.random() * 120 - 60).toFixed(0) + 'deg');
          el.style.animationDelay = (Math.random() * 0.25).toFixed(2) + 's';
          host.appendChild(el); setTimeout(() => el.remove(), 1800);
        }
      }
      function paint(box) {
        const t = BT[LANG] || BT.ru;
        const n = window.bonusChoice;
        box.querySelector('.gift-h1').textContent = n ? '🎁 ' + t.ok + n : '🎉 ' + t.h1;
        box.querySelector('.gift-h2').textContent = n ? t.chg : t.h2;
        box.classList.toggle('has-pick', !!n);
        box.querySelectorAll('.bonus-thumb').forEach(x => x.classList.toggle('sel', +x.dataset.n === n));
      }

      const prev = openProductModal;
      openProductModal = function (id) {
        prev(id);
        const p = currentModalProduct; if (!p) return;
        const old = document.querySelector('.modal-promo-note'); if (old) old.style.display = 'none';
        let box = document.getElementById('bonusModalPick');
        if (!box) {
          box = document.createElement('div'); box.id = 'bonusModalPick'; box.className = 'bonus-pick bonus-modal-pick';
          let h = '<div class="gift-banner"><div class="gift-icon">🎁</div><div><div class="gift-h1"></div><div class="gift-h2"></div></div></div><div class="bonus-pick-grid">';
          for (let i = 1; i <= 14; i++) h += '<div class="bonus-thumb" data-n="' + i + '" style="--i:' + i + '"><img src="./images/bonus/women-' + i + '.jpg" alt="Подарок ' + i + '" loading="lazy"><b>' + i + '</b></div>';
          box.innerHTML = h + '</div>';
          box.addEventListener('click', function (e) {
            const th = e.target.closest('.bonus-thumb'); if (!th) return;
            const n = +th.dataset.n;
            window.bonusChoice = (window.bonusChoice === n) ? null : n;
            paint(box);
            if (window.bonusChoice) confetti(box.querySelector('.gift-banner'));
          });
          (old || document.querySelector('.modal-trust')).after(box);
        }
        window.bonusChoice = null;
        const show = eligible(p);
        box.style.display = show ? '' : 'none';
        paint(box);
        if (show) {
          box.classList.remove('gift-reveal'); void box.offsetWidth; box.classList.add('gift-reveal');
          setTimeout(() => confetti(box.querySelector('.gift-banner')), 350);
        }
      };

      // gift ribbon on eligible catalog cards (no price talk: just a signal)
      function ribbons() {
        const t = BT[LANG] || BT.ru;
        document.querySelectorAll('.product-card').forEach(card => {
          const pr = parseInt(card.getAttribute('data-price'));
          const cat = card.getAttribute('data-category') || '';
          if (!(pr >= 25900 && pr < 999999) || cat.includes('couples')) return;
          let r = card.querySelector('.gift-ribbon');
          if (!r) { r = document.createElement('span'); r.className = 'gift-ribbon'; const ttl = card.querySelector('.card-title'); if (ttl) ttl.before(r); else card.appendChild(r); }
          r.textContent = '🎁 ' + t.ribbon;
        });
      }
      ribbons();
      const prevLang = setLang;
      setLang = function (l) { prevLang(l); ribbons(); const b = document.getElementById('bonusModalPick'); if (b) paint(b); };
    })();
    // ═════════ pair products: two names, no bonus note ═════════
    (function () {
      const origOpen = openProductModal;
      const T = {
        ru: { one: 'Что написать на циферблате (имя или тамга):', m: 'Имя на мужских часах:', f: 'Имя на женских часах:', ph1: 'Например: Бауыржан / Найман, 15.06.2026', phm: 'Например: Бауыржан', phf: 'Например: Айгерим' },
        kk: { one: 'Сағатқа жазылатын жеке есім немесе ру таңбасы:', m: 'Ерлер сағатындағы есім:', f: 'Әйелдер сағатындағы есім:', ph1: 'Мысалы: Бауыржан / Найман, 15.06.2026', phm: 'Мысалы: Бауыржан', phf: 'Мысалы: Айгерім' }
      };
      openProductModal = function (id) {
        origOpen(id);
        const p = currentModalProduct; if (!p) return;
        const pair = /couples/.test(p.cat);
        const t = T[LANG] || T.ru;
        const i1 = document.getElementById('modalEngraveText');
        let i2 = document.getElementById('modalEngraveText2');
        let lab2 = document.getElementById('modalEngraveLabel2');
        if (!i2) {
          i2 = document.createElement('input'); i2.type = 'text'; i2.id = 'modalEngraveText2'; i2.className = 'modal-input-engrave'; i1.after(i2);
          lab2 = document.createElement('label'); lab2.id = 'modalEngraveLabel2'; lab2.className = 'modal-customizer-label'; lab2.style.marginTop = '8px'; i2.before(lab2);
        }
        const lab = i1.parentElement.querySelector('.modal-customizer-label');
        if (lab) lab.textContent = pair ? t.m : t.one;
        i1.placeholder = pair ? t.phm : t.ph1;
        i2.placeholder = t.phf; i2.style.display = pair ? '' : 'none';
        if (!pair) i2.value = '';
        lab2.textContent = t.f; lab2.style.display = pair ? '' : 'none';
        const note = document.querySelector('.modal-promo-note');
        if (note) note.style.display = 'none';
      };
    })();
'''


PROMO_BODY = (
    '<div class="promo-steps">'
    + '<div class="promo-step"><i>1</i>' + bi("Выберите любые часы от 25 900 ₸", "25 900 ₸-ден бастап кез келген сағатты таңдаңыз", "span") + '</div>'
    + '<div class="promo-step"><i>2</i>' + bi("Вторые часы дарим мы, бесплатно", "Екінші сағатты біз сыйлаймыз, тегін", "span") + '</div>'
    + '<div class="promo-step"><i>3</i>' + bi("Подарок выберете сами из 14 женских моделей", "Сыйлықты 14 әйелдер моделінен өзіңіз таңдайсыз", "span") + '</div>'
    + '</div>'
)

BONUS_GALLERY = (
    '<div class="bonus-pick">'
    + bi("Бонусные женские часы: 14 моделей на выбор", "Бонус әйелдер сағаттары: таңдауға 14 модель", "div", "bonus-pick-title")
    + '<div class="bonus-pick-grid">'
    + "".join('<div class="bonus-thumb"><img src="./images/bonus/women-%d.jpg" alt="Бонус %d" loading="lazy"><b>%d</b></div>' % (i, i, i) for i in range(1, 15))
    + '</div></div>'
)

CSS_BONUS = '''
    .bonus-pick { margin: 18px 0 4px; }
    .bonus-pick-title { font-weight: 700; font-size: 15px; margin-bottom: 10px; color: var(--text); }
    .bonus-pick-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px; }
    .bonus-thumb { position: relative; }
    .bonus-thumb img { display: block; width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 12px; border: 2px solid var(--border); }
    .bonus-thumb b { position: absolute; left: 4px; top: 4px; min-width: 20px; height: 20px; padding: 0 4px; border-radius: 10px; background: rgba(15,23,42,.82); color: #fff; font-size: 11px; line-height: 20px; text-align: center; }
    @media (min-width: 700px) { .bonus-pick-grid { grid-template-columns: repeat(7, minmax(0, 1fr)); } }
    /* picker inside the order modal */
    .bonus-modal-pick { margin: 14px 0; }
    .bonus-modal-pick .bonus-pick-title { margin-bottom: 4px; }
    .bonus-modal-hint { font-size: 12.5px; opacity: .7; margin-bottom: 8px; }
    .bonus-modal-pick .bonus-thumb { cursor: pointer; -webkit-tap-highlight-color: transparent; }
    .bonus-modal-pick .bonus-thumb.sel img { border-color: #d4af37; box-shadow: 0 0 0 2px rgba(212,175,55,.45); }
    .bonus-modal-pick .bonus-thumb.sel::after { content: '\\2713'; position: absolute; right: 6px; bottom: 6px; width: 24px; height: 24px; border-radius: 12px; background: #d4af37; color: #0f172a; font-weight: 800; text-align: center; line-height: 24px; }

    /* gift reveal in modal */
    .gift-banner { position: relative; display: flex; align-items: center; gap: 12px; padding: 14px; border-radius: 16px; background: linear-gradient(135deg, rgba(212,175,55,.22), rgba(190,24,93,.18)); border: 1px solid rgba(212,175,55,.55); margin-bottom: 12px; overflow: visible; }
    .gift-icon { font-size: 34px; line-height: 1; flex: 0 0 auto; }
    .gift-h1 { font-weight: 800; font-size: 15.5px; line-height: 1.25; }
    .gift-h2 { font-size: 12.5px; opacity: .8; margin-top: 3px; }
    .bonus-modal-pick.gift-reveal .gift-banner { animation: giftPop .55s cubic-bezier(.2,1.4,.4,1) backwards; }
    .bonus-modal-pick.gift-reveal .gift-icon { animation: giftWiggle 1.1s .4s ease-in-out 2; transform-origin: 50% 80%; }
    .bonus-modal-pick.has-pick .gift-banner { background: linear-gradient(135deg, rgba(34,197,94,.22), rgba(212,175,55,.2)); border-color: rgba(74,222,128,.6); }
    .gift-conf { position: absolute; left: 30px; top: 14px; font-size: 18px; pointer-events: none; z-index: 5; animation: confFly 1.5s ease-out forwards; }
    @keyframes giftPop { 0% { transform: scale(.9) translateY(8px); opacity: .55; } 100% { transform: none; opacity: 1; } }
    @keyframes giftWiggle { 0%,100% { transform: rotate(0); } 20% { transform: rotate(-14deg) scale(1.1); } 40% { transform: rotate(12deg) scale(1.1); } 60% { transform: rotate(-8deg); } 80% { transform: rotate(6deg); } }
    @keyframes thumbIn { from { opacity: .55; transform: scale(.92); } to { opacity: 1; transform: none; } }
    @keyframes confFly { 0% { transform: translate(0,0) rotate(0) scale(.6); opacity: 1; } 100% { transform: translate(var(--dx), var(--dy)) rotate(var(--rot)) scale(1.15); opacity: 0; } }
    /* gift ribbon on catalog cards */
        .gift-ribbon { display: inline-block; margin: 0 0 8px; padding: 4px 9px; border-radius: 12px; font-size: 11px; font-weight: 800; color: #fff; background: linear-gradient(135deg, #e11d48, #be185d); box-shadow: 0 4px 10px rgba(190,24,93,.35); pointer-events: none; }
    /* promo steps */
    .promo-steps { display: grid; gap: 10px; margin: 14px 0; }
    .promo-step { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 14px; background: rgba(255,255,255,.06); border: 1px solid rgba(212,175,55,.35); font-weight: 600; line-height: 1.3; }
    .promo-step i { flex: 0 0 auto; width: 28px; height: 28px; border-radius: 14px; background: #d4af37; color: #0f172a; font-style: normal; font-weight: 800; text-align: center; line-height: 28px; }
    @media (prefers-reduced-motion: reduce) { .gift-banner, .gift-icon, .bonus-thumb { animation: none !important; } }

    /* modal: swipe strip instead of a tall grid */
    .bonus-modal-pick .bonus-pick-grid { display: flex; overflow-x: auto; gap: 8px; padding-bottom: 8px; scroll-snap-type: x proximity; -webkit-overflow-scrolling: touch; }
    .bonus-modal-pick { width: 100%; max-width: 100%; min-width: 0; contain: inline-size; }
    .bonus-modal-pick .bonus-thumb { flex: 0 0 92px; scroll-snap-align: start; }
    @media (max-width: 700px) {
      .modal-card { grid-template-columns: minmax(0, 1fr) !important; }
      .modal-img-col, .modal-info-col { min-width: 0; }
      .modal-price-box { flex-wrap: wrap; }
      .modal-trust { font-size: 13px; }
    }
    .promo-features .promo-feat-item:nth-child(-n+2) { display: none; }
    @media (max-width: 700px) { .promo-heading { font-size: clamp(24px, 7.2vw, 32px) !important; line-height: 1.2; } }
'''
