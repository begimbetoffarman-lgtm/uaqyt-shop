# -*- coding: utf-8 -*-
import os, json, re

products = [
    {
        'id': 'p26900_karakerey',
        'name': '«Болат / Қаракерей»',
        'cat': 'mens ornament',
        'price': 26900,
        'tag': 'Минералды • Кварц',
        'desc': 'Алтын жалатылған корпус, қоңыр табиғи былғары бау, Қаракерей руының таңбасы мен есімі.',
        'img': './images/watch-26900-karakerey.jpg',
        'badge': 'Бастапқы баға'
    },
    {
        'id': 'p27900_shekara',
        'name': '«ҰҚК Шекара қызметі»',
        'cat': 'service mens',
        'price': 27900,
        'tag': 'Қызметтік • ҰҚК',
        'desc': 'ҚР ҰҚК Шекара қызметінің ресми эмблемасымен жасалған тот баспайтын болат сағат.',
        'img': './images/watch-27900-shekara-knb.jpg',
        'badge': 'ҰҚК • КНБ'
    },
    {
        'id': 'p27900_zhasulan',
        'name': '«Жасұлан» классикалық болат',
        'cat': 'mens',
        'price': 27900,
        'tag': 'Классика • Болат',
        'desc': 'Қара циферблаттағы ақ таңбалы есім, классикалық болат бау, сызатқа төзімді шыны.',
        'img': './images/watch-27900-zhasulan.jpg',
        'badge': 'Классика'
    },
    {
        'id': 'p34900_nayman',
        'name': '«Найман / Болатшы» Two-Tone',
        'cat': 'mens ornament',
        'price': 34900,
        'tag': 'Комби • Ою-өрнек',
        'desc': 'Алтын мен күміс үйлесімі (Two-Tone), Найман руының алтын түсті оюлы эмблемасы.',
        'img': './images/watch-34900-nayman.jpg',
        'badge': 'Two-Tone'
    },
    {
        'id': 'p34900_mangytay',
        'name': '«Маңғытай / Марлен» Jubilee',
        'cat': 'mens ornament',
        'price': 34900,
        'tag': 'Юбилейный • Ою',
        'desc': 'Дөңгелек ою-өрнекті циферблат, сызатқа төзімді минералды шыны, Jubilee болат бау.',
        'img': './images/watch-34900-mangytay.jpg',
        'badge': 'Хит үлгі'
    },
    {
        'id': 'p36900_azamat',
        'name': '«Азамат» Араб каллиграфиясы',
        'cat': 'mens',
        'price': 36900,
        'tag': 'Каллиграфия • Изумруд',
        'desc': 'Шығыстық араб өрнектері мен жеке есім, күміс корпус, изумруд сыйлық қорабында.',
        'img': './images/watch-36900-azamat-calligraphy.jpg',
        'badge': 'Изумруд бокс'
    },
    {
        'id': 'p37900_shapyrashty',
        'name': '«Аймұрат / Шапырашты» Оюлы алтын',
        'cat': 'mens ornament',
        'price': 37900,
        'tag': 'Оюлы корпус • Алтын',
        'desc': 'Корпусы мен бауы тұтастай антикварлық қазақи оюмен өрнектелген алтын сағат.',
        'img': './images/watch-37900-shapyrashty-carved.jpg',
        'badge': 'Толық оюланған'
    },
    {
        'id': 'p37900_tolengit',
        'name': '«Жандос / Төлеңгіт» Оюлы күміс',
        'cat': 'mens ornament',
        'price': 37900,
        'tag': 'Оюлы корпус • Күміс',
        'desc': 'Корпусы мен бауына лазерлік ою ойылған асыл күміс түсті мәртебелі сағат.',
        'img': './images/watch-37900-tolengit-silver.jpg',
        'badge': 'Толық оюланған'
    },
    {
        'id': 'p38900_mvd',
        'name': '«ІІМ Қазақстан / Абдуллин А.Д.»',
        'cat': 'service mens woodbox',
        'price': 38900,
        'tag': 'ІІМ • Ұзын ағаш футляр',
        'desc': 'Ішкі істер министрлігінің ресми эмблемасы, қызметкердің тегі, көбелек қысқышты былғары бау.',
        'img': './images/watch-38900-mvd-abdullin.jpg',
        'badge': 'ІІМ • МВД'
    },
    {
        'id': 'p39900_aday',
        'name': '«Бағлан / Адай» Алтын сағат',
        'cat': 'mens ornament',
        'price': 39900,
        'tag': 'Ұлттық нақыш • Алтын',
        'desc': 'Адай руының таңбасы, ұлттық ою-өрнек, алтын түсті болат бау және брендтік UAQYT пакеті.',
        'img': './images/watch-39900-aday-gold.jpg',
        'badge': 'Top Choice'
    },
    {
        'id': 'p39900_couples',
        'name': '1+1 Жұптық жиынтық «Мәдихан ❤️ Зәуре»',
        'cat': 'couples',
        'price': 39900,
        'tag': '1+1 Жұптық • Раушан гүлдер',
        'desc': 'Ерлер мен әйелдер сағаты + 6 қызыл раушан гүлі бар сыйлық қорабы + брендтік UAQYT пакеті.',
        'img': './images/watch-39900-couples-roses.jpg',
        'badge': '❤️ 1+1 Жұптық'
    },
    {
        'id': 'p39900_alshyn',
        'name': '«Данияр / Алшын» Изумруд бокс',
        'cat': 'mens ornament',
        'price': 39900,
        'tag': 'Былғары бау • Изумруд',
        'desc': 'Алшын руының қасиетті таңбасы, оюлы күміс безель, қара табиғи былғары бау.',
        'img': './images/watch-39900-alshyn.jpg',
        'badge': 'Изумруд бокс'
    },
    {
        'id': 'p39900_nautilus',
        'name': '«Авазматов / Бахадур» Nautilus',
        'cat': 'mens',
        'price': 39900,
        'tag': 'Nautilus • Күміс',
        'desc': 'Жастық тәріздес Nautilus корпусы, күміс болат бау, изумруд түсті сыйлық қорабы.',
        'img': './images/watch-39900-nautilus-bakhadur.jpg',
        'badge': 'Nautilus'
    },
    {
        'id': 'p41900_lion',
        'name': '«Нұрдәулет» Royal Lion Stealth',
        'cat': 'mens',
        'price': 41900,
        'tag': 'Stealth Black • Тәжді арыстан',
        'desc': 'Тәж киген арыстан мен лавр жапырағы, қара матовый сатинирленген болат корпус.',
        'img': './images/watch-41900-lion-black.jpg',
        'badge': 'Stealth Black'
    },
    {
        'id': 'p52900_alban',
        'name': '«Абай / Албан» Механикалық сағат',
        'cat': 'mechanic mens woodbox ornament',
        'price': 52900,
        'tag': 'Механика • Сапфир • Футляр',
        'desc': 'Автоподзавод механизмі, сапфирлік шыны, Албан руының таңбасы, ұзын ағаш футлярда.',
        'img': './images/watch-52900-alban-mech.jpg',
        'badge': '⚙️ Механика'
    },
    {
        'id': 'p52900_royaloak',
        'name': '«Нұрланбек» Royal Oak Edition',
        'cat': 'mens',
        'price': 52900,
        'tag': 'Сапфир • Сегізқырлы',
        'desc': 'Аңызға айналған сегізқырлы безель, көк циферблаттағы грек оюы, сапфир шыны, изумруд бокс.',
        'img': './images/watch-52900-royaloak-blue.jpg',
        'badge': 'Royal Oak'
    },
    {
        'id': 'p54900_shekti',
        'name': '«Әлім / Шекті / Нұрсат» Ағаш қорапта',
        'cat': 'mens woodbox ornament',
        'price': 54900,
        'tag': 'Сапфир • Премиум ағаш',
        'desc': 'Сапфирлік шыны, соққыға төзімді, қымбат вишня ағашынан жасалған лакталған шкатулка.',
        'img': './images/watch-54900-shekti-woodbox.jpg',
        'badge': '🪵 Ағаш қорап'
    },
    {
        'id': 'p54900_tana',
        'name': '«Кіші жүз / Тана» Ағаш қорапта',
        'cat': 'mens woodbox ornament',
        'price': 54900,
        'tag': 'Сапфир • Қара корпус',
        'desc': 'Кіші жүз Тана руы, қара стильді корпус, сапфир әйнек, премиум ағаш шкатулка.',
        'img': './images/watch-54900-kishizhuz-tana.jpg',
        'badge': '🪵 Ағаш қорап'
    },
    {
        'id': 'p55900_tanatbek',
        'name': '«Ғаббасұлы Таңатбек» Елтаңбалы сағат',
        'cat': 'mens woodbox',
        'price': 55900,
        'tag': 'Елтаңба • Сапфир • Ағаш',
        'desc': 'Қазақстанның көк байрағы мен қыран бүркіт, сапфир шыны, қымбат ағаш шкатулка.',
        'img': './images/watch-55900-tanatbek-woodbox.jpg',
        'badge': 'Елтаңба'
    },
    {
        'id': 'p56900_manarbek',
        'name': '«ІІМ Manarbek» Полиция сағаты',
        'cat': 'service mens woodbox',
        'price': 56900,
        'tag': 'ІІМ • Сапфир • Ағаш қорап',
        'desc': 'ҚР Ішкі Істер Органдарының ресми жұлдызды эмблемасы, қара болат корпус, ағаш шкатулка.',
        'img': './images/watch-56900-mvd-manarbek.jpg',
        'badge': 'ІІМ • МВД'
    },
    {
        'id': 'p56900_zhangabyl',
        'name': '«Қуандық / Жанғабыл» Алтын сағат',
        'cat': 'mens woodbox ornament',
        'price': 56900,
        'tag': 'Алтын болат • Ағаш қорап',
        'desc': 'Қуандық руы, алтын түсті болат бау, сапфир әйнек, премиум лакталған ағаш қорап.',
        'img': './images/watch-56900-zhangabyl-gold.jpg',
        'badge': '🪵 Ағаш қорап'
    },
    {
        'id': 'p66900_tortkara',
        'name': '«Шыңғыс / Төртқара» Механикалық',
        'cat': 'mechanic mens woodbox ornament',
        'price': 66900,
        'tag': '⚙️ Механика • Сапфир',
        'desc': 'Әлім Төртқара руы, сегізқырлы сатинирленген қара корпус, автоподзавод механикасы, ағаш қорап.',
        'img': './images/watch-66900-tortkara-mech.jpg',
        'badge': '⚙️ Механика'
    },
    {
        'id': 'p69900_iibb',
        'name': '«ІІББ Ринат» Hublot Style Механика',
        'cat': 'service mechanic mens woodbox',
        'price': 69900,
        'tag': '⚙️ Механика • Сапфир • ІІББ',
        'desc': 'Ішкі Істер Басқармасы (ГУВД) қалқан мен қылыш эмблемасы, Hublot безелі, механикалық калибр.',
        'img': './images/watch-69900-iibb-rinat-mech.jpg',
        'badge': 'ІІББ • Механика'
    },
    {
        'id': 'p75900_argyn',
        'name': '«Дархан / Арғын» Флагмандық Механика',
        'cat': 'mechanic mens woodbox ornament',
        'price': 75900,
        'tag': '⚙️ Механика • Сапфир • Арғын',
        'desc': 'Арғын руы, ҚР қыран бүркіті, швейцар сапасындағы сапфирлік шыны, табиғи ағаш шкатулка.',
        'img': './images/watch-75900-argyn-mech.jpg',
        'badge': 'Флагман Механика'
    },
    {
        'id': 'p75900_rahat',
        'name': '«Рахат Шекті / Ардана» Мерейтойлық',
        'cat': 'mechanic mens woodbox ornament',
        'price': 75900,
        'tag': '⚙️ Механика • 13.11.1979',
        'desc': 'Мерейтойға арналған автоподзаводты механикалық сағат, сапфир әйнек, қымбат ағаш қорап.',
        'img': './images/watch-75900-rahat-mech.jpg',
        'badge': 'Флагман Механика'
    },
    {
        'id': 'p75900_sharkesh',
        'name': '«Нұркен / Шәркеш» Алтын Механика',
        'cat': 'mechanic mens woodbox ornament',
        'price': 75900,
        'tag': '⚙️ Механика • Медициналық сталь',
        'desc': 'Медициналық болаттан соғылған алтын корпус, Шәркеш руының оюы, автоподзавод калибрі.',
        'img': './images/watch-75900-sharkesh-goldmech.jpg',
        'badge': 'Флагман Механика'
    }
]

# Sort ascending by price: cheap to expensive!
products = sorted(products, key=lambda x: x['price'])

card_template = """
        <!-- Card: {name} ({price} KZT) -->
        <div class="product-card" data-category="{cat}" data-price="{price}" data-name="{name}">
          <div class="card-badge">{badge}</div>
          <div class="card-img-box">
            <img src="{img}" alt="{name}">
          </div>
          <div class="card-body">
            <div class="card-category-tag">{tag}</div>
            <h3 class="card-title">{name}</h3>
            <p class="card-desc">{desc}</p>
            <div class="card-footer">
              <span class="card-price">{price_str} ₸</span>
              <button class="btn-card-action" onclick="openOrderModal('{name}', {price}, '{img}')">
                Тапсырыс беру
              </button>
            </div>
          </div>
        </div>
"""

cards_html = []
for p in products:
    price_str = f"{p['price']:,}".replace(',', ' ')
    c = card_template.format(
        id=p['id'],
        name=p['name'],
        cat=p['cat'],
        price=p['price'],
        price_str=price_str,
        tag=p['tag'],
        desc=p['desc'],
        img=p['img'],
        badge=p['badge']
    )
    cards_html.append(c)

all_cards_str = "\n".join(cards_html)

# Update index.html
html_path = r'D:\watch-boutique\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace product grid
pattern = r'(<div class="product-grid" id="productGrid">)([\s\S]*?)(</div>\s*<!-- Departmental Special Banner -->)'
match = re.search(pattern, content)
if match:
    new_grid = match.group(1) + "\n" + all_cards_str + "\n      " + match.group(3)
    content = content[:match.start()] + new_grid + content[match.end():]
    print('Product grid replaced successfully!')
else:
    print('ERROR: Product grid pattern not found!')

# Update counter default
content = content.replace('5 модель табылды', f'{len(products)} модель табылды (арзаннан қымбатқа)')

# Also add Real WhatsApp Review Screenshot in reviews section
review_block = """
      <!-- Real WhatsApp Review Card with Screenshot -->
      <div class="review-card" style="grid-column: span 1; border: 1.5px solid var(--accent-gold);">
        <div class="review-header">
          <div class="reviewer-info">
            <h4 style="display:flex; align-items:center; gap:6px;">Матлуба (Алматы) <span style="font-size:11px; background:#dcfce7; color:#166534; padding:2px 8px; border-radius:10px;">Расталған сатып алушы</span></h4>
            <div class="reviewer-meta">WhatsApp арқылы жеткізілді • Бүгін</div>
          </div>
          <span class="source-tag" style="background:#25D366; color:#fff;">WhatsApp</span>
        </div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text" style="font-style:italic; font-weight:500;">
          «Сәлеметсізбе! Алдым заказымды, рахмет! Көп-көп клиенттеріңіз көп болсын! 🥰 Жұптық сағат өте әдемі шығыпты: «Шынар / Кіші жүз» және «Әділбек / Кіші жүз». Яндекс доставкамен тез жеткізді!»
        </p>
        <div style="margin: 10px 0; border-radius: 12px; overflow: hidden; max-height: 240px; border: 1px solid var(--border);">
          <img src="./images/reviews/review-matluba.jpg" alt="WhatsApp отзыв Матлуба" style="width: 100%; object-fit: cover; object-position: center bottom;">
        </div>
        <div class="review-product-tag">Тапсырыс: Жұптық сағаттар (Кіші жүз)</div>
      </div>
"""

# Insert review block into reviews-rail
content = content.replace('<div class="reviews-rail">', '<div class="reviews-rail">\n' + review_block)

# Update category chips to include Mechanic
chips_old = """<button class="chip-btn active" onclick="filterCategory('all', this)">Барлық топтама</button>
          <button class="chip-btn" onclick="filterCategory('service', this)">🛡️ Қызметтік / Госслужба (МВД, КНБ, МЧС)</button>
          <button class="chip-btn" onclick="filterCategory('couples', this)">❤️ Жұптық сағаттар (Парные)</button>
          <button class="chip-btn" onclick="filterCategory('mens', this)">Ерлер сағаты (Мужские)</button>
          <button class="chip-btn" onclick="filterCategory('woodbox', this)">🪵 Ағаш қораппен (Премиум)</button>
          <button class="chip-btn" onclick="filterCategory('ornament', this)">Қазақи ою-өрнекпен</button>"""

chips_new = f"""<button class="chip-btn active" onclick="filterCategory('all', this)">Барлық топтама ({len(products)})</button>
          <button class="chip-btn" onclick="filterCategory('service', this)">🛡️ Қызметтік / Органдарға (МВД, ҰҚК, ТЖМ)</button>
          <button class="chip-btn" onclick="filterCategory('couples', this)">❤️ Жұптық сағаттар (1+1 Раушан)</button>
          <button class="chip-btn" onclick="filterCategory('mens', this)">Ерлер сағаты</button>
          <button class="chip-btn" onclick="filterCategory('mechanic', this)">⚙️ Механикалық сағаттар</button>
          <button class="chip-btn" onclick="filterCategory('woodbox', this)">🪵 Ағаш қораптағы люкс</button>
          <button class="chip-btn" onclick="filterCategory('ornament', this)">❖ Ұлттық ою / Шежіре-Ру</button>"""

content = content.replace(chips_old, chips_new)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html successfully!')
