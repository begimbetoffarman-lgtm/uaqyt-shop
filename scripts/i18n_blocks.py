# -*- coding: utf-8 -*-
"""New site blocks (plain strings, single braces). Russian is the default text, Kazakh is carried in data-kk."""
import html as _h


def bi(ru, kk, tag="span", cls="", attrs=""):
    c = f' class="{cls}"' if cls else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag}{c}{a} data-bi data-ru="{_h.escape(ru, quote=True)}" data-kk="{_h.escape(kk, quote=True)}">{_h.escape(ru)}</{tag}>'


LANG_SWITCH = '''<div class="lang-switch" role="group" aria-label="Язык / Тіл">
        <button type="button" class="lang-btn active" data-l="ru" onclick="setLang('ru')">RU</button>
        <button type="button" class="lang-btn" data-l="kk" onclick="setLang('kk')">ҚАЗ</button>
      </div>'''

RIBBON = '''<div class="holiday-ribbon" id="holidayRibbon"><a href="#holidays" id="holidayRibbonText"></a></div>'''

HOLIDAY_SECTION = f'''<section class="holiday-section" id="holidays">
    <div class="holiday-head">
      {bi("Ближайшие праздники: время выбрать подарок", "Алдағы мерекелер: сыйлық таңдайтын уақыт", "h2", "picker-title")}
      {bi("Часы с гравировкой лучше заказывать заранее. Подскажем, что выбрать к каждому празднику.", "Гравировкалы сағатты алдын ала тапсырыс берген дұрыс. Әр мерекеге не таңдау керегін айтып береміз.", "p", "picker-sub")}
    </div>
    <div class="holiday-grid" id="holidayGrid"></div>
  </section>'''

STORY_SECTION = f'''<section class="story-section" id="story">
    <div class="holiday-head">
      {bi("Наши часы вживую", "Біздің сағаттар тікелей", "h2", "picker-title")}
      {bi("Посмотрите, как выглядят часы с гравировкой на руке и в коробке. Имя и дата на циферблате превращают их в личную память.", "Гравировкалы сағаттардың қолда және қорапта қалай көрінетінін қараңыз. Циферблаттағы есім мен күн оны жеке естелікке айналдырады.", "p", "picker-sub")}
    </div>
    <div class="story-reel">
      <figure class="story-v"><video autoplay muted loop playsinline preload="metadata" poster="./video/w1.jpg" aria-label="Часы UAQYT, видео 1"><source src="./video/w1.mp4" type="video/mp4"></video></figure>
      <figure class="story-v"><video autoplay muted loop playsinline preload="metadata" poster="./video/w2.jpg" aria-label="Часы UAQYT, видео 2"><source src="./video/w2.mp4" type="video/mp4"></video></figure>
      <figure class="story-v"><video autoplay muted loop playsinline preload="metadata" poster="./video/w3.jpg" aria-label="Часы UAQYT, видео 3"><source src="./video/w3.mp4" type="video/mp4"></video></figure>
      <figure class="story-v"><video autoplay muted loop playsinline preload="metadata" poster="./video/w4.jpg" aria-label="Часы UAQYT, видео 4"><source src="./video/w4.mp4" type="video/mp4"></video></figure>
      <figure class="story-v"><video autoplay muted loop playsinline preload="metadata" poster="./video/w5.jpg" aria-label="Часы UAQYT, видео 5"><source src="./video/w5.mp4" type="video/mp4"></video></figure>
    </div>
    <div class="story-cta">
      <a class="story-btn red" href="#picks">{bi("Подобрать подарок", "Сыйлық таңдау")}</a>
      <a class="story-btn light" href="#customizer">{bi("Создать свои часы", "Өз сағатыңызды жасау")}</a>
    </div>
  </section>'''

CSS_EXTRA = '''
    /* ───────── language switch ───────── */
    .lang-switch { display: inline-flex; background: var(--bg-alt); border: 1px solid var(--border); border-radius: 22px; padding: 3px; gap: 2px; }
    .lang-btn { border: none; background: transparent; padding: 7px 12px; border-radius: 18px; font-size: 13px; font-weight: 700; color: var(--text-muted); cursor: pointer; transition: var(--transition); font-family: inherit; }
    .lang-btn.active { background: var(--accent-gold); color: #111; }

    /* ───────── holiday ribbon + calendar ───────── */
    .holiday-ribbon { background: var(--accent-gold); color: #111; text-align: center; font-size: 14.5px; font-weight: 600; padding: 9px 16px; }
    .holiday-ribbon a { color: #111; text-decoration: none; }
    .holiday-ribbon a b { color: #111; }
    .holiday-section, .story-section { padding: 64px 32px 8px; max-width: 1240px; margin: 0 auto; }
    .holiday-head { text-align: center; margin-bottom: 28px; }
    .holiday-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    .holiday-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 24px; padding: 22px 20px 20px; display: flex; flex-direction: column; gap: 10px; box-shadow: var(--shadow-sm, 0 2px 10px rgba(0,0,0,.04)); transition: var(--transition); }
    .holiday-card:hover { transform: translateY(-4px); border-color: var(--accent-gold); }
    .holiday-card.first { background: var(--accent-gold-soft); border-color: var(--border-gold); }
    .holiday-date { display: flex; align-items: baseline; gap: 8px; color: var(--accent-gold-dark, #8a6a2f); font-weight: 800; }
    .holiday-day { font-family: var(--font-serif); font-size: 44px; line-height: 1; }
    .holiday-mon { font-size: 15px; text-transform: uppercase; letter-spacing: 1px; }
    .holiday-name { font-family: var(--font-serif); font-size: 22px; font-weight: 700; line-height: 1.2; color: var(--text); }
    .holiday-left { display: inline-block; align-self: flex-start; padding: 5px 12px; border-radius: 16px; background: rgba(225,29,72,.18); color: #fca5a5; font-size: 13.5px; font-weight: 700; }
    .holiday-tip { color: var(--text); font-size: 15px; flex: 1; }
    .holiday-actions { display: flex; flex-direction: column; gap: 8px; margin-top: 6px; }
    .holiday-btn { padding: 11px 14px; border-radius: 14px; border: none; font-weight: 700; font-size: 14.5px; cursor: pointer; text-align: center; text-decoration: none; font-family: inherit; }
    .holiday-remind { text-align: center; color: var(--text-muted); font-size: 13.5px; text-decoration: underline; padding-top: 2px; }
    .holiday-btn.dark { background: var(--accent-gold); color: #111; }
    .holiday-btn.wa { background: var(--accent-green); color: #fff; }

    /* ───────── video reel (own watch videos) ───────── */
    .story-reel { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
    .story-v { margin: 0; overflow: hidden; background: #111827; border-radius: 22px; aspect-ratio: 464 / 832; position: relative; cursor: pointer; }
    .story-v video { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform .8s cubic-bezier(.2,.7,.1,1); }
    .story-v:hover video { transform: scale(1.04); }
    .story-cta { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 24px; }
    .story-btn { padding: 14px 24px; border-radius: 16px; font-weight: 700; font-size: 16px; text-decoration: none; }
    .story-btn.red { background: var(--accent-red); color: #fff; }
    .story-btn.light { background: #fff; color: #111827; }

    /* ───────── motion ───────── */
    .reveal { opacity: 0; transform: translateY(26px); transition: opacity .8s cubic-bezier(.2,.7,.1,1), transform .8s cubic-bezier(.2,.7,.1,1); }
    .reveal.in { opacity: 1; transform: none; }
    .hero-showcase-card { animation: floaty 7s ease-in-out infinite; }
    @keyframes floaty { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    .btn-hero-primary, .picker-btn.dark, .holiday-btn.dark { position: relative; overflow: hidden; }
    .btn-hero-primary::after, .picker-btn.dark::after { content: ""; position: absolute; top: 0; left: -60%; width: 40%; height: 100%; background: rgba(255,255,255,.18); transform: skewX(-20deg); animation: shine 4.5s ease-in-out infinite; }
    @keyframes shine { 0%, 60% { left: -60%; } 100% { left: 140%; } }
    @media (prefers-reduced-motion: reduce) {
      .reveal { opacity: 1; transform: none; transition: none; }
      .hero-showcase-card, .btn-hero-primary::after, .picker-btn.dark::after { animation: none; }
    }


    @media (max-width: 1420px) {
      .navbar .nav-links { gap: 18px; }
      .btn-nav-2gis { display: none !important; }
    }
    .modal-price, .pick-card-price, .card-price { white-space: nowrap; }
    .review-card .review-content { padding-top: 12px; }
    .review-card .review-quote { font-size: 14.5px; color: var(--text-muted); margin: 0; }

    @media (max-width: 1000px) {
      .holiday-grid { grid-template-columns: repeat(2, 1fr); }
      .story-reel { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 768px) {
      .holiday-section, .story-section { padding: 44px 16px 4px; }
      .holiday-grid { gap: 10px; }
      .holiday-card { padding: 16px 14px; border-radius: 20px; }
      .holiday-day { font-size: 34px; }
      .holiday-name { font-size: 18px; }
      .holiday-tip { font-size: 14px; }
      .lang-btn { padding: 6px 9px; }
      .story-reel { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 12px; padding-bottom: 8px; margin-right: -16px; padding-right: 16px; }
      .story-v { flex: 0 0 64%; scroll-snap-align: start; }
      .holiday-ribbon { font-size: 13px; padding: 8px 12px; }
    }
'''

JS_EXTRA = r'''
    // ═════════ language + dynamic texts ═════════
    const I18N = {
      ru: {
        buy: 'Купить', ask_price: 'Узнать цену', price_req: 'Цена по запросу', price_individual: 'Цена уточняется индивидуально',
        inst: (m) => 'Рассрочка Kaspi Red: ' + m + ' ₸ в месяц (0-0-12)', inst_req: 'Цену уточним в WhatsApp',
        btn_order: 'Купить: отправить заказ в WhatsApp', btn_ask: 'Узнать цену в WhatsApp',
        found: (n) => 'Найдено моделей: ' + n, none: 'По этому фильтру ничего не найдено. Выберите другую категорию или цену.',
        pick_empty: 'В этом бюджете нет моделей с готовой ценой. Выберите другой бюджет или напишите нам, подберём вручную.',
        pick_inst: (m) => 'Kaspi Red: ' + m + ' ₸ в месяц',
        review_cap: 'Отзыв клиента в WhatsApp',
        days_left: (n) => n === 0 ? 'сегодня' : (n === 1 ? 'остался 1 день' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 'осталось ' + n + ' дня' : 'осталось ' + n + ' дней')),
        ribbon: (name, n) => '🎁 ' + (n === 0 ? 'Сегодня ' + name : 'До праздника ' + qn(name) + ' ' + (n === 1 ? 'остался 1 день' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 'осталось ' + n + ' дня' : 'осталось ' + n + ' дней'))) + '. Закажите гравировку заранее →',
        h_pick: 'Подобрать часы', h_order: 'Заказать к празднику',
        months: ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'],
        wa_hello: 'Здравствуйте! Пишу с сайта UAQYT. Хочу заказать часы, подскажите, пожалуйста.',
        wa_product: (name, price) => 'Здравствуйте! Хочу заказать часы ' + qn(name) + '' + (price ? ' (' + price + ')' : '') + ' с сайта UAQYT.',
        wa_request: (name, tag) => 'Здравствуйте! Хочу узнать цену и срок изготовления часов с сайта UAQYT:\n\n• Модель: ' + qn(name) + '\n• Категория: ' + tag,
        wa_engrave: 'Что написать на циферблате', wa_city: 'Город',
        wa_dial: (name, sub) => 'Здравствуйте! Я собрал(а) свои часы в конструкторе на сайте UAQYT:\n\n• Имя: ' + qn(name) + '\n• Надпись / род: «' + sub + '»\n\nПодскажите цену и сроки.',
        wa_pick: (who, bud) => 'Здравствуйте! Помогите выбрать часы. Кому: ' + who + '. Бюджет: ' + bud + '.',
        wa_holiday: (name, date) => 'Здравствуйте! Хочу заказать часы с гравировкой к празднику ' + qn(name) + ' (' + date + '). Подскажите, что выбрать и успеем ли.',
        who: { mens: 'мужчине', couples: 'паре (1+1)', service: 'сотруднику', none: 'не выбрано' },
        bud: { t1: 'до 30 000 ₸', t2: '30 000 – 40 000 ₸', t3: '40 000 – 55 000 ₸', t4: 'от 55 000 ₸', none: 'не важен' }
      },
      kk: {
        buy: 'Сатып алу', ask_price: 'Бағасын білу', price_req: 'Бағасы сұрау бойынша', price_individual: 'Бағасы жеке нақтыланады',
        inst: (m) => 'Kaspi Red бөліп төлеу: айына ' + m + ' ₸ (0-0-12)', inst_req: 'Бағасын WhatsApp-та нақтылаймыз',
        btn_order: 'Сатып алу: тапсырысты WhatsApp-қа жіберу', btn_ask: 'Бағасын WhatsApp-та білу',
        found: (n) => 'Табылған үлгі: ' + n, none: 'Бұл сүзгі бойынша ештеңе табылмады. Басқа санатты немесе бағаны таңдаңыз.',
        pick_empty: 'Бұл бюджетте бағасы дайын үлгі жоқ. Басқа бюджетті таңдаңыз немесе бізге жазыңыз, қолмен таңдап береміз.',
        pick_inst: (m) => 'Kaspi Red: айына ' + m + ' ₸',
        review_cap: 'Клиенттің WhatsApp-тағы пікірі',
        days_left: (n) => n === 0 ? 'бүгін' : n + ' күн қалды',
        ribbon: (name, n) => '🎁 ' + (n === 0 ? 'Бүгін: ' + name : '' + qn(name) + ' мерекесіне ' + n + ' күн қалды') + '. Гравировканы алдын ала тапсырыс беріңіз →',
        h_pick: 'Сағат таңдау', h_order: 'Мерекеге тапсырыс беру',
        months: ['қаңтар','ақпан','наурыз','сәуір','мамыр','маусым','шілде','тамыз','қыркүйек','қазан','қараша','желтоқсан'],
        wa_hello: 'Сәлеметсіз бе! UAQYT сайтынан жазып отырмын. Сағат тапсырыс бергім келеді, көмектесіңізші.',
        wa_product: (name, price) => 'Сәлеметсіз бе! UAQYT сайтындағы ' + qn(name) + '' + (price ? ' (' + price + ')' : '') + ' сағатын тапсырыс бергім келеді.',
        wa_request: (name, tag) => 'Сәлеметсіз бе! UAQYT сайтындағы сағаттың бағасы мен дайындалу мерзімін білгім келеді:\n\n• Үлгі: ' + qn(name) + '\n• Санат: ' + tag,
        wa_engrave: 'Циферблатқа жазылатын мәтін', wa_city: 'Қала',
        wa_dial: (name, sub) => 'Сәлеметсіз бе! UAQYT сайтындағы конструкторда өз сағатымды құрастырдым:\n\n• Есім: ' + qn(name) + '\n• Жазу / ру: «' + sub + '»\n\nБағасы мен мерзімін айтыңызшы.',
        wa_pick: (who, bud) => 'Сәлеметсіз бе! Сағат таңдауға көмектесіңізші. Кімге: ' + who + '. Бюджет: ' + bud + '.',
        wa_holiday: (name, date) => 'Сәлеметсіз бе! ' + qn(name) + ' (' + date + ') мерекесіне гравировкалы сағат тапсырыс бергім келеді. Не таңдау керегін айтыңызшы, үлгеріп қаламыз ба?',
        who: { mens: 'ер адамға', couples: 'жұпқа (1+1)', service: 'қызметкерге', none: 'таңдалмаған' },
        bud: { t1: '30 000 ₸ дейін', t2: '30 000 – 40 000 ₸', t3: '40 000 – 55 000 ₸', t4: '55 000 ₸ бастап', none: 'маңызды емес' }
      }
    };
    let LANG = 'ru';
    function tt(k) { return (I18N[LANG] && I18N[LANG][k] !== undefined) ? I18N[LANG][k] : I18N.ru[k]; }
    function pf(p, f) { return (LANG === 'ru' && p.ru && p.ru[f]) ? p.ru[f] : p[f]; }
    function qn(n) { return n.indexOf('«') >= 0 ? n : '«' + n + '»'; }
    function money(n) { return n.toLocaleString('ru-RU') + ' ₸'; }
    function waLink(text) { return 'https://wa.me/__WA__?text=' + encodeURIComponent(text); }

    function setLang(l) {
      LANG = (l === 'kk') ? 'kk' : 'ru';
      try { localStorage.setItem('uaqytLang', LANG); } catch (e) {}
      document.documentElement.lang = LANG;
      document.querySelectorAll('[data-bi]').forEach(el => { el.textContent = el.dataset[LANG]; });
      document.querySelectorAll('[data-bia]').forEach(el => {
        el.getAttribute('data-bia').split(',').forEach(a => {
          const v = el.getAttribute('data-' + LANG + '-' + a);
          if (v !== null) el.setAttribute(a, v);
        });
      });
      document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.l === LANG));
      document.title = LANG === 'kk' ? 'UAQYT: гравировкасы бар есімді сағаттар, Алматы' : 'UAQYT: именные часы с гравировкой в Алматы';
      renderProductCards();
      filterCatalog();
      renderPicks();
      renderHolidays();
      renderFeatures();
      if (document.getElementById('productModal').classList.contains('active') && currentModalProduct) openProductModal(currentModalProduct.id);
    }

    // product cards: texts that depend on the product data
    function renderProductCards() {
      document.querySelectorAll('.product-card').forEach(card => {
        const p = productsData.find(x => x.id === card.getAttribute('data-id'));
        if (!p) return;
        const set = (sel, txt) => { const e = card.querySelector(sel); if (e) e.textContent = txt; };
        set('.card-badge', pf(p, 'badge'));
        set('.card-title', pf(p, 'name'));
        set('.card-desc', pf(p, 'desc'));
        set('.card-category-tag', pf(p, 'tag'));
        const alt = card.querySelector('img'); if (alt) alt.alt = pf(p, 'name');
        const btn = card.querySelector('.btn-card-action span');
        if (btn) btn.textContent = p.is_price_on_request ? tt('ask_price') : tt('buy');
        const req = card.querySelector('.price-request-badge'); if (req) req.textContent = tt('price_req');
        const pill = card.querySelector('.installment-pill span');
        if (pill) pill.textContent = p.is_price_on_request ? tt('inst_req') : tt('pick_inst')(Math.floor(p.price / 12).toLocaleString('ru-RU'));
      });
    }

    function filterCatalog() {
      const query = document.getElementById('catalogSearch').value.toLowerCase().trim();
      let shown = 0;
      document.querySelectorAll('.product-card').forEach(card => {
        const cardCat = card.getAttribute('data-category') || '';
        const text = (card.querySelector('.card-title').textContent + ' ' + card.querySelector('.card-desc').textContent + ' ' + card.querySelector('.card-category-tag').textContent).toLowerCase();
        let matchesCat = true;
        if (activeFilter !== 'all') {
          if (activeFilter === 'mens') matchesCat = cardCat.includes('mens') && !cardCat.includes('couples');
          else matchesCat = cardCat.includes(activeFilter);
        }
        const ok = matchesCat && (!query || text.includes(query)) && priceMatches(parseInt(card.getAttribute('data-price')));
        card.style.display = ok ? 'flex' : 'none';
        if (ok) shown++;
      });
      const cnt = document.getElementById('catalogCount');
      if (cnt) cnt.textContent = shown ? tt('found')(shown) : tt('none');
    }

    function openProductModal(productId) {
      const p = productsData.find(item => item.id === productId);
      if (!p) return;
      currentModalProduct = p;
      document.getElementById('modalImg').src = p.img;
      document.getElementById('modalImg').alt = pf(p, 'name');
      document.getElementById('modalTitle').textContent = pf(p, 'name');
      document.getElementById('modalBadge').textContent = pf(p, 'badge');
      const priceElem = document.getElementById('modalPrice');
      const instElem = document.getElementById('modalInstallment');
      const btnText = document.getElementById('modalOrderBtnText');
      if (p.is_price_on_request) {
        priceElem.textContent = tt('price_individual'); priceElem.style.fontSize = '20px';
        instElem.textContent = tt('inst_req'); btnText.textContent = tt('btn_ask');
      } else {
        priceElem.textContent = money(p.price); priceElem.style.fontSize = '28px';
        instElem.textContent = tt('inst')(Math.floor(p.price / 12).toLocaleString('ru-RU')); btnText.textContent = tt('btn_order');
      }
      document.getElementById('modalMech').textContent = pf(p, 'mech');
      document.getElementById('modalGlass').textContent = pf(p, 'glass');
      document.getElementById('modalCase').textContent = pf(p, 'case');
      document.getElementById('modalStrap').textContent = pf(p, 'strap');
      document.getElementById('productModal').classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function sendOrderFromModal() {
      if (!currentModalProduct) return;
      const p = currentModalProduct;
      const engrave = document.getElementById('modalEngraveText').value.trim();
      const city = (document.getElementById('modalCity') || { value: '' }).value.trim();
      let msg = p.is_price_on_request ? tt('wa_request')(pf(p, 'name'), pf(p, 'tag')) : tt('wa_product')(pf(p, 'name'), money(p.price));
      if (engrave) msg += '\n• ' + tt('wa_engrave') + ': «' + engrave + '»';
      if (city) msg += '\n• ' + tt('wa_city') + ': ' + city;
      window.open(waLink(msg), '_blank');
    }

    function orderCustomizedDial() {
      const name = document.getElementById('inputName').value || '—';
      const sub = document.getElementById('inputSub').value || '—';
      window.open(waLink(tt('wa_dial')(name, sub)), '_blank');
    }

    function updateLightboxContent() {
      const r = reviewsData[currentReviewIndex];
      if (!r) return;
      document.getElementById('lightboxReviewImg').src = r.img;
      document.getElementById('lightboxReviewCaption').textContent = tt('review_cap') + ' (' + (currentReviewIndex + 1) + '/' + reviewsData.length + ')';
    }

    function renderPicks() {
      const box = document.getElementById('pickResults');
      if (!box) return;
      let list = productsData.filter(p => !p.is_price_on_request);
      if (pick.who === 'mens') list = list.filter(p => p.cat.includes('mens') && !p.cat.includes('couples'));
      if (pick.who === 'couples') list = list.filter(p => p.cat.includes('couples'));
      if (pick.who === 'service') list = list.filter(p => p.cat.includes('service'));
      list = list.filter(p => pickBudgetOk(p.price));
      const chosen = (pick.who || pick.budget) ? list.slice(0, 4) : PICK_DEFAULT.map(id => productsData.find(p => p.id === id)).filter(Boolean);
      if (!chosen.length) {
        box.innerHTML = '<div class="picker-empty">' + tt('pick_empty') + '</div>';
      } else {
        box.innerHTML = chosen.map(p => `<div class="pick-card" onclick="openProductModal('${p.id}')">
          <img src="${p.img}" alt="${pf(p, 'name')}" loading="lazy">
          <div class="pick-card-body">
            <div class="pick-card-name">${pf(p, 'name')}</div>
            <div class="pick-card-price">${money(p.price)}</div>
            <div class="pick-card-inst">${tt('pick_inst')(Math.floor(p.price / 12).toLocaleString('ru-RU'))}</div>
            <button type="button" class="pick-card-btn">${tt('buy')}</button>
          </div></div>`).join('');
      }
      const wa = document.getElementById('pickWa');
      if (wa) wa.href = waLink(tt('wa_pick')(tt('who')[pick.who || 'none'], tt('bud')[pick.budget || 'none']));
    }

    // ═════════ holidays ═════════
    const HOLIDAYS = [
      { m: 1, d: 1, ru: 'Новый год', kk: 'Жаңа жыл', who: 'mens', tip_ru: 'Именные часы для мужа, отца или брата: подарок, который останется на годы.', tip_kk: 'Күйеуге, әкеге не ағаға есімді сағат: жылдар бойы сақталатын сыйлық.' },
      { m: 2, d: 14, ru: 'День влюблённых', kk: 'Ғашықтар күні', who: 'couples', tip_ru: 'Парные часы 1+1 с вашими именами.', tip_kk: 'Есімдеріңіз жазылған жұптық 1+1 сағаттар.' },
      { m: 2, d: 23, ru: '23 февраля', kk: '23 ақпан', who: 'mens', tip_ru: 'Классика и гравировка имени: достойный подарок мужчине.', tip_kk: 'Классикалық сағат пен есім гравировкасы: ер адамға лайықты сыйлық.' },
      { m: 3, d: 22, ru: 'Наурыз', kk: 'Наурыз мейрамы', who: 'mens', tip_ru: 'Часы с родовой тамгой: память для всей семьи.', tip_kk: 'Ру таңбасы бар сағат: бүкіл отбасына естелік.' },
      { m: 5, d: 7, ru: 'День защитника Отечества', kk: 'Отан қорғаушы күні', who: 'service', tip_ru: 'Эмблема службы или герб на циферблате.', tip_kk: 'Циферблаттағы қызмет эмблемасы немесе елтаңба.' },
      { m: 12, d: 16, ru: 'День Независимости', kk: 'Тәуелсіздік күні', who: 'service', tip_ru: 'Часы с гербом РК или эмблемой службы.', tip_kk: 'ҚР елтаңбасы немесе қызмет эмблемасы бар сағат.' }
    ];
    function nextOccurrence(h) {
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      let dt = new Date(now.getFullYear(), h.m - 1, h.d);
      if (dt < today) dt = new Date(now.getFullYear() + 1, h.m - 1, h.d);
      return { dt, left: Math.round((dt - today) / 86400000) };
    }
    function renderHolidays() {
      const grid = document.getElementById('holidayGrid');
      if (!grid) return;
      const list = HOLIDAYS.map(h => Object.assign({ h }, nextOccurrence(h))).sort((a, b) => a.left - b.left).slice(0, 4);
      const months = tt('months');
      grid.innerHTML = list.map((x, i) => {
        const name = x.h[LANG]; const date = x.dt.getDate() + ' ' + months[x.dt.getMonth()];
        return `<div class="holiday-card reveal in${i === 0 ? ' first' : ''}">
          <div class="holiday-date"><span class="holiday-day">${x.dt.getDate()}</span><span class="holiday-mon">${months[x.dt.getMonth()]}</span></div>
          <div class="holiday-name">${name}</div>
          <span class="holiday-left">${tt('days_left')(x.left)}</span>
          <div class="holiday-tip">${x.h['tip_' + LANG]}</div>
          <div class="holiday-actions">
            <button type="button" class="holiday-btn dark" onclick="applyHoliday('${x.h.who}')">${tt('h_pick')}</button>
            <a class="holiday-btn wa" target="_blank" rel="noopener" href="${waLink(tt('wa_holiday')(name, date))}">${tt('h_order')}</a>
            <a class="holiday-remind" target="_blank" rel="noopener" href="${waLink(tt('wa_remind')(name, date))}">${tt('remind')}</a>
          </div></div>`;
      }).join('');
      const rb = document.getElementById('holidayRibbonText');
      if (rb && list.length) rb.textContent = tt('ribbon')(list[0].h[LANG], list[0].left);
    }
    function applyHoliday(who) {
      const tab = document.querySelector('[data-filter="' + who + '"]');
      if (tab) setCategoryFilter(who, tab);
      const chip = document.querySelectorAll('.price-chip')[0];
      if (chip) setPriceFilter('all', chip);
      document.getElementById('catalog').scrollIntoView({ behavior: 'smooth' });
    }

    // ═════════ scroll reveal + videos ═════════
    function initMotion() {
      const targets = document.querySelectorAll('.picker-box, .holiday-head, .story-banner, .story-v, .promo-container, .sim-grid, .social-card, .review-card, .contact-card, .catalog-header, .reviews-header');
      targets.forEach(el => el.classList.add('reveal'));
      document.querySelectorAll('.product-card').forEach((el, i) => { el.classList.add('reveal'); el.style.transitionDelay = ((i % 4) * 70) + 'ms'; });
      if (!('IntersectionObserver' in window)) { document.querySelectorAll('.reveal').forEach(e => e.classList.add('in')); return; }
      const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
      document.querySelectorAll('.reveal:not(.in)').forEach(e => io.observe(e));
      const vids = document.querySelectorAll('.story-section video');
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { vids.forEach(v => v.removeAttribute('autoplay')); return; }
      const vo = new IntersectionObserver(es => es.forEach(e => { const v = e.target; if (e.isIntersecting) { const p = v.play(); if (p && p.catch) p.catch(() => {}); } else v.pause(); }), { threshold: 0.2 });
      vids.forEach(v => vo.observe(v));
    }

    // if the browser blocks autoplay, show a play button on the banner
    setTimeout(() => {
      const main = document.querySelector('.story-main'), btn = document.querySelector('.story-play');
      if (main && btn) {
        if (main.paused) btn.hidden = false;
        btn.addEventListener('click', () => { main.play(); btn.hidden = true; });
        main.addEventListener('click', () => { if (main.paused) main.play(); else main.pause(); });
      }
      document.querySelectorAll('.story-v video').forEach(v => v.addEventListener('click', () => { if (v.paused) v.play(); else v.pause(); }));
    }, 1500);

    (function bootLang() {
      let l = 'ru';
      try {
        const q = new URLSearchParams(location.search).get('lang');
        l = (q === 'kk' || q === 'ru') ? q : (localStorage.getItem('uaqytLang') || 'ru');
      } catch (e) {}
      initMotion();
      setLang(l);
    })();
'''
