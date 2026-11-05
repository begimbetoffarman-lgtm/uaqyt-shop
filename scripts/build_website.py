# -*- coding: utf-8 -*-
import os, sys, json

sys.path.insert(0, os.path.dirname(__file__))
sys.stdout.reconfigure(encoding='utf-8')

from compile_data import all_products_sorted, customer_reviews, mens_all, couples_all, priced_products, request_products
from i18n_products import PROD_RU, STRAP_RU, BRAND_SWAP, ru_piece_join
from i18n_faq import FAQ_SECTION, CSS_FAQ, JS_FAQ, BONUS_GALLERY, CSS_BONUS
from i18n_blocks import bi, LANG_SWITCH, RIBBON, HOLIDAY_SECTION, STORY_SECTION, CSS_EXTRA, JS_EXTRA
from i18n_features import PICKER_SECTION, DOCK_HTML, CART_HTML, CSS_FEATURES, JS_FEATURES
import i18n_engine

# Review screenshots that show other people's phone numbers / delivery documents are not published
PRIVATE_REVIEW_IMGS = ("review-2.jpg", "review-4.jpg", "review-7.jpg", "review-8.jpg", "review-11.jpg")
customer_reviews = [r for r in customer_reviews if not r["img"].endswith(PRIVATE_REVIEW_IMGS)]

# Single source of truth for contact data
WA = "77079781857"          # WhatsApp number used on every button (change here only)
WA_DISP = "+7 707 978 18 57"
JS_EXTRA_WA = JS_EXTRA.replace("    // if the browser blocks autoplay", JS_FEATURES + JS_FAQ + "\n    // if the browser blocks autoplay", 1).replace("__WA__", WA)

# Only facts confirmed by the owner's photos are shown on the site
def _clean_text(t):
    if not isinstance(t, str):
        return t
    for a, b in [("316L ", ""), ("316L", "болат"), (" (Miyota)", ""), ("Жапондық дәл ", ""), ("Жапондық ", ""),
                 ("ресми зауыттық кепілдік", "кепілдік"), ("1000+ видео мен фото", "жаңа жұмыстар мен пікірлер")]:
        t = t.replace(a, b)
    return t

for _p in list(all_products_sorted):
    is_mech = "mechanic" in _p.get("cat", "")
    _p["mech"] = "Механика" if is_mech else "Кварц"
    _p["glass"] = "Сапфирлік шыны, соққыға төзімді" if (is_mech or _p.get("sapphire")) else "Минералды шыны, сызатқа төзімді"
    _old_case = (_p.get("case") or "").lower()
    _p["case"] = "Алтын түсті корпус" if "алтын" in _old_case else "Болат корпус"
    _p["water"] = "WhatsApp-та нақтылаймыз"
    for _k in ("desc", "name", "tag", "strap"):
        if _k in _p:
            _p[_k] = _clean_text(_p[_k])

# Kazakh copy fixes: no third-party brand names, no unverifiable claims
KK_FIX = {
    "p39900_nautilus": {"name": "«Баһадүр» көк циферблат", "badge": "Көк циферблат", "tag": "Көк циферблат • Араб өрнегі",
                        "desc": "Спорт-элегант корпусы, көлденең сызықты көк циферблат, араб каллиграфиясы."},
    "p69900_iibb": {"name": "«ІІББ» Механика", "desc": "Ішкі Істер Басқармасының қалқан мен қылыш эмблемасы, бұрандалы безель, механикалық калибр."},
    "p39900_aday": {"desc": "Кіші жүз Адай руының жебе таңбасы, сегізқырлы безель, қара циферблаттағы алтын жазу."},
    "showcase_baglan": {"desc": "Сегізқырлы корпус, алтын таңба, сары алтын жылтыры, фирмалық сыйлық қаптамасы."},
    "p75900_argyn": {"desc": "Арғын руы, ҚР қыран бүркіті, сапфир әйнек, табиғи ағаш қобдиша."},
    "p75900_rahat_showcase": {"desc": "Көк циферблаттағы күн мен қыран, мерейтойлық жазу, безель, қымбат вишня қобдишасы."},
    "p66900_tortkara": {"desc": "Әлім Төртқара руы, сегізқырлы қара корпус, механикалық калибр, ағаш қорап."},
    "p75900_sharkesh": {"desc": "Медициналық болаттан жасалған алтын түсті корпус, Шәркеш руының оюы, механикалық калибр."},
}
for _p in all_products_sorted:
    for _k in ("name", "badge", "tag", "desc"):
        v = _p.get(_k)
        if isinstance(v, str):
            for a, b in BRAND_SWAP:
                v = v.replace(a, b)
            v = v.replace("матовый ", "").replace("Комбинирленген", "Аралас түсті").replace("шкатулкасында", "қобдишасында").replace("шкатулка", "қобдиша").replace("Шкатулка", "Қобдиша").replace("Алтын жалатылған", "Алтын түсті").replace("алтын жалатылған", "алтын түсті").replace("жалатылған", "түсті")
            _p[_k] = " ".join(v.split())
    for _k, v in KK_FIX.get(_p["id"], {}).items():
        _p[_k] = v
    _r = PROD_RU.get(_p["id"], (None, None))
    _mech = "mechanic" in _p.get("cat", "")
    _gold = "алтын" in (_p.get("case") or "").lower()
    _p["ru"] = {
        "name": _r[0] or _p["name"],
        "desc": _r[1] or _p["desc"],
        "badge": ru_piece_join(_p["badge"]),
        "tag": (_r[2] if len(_r) > 2 and _r[2] else ru_piece_join(_p["tag"])),
        "strap": STRAP_RU.get(_p.get("strap"), _p.get("strap")),
        "mech": "Механика" if _mech else "Кварц",
        "glass": "Сапфировое стекло, ударопрочное" if (_mech or _p.get("sapphire")) else "Минеральное стекло, стойкое к царапинам",
        "case": "Золотистый корпус" if _gold else "Стальной корпус",
    }

_prices = [p["price"] for p in priced_products]
T1 = sum(1 for x in _prices if x < 30000)
T2 = sum(1 for x in _prices if 30000 <= x < 40000)
T3 = sum(1 for x in _prices if 40000 <= x < 55000)
T4 = sum(1 for x in _prices if x >= 55000)

print(f"Loaded {len(all_products_sorted)} products (Men: {len(mens_all)}, Couples: {len(couples_all)}) and {len(customer_reviews)} reviews.")

# JSON dump for frontend interactive search and modal lookup
products_json = json.dumps(all_products_sorted, ensure_ascii=False)
reviews_json = json.dumps([{"img": r["img"]} for r in customer_reviews], ensure_ascii=False)

def generate():
    # Generate cards HTML
    cards_html = []
    for p in all_products_sorted:
        is_req = p.get('is_price_on_request', False)
        pid = p['id']
        name = p['name']
        cat = p['cat']
        tag = p['tag']
        desc = p['desc']
        img = p['img']
        badge = p['badge']
        
        if is_req:
            price_val = 999999
            price_display = '<span class="price-request-badge">Бағасын нақтылау</span>'
            installment_html = '''
            <div class="installment-pill req" title="Жеке жиынтыққа қарай есептеледі">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
              <span>WhatsApp-та бағасын нақтылау</span>
            </div>'''
            btn_html = f'''
            <button class="btn-card-action btn-req" onclick="openProductModal('{pid}')">
              <span>Бағасын білу</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </button>'''
        else:
            price_val = p['price']
            price_str = f"{p['price']:,}".replace(',', ' ')
            monthly = f"{p['price'] // 12:,}".replace(',', ' ')
            price_display = f'<span class="card-price">{price_str} ₸</span>'
            installment_html = f'''
            <div class="installment-pill" title="Бөліп төлеу мүмкіндігі">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
              <span>Бөліп төлеу: айына <strong>{monthly} ₸</strong></span>
            </div>'''
            btn_html = f'''
            <button class="btn-card-action" onclick="openProductModal('{pid}')">
              <span>Сатып алу</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </button>'''

        card = f'''
        <div class="product-card" data-category="{cat}" data-price="{price_val}" data-id="{pid}" onclick="openProductModal('{pid}')">
          <div class="card-badge">{badge}</div>
          <div class="card-img-box" title="Толық көру үшін басыңыз">
            <img src="{img}" alt="{name}" loading="lazy">
            <span class="zoom-hint">✨ Толығырақ көру</span>
          </div>
          <div class="card-body">
            <div class="card-category-tag">{tag}</div>
            <h3 class="card-title">{name}</h3>
            <p class="card-desc">{desc}</p>
            {installment_html}
            <div class="card-footer">
              {price_display}
              {btn_html}
            </div>
          </div>
        </div>'''
        cards_html.append(card)

    all_cards_str = "\n".join(cards_html)

    # Generate customer reviews cards HTML
    review_cards_html = []
    for idx, r in enumerate(customer_reviews):
        rev_id = r['id']
        author = r['author']
        city = r['city']
        order = r['order']
        quote = r['quote']
        img = r['img']
        tag = r['tag']
        badge = r['badge']

        # Determine filter category
        rev_cat = 'whatsapp'
        if '1+1' in order or 'жұптық' in order.lower():
            rev_cat += ' couples'
        if 'іім' in order.lower() or 'ұқк' in order.lower() or 'қызмет' in order.lower():
            rev_cat += ' service'
        if 'ру' in tag.lower() or 'таңба' in tag.lower() or 'руы' in tag.lower():
            rev_cat += ' ornament'

        rcard = f'''
        <div class="review-card" onclick="openReviewLightbox({idx})">
          <div class="review-img-wrapper" title="Үлкейтіп оқу үшін басыңыз">
            <img src="{img}" alt="Клиенттің WhatsApp пікірі" loading="lazy">
            <div class="review-overlay-hover">
              <span class="review-read-pill">🔍 Скриншотты толық оқу</span>
            </div>
          </div>
        </div>'''
        review_cards_html.append(rcard)

    all_reviews_str = "\n".join(review_cards_html)

    # Let's write the complete HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>UAQYT — Жеке жазуы бар есімді сағаттар бутигі | Сайран Сити 320</title>
  <meta name="description" content="UAQYT — жеке есім мен шежіре-ру таңбалары, қызметтік органдардың (ІІМ, ҰҚК, ТЖМ, ҚР ҚК) ресми эмблемалары қашалған мәртебелі қол сағаттар бутигі. 1 сатып алсаңыз — 2-ші сағат ТЕГІН!">
  <link rel="icon" href="./favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="./images/favicon-192.png">
  <link rel="apple-touch-icon" href="./images/apple-touch-icon.png">
  <meta name="theme-color" content="#0f172a">
  <link rel="canonical" href="https://uaqyt-shop.vercel.app/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="UAQYT">
  <meta property="og:title" content="UAQYT: именные часы с гравировкой в Алматы">
  <meta property="og:description" content="Имя, дата или родовая тамга на циферблате. Доставка по Казахстану. От 25 900 ₸ вторые часы в подарок.">
  <meta property="og:url" content="https://uaqyt-shop.vercel.app/">
  <meta property="og:image" content="https://uaqyt-shop.vercel.app/images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Store", "name": "UAQYT", "description": "Именные часы с гравировкой: имя, дата или родовая тамга на циферблате. Алматы, доставка по Казахстану.", "url": "https://uaqyt-shop.vercel.app/", "image": "https://uaqyt-shop.vercel.app/images/og-image.jpg", "telephone": "+77079781857", "address": {{"@type": "PostalAddress", "streetAddress": "ул. Утеген батыра 11а, БЦ «Сайран Сити», офис 320", "addressLocality": "Алматы", "addressCountry": "KZ"}}, "openingHoursSpecification": [{{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "10:00", "closes": "20:00"}}], "sameAs": ["https://www.instagram.com/uaqyt.kzt"]}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #ffffff;
      --bg-alt: #f8f9fa;
      --bg-card: #ffffff;
      --border: #e9ecef;
      --border-focus: #c5a880;
      --border-gold: rgba(184, 142, 79, 0.35);
      --text: #111827;
      --text-muted: #6b7280;
      --accent-gold: #b88e4f;
      --accent-gold-soft: #fbf7ee;
      --accent-gold-dark: #8c682e;
      --accent-green: #25D366;
      --accent-green-dark: #128C7E;
      --accent-red: #e11d48;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
      --shadow-md: 0 10px 30px rgba(0,0,0,0.06);
      --shadow-lg: 0 20px 45px rgba(0,0,0,0.09);
      --font-serif: 'Cormorant Garamond', Georgia, serif;
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --nav-height: 70px;
      --transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.6;
      overflow-x: hidden;
    }}

    ::selection {{
      background: var(--accent-gold-soft);
      color: var(--accent-gold-dark);
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    /* ───────── TOP BAR: ANNOUNCEMENT & 2GIS ───────── */
    .pitch-banner {{
      background: #fdfaf3;
      border-bottom: 1px solid rgba(184, 142, 79, 0.25);
      padding: 9px 24px;
      font-size: 13px;
      color: var(--accent-gold-dark);
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      z-index: 101;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .pitch-left {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .pitch-badge {{
      background: var(--accent-gold);
      color: #fff;
      padding: 3px 9px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .pitch-text strong {{
      color: #724c16;
    }}

    .pitch-right {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .pitch-2gis-link {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      color: #0284c7;
      font-weight: 600;
      transition: var(--transition);
      background: #f0f9ff;
      padding: 3px 10px;
      border-radius: 12px;
      border: 1px solid #bae6fd;
    }}

    .pitch-2gis-link:hover {{
      background: #e0f2fe;
      transform: translateY(-1px);
    }}

    .pitch-social-link {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      transition: var(--transition);
    }}

    .pitch-social-link:hover {{
      color: var(--accent-gold);
    }}

    /* ───────── NAVBAR ───────── */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
      height: var(--nav-height);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 32px;
      transition: var(--transition);
    }}

    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }}

    .brand-logo-img {{
      width: 44px;
      height: 44px;
      border-radius: 10px;
      object-fit: cover;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: transform 0.25s ease;
      flex-shrink: 0;
    }}

    .brand-logo-img:hover {{
      transform: scale(1.05);
    }}

    .brand-logo-mark {{
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, #fdf8ef 0%, #f6e8d2 100%);
      border: 1.5px solid var(--accent-gold);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--accent-gold);
      box-shadow: 0 4px 12px rgba(184, 142, 79, 0.15);
    }}

    .brand-text {{
      display: flex;
      flex-direction: column;
    }}

    .brand-name {{
      font-family: var(--font-serif);
      font-size: 26px;
      font-weight: 700;
      letter-spacing: 2px;
      color: var(--text);
      line-height: 1;
    }}

    .brand-sub {{
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--accent-gold);
      font-weight: 700;
      margin-top: 2px;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 28px;
      list-style: none;
    }}

    .nav-link {{
      white-space: nowrap;
      font-size: 14px;
      font-weight: 500;
      color: var(--text);
      transition: var(--transition);
      position: relative;
    }}

    .nav-link:hover {{
      color: var(--accent-gold);
    }}

    .nav-link.highlight {{
      color: var(--accent-red);
      font-weight: 700;
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn-nav-2gis {{
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      color: #166534;
      padding: 8px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: var(--transition);
    }}

    .btn-nav-2gis:hover {{
      background: #dcfce7;
      transform: translateY(-1px);
    }}

    .btn-nav-whatsapp {{
      background: var(--accent-green);
      color: #fff;
      padding: 9px 18px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(37, 211, 102, 0.3);
      transition: var(--transition);
      border: none;
      cursor: pointer;
    }}

    .btn-nav-whatsapp:hover {{
      background: var(--accent-green-dark);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
    }}

    /* ───────── HERO SECTION ───────── */
    .hero {{
      padding: 60px 32px 70px;
      max-width: 1320px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 48px;
      align-items: center;
    }}

    .hero-tag-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--accent-gold-soft);
      border: 1px solid var(--border-gold);
      padding: 6px 14px;
      border-radius: 20px;
      color: var(--accent-gold-dark);
      font-size: 12.5px;
      font-weight: 700;
      letter-spacing: 0.5px;
      margin-bottom: 20px;
    }}

    .hero-title {{
      font-family: var(--font-serif);
      font-size: 56px;
      font-weight: 700;
      line-height: 1.1;
      letter-spacing: -0.5px;
      color: var(--text);
      margin-bottom: 20px;
    }}

    .hero-title span {{
      color: var(--accent-gold);
      font-style: italic;
    }}

    .hero-lead {{
      font-size: 18px;
      line-height: 1.65;
      color: var(--text-muted);
      margin-bottom: 32px;
      max-width: 580px;
    }}

    .hero-perks-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 36px;
    }}

    .perk-card {{
      background: var(--bg-alt);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      text-align: left;
    }}

    .perk-icon {{
      font-size: 20px;
      margin-bottom: 6px;
      display: block;
    }}

    .perk-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 2px;
    }}

    .perk-desc {{
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.35;
    }}

    .hero-cta-group {{
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .btn-hero-primary {{
      background: var(--text);
      color: #fff;
      padding: 15px 30px;
      border-radius: 30px;
      font-size: 15px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      transition: var(--transition);
      box-shadow: var(--shadow-md);
    }}

    .btn-hero-primary:hover {{
      background: #000;
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
    }}

    .btn-hero-secondary {{
      background: #fff;
      color: var(--text);
      border: 1.5px solid var(--border);
      padding: 14px 26px;
      border-radius: 30px;
      font-size: 15px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
    }}

    .btn-hero-secondary:hover {{
      border-color: var(--accent-gold);
      color: var(--accent-gold-dark);
      transform: translateY(-2px);
    }}

    /* Hero Left: Prominent Social Strip (Instagram & TikTok) */
    .hero-social-strip {{
      margin-top: 26px;
      padding-top: 20px;
      border-top: 1px dashed rgba(184, 142, 79, 0.28);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .hero-social-label {{
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }}

    .hero-social-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .hero-social-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 18px;
      border-radius: 999px;
      font-size: 13.5px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.25s ease;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }}

    .hero-social-badge.insta {{
      background: linear-gradient(135deg, #fdf2f8 0%, #fff1f2 100%);
      color: #be185d;
      border: 1px solid rgba(225, 29, 72, 0.25);
    }}

    .hero-social-badge.insta:hover {{
      background: linear-gradient(135deg, #fce7f3 0%, #ffe4e6 100%);
      transform: translateY(-2px);
      box-shadow: 0 4px 14px rgba(225, 29, 72, 0.25);
    }}

    .hero-social-badge.tiktok {{
      background: #0f172a;
      color: #ffffff;
      border: 1px solid #1e293b;
    }}

    .hero-social-badge.tiktok:hover {{
      background: #020617;
      transform: translateY(-2px);
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.35);
    }}

    /* Hero Right: Luxury Watch Showcase Card (Replaces CSS clock with genuine photo) */
    .hero-showcase-card {{
      background: linear-gradient(160deg, #ffffff 0%, #faf8f5 100%);
      border: 1px solid rgba(184, 142, 79, 0.25);
      border-radius: 28px;
      padding: 22px;
      box-shadow: 0 20px 45px -15px rgba(184, 142, 79, 0.18), 0 4px 16px rgba(0, 0, 0, 0.04);
      position: relative;
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: all 0.3s ease;
    }}

    .hero-showcase-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }}

    .hero-showcase-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .hero-showcase-logo-img {{
      width: 34px;
      height: 34px;
      border-radius: 8px;
      object-fit: cover;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }}

    .hero-showcase-brand-meta {{
      display: flex;
      flex-direction: column;
      text-align: left;
    }}

    .hero-showcase-brand-meta span {{
      font-family: var(--font-serif);
      font-size: 15px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.1;
      letter-spacing: 0.5px;
    }}

    .hero-showcase-brand-meta small {{
      font-size: 10px;
      color: var(--accent-gold-dark);
      font-weight: 600;
      letter-spacing: 0.5px;
    }}

    .hero-showcase-badge {{
      background: linear-gradient(135deg, #e11d48, #be123c);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: 20px;
      letter-spacing: 0.5px;
      box-shadow: 0 4px 12px rgba(225, 29, 72, 0.25);
      animation: pulse 2s infinite;
      white-space: nowrap;
    }}

    .hero-showcase-visual {{
      position: relative;
      border-radius: 20px;
      overflow: hidden;
      background: radial-gradient(circle at center, #ffffff 0%, #f3eee7 100%);
      box-shadow: inset 0 0 0 1px rgba(184, 142, 79, 0.18);
      max-height: 360px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }}

    .hero-showcase-visual img {{
      width: 100%;
      height: 100%;
      max-height: 360px;
      object-fit: cover;
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .hero-showcase-visual:hover img {{
      transform: scale(1.04);
    }}

    .hero-showcase-visual-overlay {{
      position: absolute;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(17, 24, 39, 0.78);
      backdrop-filter: blur(8px);
      color: #fff;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 6px;
      opacity: 0.9;
      transition: opacity 0.2s ease;
      white-space: nowrap;
    }}

    .hero-showcase-visual:hover .hero-showcase-visual-overlay {{
      opacity: 1;
      background: rgba(17, 24, 39, 0.95);
    }}

    .hero-showcase-info {{
      text-align: left;
    }}

    .hero-showcase-tag {{
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-gold-dark);
      letter-spacing: 0.5px;
      margin-bottom: 2px;
    }}

    .hero-showcase-title {{
      font-family: var(--font-serif);
      font-size: 20px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 4px;
      line-height: 1.25;
    }}

    .hero-showcase-desc {{
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 12px;
      line-height: 1.4;
    }}

    .hero-showcase-thumbs {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }}

    .hero-thumb-btn {{
      background: #fff;
      border: 1.5px solid var(--border);
      border-radius: 12px;
      padding: 6px 8px;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      text-align: left;
    }}

    .hero-thumb-btn:hover {{
      border-color: var(--accent-gold);
      background: #fdfbf7;
    }}

    .hero-thumb-btn.active {{
      border-color: var(--accent-gold);
      background: #fcf9f2;
      box-shadow: 0 0 0 2px rgba(184, 142, 79, 0.25);
    }}

    .hero-thumb-btn img {{
      width: 32px;
      height: 32px;
      border-radius: 8px;
      object-fit: cover;
      flex-shrink: 0;
    }}

    .hero-thumb-btn span {{
      font-size: 11px;
      font-weight: 600;
      color: var(--text);
      line-height: 1.2;
    }}

    /* Old visual card compatibility */
    .hero-visual-card {{
      background: linear-gradient(145deg, #ffffff 0%, #faf8f5 100%);
      border: 1px solid var(--border);
      border-radius: 28px;
      padding: 32px;
      box-shadow: var(--shadow-lg);
      text-align: center;
      position: relative;
    }}

    .hero-promo-badge {{
      position: absolute;
      top: 18px;
      right: 18px;
      background: linear-gradient(135deg, #e11d48, #be123c);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: 20px;
      letter-spacing: 0.5px;
      box-shadow: 0 4px 12px rgba(225, 29, 72, 0.3);
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.04); }}
    }}

    /* ───────── EXCLUSIVE 1+1 PROMO SECTION ───────── */
    .promo-banner-section {{
      background: linear-gradient(135deg, #fef2f2 0%, #fff1f2 100%);
      border-top: 1px solid #fecdd3;
      border-bottom: 1px solid #fecdd3;
      padding: 50px 32px;
      margin: 20px 0 60px;
    }}

    .promo-container {{
      max-width: 1200px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 40px;
      align-items: center;
    }}

    .promo-img-box {{
      position: relative;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 16px 36px rgba(225, 29, 72, 0.15);
      border: 3px solid #fff;
    }}

    .promo-img-box img {{
      width: 100%;
      height: 380px;
      object-fit: cover;
      display: block;
      transition: transform 0.5s ease;
    }}

    .promo-img-box:hover img {{
      transform: scale(1.03);
    }}

    .promo-tag {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent-red);
      color: #fff;
      font-size: 12px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 16px;
    }}

    .promo-heading {{
      font-family: var(--font-serif);
      font-size: 40px;
      font-weight: 700;
      color: #881337;
      line-height: 1.15;
      margin-bottom: 16px;
    }}

    .promo-text {{
      font-size: 16px;
      color: #9f1239;
      line-height: 1.6;
      margin-bottom: 24px;
    }}

    .promo-features {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 28px;
    }}

    .promo-feat-item {{
      background: rgba(255, 255, 255, 0.7);
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      color: #881337;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .btn-promo-action {{
      background: var(--accent-red);
      color: #fff;
      padding: 14px 28px;
      border-radius: 30px;
      font-size: 15px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 6px 18px rgba(225, 29, 72, 0.35);
      transition: var(--transition);
      border: none;
      cursor: pointer;
    }}

    .btn-promo-action:hover {{
      background: #be123c;
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(225, 29, 72, 0.45);
    }}

    /* ───────── INTERACTIVE DIAL SIMULATOR ───────── */
    .simulator-section {{
      padding: 70px 32px;
      max-width: 1200px;
      margin: 0 auto 60px;
      background: var(--bg-alt);
      border: 1px solid var(--border);
      border-radius: 28px;
    }}

    .sim-header {{
      text-align: center;
      max-width: 700px;
      margin: 0 auto 40px;
    }}

    .sim-subtitle {{
      color: var(--accent-gold);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 2px;
      font-weight: 700;
      margin-bottom: 8px;
    }}

    .sim-title {{
      font-family: var(--font-serif);
      font-size: 38px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.2;
    }}

    .sim-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 48px;
      align-items: center;
    }}

    .dial-display-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 40px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-md);
      position: relative;
    }}

    .dial-case {{
      width: 290px;
      height: 290px;
      border-radius: 50%;
      background: radial-gradient(circle at 35% 35%, #ffffff 0%, #f4f4f5 100%);
      border: 14px solid #d4af37;
      box-shadow: 0 15px 35px rgba(212, 175, 55, 0.25), inset 0 2px 10px rgba(0,0,0,0.1);
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .dial-ticks {{
      position: absolute;
      inset: 6px;
      border-radius: 50%;
      border: 1px dashed rgba(0,0,0,0.15);
    }}

    .dial-center-content {{
      text-align: center;
      z-index: 2;
      width: 180px;
    }}

    .dial-tamga-icon {{
      width: 52px;
      height: 52px;
      margin: 0 auto 8px;
      color: #92400e;
      transition: var(--transition);
    }}

    .dial-name {{
      font-family: var(--font-serif);
      font-size: 21px;
      font-weight: 700;
      color: #111827;
      letter-spacing: 1px;
      text-transform: uppercase;
      line-height: 1.1;
    }}

    .dial-sub {{
      font-size: 11px;
      color: #92400e;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-top: 3px;
    }}

    .dial-date {{
      font-size: 9.5px;
      color: #6b7280;
      letter-spacing: 1px;
      margin-top: 5px;
    }}

    /* Clock hands */
    .hand {{
      position: absolute;
      bottom: 50%;
      left: 50%;
      transform-origin: 50% 100%;
      border-radius: 4px;
    }}

    .hour-hand {{
      width: 4px;
      height: 60px;
      background: #1e293b;
      margin-left: -2px;
      transform: rotate(60deg);
      z-index: 3;
    }}

    .min-hand {{
      width: 3px;
      height: 85px;
      background: #1e293b;
      margin-left: -1.5px;
      transform: rotate(190deg);
      z-index: 4;
    }}

    .sec-hand {{
      width: 1.5px;
      height: 98px;
      background: #e11d48;
      margin-left: -0.75px;
      z-index: 5;
    }}

    .center-pin {{
      width: 10px;
      height: 10px;
      background: #d4af37;
      border: 2px solid #fff;
      border-radius: 50%;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 6;
    }}

    .sim-controls-form {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}

    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .form-label {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
    }}

    html {{ color-scheme: light; }}
    .form-input, .form-select, .search-input, .sort-select, .modal-input-engrave {{ color: #111827; background-color: #fff; }}
    .form-input::placeholder, .search-input::placeholder, .modal-input-engrave::placeholder {{ color: #9ca3af; }}
    .form-input, .form-select {{
      padding: 12px 16px;
      border: 1.5px solid var(--border);
      border-radius: 12px;
      font-family: inherit;
      font-size: 14px;
      background: #fff;
      transition: var(--transition);
    }}

    .form-input:focus, .form-select:focus {{
      outline: none;
      border-color: var(--accent-gold);
      box-shadow: 0 0 0 3px rgba(184, 142, 79, 0.15);
    }}

    .btn-apply-sim {{
      background: var(--accent-gold);
      color: #fff;
      border: none;
      padding: 14px 24px;
      border-radius: 14px;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: var(--transition);
      box-shadow: 0 4px 14px rgba(184, 142, 79, 0.25);
    }}

    .btn-apply-sim:hover {{
      background: var(--accent-gold-dark);
      transform: translateY(-2px);
    }}

    /* ───────── CATALOG SECTION ───────── */
    .catalog-section {{
      padding: 60px 32px 90px;
      max-width: 1360px;
      margin: 0 auto;
    }}

    .catalog-header {{
      text-align: center;
      margin-bottom: 36px;
    }}

    .section-subtitle {{
      color: var(--accent-gold);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 2px;
      font-weight: 700;
      margin-bottom: 8px;
    }}

    .section-title {{
      font-family: var(--font-serif);
      font-size: 42px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.2;
    }}

    .section-desc {{
      color: var(--text-muted);
      font-size: 16px;
      max-width: 620px;
      margin: 10px auto 0;
    }}

    /* Search & Filter Toolbar */
    .catalog-toolbar {{
      display: flex;
      flex-direction: column;
      gap: 20px;
      margin-bottom: 40px;
    }}

    .search-sort-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .search-box {{
      position: relative;
      flex: 1;
      max-width: 480px;
    }}

    .search-box svg {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
    }}

    .search-input {{
      width: 100%;
      padding: 12px 18px 12px 46px;
      border: 1.5px solid var(--border);
      border-radius: 30px;
      font-family: inherit;
      font-size: 14px;
      background: #fff;
      transition: var(--transition);
    }}

    .search-input:focus {{
      outline: none;
      border-color: var(--accent-gold);
      box-shadow: 0 0 0 3px rgba(184, 142, 79, 0.15);
    }}

    .sort-select {{
      padding: 12px 20px;
      border: 1.5px solid var(--border);
      border-radius: 30px;
      font-family: inherit;
      font-size: 13.5px;
      background: #fff;
      font-weight: 600;
      color: var(--text);
      cursor: pointer;
    }}

    .filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      padding-bottom: 6px;
    }}

    .filter-tabs::-webkit-scrollbar {{
      display: none;
    }}

    .filter-tab {{
      padding: 9px 18px;
      border-radius: 24px;
      background: var(--bg-alt);
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: var(--transition);
    }}

    .filter-tab:hover {{
      color: var(--text);
      border-color: #cbd5e1;
    }}

    .filter-tab.active {{
      background: var(--text);
      color: #fff;
      border-color: var(--text);
    }}

    .filter-tab.active-special {{
      background: var(--accent-red);
      color: #fff;
      border-color: var(--accent-red);
    }}

    /* Products Grid */
    .products-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 28px;
    }}

    .product-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 20px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
      transition: var(--transition);
      cursor: pointer;
    }}

    .product-card:hover {{
      transform: translateY(-6px);
      box-shadow: var(--shadow-lg);
      border-color: var(--border-gold);
    }}

    .card-badge {{
      position: absolute;
      top: 14px;
      left: 14px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-gold-dark);
      border: 1px solid rgba(184, 142, 79, 0.25);
      z-index: 2;
    }}

    .card-img-box {{
      width: 100%;
      height: 290px;
      background: #fafafa;
      position: relative;
      overflow: hidden;
    }}

    .card-img-box img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .product-card:hover .card-img-box img {{
      transform: scale(1.05);
    }}

    .zoom-hint {{
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(6px);
      color: #fff;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 14px;
      opacity: 0;
      transform: translateY(4px);
      transition: var(--transition);
    }}

    .product-card:hover .zoom-hint {{
      opacity: 1;
      transform: translateY(0);
    }}

    .card-body {{
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .card-category-tag {{
      font-size: 11.5px;
      font-weight: 700;
      color: var(--accent-gold);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }}

    .card-title {{
      font-family: var(--font-serif);
      font-size: 20px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.25;
      margin-bottom: 8px;
    }}

    .card-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 14px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .installment-pill {{
      background: #fdfaf3;
      border: 1px solid rgba(184, 142, 79, 0.25);
      border-radius: 8px;
      padding: 6px 10px;
      font-size: 11.5px;
      color: var(--accent-gold-dark);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 16px;
    }}

    .installment-pill.req {{
      background: #f0fdf4;
      border-color: #bbf7d0;
      color: #166534;
    }}

    .card-footer {{
      margin-top: auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
    }}

    .card-price {{
      font-size: 20px;
      font-weight: 800;
      color: var(--text);
      letter-spacing: -0.5px;
    }}

    .price-request-badge {{
      font-size: 13px;
      font-weight: 700;
      color: #047857;
      background: #ecfdf5;
      padding: 4px 10px;
      border-radius: 8px;
      border: 1px solid #a7f3d0;
    }}

    .btn-card-action {{
      background: var(--bg-alt);
      color: var(--text);
      border: 1.5px solid var(--border);
      padding: 8px 14px;
      border-radius: 20px;
      font-size: 12.5px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: var(--transition);
    }}

    .btn-card-action:hover {{
      background: var(--text);
      color: #fff;
      border-color: var(--text);
    }}

    .btn-card-action.btn-req {{
      background: #ecfdf5;
      color: #047857;
      border-color: #a7f3d0;
    }}

    .btn-card-action.btn-req:hover {{
      background: #047857;
      color: #fff;
    }}

    /* ───────── SOCIAL MEDIA SHOWCASE (INSTAGRAM & TIKTOK) ───────── */
    .social-section {{
      padding: 60px 32px;
      max-width: 1200px;
      margin: 0 auto 70px;
    }}

    .social-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 28px;
    }}

    .social-card {{
      border-radius: 24px;
      padding: 36px;
      color: #fff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      box-shadow: var(--shadow-lg);
      transition: var(--transition);
    }}

    .social-card:hover {{
      transform: translateY(-5px);
    }}

    .social-card.instagram {{
      background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%);
    }}

    .social-card.tiktok {{
      background: #000000;
      border: 1.5px solid #222;
    }}

    .social-card.tiktok::before {{
      content: '';
      position: absolute;
      top: -50%;
      right: -50%;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle, rgba(0, 242, 234, 0.15) 0%, transparent 70%);
      pointer-events: none;
    }}

    .social-card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
    }}

    .social-icon-box {{
      width: 54px;
      height: 54px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .social-handle {{
      font-size: 15px;
      font-weight: 700;
      background: rgba(255, 255, 255, 0.2);
      padding: 6px 14px;
      border-radius: 20px;
      backdrop-filter: blur(6px);
    }}

    .social-card-title {{
      font-family: var(--font-serif);
      font-size: 32px;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 12px;
    }}

    .social-card-desc {{
      font-size: 14.5px;
      opacity: 0.9;
      line-height: 1.55;
      margin-bottom: 28px;
    }}

    .btn-social-cta {{
      background: #fff;
      color: #000;
      padding: 12px 24px;
      border-radius: 30px;
      font-size: 14px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      align-self: flex-start;
      transition: var(--transition);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    .btn-social-cta:hover {{
      background: #f8f9fa;
      transform: scale(1.03);
    }}

    /* ───────── VERIFIED CUSTOMER REVIEWS (22 REAL WHATSAPP SCREENSHOTS) ───────── */
    .reviews-section {{
      padding: 70px 32px 90px;
      background: var(--bg-alt);
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
    }}

    .reviews-container {{
      max-width: 1360px;
      margin: 0 auto;
    }}

    .reviews-header {{
      text-align: center;
      margin-bottom: 40px;
    }}

    .rev-filter-tabs {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      margin-bottom: 36px;
      flex-wrap: wrap;
    }}

    .rev-filter-tab {{
      padding: 8px 18px;
      border-radius: 20px;
      background: #fff;
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }}

    .rev-filter-tab.active {{
      background: var(--accent-gold);
      color: #fff;
      border-color: var(--accent-gold);
    }}

    .reviews-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
      gap: 26px;
    }}

    .review-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 20px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      transition: var(--transition);
      cursor: pointer;
    }}

    .review-card:hover {{
      transform: translateY(-5px);
      box-shadow: var(--shadow-lg);
      border-color: var(--accent-gold);
    }}

    .review-status-bar {{
      padding: 10px 16px;
      background: #fdfaf3;
      border-bottom: 1px solid rgba(184, 142, 79, 0.15);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11.5px;
      color: var(--accent-gold-dark);
      font-weight: 600;
    }}

    .status-indicator {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      display: inline-block;
      margin-right: 4px;
    }}

    .review-img-wrapper {{
      width: 100%;
      height: 380px;
      background: #f1f5f9;
      position: relative;
      overflow: hidden;
    }}

    .review-img-wrapper img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      transition: transform 0.4s ease;
    }}

    .review-card:hover .review-img-wrapper img {{
      transform: scale(1.03);
    }}

    .review-overlay-hover {{
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: var(--transition);
    }}

    .review-card:hover .review-overlay-hover {{
      opacity: 1;
    }}

    .review-read-pill {{
      background: #fff;
      color: #111827;
      font-size: 13px;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: 24px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }}

    .review-content {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .review-stars {{
      color: #f59e0b;
      font-size: 14px;
      margin-bottom: 8px;
      letter-spacing: 2px;
    }}

    .review-quote {{
      font-size: 13.5px;
      line-height: 1.5;
      color: var(--text);
      font-style: italic;
      margin-bottom: 14px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .reviewer-meta-box {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: auto;
      padding-top: 10px;
      border-top: 1px solid var(--border);
    }}

    .reviewer-avatar {{
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: var(--accent-gold-soft);
      border: 1px solid var(--accent-gold);
      color: var(--accent-gold-dark);
      font-weight: 700;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .reviewer-details {{
      display: flex;
      flex-direction: column;
    }}

    .reviewer-name {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
    }}

    .reviewer-order {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    /* ───────── SHOWROOM & 2GIS SECTION ───────── */
    .showroom-section {{
      padding: 70px 32px 80px;
      max-width: 1200px;
      margin: 0 auto;
    }}

    .showroom-card {{
      background: linear-gradient(145deg, #ffffff 0%, #fbfaf8 100%);
      border: 1.5px solid var(--border-gold);
      border-radius: 28px;
      padding: 48px;
      box-shadow: var(--shadow-lg);
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 48px;
      align-items: center;
    }}

    .showroom-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent-gold-soft);
      color: var(--accent-gold-dark);
      font-size: 12px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 16px;
    }}

    .showroom-title {{
      font-family: var(--font-serif);
      font-size: 40px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.2;
      margin-bottom: 16px;
    }}

    .showroom-desc {{
      font-size: 16px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 28px;
    }}

    .info-list {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 32px;
    }}

    .info-item {{
      display: flex;
      align-items: flex-start;
      gap: 12px;
      font-size: 14px;
      color: var(--text);
    }}

    .info-item svg {{
      color: var(--accent-gold);
      flex-shrink: 0;
      margin-top: 3px;
    }}

    .showroom-cta-box {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }}

    .btn-2gis-primary {{
      background: #0284c7;
      color: #fff;
      padding: 14px 26px;
      border-radius: 30px;
      font-size: 14.5px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      box-shadow: 0 4px 16px rgba(2, 132, 199, 0.3);
    }}

    .btn-2gis-primary:hover {{
      background: #0369a1;
      transform: translateY(-2px);
    }}

    .btn-whatsapp-showroom {{
      background: var(--accent-green);
      color: #fff;
      padding: 14px 26px;
      border-radius: 30px;
      font-size: 14.5px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      box-shadow: 0 4px 16px rgba(37, 211, 102, 0.3);
    }}

    .btn-whatsapp-showroom:hover {{
      background: var(--accent-green-dark);
      transform: translateY(-2px);
    }}

    .showroom-map-mockup {{
      background: #e2e8f0;
      border-radius: 20px;
      overflow: hidden;
      border: 1px solid var(--border);
      position: relative;
      height: 340px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 24px;
      background: linear-gradient(135deg, #0f172a, #1e293b);
    }}

    .map-overlay {{
      position: absolute;
      inset: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(4px);
    }}

    .map-content {{
      position: relative;
      z-index: 2;
      color: #fff;
    }}

    .map-pin-icon {{
      width: 48px;
      height: 48px;
      background: #ef4444;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 12px;
      box-shadow: 0 0 0 8px rgba(239, 68, 68, 0.3);
    }}

    /* ───────── FOOTER ───────── */
    .footer {{
      background: #111827;
      color: #9ca3af;
      padding: 60px 32px 30px;
      border-top: 1px solid #1f2937;
    }}

    .footer-container {{
      max-width: 1200px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1.5fr 1fr 1fr 1fr;
      gap: 40px;
      margin-bottom: 50px;
    }}

    .footer-brand {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .footer-logo {{
      font-family: var(--font-serif);
      font-size: 28px;
      font-weight: 700;
      color: #fff;
      letter-spacing: 2px;
    }}

    .footer-links {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      list-style: none;
    }}

    .footer-title {{
      color: #fff;
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 14px;
      letter-spacing: 0.5px;
    }}

    .footer-link {{
      font-size: 13.5px;
      transition: var(--transition);
    }}

    .footer-link:hover {{
      color: var(--accent-gold);
    }}

    .footer-bottom {{
      max-width: 1200px;
      margin: 0 auto;
      padding-top: 24px;
      border-top: 1px solid #1f2937;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      flex-wrap: wrap;
      gap: 12px;
    }}

    /* ───────── PRODUCT DETAIL MODAL (APPLE-STYLE) ───────── */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      transition: opacity 0.3s ease;
    }}

    .modal-overlay.active {{
      display: flex;
      opacity: 1;
    }}

    .modal-card {{
      background: #ffffff;
      border-radius: 28px;
      max-width: 860px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
      position: relative;
      display: grid;
      grid-template-columns: 1fr 1.15fr;
      transform: scale(0.95);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .modal-overlay.active .modal-card {{
      transform: scale(1);
    }}

    .btn-close-modal {{
      position: absolute;
      top: 18px;
      right: 18px;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.06);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #4b5563;
      font-size: 18px;
      transition: var(--transition);
      z-index: 10;
    }}

    .btn-close-modal:hover {{
      background: rgba(0, 0, 0, 0.12);
      transform: scale(1.05);
    }}

    .modal-img-col {{
      background: #fafafa;
      padding: 30px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border-right: 1px solid var(--border);
      position: relative;
    }}

    .modal-img-box {{
      width: 100%;
      height: 360px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: var(--shadow-md);
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .modal-img-box img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
      cursor: zoom-in;
    }}

    .modal-img-box:hover img {{
      transform: scale(1.06);
    }}

    .modal-info-col {{
      padding: 36px 32px;
      display: flex;
      flex-direction: column;
    }}

    .modal-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent-gold-soft);
      color: var(--accent-gold-dark);
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      align-self: flex-start;
      margin-bottom: 10px;
    }}

    .modal-title {{
      font-family: var(--font-serif);
      font-size: 28px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.2;
      margin-bottom: 10px;
    }}

    .modal-price-box {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .modal-price {{
      font-size: 28px;
      font-weight: 800;
      color: var(--text);
    }}

    .modal-installment {{
      background: #fdfaf3;
      border: 1px solid rgba(184, 142, 79, 0.3);
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 12px;
      color: var(--accent-gold-dark);
      font-weight: 600;
    }}

    .modal-promo-note {{
      background: #fff1f2;
      border: 1px solid #fecdd3;
      color: #9f1239;
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 18px;
    }}

    .modal-specs-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
      font-size: 12.5px;
    }}

    .modal-specs-table tr {{
      border-bottom: 1px solid var(--border);
    }}

    .modal-specs-table td {{
      padding: 8px 4px;
    }}

    .modal-specs-table td.spec-name {{
      color: var(--text-muted);
      width: 40%;
      font-weight: 600;
    }}

    .modal-specs-table td.spec-val {{
      color: var(--text);
      font-weight: 600;
    }}

    /* Custom engraving input inside modal */
    .modal-customizer-box {{
      background: var(--bg-alt);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      margin-bottom: 20px;
    }}

    .modal-customizer-label {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 6px;
      display: block;
    }}

    .modal-input-engrave {{
      width: 100%;
      padding: 10px 14px;
      border: 1.5px solid var(--border);
      border-radius: 10px;
      font-family: inherit;
      font-size: 13.5px;
      background: #fff;
    }}

    .modal-cta-group {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: auto;
    }}

    .btn-modal-whatsapp {{
      background: var(--accent-green);
      color: #fff;
      border: none;
      padding: 14px 20px;
      border-radius: 14px;
      font-size: 15px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(37, 211, 102, 0.35);
      transition: var(--transition);
    }}

    .btn-modal-whatsapp:hover {{
      background: var(--accent-green-dark);
      transform: translateY(-2px);
    }}

    .btn-modal-2gis {{
      background: #f0f9ff;
      color: #0284c7;
      border: 1px solid #bae6fd;
      padding: 10px 16px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: var(--transition);
    }}

    .btn-modal-2gis:hover {{
      background: #e0f2fe;
    }}

    /* ───────── REVIEW LIGHTBOX (SWIPER / VIEWER) ───────── */
    .lightbox-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.9);
      backdrop-filter: blur(12px);
      z-index: 1100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      transition: opacity 0.3s ease;
    }}

    .lightbox-overlay.active {{
      display: flex;
      opacity: 1;
    }}

    .lightbox-box {{
      position: relative;
      max-width: 520px;
      width: 100%;
      height: 90vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}

    .lightbox-img {{
      max-width: 100%;
      max-height: 82vh;
      border-radius: 18px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
      border: 2px solid rgba(255,255,255,0.2);
      object-fit: contain;
    }}

    .lightbox-caption {{
      color: #fff;
      font-size: 13.5px;
      text-align: center;
      margin-top: 14px;
      font-weight: 500;
    }}

    .btn-lightbox-nav {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
      border: none;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      transition: var(--transition);
    }}

    .btn-lightbox-nav:hover {{
      background: rgba(255, 255, 255, 0.4);
    }}

    .btn-lightbox-prev {{
      left: -60px;
    }}

    .btn-lightbox-next {{
      right: -60px;
    }}

    .btn-close-lightbox {{
      position: absolute;
      top: -40px;
      right: 0;
      background: transparent;
      color: #fff;
      border: none;
      font-size: 28px;
      cursor: pointer;
    }}

    /* ───────── MOBILE STICKY BOTTOM BAR ───────── */
    .mobile-bottom-bar {{
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-top: 1px solid var(--border);
      padding: 10px 16px;
      display: none;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      z-index: 99;
      box-shadow: 0 -4px 16px rgba(0,0,0,0.08);
    }}

    .btn-mobile-wa {{
      flex: 1.5;
      background: var(--accent-green);
      color: #fff;
      border: none;
      padding: 12px;
      border-radius: 14px;
      font-size: 14px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }}

    .btn-mobile-2gis {{
      flex: 1;
      background: #f0f9ff;
      color: #0284c7;
      border: 1px solid #bae6fd;
      padding: 12px;
      border-radius: 14px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }}

    /* Responsive Queries */
    @media (max-width: 992px) {{
      .hero {{
        grid-template-columns: 1fr;
        padding: 40px 20px;
      }}
      .promo-container {{
        grid-template-columns: 1fr;
      }}
      .sim-grid {{
        grid-template-columns: 1fr;
      }}
      .showroom-card {{
        grid-template-columns: 1fr;
        padding: 32px 24px;
      }}
      .social-grid {{
        grid-template-columns: 1fr;
      }}
      .footer-container {{
        grid-template-columns: 1fr 1fr;
      }}
      .modal-card {{
        grid-template-columns: 1fr;
        max-height: 85vh;
      }}
      .modal-img-col {{
        border-right: none;
        border-bottom: 1px solid var(--border);
      }}
      .btn-lightbox-prev {{
        left: 10px;
      }}
      .btn-lightbox-next {{
        right: 10px;
      }}
    }}

    @media (max-width: 768px) {{
      .pitch-banner {{
        display: none;
      }}
      .btn-nav-2gis {{
        display: none !important;
      }}
      .navbar {{
        padding: 0 16px;
        height: 60px;
      }}
      .nav-links {{
        display: none;
      }}
      .brand-logo-img {{
        width: 38px;
        height: 38px;
      }}
      .brand-name {{
        font-size: 20px;
      }}
      .brand-sub {{
        font-size: 9px;
      }}
      .btn-nav-whatsapp {{
        padding: 7px 14px;
        font-size: 12.5px;
      }}
      .hero-title {{
        font-size: 34px;
      }}
      .hero-perks-grid {{
        grid-template-columns: 1fr;
      }}
      .hero-social-links {{
        flex-direction: column;
      }}
      .hero-social-badge {{
        width: 100%;
        justify-content: center;
      }}
      .hero-showcase-visual {{
        max-height: 280px;
      }}
      .hero-showcase-visual img {{
        max-height: 280px;
      }}
      .hero-showcase-thumbs {{
        grid-template-columns: 1fr;
      }}
      .mobile-bottom-bar {{
        display: flex;
      }}
      body {{
        padding-bottom: 70px;
      }}
    }}

    /* ───────── CORRECTIONS: tabs, price tiers, offer, mobile menu ───────── */
    body {{ font-size: 15px; }}
    .filter-tab {{ font-size: 14.5px; padding: 10px 18px; }}
    .filter-tab-hot {{ background: #fff1f2; border-color: #fecdd3; color: var(--accent-red); font-weight: 700; }}
    .filter-tab-hot.active-special {{ background: var(--accent-red); border-color: var(--accent-red); color: #fff; }}
    .price-tabs {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin-top: 14px; }}
    .price-tabs-label {{ font-size: 14px; font-weight: 700; color: var(--text); margin-right: 4px; }}
    .price-chip {{ padding: 9px 16px; border-radius: 24px; background: #fffbeb; border: 1px solid #fde68a; color: #92400e; font-size: 14px; font-weight: 600; cursor: pointer; white-space: nowrap; transition: var(--transition); }}
    .price-chip:hover {{ border-color: var(--accent-gold); }}
    .price-chip.active {{ background: var(--accent-gold-dark, #8a6a2f); border-color: var(--accent-gold-dark, #8a6a2f); color: #fff; }}
    .catalog-count {{ margin-top: 14px; font-size: 14px; color: var(--text-muted); }}
    .card-desc {{ font-size: 14.5px; }}

    .nav-burger {{ display: none; width: 42px; height: 42px; border-radius: 12px; border: 1px solid var(--border); background: #fff; cursor: pointer; align-items: center; justify-content: center; flex-direction: column; gap: 5px; padding: 0; }}
    .nav-burger span {{ display: block; width: 18px; height: 2px; background: var(--text); border-radius: 2px; transition: transform .25s, opacity .2s; }}
    .navbar.open .nav-burger span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
    .navbar.open .nav-burger span:nth-child(2) {{ opacity: 0; }}
    .navbar.open .nav-burger span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}

    .btn-mobile-soc {{ width: 46px; height: 46px; border-radius: 14px; display: inline-flex; align-items: center; justify-content: center; border: 1px solid var(--border); background: #fff; color: var(--text); flex-shrink: 0; }}
    .btn-mobile-soc.insta {{ color: #be185d; border-color: #fbcfe8; background: #fdf2f8; }}
    .btn-mobile-soc.tiktok {{ background: #111827; color: #fff; border-color: #111827; }}

    .offer-overlay {{ position: fixed; inset: 0; background: rgba(17,24,39,.55); z-index: 300; display: none; align-items: center; justify-content: center; padding: 20px; }}
    .offer-overlay.active {{ display: flex; }}
    .offer-card {{ position: relative; background: #fff; border-radius: 24px; max-width: 440px; width: 100%; padding: 32px 28px 26px; text-align: center; }}
    .offer-close {{ position: absolute; top: 12px; right: 14px; border: none; background: transparent; font-size: 24px; cursor: pointer; color: var(--text-muted); }}
    .offer-title {{ font-family: var(--font-serif); font-size: 28px; line-height: 1.15; font-weight: 700; color: var(--text); margin-bottom: 12px; }}
    .offer-text {{ font-size: 16px; color: var(--text); margin-bottom: 22px; }}
    .offer-actions {{ display: flex; flex-direction: column; gap: 10px; }}
    .offer-btn {{ display: block; padding: 14px 18px; border-radius: 16px; font-weight: 700; font-size: 15px; text-align: center; text-decoration: none; cursor: pointer; border: none; }}
    .offer-btn.primary {{ background: var(--accent-red); color: #fff; }}
    .offer-btn.wa {{ background: var(--accent-green); color: #fff; }}

    @media (max-width: 768px) {{
      .nav-burger {{ display: inline-flex; }}
      .navbar {{ gap: 8px; }}
      .navbar.open .nav-links {{ display: flex !important; flex-direction: column; align-items: stretch; gap: 0; position: absolute; top: 100%; left: 0; right: 0; background: #fff; padding: 8px 20px 20px; border-bottom: 1px solid var(--border); max-height: calc(100vh - 70px); overflow-y: auto; }}
      .navbar.open .nav-links li a {{ display: block; padding: 14px 4px; font-size: 17px; border-bottom: 1px solid var(--border); }}
      .hero-title {{ font-size: 32px; }}
      .filter-tab {{ font-size: 14px; padding: 9px 14px; }}
      .price-chip {{ font-size: 13.5px; padding: 8px 13px; }}
      .brand-text {{ display: none; }}
    }}

    /* ───────── COLD-VISITOR FLOW: picker, reviews teaser, offer ───────── */
    .sort-select {{ max-width: 100%; min-width: 0; }}
    .search-box {{ max-width: 100%; min-width: 0; }}
    .picker-section {{ padding: 64px 32px 24px; max-width: 1240px; margin: 0 auto; }}
    .picker-head {{ text-align: center; margin-bottom: 28px; }}
    .picker-title {{ font-family: var(--font-serif); font-size: 38px; line-height: 1.12; font-weight: 700; color: var(--text); }}
    .picker-sub {{ margin-top: 10px; font-size: 16px; color: var(--text-muted); }}
    .picker-box {{ background: #fff; border: 1px solid var(--border); border-radius: 28px; padding: 28px; box-shadow: var(--shadow-lg); }}
    .picker-row {{ margin-bottom: 20px; }}
    .picker-label {{ font-size: 15px; font-weight: 700; margin-bottom: 10px; color: var(--text); }}
    .picker-chips {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .picker-chip {{ padding: 11px 18px; border-radius: 24px; border: 1px solid var(--border); background: var(--bg-alt); font-size: 15px; font-weight: 600; cursor: pointer; color: var(--text); transition: var(--transition); }}
    .picker-chip:hover {{ border-color: var(--accent-gold); }}
    .picker-chip.active {{ background: var(--text); border-color: var(--text); color: #fff; }}
    .picker-results {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 8px; }}
    .pick-card {{ background: var(--bg-alt); border: 1px solid var(--border); border-radius: 20px; overflow: hidden; display: flex; flex-direction: column; cursor: pointer; transition: var(--transition); }}
    .pick-card:hover {{ transform: translateY(-3px); border-color: var(--accent-gold); }}
    .pick-card img {{ width: 100%; aspect-ratio: 3 / 4; object-fit: cover; display: block; }}
    .pick-card-body {{ padding: 14px 14px 16px; display: flex; flex-direction: column; gap: 6px; flex: 1; }}
    .pick-card-name {{ font-family: var(--font-serif); font-size: 18px; font-weight: 700; line-height: 1.2; color: var(--text); }}
    .pick-card-price {{ font-size: 20px; font-weight: 800; color: var(--text); }}
    .pick-card-inst {{ font-size: 13.5px; color: var(--text-muted); }}
    .pick-card-btn {{ margin-top: auto; padding: 11px 14px; border-radius: 14px; border: none; background: var(--accent-red); color: #fff; font-weight: 700; font-size: 15px; cursor: pointer; }}
    .picker-empty {{ grid-column: 1 / -1; padding: 24px; text-align: center; color: var(--text-muted); font-size: 16px; }}
    .picker-foot {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 22px; }}
    .picker-btn {{ padding: 14px 24px; border-radius: 16px; font-size: 16px; font-weight: 700; border: none; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; }}
    .picker-btn.dark {{ background: var(--text); color: #fff; }}
    .picker-btn.wa {{ background: var(--accent-green); color: #fff; }}

    .teaser-section {{ padding: 48px 32px 8px; max-width: 1240px; margin: 0 auto; }}
    .teaser-head {{ display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 10px 20px; margin-bottom: 20px; }}
    .teaser-title {{ font-family: var(--font-serif); font-size: 32px; font-weight: 700; color: var(--text); }}
    .teaser-link {{ font-size: 15px; font-weight: 700; color: var(--accent-gold-dark, #8a6a2f); text-decoration: underline; }}
    .teaser-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
    .teaser-card {{ background: #fff; border: 1px solid var(--border); border-radius: 20px; overflow: hidden; cursor: pointer; transition: var(--transition); }}
    .teaser-card:hover {{ border-color: var(--accent-gold); transform: translateY(-3px); }}
    .teaser-card img {{ width: 100%; height: 240px; object-fit: cover; object-position: top; display: block; }}
    .teaser-cap {{ padding: 12px 16px 14px; font-size: 14.5px; color: var(--text); }}
    .teaser-cap small {{ display: block; color: var(--text-muted); font-size: 13px; margin-top: 2px; }}

    .offer-list {{ list-style: none; text-align: left; margin: 0 auto 22px; padding: 0; display: grid; gap: 10px; }}
    .offer-list li {{ font-size: 16px; font-weight: 600; color: var(--text); padding-left: 28px; position: relative; }}
    .offer-list li::before {{ content: "✓"; position: absolute; left: 0; top: 0; color: var(--accent-green); font-weight: 800; }}
    .modal-trust {{ display: flex; flex-wrap: wrap; gap: 8px 16px; margin: 12px 0 4px; font-size: 14px; font-weight: 600; color: #166534; }}
    .modal-city-box {{ margin-top: 10px; }}

    @media (max-width: 900px) {{
      .picker-results {{ grid-template-columns: repeat(2, 1fr); }}
      .teaser-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 768px) {{
      .hero-perks-grid {{ grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; }}
      .perk-card {{ padding: 12px 8px !important; text-align: center; }}
      .perk-card .perk-desc {{ display: none; }}
      .perk-card .perk-title {{ font-size: 13px; line-height: 1.25; }}
      .perk-icon {{ font-size: 22px; }}
      .hero {{ padding-top: 24px !important; gap: 28px !important; }}
      .hero-lead {{ font-size: 17px !important; }}
    }}
    @media (max-width: 768px) {{
      .picker-section {{ padding: 44px 16px 12px; }}
      .picker-title {{ font-size: 28px; }}
      .picker-box {{ padding: 18px 14px; border-radius: 22px; }}
      .teaser-section {{ padding: 36px 16px 4px; }}
      .teaser-title {{ font-size: 26px; }}
      .teaser-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
      .teaser-card img {{ height: 190px; }}
      .mobile-bottom-bar {{ gap: 8px !important; padding: 10px 12px !important; }}
      .btn-mobile-2gis {{ flex: 0 0 auto !important; padding: 12px !important; }}
      .btn-mobile-wa {{ flex: 1 1 0 !important; min-width: 0; white-space: nowrap; }}
      .sort-select {{ width: 100%; }}
      .search-sort-bar {{ flex-direction: column; align-items: stretch; }}
    }}

    /* ───────── CONSTRUCTOR DIAL v2: store emblem in the centre ───────── */
    .dial-v2 {{ width: 310px; height: 310px; background: #fffdf8; box-shadow: 0 15px 35px rgba(212, 175, 55, 0.25), inset 0 2px 10px rgba(0,0,0,0.08); }}
    .dial-v2 .dial-marks {{ position: absolute; inset: 0; }}
    .dial-v2 .dial-mark {{ position: absolute; left: 50%; top: 8px; width: 2px; height: 9px; margin-left: -1px; background: #9ca3af; transform-origin: 50% 133px; }}
    .dial-v2 .dial-mark.big {{ width: 3px; height: 14px; margin-left: -1.5px; background: #92400e; }}
    .dial-v2 .dial-tamga-top {{ position: absolute; top: 54%; left: 50%; transform: translateX(-50%); width: 24px; height: 24px; color: #92400e; z-index: 2; }}
    .dial-v2 .dial-tamga-top .dial-tamga-icon {{ width: 24px; height: 24px; margin: 0; }}
    .dial-v2 .hour-hand {{ height: 78px; width: 7px; margin-left: -3.5px; background: #92400e; border-radius: 6px; box-shadow: 0 0 0 2px #fff, 0 2px 6px rgba(0,0,0,.3); transform: rotate(-60deg); z-index: 5; }}
    .dial-v2 .min-hand {{ height: 108px; width: 5px; margin-left: -2.5px; background: #b45309; border-radius: 5px; box-shadow: 0 0 0 2px #fff, 0 2px 6px rgba(0,0,0,.3); transform: rotate(60deg); z-index: 5; }}
    .dial-v2 .dial-emblem {{ position: absolute; top: 12%; left: 50%; width: 104px; height: auto; transform: translateX(-50%); z-index: 4; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }}
    .dial-v2::after {{ content: ""; position: absolute; left: 50%; top: 50%; width: 16px; height: 16px; margin: -8px 0 0 -8px; border-radius: 50%; background: #92400e; border: 3px solid #fff; z-index: 6; }}
    .dial-v2 .dial-text {{ position: absolute; left: 50%; top: 64%; transform: translateX(-50%); width: 200px; text-align: center; z-index: 3; }}
    .dial-v2 .dial-name {{ font-size: 21px; white-space: nowrap; }}
    @media (max-width: 380px) {{
      .dial-v2 {{ width: 280px; height: 280px; }}
      .dial-v2 .dial-mark {{ transform-origin: 50% 118px; }}
      .dial-v2 .dial-emblem {{ width: 92px; }}
    }}
  /*__DARK_STOP__*/
  {CSS_EXTRA}
  {CSS_FEATURES}
  {CSS_FAQ}
  {CSS_BONUS}
  </style>
</head>
<body>

  <!-- ───────── TOP PRESENTATION BAR: ADDRESS & 2GIS ───────── -->
  <div class="pitch-banner">
    <div class="pitch-left">
      <span class="pitch-badge">UAQYT BOUTIQUE</span>
      <span class="pitch-text">📍 Алматы қ., Өтеген батыр к-сі 11а, БЦ «Сайран Сити», 3-қабат, 320-кеңсе</span>
      <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="pitch-2gis-link" title="2GIS картасынан ашу">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
        <span>2GIS-те ашу</span>
      </a>
    </div>
    <div class="pitch-right">
      <a href="https://www.instagram.com/uaqyt.kzt?psln=ZXd3MTI5cmI3NGF6" target="_blank" rel="noopener" class="pitch-social-link">Instagram: @uaqyt.kzt</a>
      <a href="https://www.tiktok.com/@uaqyt.kzz2?_t=ZM-8uQyLn8Uuxi&_r=1" target="_blank" rel="noopener" class="pitch-social-link">TikTok: @uaqyt.kzz2</a>
      <span style="color: var(--accent-gold); font-weight: 700;">Тел: {WA_DISP}</span>
    </div>
  </div>

  {RIBBON}

  <!-- ───────── NAVBAR ───────── -->
  <header class="navbar">
    <a href="#hero" class="nav-brand">
      <img src="./images/logo.jpg" alt="UAQYT kzt" class="brand-logo-img">
      <div class="brand-text">
        <span class="brand-name">UAQYT</span>
        <span class="brand-sub">kzt • Есімді сағаттар бутигі</span>
      </div>
    </a>

    <nav>
      <ul class="nav-links">
        <li><a href="#picks" class="nav-link">Сыйлық таңдау</a></li>
        <li><a href="#bonus" class="nav-link highlight">🎁 1+1 Бонус</a></li>
        <li><a href="#catalog" class="nav-link">Каталог</a></li>
        <li><a href="#customizer" class="nav-link">Конструктор</a></li>
        <li><a href="#reviews" class="nav-link">Пікірлер ({len(customer_reviews)})</a></li>
        <li><a href="#contact" class="nav-link">Шоурум</a></li>
      </ul>
    </nav>

    <button class="nav-burger" id="navBurger" type="button" aria-label="Мәзір" aria-expanded="false" onclick="toggleNav()"><span></span><span></span><span></span></button>

    <div class="nav-actions">
      {LANG_SWITCH}
      <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="btn-nav-2gis" title="2GIS маршрут">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
        <span>2GIS-те көру</span>
      </a>
      <a href="https://wa.me/{WA}?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%81%D1%96%D0%B7%20%D0%B1%D0%B5!%20UAQYT%20%D1%81%D0%B0%D0%B9%D1%82%D1%8B%D0%BD%D0%B0%D0%BD%20%D1%81%D0%B0%D2%93%D0%B0%D1%82%D2%9B%D0%B0%20%D1%82%D0%B0%D0%BF%D1%81%D1%8B%D1%80%D1%8B%D1%81%20%D0%B1%D0%B5%D1%80%D0%B3%D1%96%D0%BC%20%D0%BA%D0%B5%D0%BB%D0%B5%D0%B4%D1%96" target="_blank" rel="noopener" class="btn-nav-whatsapp">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.669-.699c.969.54 1.777.82 2.791.82 3.181 0 5.768-2.587 5.768-5.767.001-3.18-2.585-5.805-5.768-5.805zm0 10.457c-.888 0-1.656-.25-2.348-.687l-.168-.106-1.57.412.419-1.53-.11-.176c-.469-.747-.716-1.517-.716-2.404 0-2.482 2.019-4.501 4.493-4.501s4.493 2.019 4.493 4.501c0 2.483-2.019 4.491-4.493 4.491z"/></svg>
        <span>WhatsApp</span>
      </a>
    </div>
  </header>

  <!-- ───────── HERO SECTION ───────── -->
  <section class="hero" id="hero">
    <div class="hero-left">
      <div class="hero-tag-badge">
        <span>✨ ЕСІМІҢІЗ ЖАЗЫЛҒАН САҒАТТАР</span>
      </div>
      <h1 class="hero-title">
        Сағатыңызға <span>өз есіміңізді жазамыз</span>
      </h1>
      <p class="hero-lead">
        Есім, күн немесе ру таңбасы — циферблатқа лазермен. Қазақстан бойынша тегін жеткізу.
      </p>

      <div class="hero-perks-grid">
        <div class="perk-card">
          <span class="perk-icon">🛡️</span>
          <div class="perk-title">6-12 ай кепілдік</div>
          <div class="perk-desc">Модельге байланысты</div>
        </div>
        <div class="perk-card">
          <span class="perk-icon">✈️</span>
          <div class="perk-title">ТЕГІН жеткізу</div>
          <div class="perk-desc">Пошта немесе автобус</div>
        </div>
        <div class="perk-card">
          <span class="perk-icon">🎁</span>
          <div class="perk-title">1+1 Бонус сағат</div>
          <div class="perk-desc">Сатып алғанға сыйлық</div>
        </div>
      </div>

      <div class="hero-cta-group">
        <a href="#catalog" class="btn-hero-primary">
          <span>Каталогты қарау</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
        <a href="#customizer" class="btn-hero-secondary">
          <span>Өз сағатыңызды жасау</span>
        </a>
      </div>

      <!-- Hero Social Strip (Instagram & TikTok prominent on screen 1) -->
      <div class="hero-social-strip">
        <span class="hero-social-label">Біздің ресми парақшалар:</span>
        <div class="hero-social-links">
          <a href="https://www.instagram.com/uaqyt.kzt?psln=ZXd3MTI5cmI3NGF6" target="_blank" rel="noopener" class="hero-social-badge insta">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
            <span>Instagram: <strong>@uaqyt.kzt</strong></span>
          </a>
          <a href="https://www.tiktok.com/@uaqyt.kzz2?_t=ZM-8uQyLn8Uuxi&_r=1" target="_blank" rel="noopener" class="hero-social-badge tiktok">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64c.298 0 .591.044.87.13V9.4a6.33 6.33 0 0 0-.87-.06A6.34 6.34 0 0 0 3 15.68a6.34 6.34 0 0 0 9.17 5.65 6.27 6.27 0 0 0 3.51-5.59V8.9a8.18 8.18 0 0 0 4.79 1.54v-3.4a4.85 4.85 0 0 1-.88-.35z"/></svg>
            <span>TikTok: <strong>@uaqyt.kzz2</strong> (Видео шолулар)</span>
          </a>
        </div>
      </div>
    </div>

    <!-- Hero Right: Real Watch Showcase Photo with Official Logo & Badges -->
    <div class="hero-showcase-card">
      <div class="hero-showcase-badge">🔥 1+1 ТЕГІН БОНУС САҒАТ</div>
      <div class="hero-showcase-header">
        <div class="hero-showcase-brand">
          <img src="./images/logo.jpg" alt="UAQYT kzt" class="hero-showcase-logo-img">
          <div class="hero-showcase-brand-meta">
            <span>UAQYT</span>
            <small>kzt • Есімді сағаттар бутигі</small>
          </div>
        </div>
      </div>
      <div class="hero-showcase-visual" onclick="openShowcaseLightbox('./images/showcase/showcase-baglan-aday-gold.jpg', '«Бағлан / Адай» Сегізқырлы алтын сағат')">
        <img src="./images/showcase/showcase-baglan-aday-gold.jpg" alt="Бағлан Адай руы сағаты" id="heroShowcaseMainImg">
        <div class="hero-showcase-visual-overlay">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
          <span>Толық өлшемде көру</span>
        </div>
      </div>
      <div class="hero-showcase-info">
        <div class="hero-showcase-tag">✨ ХИТ ҮЛГІ • ЖЕКЕ ГРАВЮРА</div>
        <h3 class="hero-showcase-title" id="heroShowcaseTitle">«Бағлан / Адай» Сегізқырлы алтын сағат</h3>
        <p class="hero-showcase-desc" id="heroShowcaseDesc">Лазерлік гравюра • Фирмалық сыйлық қорабы</p>
        <div class="hero-showcase-thumbs">
          <button type="button" class="hero-thumb-btn active" onclick="switchHeroShowcase('./images/showcase/showcase-baglan-aday-gold.jpg', '«Бағлан / Адай» Сегізқырлы алтын сағат', 'Лазерлік гравюра • Фирмалық сыйлық қорабы', this)">
            <img src="./images/showcase/showcase-baglan-aday-gold.jpg" alt="Алтын Адай">
            <span>Алтын Адай</span>
          </button>
          <button type="button" class="hero-thumb-btn" onclick="switchHeroShowcase('./images/showcase/showcase-zhangeldi-erketay-black.jpg', '«Жангелді / Еркетай» Қара стиль сағаты', 'Қара стиль • Күңгірт жабын • Айрықша дизайн', this)">
            <img src="./images/showcase/showcase-zhangeldi-erketay-black.jpg" alt="Қара стиль">
            <span>Қара стиль</span>
          </button>
          <button type="button" class="hero-thumb-btn" onclick="switchHeroShowcase('./images/showcase/showcase-rahat-ardana-woodbox.jpg', '«Рахат / Ардана» Жұптық люкс ағаш қорап', '1+1 Жұптық сағаттар • Эксклюзивті табиғи ағаш қорап', this)">
            <img src="./images/showcase/showcase-rahat-ardana-woodbox.jpg" alt="Люкс ағаш қорап">
            <span>Ағаш қорап</span>
          </button>
        </div>
      </div>
    </div>
  </section>

  {PICKER_SECTION}

  {HOLIDAY_SECTION}

  {STORY_SECTION}

  <!-- ───────── 1+1 PROMO SECTION ───────── -->
  <section class="promo-banner-section" id="bonus">
    <div class="promo-container">
      <div class="promo-img-box">
        <img src="./images/bonus/bonus-watch-1.jpg" alt="1+1 Бонус сағат UAQYT">
      </div>
      <div class="promo-info">
        <span class="promo-tag">🔥 АРНАЙЫ АКЦИЯ: 1 + 1</span>
        <h2 class="promo-heading">25 900 ₸-ден бастап сағат алсаңыз — 2-ші сағат ТЕГІН!</h2>
        <p class="promo-text">
          Қазіргі науқан бойынша каталогтан кез келген ерлер немесе рулық сағатын таңдағанда — суреттегі стильді бонус сағатты сыйлық ретінде ТЕГІН аласыз! Жұбайыңызға, досыңызға немесе туысыңызға қосарланған қуаныш сыйлаңыз.
        </p>

        <div class="promo-features">
          <div class="promo-feat-item">✓ 2-ші сағат 100% ТЕГІН</div>
          <div class="promo-feat-item">✓ 25 900 ₸-ден бастап барлық сағатқа жарамды</div>
          <div class="promo-feat-item">✓ Екі сағатқа да жеке гравюра</div>
          <div class="promo-feat-item">✓ Фирмалық сыйлық қорабымен</div>
          <div class="promo-feat-item">✓ 6–12 ай кепілдік</div>
        </div>

        {BONUS_GALLERY}

        <a href="#catalog" class="btn-promo-action">
          <span>Акция бойынша сағат таңдау</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      </div>
    </div>
  </section>

  <!-- ───────── INTERACTIVE DIAL CUSTOMIZER ───────── -->
  <section class="simulator-section" id="customizer">
    <div class="sim-header">
      <div class="sim-subtitle">Интерактивті конструктор</div>
      <h2 class="sim-title">Өз сағатыңыздың дизайнын қазір жасап көріңіз</h2>
      <p style="color: var(--text-muted); font-size: 15px; margin-top: 8px;">
        Есіміңізді және руыңызды енгізіп, сағат циферблатында қалай көрінетінін нақты уақытта тамашалаңыз.
      </p>
    </div>

    <div class="sim-grid">
      <!-- Interactive Dial Display -->
      <div class="dial-display-card">
        <div class="dial-case dial-v2">
          <div class="dial-ticks"></div>
          <div class="dial-marks"><i class="dial-mark big" style="transform: rotate(0deg)"></i><i class="dial-mark" style="transform: rotate(30deg)"></i><i class="dial-mark" style="transform: rotate(60deg)"></i><i class="dial-mark big" style="transform: rotate(90deg)"></i><i class="dial-mark" style="transform: rotate(120deg)"></i><i class="dial-mark" style="transform: rotate(150deg)"></i><i class="dial-mark big" style="transform: rotate(180deg)"></i><i class="dial-mark" style="transform: rotate(210deg)"></i><i class="dial-mark" style="transform: rotate(240deg)"></i><i class="dial-mark big" style="transform: rotate(270deg)"></i><i class="dial-mark" style="transform: rotate(300deg)"></i><i class="dial-mark" style="transform: rotate(330deg)"></i></div>
          <div class="dial-tamga-top" id="simTamgaBox">
            <svg class="dial-tamga-icon" viewBox="0 0 60 60" fill="currentColor">
              <circle cx="30" cy="30" r="16" fill="none" stroke="currentColor" stroke-width="3"/>
              <circle cx="30" cy="30" r="6" fill="currentColor"/>
            </svg>
          </div>
          <div class="hand hour-hand"></div>
          <div class="hand min-hand"></div>
          <img class="dial-emblem" src="./images/emblem.png" alt="UAQYT kzt эмблемасы" width="360" height="170">
          <div class="dial-text">
            <div class="dial-name" id="simDialName">АРМАН</div>
            <div class="dial-sub" id="simDialSub">АРҒЫН РУЫ</div>
            <div class="dial-date" id="simDialDate">UAQYT KZT • 2026</div>
          </div>
        </div>
        <div style="margin-top: 18px; font-size: 13px; color: var(--accent-gold-dark); font-weight: 700;">
          Дизайн нақты уақытта өзгереді. Ортасында UAQYT эмблемасы
        </div>
      </div>

      <!-- Controls Form -->
      <div class="sim-controls-form">
        <div class="form-group">
          <label class="form-label">Циферблатқа жазылатын есім немесе лақап атыңыз:</label>
          <input type="text" class="form-input" id="inputName" value="Арман" placeholder="Мысалы: Бауыржан, Нұрлан, Қасым-Жомарт" oninput="updateDialPreview()">
        </div>

        <div class="form-group">
          <label class="form-label">Шежіре бойынша ру таңбаңызды таңдаңыз:</label>
          <select class="form-select" id="selectClan" onchange="updateClanSelection()">
            <option value="argyn" selected>Арғын (Көз таңбасы ⚯)</option>
            <option value="nayman">Найман (Бақан / Мүйіз таңбасы Ү)</option>
            <option value="kipchak">Қыпшақ (Қос алып таңбасы I I)</option>
            <option value="dulat">Дулат (Дөңгелек таңбасы ◯)</option>
            <option value="aday">Адай (Жебе / Садақ таңбасы ↑)</option>
            <option value="shapyrashty">Шапырашты (Ай таңбасы ☽)</option>
            <option value="alban">Албан (Қоңырау таңбасы ☖)</option>
            <option value="berish">Беріш (Жұлдыз таңбасы ★)</option>
            <option value="tortkara">Төртқара (Төртбұрыш / Таразы)</option>
            <option value="shekti">Шекті (Сүйір таңбасы)</option>
            <option value="ysty">Ысты (Көсеу таңбасы)</option>
            <option value="oshakty">Ошақты (Тұмар таңбасы △)</option>
            <option value="tore">Төре (Шыңғысхан әулетінің Тәжі 👑)</option>
            <option value="kozha">Қожа (Араб каллиграфиясы ﷽)</option>
            <option value="service_mvd">ҚР Ішкі Істер Министрлігі (ІІМ)</option>
            <option value="service_knb">ҚР Ұлттық Қауіпсіздік Комитеті (ҰҚК)</option>
            <option value="service_arm">ҚР Қарулы Күштері (Әскер)</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Қосымша мәтін (ру, шен немесе күн):</label>
          <input type="text" class="form-input" id="inputSub" value="АРҒЫН РУЫ" placeholder="Мысалы: АРҒЫН, ҰҚК ОФИЦЕРІ, 12.05.2026" oninput="updateDialPreview()">
        </div>

        <div class="form-group">
          <label class="form-label">Төменгі белгі (нөмір / дата):</label>
          <input type="text" class="form-input" id="inputDate" value="UAQYT KZT • 2026" oninput="updateDialPreview()">
        </div>

        <button class="btn-apply-sim" onclick="orderCustomizedDial()">
          <span>Осы дизайн бойынша WhatsApp-қа тапсырыс беру</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </button>
      </div>
    </div>
  </section>

  <!-- ───────── CATALOG SECTION ───────── -->
  <section class="catalog-section" id="catalog">
    <div class="catalog-header">
      <div class="section-subtitle">Бутик топтамасы</div>
      <h2 class="section-title">Барлық сағаттар топтамасы ({len(all_products_sorted)} үлгі)</h2>
      <p class="section-desc">
        Каталогтың басында ерлерге арналған ру-таңбалы үлгілер, одан әрі 1+1 жұптық және қызметтік топтамалар. Дайын бағасы бар хиттер немесе жеке тапсырыспен жасалатын сағаттар.
      </p>
    </div>

    <!-- Search & Filter Toolbar -->
    <div class="catalog-toolbar">
      <div class="search-sort-bar">
        <div class="search-box">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" class="search-input" id="catalogSearch" placeholder="Ру, есім немесе қызмет бойынша іздеу..." oninput="filterCatalog()">
        </div>

        <select class="sort-select" id="sortSelect" onchange="sortCatalog()">
          <option value="default">Сұрыптау: Әдепкі ретпен (Ерлер сағаттары алдында)</option>
          <option value="price_asc">Бағасы: Арзаннан қымбатқа</option>
          <option value="price_desc">Бағасы: Қымбаттан арзанға</option>
        </select>
      </div>

      <div class="filter-tabs">
        <button class="filter-tab active" data-filter="mens" onclick="setCategoryFilter('mens', this)">👑 Ерлер сағаттары ({len(mens_all)})</button>
        <button class="filter-tab filter-tab-hot" data-filter="couples" onclick="setCategoryFilter('couples', this)">❤️ 1+1 Жұптық сағаттар ({len(couples_all)})</button>
        <button class="filter-tab" data-filter="all" onclick="setCategoryFilter('all', this)">Барлығы ({len(all_products_sorted)})</button>
        <button class="filter-tab" data-filter="service" onclick="setCategoryFilter('service', this)">🛡️ Қызметтік (ІІМ, ҰҚК, ҚР ҚК)</button>
        <button class="filter-tab" data-filter="ornament" onclick="setCategoryFilter('ornament', this)">Шежіре Ру-Таңбалы</button>
        <button class="filter-tab" data-filter="mechanic" onclick="setCategoryFilter('mechanic', this)">⚙️ Механика</button>
        <button class="filter-tab" data-filter="woodbox" onclick="setCategoryFilter('woodbox', this)">🪵 Люкс ағаш қорапты</button>
      </div>

      <div class="price-tabs">
        <span class="price-tabs-label">Баға бойынша:</span>
        <button class="price-chip active" onclick="setPriceFilter('all', this)">Барлық баға</button>
        <button class="price-chip" onclick="setPriceFilter('t1', this)">30 000 ₸ дейін ({T1})</button>
        <button class="price-chip" onclick="setPriceFilter('t2', this)">30 000 – 40 000 ₸ ({T2})</button>
        <button class="price-chip" onclick="setPriceFilter('t3', this)">40 000 – 55 000 ₸ ({T3})</button>
        <button class="price-chip" onclick="setPriceFilter('t4', this)">55 000 ₸ бастап ({T4})</button>
      </div>
      <div class="catalog-count" id="catalogCount" aria-live="polite"></div>
    </div>

    <!-- Cards Grid -->
    <div class="products-grid" id="productsGrid">
      {all_cards_str}
    </div>
  </section>

  <!-- ───────── SOCIAL MEDIA SHOWCASE (INSTAGRAM & TIKTOK) ───────── -->
  <section class="social-section" id="socials">
    <div style="text-align: center; margin-bottom: 36px;">
      <div class="section-subtitle">Ресми парақшаларымыз</div>
      <h2 class="section-title">Әлеуметтік желілерде бізбен бірге болыңыз</h2>
      <p style="color: var(--text-muted); font-size: 15px; margin-top: 8px;">
        Күнделікті сағат жасау барысы, лазерлік гравюра процесі және тұтынушылардың нақты видео-шолулары.
      </p>
    </div>

    <div class="social-grid">
      <!-- Instagram Card -->
      <div class="social-card instagram">
        <div>
          <div class="social-card-top">
            <div class="social-icon-box">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
            </div>
            <span class="social-handle">@uaqyt.kzt</span>
          </div>
          <h3 class="social-card-title">Instagram-да жаңа жұмыстар мен пікірлер</h3>
          <p class="social-card-desc">
            Күнделікті Stories арқылы шеберханадан тікелей видеолар, клиенттерге жөнелтіліп жатқан сағаттар және жаңа ру таңбаларының жасалу үлгілері.
          </p>
        </div>
        <a href="https://www.instagram.com/uaqyt.kzt?psln=ZXd3MTI5cmI3NGF6" target="_blank" rel="noopener" class="btn-social-cta">
          <span>Instagram-да парақшаны ашу</span>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      </div>

      <!-- TikTok Card -->
      <div class="social-card tiktok">
        <div>
          <div class="social-card-top">
            <div class="social-icon-box" style="background: rgba(255,255,255,0.15);">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 0 0-1-.08A6.34 6.34 0 0 0 3 15.66a6.34 6.34 0 0 0 10.82 4.49 6.3 6.3 0 0 0 1.87-4.49V8.7a8.28 8.28 0 0 0 4.9 1.57V6.82a4.88 4.88 0 0 1-1-.13z"/></svg>
            </div>
            <span class="social-handle">@uaqyt.kzz2</span>
          </div>
          <h3 class="social-card-title">TikTok-тағы миллион қаралым жинаған видеолар</h3>
          <p class="social-card-desc">
            Лазерлік станоктың сағатқа өрнек қашау процесі, суға батырып тексеру сынақтары және трендтегі бейнероликтер.
          </p>
        </div>
        <a href="https://www.tiktok.com/@uaqyt.kzz2?_t=ZM-8uQyLn8Uuxi&_r=1" target="_blank" rel="noopener" class="btn-social-cta">
          <span>TikTok-қа жазылу</span>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      </div>
    </div>
  </section>

  <!-- ───────── VERIFIED CUSTOMER REVIEWS (22 REAL WHATSAPP SCREENSHOTS) ───────── -->
  <section class="reviews-section" id="reviews">
    <div class="reviews-container">
      <div class="reviews-header">
        <div class="section-subtitle">Нақты тұтынушылардың фото-есептері</div>
        <h2 class="section-title">Клиенттеріміздің шынайы WhatsApp пікірлері ({len(customer_reviews)})</h2>
        <p class="section-desc">
          Әрбір сағат — нақты адамның қуанышы мен алғысы. Барлық скриншотты басып, толықтай оқып көре аласыз!
        </p>
      </div>

      <!-- Reviews Grid -->
      <div class="reviews-grid" id="reviewsGrid">
        {all_reviews_str}
      </div>
    </div>
  </section>

  <!-- ───────── SHOWROOM & 2GIS SECTION ───────── -->
  {FAQ_SECTION}

  <section class="showroom-section" id="contact">
    <div class="showroom-card">
      <div class="showroom-info">
        <span class="showroom-badge">ШОУРУМ ЖӘНЕ ШЕБЕРХАНА</span>
        <h2 class="showroom-title">Алматы қаласындағы ресми бутикке келіңіз</h2>
        <p class="showroom-desc">
          Барлық сағатты қолыңызбен ұстап көріп, салмағын байқап, лазерлік гравюра үрдісіне өзіңіз куә бола аласыз. 2GIS картасы арқылы жолды оңай тауып келіңіз!
        </p>

        <div class="info-list">
          <div class="info-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <strong>Мекен-жайымыз:</strong> Алматы қаласы, Өтеген батыр көшесі 11а, БЦ «Сайран Сити», 3-қабат, 320-кеңсе
            </div>
          </div>
          <div class="info-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <strong>Жұмыс уақыты:</strong> Дүйсенбі – Сенбі, 10:00 – 20:00, жексенбі демалыс
            </div>
          </div>
          <div class="info-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
            <div>
              <strong>Төлем тәсілдері:</strong> Kaspi Red, Kaspi 0-0-12 (бөліп төлеу), Halyk, Қолма-қол
            </div>
          </div>
          <div class="info-item">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            <div>
              <strong>ҚР бойынша жеткізу:</strong> Қазпошта немесе автобуспен барлық қалаға ТЕГІН
            </div>
          </div>
        </div>

        <div class="showroom-cta-box">
          <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="btn-2gis-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
            <span>2GIS маршрутын ашу</span>
          </a>
          <a href="https://wa.me/{WA}?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%81%D1%96%D0%B7%20%D0%B1%D0%B5!%20%D0%A1%D0%B0%D0%B9%D1%80%D0%B0%D0%BD%20%D0%A1%D0%B8%D1%82%D0%B8%D0%B4%D0%B5%D0%B3%D1%96%20320%20%D0%BA%D0%B5%D2%A3%D1%81%D0%B5%D0%B3%D0%B5%20%D0%BA%D0%B5%D0%BB%D0%B3%D1%96%D0%BC%20%D0%BA%D0%B5%D0%BB%D0%B5%D0%B4%D1%96" target="_blank" rel="noopener" class="btn-whatsapp-showroom">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.669-.699c.969.54 1.777.82 2.791.82 3.181 0 5.768-2.587 5.768-5.767.001-3.18-2.585-5.805-5.768-5.805zm0 10.457c-.888 0-1.656-.25-2.348-.687l-.168-.106-1.57.412.419-1.53-.11-.176c-.469-.747-.716-1.517-.716-2.404 0-2.482 2.019-4.501 4.493-4.501s4.493 2.019 4.493 4.501c0 2.483-2.019 4.491-4.493 4.491z"/></svg>
            <span>WhatsApp-тан сұрау</span>
          </a>
        </div>
      </div>

      <!-- 2GIS Map Mockup -->
      <div class="showroom-map-mockup">
        <div class="map-overlay"></div>
        <div class="map-content">
          <div class="map-pin-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
          </div>
          <h3 style="font-size: 20px; font-weight: 700; margin-bottom: 6px;">БЦ «Сайран Сити», 320-кеңсе</h3>
          <p style="font-size: 13px; opacity: 0.85; margin-bottom: 16px;">Өтеген батыр көшесі 11а (Төле би қиылысы маңы)</p>
          <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="btn-2gis-primary" style="padding: 10px 20px; font-size: 13px;">
            2GIS арқылы бару
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- ───────── FOOTER ───────── -->
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-brand">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
          <img src="./images/logo.jpg" alt="UAQYT kzt" style="width: 44px; height: 44px; border-radius: 10px; object-fit: cover; border: 1px solid rgba(255,255,255,0.15);">
          <div>
            <div class="footer-logo" style="margin: 0; line-height: 1;">UAQYT</div>
            <small style="color: var(--accent-gold); font-size: 11px; letter-spacing: 1px; font-weight: 700;">kzt boutique</small>
          </div>
        </div>
        <p style="font-size: 13.5px; line-height: 1.6;">
          Жеке есім, ру таңбасы және ведомстволық эмблема қашалған қол сағаттар бутигі. Қазақстан бойынша 1000-нан астам риза клиент.
        </p>
        <div style="margin-top: 10px; font-size: 13px;">
          📍 Алматы, Өтеген батыр 11а, БЦ Сайран Сити 320
        </div>
      </div>

      <div>
        <h4 class="footer-title">Навигация</h4>
        <ul class="footer-links">
          <li><a href="#hero" class="footer-link">Басты бет</a></li>
          <li><a href="#bonus" class="footer-link">1+1 Бонус сағат</a></li>
          <li><a href="#catalog" class="footer-link">Сағаттар каталогы</a></li>
          <li><a href="#customizer" class="footer-link">Интерактивті циферблат</a></li>
          <li><a href="#reviews" class="footer-link">Клиенттер пікірі</a></li>
          <li><a href="#contact" class="footer-link">Шоурум мекен-жайы</a></li>
        </ul>
      </div>

      <div>
        <h4 class="footer-title">Әлеуметтік желілер</h4>
        <ul class="footer-links">
          <li><a href="https://www.instagram.com/uaqyt.kzt?psln=ZXd3MTI5cmI3NGF6" target="_blank" rel="noopener" class="footer-link">Instagram: @uaqyt.kzt</a></li>
          <li><a href="https://www.tiktok.com/@uaqyt.kzz2?_t=ZM-8uQyLn8Uuxi&_r=1" target="_blank" rel="noopener" class="footer-link">TikTok: @uaqyt.kzz2</a></li>
          <li><a href="https://wa.me/{WA}" target="_blank" rel="noopener" class="footer-link">WhatsApp: {WA_DISP}</a></li>
          <li><a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="footer-link">2GIS: Сайран Сити 320</a></li>
        </ul>
      </div>

      <div>
        <h4 class="footer-title">Кепілдік және төлем</h4>
        <p style="font-size: 13px; line-height: 1.6; margin-bottom: 12px;">
          Барлық сағатқа 6-12 ай кепілдік талоны беріледі.
        </p>
        <p style="font-size: 13px; line-height: 1.6; color: var(--accent-gold);">
          Kaspi Red, Kaspi 0-0-12, Halyk арқылы бөліп төлеу қарастырылған.
        </p>
      </div>
    </div>

    <div class="footer-bottom">
      <div>© 2026 UAQYT BOUTIQUE. Барлық құқықтар қорғалған.</div>
      <div>Сайт Apple стилінде жеке тапсырыспен әзірленген.</div>
    </div>
  </footer>

  {DOCK_HTML}

  {CART_HTML}

  <!-- ───────── ENTRY OFFER ───────── -->
  <div class="offer-overlay" id="offerOverlay" onclick="closeOffer()">
    <div class="offer-card" onclick="event.stopPropagation()" role="dialog" aria-modal="true" aria-labelledby="offerTitle">
      <button class="offer-close" type="button" onclick="closeOffer()" aria-label="Жабу">✕</button>
      <div class="offer-title" id="offerTitle">Сағатты таңдаңыз, қалғанын өзіміз жасаймыз</div>
      <ul class="offer-list">
        <li>Қазақстан бойынша ТЕГІН жеткізу</li>
        <li>Kaspi Red арқылы бөліп төлеу (0-0-12)</li>
        <li>Сатып алғанға бонус сағат сыйлыққа</li>
        <li>6–12 ай кепілдік және сыйлық қорабы</li>
      </ul>
      <div class="offer-actions">
        <a class="offer-btn primary" href="#picks" onclick="closeOffer()">Сағат таңдау</a>
        <a class="offer-btn wa" target="_blank" rel="noopener" href="https://wa.me/{WA}?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%81%D1%96%D0%B7%20%D0%B1%D0%B5!%20%D0%A1%D0%B0%D2%93%D0%B0%D1%82%20%D1%82%D0%B0%D2%A3%D0%B4%D0%B0%D1%83%D2%93%D0%B0%20%D0%BA%D3%A9%D0%BC%D0%B5%D0%BA%D1%82%D0%B5%D1%81%D1%96%D2%A3%D1%96%D0%B7%D1%88%D1%96">WhatsApp-та сұрау</a>
      </div>
    </div>
  </div>

  <!-- ───────── MOBILE STICKY BOTTOM BAR ───────── -->
  <div class="mobile-bottom-bar">
    <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="btn-mobile-2gis">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
      <span>2GIS</span>
    </a>
    <a href="https://www.instagram.com/uaqyt.kzt?psln=ZXd3MTI5cmI3NGF6" target="_blank" rel="noopener" class="btn-mobile-soc insta" aria-label="Instagram @uaqyt.kzt">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
    </a>
    <a href="https://www.tiktok.com/@uaqyt.kzz2?_t=ZM-8uQyLn8Uuxi&_r=1" target="_blank" rel="noopener" class="btn-mobile-soc tiktok" aria-label="TikTok @uaqyt.kzz2">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64c.298 0 .591.044.87.13V9.4a6.33 6.33 0 0 0-.87-.06A6.34 6.34 0 0 0 3 15.68a6.34 6.34 0 0 0 9.17 5.65 6.27 6.27 0 0 0 3.51-5.59V8.9a8.18 8.18 0 0 0 4.79 1.54v-3.4a4.85 4.85 0 0 1-.88-.35z"/></svg>
    </a>
    <a href="https://wa.me/{WA}?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%81%D1%96%D0%B7%20%D0%B1%D0%B5!%20UAQYT%20%D1%81%D0%B0%D0%B9%D1%82%D1%8B%D0%BD%D0%B0%D0%BD%20%D1%81%D0%B0%D2%93%D0%B0%D1%82%D2%9B%D0%B0%20%D1%82%D0%B0%D0%BF%D1%81%D1%8B%D1%80%D1%8B%D1%81%20%D0%B1%D0%B5%D1%80%D0%B3%D1%96%D0%BC%20%D0%BA%D0%B5%D0%BB%D0%B5%D0%B4%D1%96" target="_blank" rel="noopener" class="btn-mobile-wa">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.669-.699c.969.54 1.777.82 2.791.82 3.181 0 5.768-2.587 5.768-5.767.001-3.18-2.585-5.805-5.768-5.805zm0 10.457c-.888 0-1.656-.25-2.348-.687l-.168-.106-1.57.412.419-1.53-.11-.176c-.469-.747-.716-1.517-.716-2.404 0-2.482 2.019-4.501 4.493-4.501s4.493 2.019 4.493 4.501c0 2.483-2.019 4.491-4.493 4.491z"/></svg>
      <span>WhatsApp</span>
    </a>
  </div>

  <!-- ───────── APPLE-STYLE PRODUCT DETAIL MODAL ───────── -->
  <div class="modal-overlay" id="productModal" onclick="closeProductModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <button class="btn-close-modal" onclick="closeProductModal()" title="Жабу">✕</button>

      <div class="modal-img-col">
        <div class="modal-img-box">
          <img id="modalImg" src="" alt="" onclick="openLightboxFromModal()">
        </div>
        <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 10px;">
          🔍 Суретті толық экранда көру үшін басыңыз
        </div>
      </div>

      <div class="modal-info-col">
        <span class="modal-badge" id="modalBadge">Хит үлгі</span>
        <h3 class="modal-title" id="modalTitle">Сағат атауы</h3>

        <div class="modal-price-box">
          <span class="modal-price" id="modalPrice">34 900 ₸</span>
          <span class="modal-installment" id="modalInstallment">Бөліп төлеу: айына 2 908 ₸</span>
        </div>

        <div class="modal-trust"><span>✓ Тегін жеткізу</span><span>✓ Kaspi Red 0-0-12</span><span>✓ Сыйлық қорабы</span></div>

        <div class="modal-promo-note">
          <span>🎁</span>
          <span>25 900 ₸-ден бастап сағатқа — 2-ші сағат бонуске ТЕГІН беріледі!</span>
        </div>

        <table class="modal-specs-table">
          <tr>
            <td class="spec-name">⚙️ Механизмі:</td>
            <td class="spec-val" id="modalMech">Кварц</td>
          </tr>
          <tr>
            <td class="spec-name">💎 Әйнегі:</td>
            <td class="spec-val" id="modalGlass">Сызатқа төзімді сапфир / шыңдалған</td>
          </tr>
          <tr>
            <td class="spec-name">🛡️ Корпусы:</td>
            <td class="spec-val" id="modalCase">Болат корпус</td>
          </tr>
          <tr>
            <td class="spec-name">🔗 Бауы:</td>
            <td class="spec-val" id="modalStrap">Құйылған болат бау</td>
          </tr>
          <tr>
            <td class="spec-name">📜 Кепілдік:</td>
            <td class="spec-val">6–12 ай (модельге байланысты)</td>
          </tr>
          <tr>
            <td class="spec-name">🎁 Жинақтау:</td>
            <td class="spec-val">Фирмалық сыйлық қорабы + пакет + талон</td>
          </tr>
        </table>

        <!-- Custom Engraving Input -->
        <div class="modal-customizer-box">
          <label class="modal-customizer-label">Сағатқа жазылатын жеке есім немесе ру таңбасы:</label>
          <input type="text" class="modal-input-engrave" id="modalEngraveText" placeholder="Мысалы: Бауыржан / Найман, 15.06.2026">
          <div class="modal-city-box">
            <label class="modal-customizer-label">Қалаңыз (жеткізу үшін):</label>
            <input type="text" class="modal-input-engrave" id="modalCity" placeholder="Мысалы: Шымкент">
          </div>
        </div>

        <div class="modal-cta-group">
          <button class="btn-modal-whatsapp" onclick="sendOrderFromModal()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.669-.699c.969.54 1.777.82 2.791.82 3.181 0 5.768-2.587 5.768-5.767.001-3.18-2.585-5.805-5.768-5.805zm0 10.457c-.888 0-1.656-.25-2.348-.687l-.168-.106-1.57.412.419-1.53-.11-.176c-.469-.747-.716-1.517-.716-2.404 0-2.482 2.019-4.501 4.493-4.501s4.493 2.019 4.493 4.501c0 2.483-2.019 4.491-4.493 4.491z"/></svg>
            <span id="modalOrderBtnText">WhatsApp арқылы тапсырыс беру</span>
          </button>
          <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="btn-modal-2gis">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
            <span>Сайран Ситидегі шоурумға келіп көру (2GIS)</span>
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- ───────── REVIEW LIGHTBOX VIEWER ───────── -->
  <div class="lightbox-overlay" id="reviewLightbox" onclick="closeReviewLightbox(event)">
    <div class="lightbox-box" onclick="event.stopPropagation()">
      <button class="btn-close-lightbox" onclick="closeReviewLightbox()">✕</button>
      <button class="btn-lightbox-nav btn-lightbox-prev" onclick="changeReviewLightbox(-1)">‹</button>
      <img class="lightbox-img" id="lightboxReviewImg" src="" alt="WhatsApp пікір">
      <div class="lightbox-caption" id="lightboxReviewCaption">Клиенттің WhatsApp пікірі</div>
      <button class="btn-lightbox-nav btn-lightbox-next" onclick="changeReviewLightbox(1)">›</button>
    </div>
  </div>

  <!-- ───────── JAVASCRIPT LOGIC ───────── -->
  <script>
    // All products compiled data
    const productsData = {products_json};
    const reviewsData = {reviews_json};

    let activeFilter = 'mens';
    let activePrice = 'all';
    let activeSort = 'default';
    let currentModalProduct = null;
    let currentReviewIndex = 0;

    // Real-time sweeping second hand animation
    function animateHands() {{
      const now = new Date();
      const sec = now.getSeconds() + now.getMilliseconds() / 1000;
      const deg = sec * 6; // 360 / 60
      const heroSec = document.getElementById('liveHeroSecHand');
      const simSec = document.getElementById('liveSimSecHand');
      if (heroSec) heroSec.style.transform = `rotate(${{deg}}deg)`;
      if (simSec) simSec.style.transform = `rotate(${{deg}}deg)`;
      requestAnimationFrame(animateHands);
    }}
    requestAnimationFrame(animateHands);

    // Interactive Dial preview updater
    function updateDialPreview() {{
      const name = document.getElementById('inputName').value || 'АРМАН';
      const sub = document.getElementById('inputSub').value || 'АРҒЫН РУЫ';
      const dt = document.getElementById('inputDate').value || 'UAQYT KZT • 2026';

      const dialName = document.getElementById('simDialName');
      const dialSub = document.getElementById('simDialSub');
      const dialDate = document.getElementById('simDialDate');

      if (dialName) {{
        dialName.textContent = name.toUpperCase();
        const n = name.length;
        dialName.style.fontSize = Math.max(13, Math.min(21, 21 - Math.max(0, n - 9) * 1.1)) + 'px';
      }}
      if (dialSub) dialSub.textContent = sub.toUpperCase();
      if (dialDate) dialDate.textContent = dt;
    }}

    function updateClanSelection() {{
      const sel = document.getElementById('selectClan');
      const val = sel.value;
      const subInput = document.getElementById('inputSub');
      const tamgaBox = document.getElementById('simTamgaBox');

      const clanMap = {{
        'argyn': {{ name: 'АРҒЫН РУЫ', icon: '<circle cx="20" cy="30" r="10" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="40" cy="30" r="10" fill="none" stroke="currentColor" stroke-width="3"/>' }},
        'nayman': {{ name: 'НАЙМАН РУЫ', icon: '<path d="M15 15 L30 35 L45 15 M30 35 L30 55" fill="none" stroke="currentColor" stroke-width="4"/>' }},
        'kipchak': {{ name: 'ҚЫПШАҚ РУЫ', icon: '<line x1="20" y1="10" x2="20" y2="50" stroke="currentColor" stroke-width="4"/><line x1="40" y1="10" x2="40" y2="50" stroke="currentColor" stroke-width="4"/>' }},
        'dulat': {{ name: 'ДУЛАТ РУЫ', icon: '<circle cx="30" cy="30" r="18" fill="none" stroke="currentColor" stroke-width="4"/>' }},
        'aday': {{ name: 'АДАЙ РУЫ', icon: '<path d="M30 10 L30 50 M20 20 L30 10 L40 20" fill="none" stroke="currentColor" stroke-width="4"/>' }},
        'shapyrashty': {{ name: 'ШАПЫРАШТЫ РУЫ', icon: '<path d="M35 15 A15 15 0 1 0 35 45 A10 10 0 1 1 35 15" fill="currentColor"/>' }},
        'alban': {{ name: 'АЛБАН РУЫ', icon: '<path d="M30 10 L45 35 L15 35 Z M20 35 L20 50 M40 35 L40 50" fill="none" stroke="currentColor" stroke-width="3.5"/>' }},
        'berish': {{ name: 'БЕРІШ РУЫ', icon: '<polygon points="30,5 37,22 55,22 41,34 46,51 30,40 14,51 19,34 5,22 23,22" fill="currentColor"/>' }},
        'tortkara': {{ name: 'ТӨРТҚАРА РУЫ', icon: '<rect x="15" y="15" width="30" height="30" fill="none" stroke="currentColor" stroke-width="4"/>' }},
        'shekti': {{ name: 'ШЕКТІ РУЫ', icon: '<path d="M30 10 L50 45 L10 45 Z" fill="none" stroke="currentColor" stroke-width="4"/>' }},
        'ysty': {{ name: 'ЫСТЫ РУЫ', icon: '<line x1="15" y1="15" x2="45" y2="45" stroke="currentColor" stroke-width="4"/><circle cx="15" cy="15" r="5" fill="currentColor"/>' }},
        'oshakty': {{ name: 'ОШАҚТЫ РУЫ', icon: '<polygon points="30,12 48,48 12,48" fill="none" stroke="currentColor" stroke-width="4"/>' }},
        'tore': {{ name: 'ТӨРЕ ӘУЛЕТІ', icon: '<path d="M10 40 L15 15 L25 30 L30 10 L35 30 L45 15 L50 40 Z" fill="none" stroke="currentColor" stroke-width="3.5"/>' }},
        'kozha': {{ name: 'ҚОЖА ӘУЛЕТІ', icon: '<circle cx="30" cy="30" r="18" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="30" cy="30" r="8" fill="currentColor"/>' }},
        'service_mvd': {{ name: 'ҚР ІІМ ПОЛИЦИЯ', icon: '<path d="M30 10 L48 20 L48 35 C48 45 30 52 30 52 C30 52 12 45 12 35 L12 20 Z" fill="none" stroke="currentColor" stroke-width="3"/>' }},
        'service_knb': {{ name: 'ҚР ҰҚК КНБ', icon: '<path d="M30 8 L46 16 L46 32 C46 44 30 52 30 52 C30 52 14 44 14 32 L14 16 Z" fill="none" stroke="currentColor" stroke-width="3"/><line x1="30" y1="12" x2="30" y2="48" stroke="currentColor" stroke-width="2"/>' }},
        'service_arm': {{ name: 'ҚР ҚАРУЛЫ КҮШТЕРІ', icon: '<polygon points="30,8 36,22 52,22 39,32 44,48 30,38 16,48 21,32 8,22 24,22" fill="currentColor"/>' }}
      }};

      const match = clanMap[val];
      if (match) {{
        subInput.value = match.name;
        tamgaBox.innerHTML = `<svg class="dial-tamga-icon" viewBox="0 0 60 60" fill="currentColor">${{match.icon}}</svg>`;
        updateDialPreview();
      }}
    }}

    function orderCustomizedDial() {{
      const name = document.getElementById('inputName').value || 'Арман';
      const sub = document.getElementById('inputSub').value || 'Арғын руы';
      const text = encodeURIComponent(`Сәлеметсіз бе! Мен UAQYT сайтының конструкторынан өз сағатымды құрастырдым:\n\n• Есім: «${{name}}»\n• Таңба/Шен: «${{sub}}»\n• 1+1 Бонус сағат акциясы бойынша тапсырыс бергім келеді.`);
      window.open(`https://wa.me/{WA}?text=${{text}}`, '_blank');
    }}

    // Hero Showcase Switcher & Lightbox
    function switchHeroShowcase(imgSrc, title, desc, btn) {{
      const imgElem = document.getElementById('heroShowcaseMainImg');
      const titleElem = document.getElementById('heroShowcaseTitle');
      const descElem = document.getElementById('heroShowcaseDesc');
      if (imgElem) imgElem.src = imgSrc;
      if (titleElem) titleElem.textContent = title;
      if (descElem && desc) descElem.textContent = desc;
      document.querySelectorAll('.hero-thumb-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
    }}

    function openShowcaseLightbox(imgSrc, title) {{
      const currentImg = document.getElementById('heroShowcaseMainImg');
      const src = currentImg ? currentImg.src : imgSrc;
      window.open(src, '_blank');
    }}

    // Filter catalog
    function setCategoryFilter(cat, btn) {{
      activeFilter = cat;
      document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active', 'active-special'));
      if (cat === 'couples') {{
        btn.classList.add('active-special');
      }} else {{
        btn.classList.add('active');
      }}
      filterCatalog();
    }}

    function setPriceFilter(range, btn) {{
      activePrice = range;
      document.querySelectorAll('.price-chip').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
      filterCatalog();
    }}

    function priceMatches(price) {{
      if (activePrice === 'all') return true;
      if (price >= 999999) return false;
      if (activePrice === 't1') return price < 30000;
      if (activePrice === 't2') return price >= 30000 && price < 40000;
      if (activePrice === 't3') return price >= 40000 && price < 55000;
      if (activePrice === 't4') return price >= 55000;
      return true;
    }}

    function filterCatalog() {{
      const query = document.getElementById('catalogSearch').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.product-card');
      let shown = 0;

      cards.forEach(card => {{
        const cardCat = card.getAttribute('data-category') || '';
        const cardTitle = card.querySelector('.card-title').textContent.toLowerCase();
        const cardDesc = card.querySelector('.card-desc').textContent.toLowerCase();
        const cardTag = card.querySelector('.card-category-tag').textContent.toLowerCase();

        let matchesCat = true;
        if (activeFilter !== 'all') {{
          if (activeFilter === 'priced') {{
            matchesCat = cardCat.includes('priced');
          }} else if (activeFilter === 'request') {{
            matchesCat = cardCat.includes('request');
          }} else if (activeFilter === 'mens') {{
            matchesCat = cardCat.includes('mens') && !cardCat.includes('couples');
          }} else {{
            matchesCat = cardCat.includes(activeFilter);
          }}
        }}

        let matchesQuery = true;
        if (query) {{
          matchesQuery = cardTitle.includes(query) || cardDesc.includes(query) || cardTag.includes(query);
        }}

        const matchesPrice = priceMatches(parseInt(card.getAttribute('data-price')));

        if (matchesCat && matchesQuery && matchesPrice) {{
          card.style.display = 'flex';
          shown++;
        }} else {{
          card.style.display = 'none';
        }}
      }});
      const cnt = document.getElementById('catalogCount');
      if (cnt) cnt.textContent = shown ? ('Табылды: ' + shown + ' сағат') : 'Бұл сүзгі бойынша сағат табылмады. Басқа санатты немесе бағаны таңдаңыз.';
    }}

    function sortCatalog() {{
      const sortVal = document.getElementById('sortSelect').value;
      const grid = document.getElementById('productsGrid');
      const cards = Array.from(grid.querySelectorAll('.product-card'));

      if (!grid.dataset.indexed) {{ cards.forEach((c, i) => c.dataset.idx = i); grid.dataset.indexed = '1'; }}
      const pv = c => {{ const v = parseInt(c.getAttribute('data-price')); return v >= 999999 ? null : v; }};
      const byIdx = (a, b) => a.dataset.idx - b.dataset.idx;
      if (sortVal === 'price_asc' || sortVal === 'price_desc') {{
        const dir = sortVal === 'price_asc' ? 1 : -1;
        cards.sort((a, b) => {{
          const x = pv(a), y = pv(b);
          if (x === null && y === null) return byIdx(a, b);
          if (x === null) return 1;
          if (y === null) return -1;
          return (x - y) * dir || byIdx(a, b);
        }});
      }} else {{
        cards.sort(byIdx);
      }}

      cards.forEach(c => grid.appendChild(c));
    }}

    // Reviews Filter
    function filterReviews(filter, btn) {{
      document.querySelectorAll('.rev-filter-tab').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
      const cards = document.querySelectorAll('.review-card');

      cards.forEach(c => {{
        const cat = c.getAttribute('data-rev-cat') || '';
        if (filter === 'all' || cat.includes(filter)) {{
          c.style.display = 'flex';
        }} else {{
          c.style.display = 'none';
        }}
      }});
    }}

    // Open Product Modal
    function openProductModal(productId) {{
      const p = productsData.find(item => item.id === productId);
      if (!p) return;
      currentModalProduct = p;

      document.getElementById('modalImg').src = p.img;
      document.getElementById('modalImg').alt = p.name;
      document.getElementById('modalTitle').textContent = p.name;
      document.getElementById('modalBadge').textContent = p.badge;

      const isReq = p.is_price_on_request;
      const priceElem = document.getElementById('modalPrice');
      const instElem = document.getElementById('modalInstallment');
      const btnText = document.getElementById('modalOrderBtnText');

      if (isReq) {{
        priceElem.textContent = 'Бағасы жеке нақтыланады';
        priceElem.style.fontSize = '20px';
        instElem.textContent = 'WhatsApp-та бағасын нақтылау';
        btnText.textContent = 'WhatsApp арқылы бағасын білу';
      }} else {{
        priceElem.textContent = `${{p.price.toLocaleString('ru-RU')}} ₸`;
        priceElem.style.fontSize = '28px';
        const monthly = Math.floor(p.price / 12).toLocaleString('ru-RU');
        instElem.textContent = `Kaspi Red: айына ${{monthly}} ₸ (0-0-12)`;
        btnText.textContent = 'Сатып алу: WhatsApp-қа жіберу';
      }}

      document.getElementById('modalMech').textContent = p.mech || 'Кварц';
      document.getElementById('modalGlass').textContent = p.glass || 'Сызатқа төзімді шыңдалған минералды / сапфир';
      document.getElementById('modalCase').textContent = p.case || 'Болат корпус';
      document.getElementById('modalStrap').textContent = p.strap || 'Құйылған болат бау';

      const modal = document.getElementById('productModal');
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeProductModal(e) {{
      const modal = document.getElementById('productModal');
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }}

    function sendOrderFromModal() {{
      if (!currentModalProduct) return;
      const engrave = document.getElementById('modalEngraveText').value.trim();
      const p = currentModalProduct;
      let msg = '';

      if (p.is_price_on_request) {{
        msg = `Сәлеметсіз бе! UAQYT сайтынан мына сағаттың бағасы мен дайындалу мерзімін білгім келеді:\n\n• Үлгі: «${{p.name}}»\n• Категория: ${{p.tag}}`;
      }} else {{
        msg = `Сәлеметсіз бе! UAQYT сайтынан сағатқа тапсырыс бергім келеді:\n\n• Үлгі: «${{p.name}}»\n• Бағасы: ${{p.price.toLocaleString('ru-RU')}} ₸\n• 1+1 Бонус сағат акциясы бойынша`;
      }}

      const city = (document.getElementById('modalCity') || {{ value: '' }}).value.trim();
      if (city) {{
        msg += `
• Қала: ${{city}}`;
      }}

      if (engrave) {{
        msg += `\n• Нақышталатын мәтін: «${{engrave}}»`;
      }}

      window.open(`https://wa.me/{WA}?text=${{encodeURIComponent(msg)}}`, '_blank');
    }}

    function openLightboxFromModal() {{
      if (!currentModalProduct) return;
      window.open(currentModalProduct.img, '_blank');
    }}

    // Review Lightbox Logic
    function openReviewLightbox(index) {{
      currentReviewIndex = index;
      updateLightboxContent();
      const lb = document.getElementById('reviewLightbox');
      lb.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeReviewLightbox(e) {{
      const lb = document.getElementById('reviewLightbox');
      lb.classList.remove('active');
      document.body.style.overflow = '';
    }}

    function changeReviewLightbox(dir) {{
      currentReviewIndex = (currentReviewIndex + dir + reviewsData.length) % reviewsData.length;
      updateLightboxContent();
    }}

    function updateLightboxContent() {{
      const r = reviewsData[currentReviewIndex];
      if (!r) return;
      document.getElementById('lightboxReviewImg').src = r.img;
      document.getElementById('lightboxReviewCaption').textContent = `${{r.author}} (${{r.city}}) • ${{r.order}}`;
    }}

    // ───── Gift picker ─────
    const PICK_DEFAULT = ['p26900_karakerey', 'p34900_nayman', 'p39900_aday', 'p54900_kishizhuz'];
    const pick = {{ who: null, budget: null }};
    const PICK_WHO_TAB = {{ mens: 'mens', couples: 'couples', service: 'service' }};

    function pickBudgetOk(price) {{
      if (!pick.budget) return true;
      if (pick.budget === 't1') return price < 30000;
      if (pick.budget === 't2') return price >= 30000 && price < 40000;
      if (pick.budget === 't3') return price >= 40000 && price < 55000;
      return price >= 55000;
    }}

    function setPick(group, val, btn) {{
      pick[group] = pick[group] === val ? null : val;
      btn.parentNode.querySelectorAll('.picker-chip').forEach(b => b.classList.toggle('active', b.dataset.v === pick[group]));
      renderPicks();
    }}

    function renderPicks() {{
      const box = document.getElementById('pickResults');
      if (!box) return;
      let list = productsData.filter(p => !p.is_price_on_request);
      if (pick.who === 'mens') list = list.filter(p => p.cat.includes('mens') && !p.cat.includes('couples'));
      if (pick.who === 'couples') list = list.filter(p => p.cat.includes('couples'));
      if (pick.who === 'service') list = list.filter(p => p.cat.includes('service'));
      list = list.filter(p => pickBudgetOk(p.price));
      let chosen;
      if (pick.who || pick.budget) {{
        chosen = list.slice(0, 4);
      }} else {{
        chosen = PICK_DEFAULT.map(id => productsData.find(p => p.id === id)).filter(Boolean);
      }}
      if (!chosen.length) {{
        box.innerHTML = '<div class="picker-empty">Бұл бюджетте дайын бағасы бар үлгі жоқ. Басқа бюджетті таңдаңыз немесе WhatsApp-қа жазыңыз, жеке таңдап береміз.</div>';
      }} else {{
        box.innerHTML = chosen.map(p => {{
          const price = p.price.toLocaleString('ru-RU');
          const monthly = Math.floor(p.price / 12).toLocaleString('ru-RU');
          return `<div class="pick-card" onclick="openProductModal('${{p.id}}')">
            <img src="${{p.img}}" alt="${{p.name}}" loading="lazy">
            <div class="pick-card-body">
              <div class="pick-card-name">${{p.name}}</div>
              <div class="pick-card-price">${{price}} ₸</div>
              <div class="pick-card-inst">Kaspi Red: айына ${{monthly}} ₸</div>
              <button type="button" class="pick-card-btn">Сатып алу</button>
            </div>
          </div>`;
        }}).join('');
      }}
      const wa = document.getElementById('pickWa');
      if (wa) {{
        const who = {{ mens: 'ерлерге сыйлық', couples: 'жұбайларға (1+1)', service: 'қызметкерге' }}[pick.who] || 'таңдалмаған';
        const bud = {{ t1: '30 000 ₸ дейін', t2: '30 000 – 40 000 ₸', t3: '40 000 – 55 000 ₸', t4: '55 000 ₸ бастап' }}[pick.budget] || 'маңызды емес';
        wa.href = 'https://wa.me/{WA}?text=' + encodeURIComponent('Сәлеметсіз бе! Сағат таңдауға көмектесіңізші. Кімге: ' + who + '. Бюджет: ' + bud + '.');
      }}
    }}

    function applyPickToCatalog() {{
      const tab = document.querySelector('[data-filter="' + (PICK_WHO_TAB[pick.who] || 'all') + '"]');
      if (tab) setCategoryFilter(PICK_WHO_TAB[pick.who] || 'all', tab);
      const chips = document.querySelectorAll('.price-chip');
      const idx = {{ t1: 1, t2: 2, t3: 3, t4: 4 }}[pick.budget] || 0;
      if (chips[idx]) setPriceFilter(pick.budget || 'all', chips[idx]);
      document.getElementById('catalog').scrollIntoView({{ behavior: 'smooth' }});
    }}

    // ───── Reviews teaser ─────
    function renderTeaser() {{
      const g = document.getElementById('teaserGrid');
      if (!g) return;
      const pick = ['review-12', 'review-13', 'review-15', 'review-16', 'review-18', 'review-19'];
      const items = reviewsData.map((r, i) => ({{ r, i }})).filter(x => pick.some(t => x.r.img.includes(t + '.jpg'))).slice(0, 6);
      g.innerHTML = items.map(({{ r, i }}) => `<div class="teaser-card" onclick="openReviewLightbox(${{i}})">
        <img src="${{r.img}}" alt="Клиент пікірі" loading="lazy">
        <div class="teaser-cap">${{r.author}}, ${{r.city.replace(' қаласы', '')}}<small>${{r.order}}</small></div>
      </div>`).join('');
    }}

    // Mobile navigation
    function toggleNav() {{
      const nb = document.querySelector('.navbar');
      const open = nb.classList.toggle('open');
      document.getElementById('navBurger').setAttribute('aria-expanded', open);
    }}
    document.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => {{
      document.querySelector('.navbar').classList.remove('open');
    }}));

    // Entry offer (once per session)
    function closeOffer() {{
      document.getElementById('offerOverlay').classList.remove('active');
    }}
    try {{
      if (!sessionStorage.getItem('uaqytOfferSeen')) {{
        setTimeout(() => {{
          document.getElementById('offerOverlay').classList.add('active');
          sessionStorage.setItem('uaqytOfferSeen', '1');
        }}, 2500);
      }}
    }} catch (e) {{}}

    // Initial catalog state: men's watches first

    // Keyboard navigation for modals
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') {{
        closeProductModal();
        closeReviewLightbox();
        closeOffer();
      }} else if (e.key === 'ArrowLeft') {{
        const lb = document.getElementById('reviewLightbox');
        if (lb.classList.contains('active')) changeReviewLightbox(-1);
      }} else if (e.key === 'ArrowRight') {{
        const lb = document.getElementById('reviewLightbox');
        if (lb.classList.contains('active')) changeReviewLightbox(1);
      }}
    }});
    {JS_EXTRA_WA}
  </script>
</body>
</html>'''

    soup, unmapped = i18n_engine.localize(html_content, all_products_sorted)
    i18n_engine.apply_dark(soup)
    i18n_engine.reorder(soup, ["hero", "story", "picks", "holidays", "bonus", "catalog", "customizer", "reviews", "socials", "contact"])
    if unmapped:
        print("UNMAPPED Kazakh strings:", len(unmapped))
        for u in unmapped[:60]:
            print("  -", u[:140])
    html_content = "<!DOCTYPE html>\n" + str(soup).replace("<!DOCTYPE html>", "", 1).lstrip()
    with open('D:/watch-boutique/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Successfully built D:/watch-boutique/index.html")

if __name__ == '__main__':
    generate()
