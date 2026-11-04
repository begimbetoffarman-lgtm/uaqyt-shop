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
     "При покупке любых часов дороже 25 900 ₸ вторые часы вы получаете в подарок. Подробности и выбор бонусных часов уточните в WhatsApp.",
     "25 900 ₸-ден жоғары кез келген сағатты алсаңыз, екінші сағат сыйлыққа беріледі. Бонус сағатты таңдау мен толық шарттарды WhatsApp-та нақтылаңыз."),
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
    }
'''

JS_FAQ = '''
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
        if (note) note.style.display = (pair || (!p.is_price_on_request && p.price <= 25900)) ? 'none' : '';
      };
    })();
'''
