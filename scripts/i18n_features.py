# -*- coding: utf-8 -*-
"""Convenience features: my selection (favourites + order request), compare, engraving preview,
quick questions, extended gift picker. Russian default, Kazakh via data-kk / I18N."""
from i18n_blocks import bi


def chips(group, items):
    out = []
    for val, ru, kk in items:
        out.append(f'<button type="button" class="picker-chip" data-v="{val}" onclick="setPick(\'{group}\',\'{val}\',this)">{bi(ru, kk)}</button>')
    return "\n          ".join(out)


PICKER_SECTION = f'''<section class="picker-section" id="picks">
    <div class="picker-head">
      {bi("Подарок за 30 секунд", "Сыйлықты 30 секундта таңдаймыз", "h2", "picker-title")}
      {bi("Ответьте на несколько вопросов: покажем подходящие часы с ценой, рассрочкой и бесплатной доставкой.", "Бірнеше сұраққа жауап беріңіз: лайықты сағатты бағасымен, бөліп төлеумен және тегін жеткізумен көрсетеміз.", "p", "picker-sub")}
    </div>
    <div class="picker-box">
      <div class="picker-row">
        {bi("Кому дарим?", "Кімге сыйлаймыз?", "div", "picker-label")}
        <div class="picker-chips" id="pickWho">
          {chips("who", [("husband", "👨 Мужу", "👨 Күйеуге"), ("dad", "👴 Папе", "👴 Әкеге"), ("bro", "🧑 Брату", "🧑 Ағаға, інісіне"), ("friend", "🤝 Другу или коллеге", "🤝 Досқа немесе әріптеске"), ("couples", "💑 Паре (1+1)", "💑 Жұпқа (1+1)"), ("service", "🛡️ Сотруднику (МВД, КНБ, ВС)", "🛡️ Қызметкерге (ІІМ, ҰҚК, ҚР ҚК)")])}
        </div>
      </div>
      <div class="picker-row">
        {bi("Какой повод?", "Қандай мереке?", "div", "picker-label")}
        <div class="picker-chips" id="pickOcc">
          {chips("occ", [("bday", "День рождения", "Туған күн"), ("jub", "Юбилей", "Мерейтой"), ("ann", "Годовщина", "Той жылдығы"), ("ny", "Новый год", "Жаңа жыл"), ("feb23", "23 февраля", "23 ақпан"), ("any", "Просто так", "Себепсіз")])}
        </div>
      </div>
      <div class="picker-row">
        {bi("Какой стиль ближе?", "Қандай стиль ұнайды?", "div", "picker-label")}
        <div class="picker-chips" id="pickStyle">
          {chips("style", [("tamga", "С родовой тамгой", "Ру таңбасымен"), ("classic", "Строгая классика", "Қатаң классика"), ("mech", "Механика", "Механика"), ("box", "В деревянной коробке", "Ағаш қорапта")])}
        </div>
      </div>
      <div class="picker-row">
        {bi("Бюджет:", "Бюджет:", "div", "picker-label")}
        <div class="picker-chips" id="pickBudget">
          {chips("budget", [("t1", "до 30 000 ₸", "30 000 ₸-ге дейін"), ("t2", "30 000 – 40 000 ₸", "30 000 – 40 000 ₸"), ("t3", "40 000 – 55 000 ₸", "40 000 – 55 000 ₸"), ("t4", "от 55 000 ₸", "55 000 ₸-ден бастап")])}
        </div>
      </div>
      <p class="picker-tip" id="pickTip"></p>
      <div class="picker-results" id="pickResults" aria-live="polite"></div>
      <div class="picker-foot">
        <button type="button" class="picker-btn dark" id="pickAll" onclick="applyPickToCatalog()">{bi("Смотреть все подходящие", "Барлық лайықтыларын қарау")}</button>
        <button type="button" class="picker-btn ghost" onclick="addPicksToSel()">{bi("Добавить подборку в мой выбор", "Осы таңдауды таңдаулыларға қосу")}</button>
        <a class="picker-btn wa" id="pickWa" target="_blank" rel="noopener" href="https://wa.me/">{bi("Помогите выбрать (WhatsApp)", "Таңдауға көмектесіңіз (WhatsApp)")}</a>
      </div>
    </div>
  </section>'''

DOCK_HTML = f'''<div class="dock" id="dock">
    <button type="button" class="dock-btn dock-sel" id="dockSel" onclick="openCart()" hidden>♥ {bi("Мой выбор", "Таңдаулылар")} <b id="selCount">0</b></button>
    <div class="ask-menu" id="askMenu" hidden></div>
    <button type="button" class="dock-btn dock-q" id="dockQ" onclick="toggleAsk()">💬 {bi("Вопрос", "Сұрақ")}</button>
  </div>'''

CART_HTML = f'''<div class="cart-overlay" id="cartOverlay" onclick="closeCart()">
    <aside class="cart-panel" onclick="event.stopPropagation()" role="dialog" aria-modal="true" aria-labelledby="cartTitle">
      <div class="cart-head">
        {bi("Мой выбор", "Таңдаулылар", "h3", "", 'id="cartTitle"')}
        <button type="button" class="cart-close" onclick="closeCart()" aria-label="Close">✕</button>
      </div>
      <div class="cart-body" id="cartBody"></div>
      <div class="cart-foot" id="cartFoot"></div>
    </aside>
  </div>'''

CSS_FEATURES = '''
    /* ───────── my selection, dock, compare, engraving preview ───────── */
    .price-chip.active, .filter-tab.active { color: #111 !important; }
    .dial-display-card { background: var(--bg-card) !important; border-color: var(--border) !important; }
    .picker-btn.ghost { background: transparent; color: var(--text); border: 1.5px solid var(--border-gold); }
    .picker-btn.ghost:hover { background: var(--accent-gold-soft); }
    .picker-tip { margin: 6px 0 14px; color: var(--accent-gold-dark); font-weight: 600; font-size: 15.5px; min-height: 1.4em; }
    .pick-card { position: relative; }
    .fav-btn { position: absolute; top: 10px; right: 10px; z-index: 4; width: 40px; height: 40px; border-radius: 50%; border: none; cursor: pointer; background: rgba(11,11,13,.62); color: #fff; font-size: 19px; line-height: 1; display: flex; align-items: center; justify-content: center; transition: var(--transition); }
    .fav-btn:hover { transform: scale(1.1); }
    .fav-btn.on { background: #fff; color: #e11d48; }
    .card-img-box { position: relative; }

    .dock { position: fixed; right: 20px; bottom: 20px; z-index: 120; display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
    .dock-btn { border: none; cursor: pointer; border-radius: 28px; padding: 13px 18px; font: 700 15px var(--font-sans); display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 10px 26px rgba(0,0,0,.5); transition: var(--transition); }
    .dock-btn:hover { transform: translateY(-2px); }
    .dock-sel { background: var(--accent-gold); color: #111; }
    .dock-sel b { background: #111; color: var(--accent-gold); border-radius: 12px; padding: 1px 8px; font-size: 13px; }
    .dock-q { background: var(--bg-card); color: var(--text); border: 1px solid var(--border-gold); }
    .ask-menu { background: var(--bg-card); border: 1px solid var(--border-gold); border-radius: 20px; padding: 10px; width: 290px; box-shadow: 0 16px 40px rgba(0,0,0,.6); }
    .ask-menu[hidden], .dock-btn[hidden] { display: none; }
    .ask-title { font-size: 13px; color: var(--text-muted); padding: 6px 10px 8px; }
    .ask-menu a { display: block; padding: 11px 12px; border-radius: 12px; color: var(--text); text-decoration: none; font-weight: 600; font-size: 15px; }
    .ask-menu a:hover { background: var(--accent-gold-soft); color: var(--accent-gold-dark); }

    .cart-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.62); z-index: 400; display: none; justify-content: flex-end; }
    .cart-overlay.active { display: flex; }
    .cart-panel { width: min(460px, 100%); height: 100%; background: var(--bg-card); display: flex; flex-direction: column; border-left: 1px solid var(--border-gold); animation: slideIn .35s cubic-bezier(.2,.7,.1,1); }
    @keyframes slideIn { from { transform: translateX(40px); opacity: 0; } to { transform: none; opacity: 1; } }
    .cart-head { display: flex; align-items: center; justify-content: space-between; padding: 18px 20px; border-bottom: 1px solid var(--border); }
    .cart-head h3 { font-family: var(--font-serif); font-size: 28px; margin: 0; color: var(--text); }
    .cart-close { background: transparent; border: none; color: var(--text); font-size: 22px; cursor: pointer; }
    .cart-body { flex: 1; overflow-y: auto; padding: 14px 20px; }
    .cart-foot { padding: 14px 20px 20px; border-top: 1px solid var(--border); display: grid; gap: 10px; }
    .cart-empty { color: var(--text-muted); text-align: center; padding: 40px 10px; font-size: 16px; }
    .cart-item { display: grid; grid-template-columns: 72px 1fr 32px; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--border); }
    .cart-item img { width: 72px; height: 96px; object-fit: cover; border-radius: 12px; }
    .cart-item .ci-name { font-family: var(--font-serif); font-size: 18px; font-weight: 700; color: var(--text); line-height: 1.2; }
    .cart-item .ci-price { color: var(--accent-gold-dark); font-weight: 700; margin: 2px 0 6px; }
    .cart-item input, .cart-foot input { width: 100%; padding: 10px 12px; border-radius: 10px; border: 1.5px solid var(--border); background: var(--bg-alt); color: var(--text); font: 400 14px var(--font-sans); }
    .cart-item .ci-del { background: transparent; border: none; color: var(--text-muted); font-size: 18px; cursor: pointer; align-self: start; }
    .cart-total { display: flex; justify-content: space-between; font-weight: 800; font-size: 18px; color: var(--text); }
    .cart-total small { display: block; font-weight: 500; color: var(--text-muted); font-size: 12.5px; }
    .cart-btn { padding: 14px 16px; border-radius: 14px; border: none; font: 700 15px var(--font-sans); cursor: pointer; text-align: center; text-decoration: none; }
    .cart-btn.wa { background: var(--accent-green); color: #fff; }
    .cart-btn.gold { background: var(--accent-gold); color: #111; }
    .cart-btn.ghost { background: transparent; color: var(--text-muted); border: 1px solid var(--border); }
    .cart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .cmp-wrap { overflow-x: auto; }
    .cmp-table { border-collapse: collapse; min-width: 100%; font-size: 14px; color: var(--text); }
    .cmp-table th, .cmp-table td { padding: 10px 8px; text-align: left; vertical-align: top; border-bottom: 1px solid var(--border); min-width: 120px; }
    .cmp-table th:first-child { min-width: 90px; color: var(--text-muted); font-weight: 600; }
    .cmp-table img { width: 90px; height: 120px; object-fit: cover; border-radius: 10px; }

    .modal-fav { width: 100%; padding: 13px 16px; border-radius: 14px; border: 1.5px solid var(--border-gold); background: transparent; color: var(--text); font: 700 15px var(--font-sans); cursor: pointer; margin-bottom: 8px; }
    .modal-fav.on { background: var(--accent-gold-soft); color: var(--accent-gold-dark); }
    .eng-preview { margin-top: 12px; padding: 12px; border-radius: 16px; background: var(--bg-alt); border: 1px solid var(--border); display: grid; grid-template-columns: 150px 1fr; gap: 12px; align-items: center; }
    .eng-preview svg { width: 150px; height: 150px; }
    .eng-title { font-weight: 700; font-size: 14px; color: var(--text); margin-bottom: 8px; }
    .eng-ctrl { display: flex; gap: 8px; margin-bottom: 8px; }
    .eng-ctrl button { padding: 6px 12px; border-radius: 14px; border: 1px solid var(--border); background: transparent; color: var(--text-muted); cursor: pointer; font: 600 13px var(--font-sans); }
    .eng-ctrl button.on { background: var(--accent-gold); color: #111; border-color: var(--accent-gold); }
    .eng-note { font-size: 12.5px; color: var(--text-muted); }

    @media (max-width: 768px) {
      .dock { right: 12px; bottom: 86px; }
      .dock-btn { padding: 11px 15px; font-size: 14px; }
      .ask-menu { width: min(290px, calc(100vw - 24px)); }
      .cart-item { grid-template-columns: 60px 1fr 30px; }
      .cart-item img { width: 60px; height: 80px; }
      .eng-preview { grid-template-columns: 110px 1fr; }
      .eng-preview svg { width: 110px; height: 110px; }
    }
'''

JS_FEATURES = r'''
    // ═════════ extra texts ═════════
    Object.assign(I18N.ru, {
      sel_add: '♡ В мой выбор', sel_on: '♥ В моём выборе', sel_title: 'Мой выбор',
      cart_empty: 'Пока ничего не выбрано. Нажмите ♥ на понравившихся часах, и они появятся здесь.',
      cart_engrave: 'Что написать на циферблате', cart_city: 'Ваш город', cart_note: 'Комментарий (необязательно)',
      cart_total: 'Итого', cart_total_note: 'Модели с ценой по запросу не входят в сумму',
      cart_cmp: 'Сравнить', cart_back: '← К списку', cart_send: 'Отправить в WhatsApp', cart_clear: 'Очистить',
      cmp_price: 'Цена', cmp_mech: 'Механизм', cmp_glass: 'Стекло', cmp_case: 'Корпус', cmp_strap: 'Ремень/браслет',
      cart_hello: 'Здравствуйте! Хочу заказать часы с сайта UAQYT:', cart_city_l: 'Город', cart_note_l: 'Комментарий', cart_text_l: 'надпись',
      ask_title: 'Спросите в WhatsApp', ask_price: 'Узнать цену', ask_term: 'Срок изготовления', ask_eng: 'Что можно написать на циферблате', ask_del: 'Доставка в мой город', ask_custom: 'Задать свой вопрос',
      m_ask_price: 'Здравствуйте! Подскажите, пожалуйста, цену часов.', m_ask_term: 'Здравствуйте! Подскажите срок изготовления часов с гравировкой.',
      m_ask_eng: 'Здравствуйте! Что можно выгравировать на циферблате и как согласуется макет?', m_ask_del: 'Здравствуйте! Подскажите, как и за сколько дней доставите часы в мой город.', m_ask_custom: 'Здравствуйте! У меня вопрос по часам с сайта UAQYT.',
      eng_title: 'Как будет выглядеть надпись', eng_black: 'Чёрный', eng_white: 'Белый', eng_note: 'Примерный вид. Макет согласуем с вами в WhatsApp.', eng_ph: 'ВАШЕ ИМЯ',
      pk_none: 'выберите ответы выше', add_picks: 'Подборка добавлена в «Мой выбор»', remind: 'Напомнить за 2 недели',
      wa_remind: (name, date) => 'Здравствуйте! Напомните мне, пожалуйста, за 2 недели до праздника «' + name + '» (' + date + '): хочу заказать часы с гравировкой.',
      wa_pick4: (who, occ, st, bud) => 'Здравствуйте! Помогите выбрать часы. Кому: ' + who + '. Повод: ' + occ + '. Стиль: ' + st + '. Бюджет: ' + bud + '.',
      pw: { husband: 'мужу', dad: 'папе', bro: 'брату', friend: 'другу или коллеге', couples: 'паре (1+1)', service: 'сотруднику', none: 'не выбрано' },
      po: { bday: 'день рождения', jub: 'юбилей', ann: 'годовщина', ny: 'Новый год', feb23: '23 февраля', any: 'просто так', none: 'не выбран' },
      ps: { tamga: 'с родовой тамгой', classic: 'строгая классика', mech: 'механика', box: 'в деревянной коробке', none: 'любой' },
      tips: { bday: 'Гравировка имени и даты рождения запомнится надолго.', jub: 'К юбилею подойдут золотистый корпус и подарочная коробка.', ann: 'На годовщину посмотрите парные часы 1+1.', ny: 'Гравировка делается под заказ: лучше написать заранее.', feb23: 'Классика и имя на циферблате: достойный подарок мужчине.', any: 'Имя на циферблате делает подарок личным даже без повода.' }
    });
    Object.assign(I18N.kk, {
      sel_add: '♡ Таңдаулыларға қосу', sel_on: '♥ Таңдаулыларда', sel_title: 'Таңдаулылар',
      cart_empty: 'Әзірге ештеңе таңдалмаған. Ұнаған сағатта ♥ батырмасын басыңыз, ол осында пайда болады.',
      cart_engrave: 'Циферблатқа не жазылсын', cart_city: 'Қалаңыз', cart_note: 'Пікір (міндетті емес)',
      cart_total: 'Барлығы', cart_total_note: 'Бағасы сұрау бойынша үлгілер қосындыға кірмейді',
      cart_cmp: 'Салыстыру', cart_back: '← Тізімге', cart_send: 'WhatsApp-қа жіберу', cart_clear: 'Тазалау',
      cmp_price: 'Бағасы', cmp_mech: 'Механизм', cmp_glass: 'Әйнек', cmp_case: 'Корпус', cmp_strap: 'Қайыс/білезік',
      cart_hello: 'Сәлеметсіз бе! UAQYT сайтынан сағат тапсырыс бергім келеді:', cart_city_l: 'Қала', cart_note_l: 'Пікір', cart_text_l: 'жазу',
      ask_title: 'WhatsApp-та сұраңыз', ask_price: 'Бағасын білу', ask_term: 'Дайындау мерзімі', ask_eng: 'Циферблатқа не жазуға болады', ask_del: 'Менің қалама жеткізу', ask_custom: 'Өз сұрағымды жазу',
      m_ask_price: 'Сәлеметсіз бе! Сағаттың бағасын айтып беріңізші.', m_ask_term: 'Сәлеметсіз бе! Есімі жазылатын сағаттың дайындалу мерзімін айтыңызшы.',
      m_ask_eng: 'Сәлеметсіз бе! Циферблатқа не жазуға болады және макет қалай келісіледі?', m_ask_del: 'Сәлеметсіз бе! Сағатты менің қалама қалай және неше күнде жеткізесіздер?', m_ask_custom: 'Сәлеметсіз бе! UAQYT сайтындағы сағатқа қатысты сұрағым бар.',
      eng_title: 'Жазу қалай көрінеді', eng_black: 'Қара', eng_white: 'Ақ', eng_note: 'Шамамен көрінісі. Макетті WhatsApp-та келісеміз.', eng_ph: 'ЕСІМІҢІЗ',
      pk_none: 'жоғарыдан жауап таңдаңыз', add_picks: 'Таңдау «Таңдаулыларға» қосылды', remind: '2 апта бұрын еске салу',
      wa_remind: (name, date) => 'Сәлеметсіз бе! «' + name + '» (' + date + ') мерекесіне 2 апта қалғанда еске салыңызшы: есімі жазылған сағат тапсырыс бергім келеді.',
      wa_pick4: (who, occ, st, bud) => 'Сәлеметсіз бе! Сағат таңдауға көмектесіңізші. Кімге: ' + who + '. Мереке: ' + occ + '. Стиль: ' + st + '. Бюджет: ' + bud + '.',
      pw: { husband: 'күйеуге', dad: 'әкеге', bro: 'ағаға/інісіне', friend: 'досқа немесе әріптеске', couples: 'жұпқа (1+1)', service: 'қызметкерге', none: 'таңдалмаған' },
      po: { bday: 'туған күн', jub: 'мерейтой', ann: 'той жылдығы', ny: 'Жаңа жыл', feb23: '23 ақпан', any: 'себепсіз', none: 'таңдалмаған' },
      ps: { tamga: 'ру таңбасымен', classic: 'қатаң классика', mech: 'механика', box: 'ағаш қорапта', none: 'кез келген' },
      tips: { bday: 'Циферблаттағы есім мен туған күн ұзақ есте қалады.', jub: 'Мерейтойға алтын түсті корпус пен сыйлық қорабы лайық.', ann: 'Той жылдығына 1+1 жұптық сағаттарды қараңыз.', ny: 'Есім тапсырыспен жазылады: алдын ала жазған дұрыс.', feb23: 'Классика мен циферблаттағы есім: ер адамға лайықты сыйлық.', any: 'Циферблаттағы есім сыйлықты себепсіз де жеке етеді.' }
    });

    // ═════════ my selection ═════════
    let SEL = [];
    try { SEL = JSON.parse(localStorage.getItem('uaqytSel') || '[]'); } catch (e) { SEL = []; }
    let cartMode = 'list';
    function byId(id) { return productsData.find(x => x.id === id); }
    function saveSel() { try { localStorage.setItem('uaqytSel', JSON.stringify(SEL)); } catch (e) {} }
    function inSel(id) { return SEL.some(x => x.id === id); }
    function toggleSel(id, text) {
      if (inSel(id)) SEL = SEL.filter(x => x.id !== id); else SEL.push({ id, text: text || '' });
      saveSel(); syncSel();
    }
    function syncSel() {
      document.querySelectorAll('[data-fav]').forEach(b => b.classList.toggle('on', inSel(b.dataset.fav)));
      const dock = document.getElementById('dockSel'), cnt = document.getElementById('selCount');
      if (cnt) cnt.textContent = SEL.length;
      if (dock) dock.hidden = SEL.length === 0;
      const mf = document.getElementById('modalFav');
      if (mf && currentModalProduct) { mf.classList.toggle('on', inSel(currentModalProduct.id)); mf.textContent = inSel(currentModalProduct.id) ? tt('sel_on') : tt('sel_add'); }
      if (document.getElementById('cartOverlay').classList.contains('active')) renderCart();
    }
    function ensureHearts() {
      document.querySelectorAll('.product-card').forEach(card => {
        const box = card.querySelector('.card-img-box');
        if (!box || box.querySelector('.fav-btn')) return;
        const id = card.getAttribute('data-id');
        const b = document.createElement('button');
        b.type = 'button'; b.className = 'fav-btn'; b.dataset.fav = id; b.textContent = '♥'; b.setAttribute('aria-label', 'Favourite');
        b.addEventListener('click', e => { e.stopPropagation(); toggleSel(id); });
        box.appendChild(b);
      });
    }
    function openCart() { cartMode = 'list'; document.getElementById('cartOverlay').classList.add('active'); document.body.style.overflow = 'hidden'; renderCart(); }
    function closeCart() { document.getElementById('cartOverlay').classList.remove('active'); document.body.style.overflow = ''; }
    function cartVal(id) { const e = document.getElementById(id); return e ? e.value.trim() : ''; }
    function cartMessage() {
      let total = 0;
      const lines = SEL.map((x, i) => {
        const p = byId(x.id); if (!p) return '';
        if (!p.is_price_on_request) total += p.price;
        return (i + 1) + ') ' + qn(pf(p, 'name')) + (p.is_price_on_request ? '' : ' — ' + money(p.price)) + (x.text ? ' (' + tt('cart_text_l') + ': «' + x.text + '»)' : '');
      }).filter(Boolean);
      let msg = tt('cart_hello') + '\n' + lines.join('\n');
      if (total) msg += '\n' + tt('cart_total') + ': ' + money(total);
      const city = cartVal('cartCity'), note = cartVal('cartNote');
      if (city) msg += '\n' + tt('cart_city_l') + ': ' + city;
      if (note) msg += '\n' + tt('cart_note_l') + ': ' + note;
      return msg;
    }
    function renderCart() {
      const body = document.getElementById('cartBody'), foot = document.getElementById('cartFoot');
      if (!body) return;
      const keepCity = cartVal('cartCity') || (localStorage.getItem('uaqytCity') || ''), keepNote = cartVal('cartNote');
      if (!SEL.length) { body.innerHTML = '<div class="cart-empty">' + tt('cart_empty') + '</div>'; foot.innerHTML = ''; return; }
      if (cartMode === 'compare') {
        const items = SEL.map(x => byId(x.id)).filter(Boolean);
        const row = (label, fn) => '<tr><th>' + label + '</th>' + items.map(p => '<td>' + fn(p) + '</td>').join('') + '</tr>';
        body.innerHTML = '<div class="cmp-wrap"><table class="cmp-table">' +
          row('', p => '<img src="' + p.img + '" alt="">') +
          row('', p => '<b>' + pf(p, 'name') + '</b>') +
          row(tt('cmp_price'), p => p.is_price_on_request ? tt('price_req') : money(p.price)) +
          row(tt('cmp_mech'), p => pf(p, 'mech')) + row(tt('cmp_glass'), p => pf(p, 'glass')) +
          row(tt('cmp_case'), p => pf(p, 'case')) + row(tt('cmp_strap'), p => pf(p, 'strap')) + '</table></div>';
        foot.innerHTML = '<button type="button" class="cart-btn ghost" onclick="cartMode=\'list\';renderCart()">' + tt('cart_back') + '</button>';
        return;
      }
      let total = 0;
      body.innerHTML = SEL.map(x => {
        const p = byId(x.id); if (!p) return '';
        if (!p.is_price_on_request) total += p.price;
        return '<div class="cart-item"><img src="' + p.img + '" alt="">' +
          '<div><div class="ci-name">' + pf(p, 'name') + '</div><div class="ci-price">' + (p.is_price_on_request ? tt('price_req') : money(p.price)) + '</div>' +
          '<input type="text" data-sel="' + p.id + '" value="' + (x.text || '').replace(/"/g, '&quot;') + '" placeholder="' + tt('cart_engrave') + '"></div>' +
          '<button type="button" class="ci-del" onclick="toggleSel(\'' + p.id + '\')" aria-label="Remove">✕</button></div>';
      }).join('');
      body.querySelectorAll('input[data-sel]').forEach(inp => inp.addEventListener('input', () => { const it = SEL.find(s => s.id === inp.dataset.sel); if (it) { it.text = inp.value; saveSel(); } }));
      foot.innerHTML =
        '<div class="cart-row"><input type="text" id="cartCity" placeholder="' + tt('cart_city') + '" value="' + keepCity.replace(/"/g, '&quot;') + '"><input type="text" id="cartNote" placeholder="' + tt('cart_note') + '" value="' + keepNote.replace(/"/g, '&quot;') + '"></div>' +
        (total ? '<div class="cart-total"><span>' + tt('cart_total') + '<small>' + tt('cart_total_note') + '</small></span><span>' + money(total) + '</span></div>' : '') +
        '<a class="cart-btn wa" id="cartSend" target="_blank" rel="noopener" href="#">' + tt('cart_send') + '</a>' +
        '<div class="cart-row">' + (SEL.length > 1 ? '<button type="button" class="cart-btn gold" onclick="cartMode=\'compare\';renderCart()">' + tt('cart_cmp') + '</button>' : '<span></span>') +
        '<button type="button" class="cart-btn ghost" onclick="SEL=[];saveSel();syncSel()">' + tt('cart_clear') + '</button></div>';
      const send = document.getElementById('cartSend');
      const upd = () => { try { localStorage.setItem('uaqytCity', cartVal('cartCity')); } catch (e) {} send.href = waLink(cartMessage()); };
      ['cartCity', 'cartNote'].forEach(id => document.getElementById(id).addEventListener('input', upd));
      body.querySelectorAll('input[data-sel]').forEach(inp => inp.addEventListener('input', upd));
      upd();
    }

    // ═════════ quick questions ═════════
    function toggleAsk() { const m = document.getElementById('askMenu'); m.hidden = !m.hidden; if (!m.hidden) renderAsk(); }
    function renderAsk() {
      const m = document.getElementById('askMenu');
      const items = [['ask_price', 'm_ask_price'], ['ask_term', 'm_ask_term'], ['ask_eng', 'm_ask_eng'], ['ask_del', 'm_ask_del'], ['ask_custom', 'm_ask_custom']];
      m.innerHTML = '<div class="ask-title">' + tt('ask_title') + '</div>' + items.map(([l, t]) => '<a target="_blank" rel="noopener" href="' + waLink(tt(t)) + '">' + tt(l) + '</a>').join('');
    }
    document.addEventListener('click', e => { const m = document.getElementById('askMenu'); if (m && !m.hidden && !e.target.closest('.dock')) m.hidden = true; });

    // ═════════ engraving preview in the product window ═════════
    let engDial = 'black';
    function engSvg() {
      const svg = document.getElementById('engSvg'); if (!svg) return;
      const raw = (document.getElementById('modalEngraveText').value || '').trim();
      const txt = (raw || tt('eng_ph')).toUpperCase();
      const dark = engDial === 'black';
      const dial = dark ? '#0e0e0f' : '#f6f2e8', ink = dark ? '#e6c65c' : '#1f1b14', tick = dark ? '#8a7a45' : '#9a8f78';
      let t = '';
      for (let i = 0; i < 12; i++) { const a = i * 30 * Math.PI / 180, r1 = i % 3 === 0 ? 76 : 80, r2 = 86; t += '<line x1="' + (100 + Math.sin(a) * r1).toFixed(1) + '" y1="' + (100 - Math.cos(a) * r1).toFixed(1) + '" x2="' + (100 + Math.sin(a) * r2).toFixed(1) + '" y2="' + (100 - Math.cos(a) * r2).toFixed(1) + '" stroke="' + tick + '" stroke-width="' + (i % 3 === 0 ? 3 : 1.5) + '"/>'; }
      const fs = Math.max(9, Math.min(19, 22 - txt.length * 0.55));
      svg.innerHTML = '<circle cx="100" cy="100" r="97" fill="#d4af37"/><circle cx="100" cy="100" r="90" fill="' + dial + '"/>' + t +
        '<defs><path id="engArc" d="M 38,100 A 62,62 0 0 1 162,100"/></defs>' +
        '<text fill="' + ink + '" font-family="Cormorant Garamond, Georgia, serif" font-weight="700" font-size="' + fs.toFixed(1) + '" opacity="' + (raw ? 1 : .45) + '"><textPath href="#engArc" startOffset="50%" text-anchor="middle">' + txt.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</textPath></text>' +
        '<image href="./images/emblem.png" x="76" y="84" width="48" height="23"/>' +
        '<line x1="100" y1="100" x2="73" y2="72" stroke="' + ink + '" stroke-width="5" stroke-linecap="round" opacity=".85"/><line x1="100" y1="100" x2="136" y2="66" stroke="' + ink + '" stroke-width="3.5" stroke-linecap="round" opacity=".85"/>';
    }
    function ensureModalExtras() {
      const grp = document.querySelector('.modal-cta-group');
      if (grp && !document.getElementById('modalFav')) {
        const b = document.createElement('button'); b.type = 'button'; b.id = 'modalFav'; b.className = 'modal-fav';
        b.addEventListener('click', () => { if (currentModalProduct) toggleSel(currentModalProduct.id, document.getElementById('modalEngraveText').value.trim()); });
        grp.insertBefore(b, grp.firstChild);
      }
      const box = document.querySelector('.modal-customizer-box');
      if (box && !document.getElementById('engSvg')) {
        const d = document.createElement('div'); d.className = 'eng-preview';
        d.innerHTML = '<svg id="engSvg" viewBox="0 0 200 200" role="img" aria-label="preview"></svg><div><div class="eng-title" id="engTitle"></div><div class="eng-ctrl"><button type="button" data-d="black" class="on"></button><button type="button" data-d="white"></button></div><div class="eng-note" id="engNote"></div></div>';
        box.appendChild(d);
        d.querySelectorAll('.eng-ctrl button').forEach(btn => btn.addEventListener('click', () => { engDial = btn.dataset.d; d.querySelectorAll('.eng-ctrl button').forEach(x => x.classList.toggle('on', x === btn)); engSvg(); }));
        document.getElementById('modalEngraveText').addEventListener('input', engSvg);
      }
      const t = document.getElementById('engTitle'); if (t) t.textContent = tt('eng_title');
      const n = document.getElementById('engNote'); if (n) n.textContent = tt('eng_note');
      const bl = document.querySelector('.eng-ctrl [data-d="black"]'), wh = document.querySelector('.eng-ctrl [data-d="white"]');
      if (bl) bl.textContent = tt('eng_black'); if (wh) wh.textContent = tt('eng_white');
      engSvg(); syncSel();
    }
    (function wrapModal() { const base = openProductModal; openProductModal = function (id) { base(id); ensureModalExtras(); }; })();

    // ═════════ extended gift picker ═════════
    pick.occ = null; pick.style = null;
    function setPick(group, val, btn) {
      pick[group] = pick[group] === val ? null : val;
      btn.parentNode.querySelectorAll('.picker-chip').forEach(b => b.classList.toggle('active', b.dataset.v === pick[group]));
      renderPicks();
    }
    function pickList() {
      let list = productsData.filter(p => !p.is_price_on_request);
      const w = pick.who;
      if (w === 'couples') list = list.filter(p => p.cat.includes('couples'));
      else if (w === 'service') list = list.filter(p => p.cat.includes('service'));
      else if (w) list = list.filter(p => p.cat.includes('mens') && !p.cat.includes('couples'));
      if (pick.style === 'tamga') list = list.filter(p => p.cat.includes('ornament'));
      if (pick.style === 'classic') list = list.filter(p => p.cat.includes('mens') && !p.cat.includes('ornament') && !p.cat.includes('service') && !p.cat.includes('mechanic') && !p.cat.includes('couples'));
      if (pick.style === 'mech') list = list.filter(p => p.cat.includes('mechanic'));
      if (pick.style === 'box') list = list.filter(p => p.cat.includes('woodbox'));
      return list.filter(p => pickBudgetOk(p.price));
    }
    function renderPicks() {
      const box = document.getElementById('pickResults'); if (!box) return;
      const any = pick.who || pick.occ || pick.style || pick.budget;
      const chosen = (pick.who || pick.style || pick.budget) ? pickList().slice(0, 4) : PICK_DEFAULT.map(id => byId(id)).filter(Boolean);
      const tipEl = document.getElementById('pickTip');
      if (tipEl) tipEl.textContent = pick.occ ? tt('tips')[pick.occ] : '';
      if (!chosen.length) box.innerHTML = '<div class="picker-empty">' + tt('pick_empty') + '</div>';
      else box.innerHTML = chosen.map(p => `<div class="pick-card" onclick="openProductModal('${p.id}')">
          <button type="button" class="fav-btn${inSel(p.id) ? ' on' : ''}" data-fav="${p.id}" onclick="event.stopPropagation();toggleSel('${p.id}')" aria-label="Favourite">♥</button>
          <img src="${p.img}" alt="${pf(p, 'name')}" loading="lazy">
          <div class="pick-card-body"><div class="pick-card-name">${pf(p, 'name')}</div><div class="pick-card-price">${money(p.price)}</div>
          <div class="pick-card-inst">${tt('pick_inst')(Math.floor(p.price / 12).toLocaleString('ru-RU'))}</div>
          <button type="button" class="pick-card-btn">${tt('buy')}</button></div></div>`).join('');
      const wa = document.getElementById('pickWa');
      if (wa) wa.href = waLink(tt('wa_pick4')(tt('pw')[pick.who || 'none'], tt('po')[pick.occ || 'none'], tt('ps')[pick.style || 'none'], tt('bud')[pick.budget || 'none']));
      window.__lastPicks = chosen;
    }
    function addPicksToSel() { (window.__lastPicks || []).forEach(p => { if (!inSel(p.id)) SEL.push({ id: p.id, text: '' }); }); saveSel(); syncSel(); openCart(); }
    function applyPickToCatalog() {
      let cat = 'all';
      if (pick.who === 'couples') cat = 'couples'; else if (pick.who === 'service') cat = 'service'; else if (pick.who) cat = 'mens';
      else if (pick.style === 'tamga') cat = 'ornament'; else if (pick.style === 'mech') cat = 'mechanic'; else if (pick.style === 'box') cat = 'woodbox';
      const tab = document.querySelector('[data-filter="' + cat + '"]'); if (tab) setCategoryFilter(cat, tab);
      const idx = { t1: 1, t2: 2, t3: 3, t4: 4 }[pick.budget] || 0; const chips = document.querySelectorAll('.price-chip');
      if (chips[idx]) setPriceFilter(pick.budget || 'all', chips[idx]);
      document.getElementById('catalog').scrollIntoView({ behavior: 'smooth' });
    }

    function renderFeatures() { ensureHearts(); syncSel(); renderAsk(); renderCart(); ensureModalExtras(); }
'''
