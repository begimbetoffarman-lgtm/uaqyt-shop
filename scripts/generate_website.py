# -*- coding: utf-8 -*-
import os, sys, json

sys.path.insert(0, os.path.dirname(__file__))
sys.stdout.reconfigure(encoding='utf-8')

from compile_data import all_products

# Card template with Zoom / Lightbox & Kaspi installment badge
card_template = """
        <div class="product-card" data-category="{cat}" data-price="{price}" data-name="{name}">
          <div class="card-badge">{badge}</div>
          <div class="card-img-box" onclick="openLightbox('{img}', '{name}', '{price_str}')" title="Үлкейтіп көру үшін басыңыз">
            <img src="{img}" alt="{name}" loading="lazy">
            <span class="zoom-hint">🔍 Үлкейтіп көру</span>
          </div>
          <div class="card-body">
            <div class="card-category-tag">{tag}</div>
            <h3 class="card-title">{name}</h3>
            <p class="card-desc">{desc}</p>
            <div class="installment-pill" title="Бөліп төлеу мүмкіндігі">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
              <span>Бөліп төлеу: айына <strong>{monthly_installment} ₸</strong></span>
            </div>
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
for p in all_products:
    price_str = f"{p['price']:,}".replace(',', ' ')
    monthly_installment = f"{p['price'] // 12:,}".replace(',', ' ')
    c = card_template.format(
        id=p['id'],
        name=p['name'],
        cat=p['cat'],
        price=p['price'],
        price_str=price_str,
        monthly_installment=monthly_installment,
        tag=p['tag'],
        desc=p['desc'],
        img=p['img'],
        badge=p['badge']
    )
    cards_html.append(c)

all_cards_str = "\n".join(cards_html)

html_template = """<!DOCTYPE html>
<html lang="kk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>UAQYT — Жеке жазуы бар есімді қол сағаттар бутігі</title>
  <meta name="description" content="UAQYT — жеке есім мен шежіре-ру таңбалары, қызметтік органдардың (ІІМ, ҰҚК, ТЖМ, ҚР ҚК) ресми эмблемалары қашалған мәртебелі қол сағаттар бутігі.">
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
      --accent-red: #e11d48;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
      --shadow-md: 0 10px 30px rgba(0,0,0,0.06);
      --shadow-lg: 0 20px 45px rgba(0,0,0,0.09);
      --font-serif: 'Cormorant Garamond', Georgia, serif;
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --nav-height: 68px;
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

    /* Top Presentation Pitch Drawer */
    .pitch-banner {{
      background: #fdfaf3;
      border-bottom: 1px solid rgba(184, 142, 79, 0.25);
      padding: 10px 20px;
      font-size: 13px;
      color: var(--accent-gold-dark);
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      z-index: 101;
    }}

    .pitch-badge {{
      background: var(--accent-gold);
      color: #fff;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .pitch-btn {{
      background: #fff;
      border: 1px solid var(--accent-gold);
      color: var(--accent-gold-dark);
      padding: 5px 16px;
      border-radius: 20px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      transition: var(--transition);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .pitch-btn:hover {{
      background: var(--accent-gold);
      color: #fff;
    }}

    .pitch-drawer {{
      display: none;
      background: #fff;
      border-bottom: 1px solid var(--border);
      padding: 24px 20px;
      position: relative;
      z-index: 100;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}

    .pitch-drawer.active {{
      display: block;
      animation: slideDown 0.3s ease;
    }}

    .pitch-grid {{
      max-width: 1240px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
    }}

    .pitch-card {{
      background: var(--bg-alt);
      border: 1px solid var(--border);
      padding: 18px;
      border-radius: 14px;
    }}

    .pitch-card h4 {{
      color: var(--accent-gold-dark);
      margin-bottom: 6px;
      font-size: 15px;
    }}

    .pitch-card p {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* Navigation */
    header {{
      position: sticky;
      top: 0;
      z-index: 99;
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: saturate(180%) blur(20px);
      -webkit-backdrop-filter: saturate(180%) blur(20px);
      border-bottom: 1px solid var(--border);
      height: var(--nav-height);
      display: flex;
      align-items: center;
      transition: var(--transition);
    }}

    .header-inner {{
      max-width: 1300px;
      margin: 0 auto;
      width: 100%;
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .brand-logo {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text);
    }}

    .logo-mark {{
      width: 40px;
      height: 40px;
      border: 1.5px solid var(--accent-gold);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-serif);
      font-weight: 700;
      font-size: 20px;
      color: var(--accent-gold);
      background: var(--accent-gold-soft);
      box-shadow: 0 2px 10px rgba(184, 142, 79, 0.15);
    }}

    .brand-name {{
      font-family: var(--font-serif);
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #111;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 22px;
      list-style: none;
    }}

    .nav-link {{
      color: #4b5563;
      text-decoration: none;
      font-size: 14px;
      font-weight: 500;
      transition: var(--transition);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .nav-link:hover {{
      color: var(--accent-gold);
    }}

    .nav-tag {{
      background: #fee2e2;
      color: #991b1b;
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 10px;
      font-weight: 700;
      animation: pulseBadge 2s infinite;
    }}

    @keyframes pulseBadge {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.08); }}
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn-wa-header {{
      background: var(--accent-green);
      color: #fff;
      padding: 9px 20px;
      border-radius: 30px;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      box-shadow: 0 4px 14px rgba(37, 211, 102, 0.28);
    }}

    .btn-wa-header:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 22px rgba(37, 211, 102, 0.38);
    }}

    /* Hero Section */
    .hero {{
      padding: 70px 24px 60px;
      max-width: 1300px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 46px;
      align-items: center;
    }}

    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--accent-gold-soft);
      border: 1px solid var(--border-gold);
      padding: 6px 16px;
      border-radius: 30px;
      font-size: 12px;
      font-weight: 600;
      color: var(--accent-gold-dark);
      margin-bottom: 24px;
      letter-spacing: 0.5px;
    }}

    .hero-badge-dot {{
      width: 8px;
      height: 8px;
      background: var(--accent-gold);
      border-radius: 50%;
    }}

    .hero-title {{
      font-family: var(--font-serif);
      font-size: 54px;
      font-weight: 400;
      line-height: 1.12;
      margin-bottom: 22px;
      color: #111;
      letter-spacing: -0.5px;
    }}

    .hero-title span {{
      color: var(--accent-gold);
      font-style: italic;
    }}

    .hero-desc {{
      color: var(--text-muted);
      font-size: 17px;
      line-height: 1.7;
      max-width: 530px;
      margin-bottom: 30px;
    }}

    .hero-pills-row {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-bottom: 34px;
    }}

    .hero-pill {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13px;
      color: #374151;
      background: #f9fafb;
      border: 1px solid var(--border);
      padding: 10px 14px;
      border-radius: 12px;
      transition: var(--transition);
    }}

    .hero-pill:hover {{
      border-color: var(--accent-gold);
      background: #fff;
      transform: translateY(-2px);
    }}

    .hero-pill svg {{
      width: 18px;
      height: 18px;
      stroke: var(--accent-gold);
      flex-shrink: 0;
    }}

    .hero-cta-group {{
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .btn-gold {{
      background: var(--accent-gold);
      color: #fff;
      padding: 15px 32px;
      border-radius: 40px;
      font-weight: 700;
      font-size: 14px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      border: none;
      cursor: pointer;
    }}

    .btn-gold:hover {{
      background: var(--accent-gold-dark);
      transform: translateY(-2px);
      box-shadow: 0 10px 25px rgba(184, 142, 79, 0.28);
    }}

    .btn-outline {{
      background: #fff;
      border: 1px solid var(--border);
      color: var(--text);
      padding: 15px 28px;
      border-radius: 40px;
      font-size: 14px;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      cursor: pointer;
    }}

    .btn-outline:hover {{
      background: var(--bg-alt);
      border-color: #cbd5e1;
      transform: translateY(-2px);
    }}

    /* Hero Showcase 3D Floating Card */
    .hero-visual-card {{
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 28px;
      padding: 18px;
      box-shadow: var(--shadow-lg);
      position: relative;
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
      cursor: pointer;
    }}

    .hero-visual-card:hover {{
      transform: translateY(-8px) scale(1.01);
      box-shadow: 0 30px 60px rgba(0,0,0,0.12);
    }}

    .hero-visual-img {{
      width: 100%;
      height: 440px;
      object-fit: cover;
      border-radius: 20px;
      display: block;
      margin-bottom: 14px;
    }}

    .hero-visual-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 6px;
    }}

    /* Section Global */
    .section-wrap {{
      padding: 70px 24px;
      max-width: 1300px;
      margin: 0 auto;
    }}

    .section-head {{
      text-align: center;
      max-width: 740px;
      margin: 0 auto 46px;
    }}

    .section-kicker {{
      font-size: 12px;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--accent-gold);
      margin-bottom: 10px;
      display: block;
      font-weight: 700;
    }}

    .section-title {{
      font-family: var(--font-serif);
      font-size: 42px;
      font-weight: 400;
      line-height: 1.2;
      margin-bottom: 12px;
      color: #111;
    }}

    .section-sub {{
      color: var(--text-muted);
      font-size: 16px;
    }}

    /* ───────── ШЕБЕРЛІК ПЕН САПА КЕПІЛІ (CRAFTSMANSHIP) ───────── */
    .craft-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-bottom: 50px;
    }}

    .craft-card {{
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 26px 22px;
      transition: var(--transition);
    }}

    .craft-card:hover {{
      border-color: var(--accent-gold);
      transform: translateY(-4px);
      box-shadow: var(--shadow-md);
    }}

    .craft-icon {{
      font-size: 28px;
      margin-bottom: 14px;
    }}

    .craft-card h4 {{
      font-size: 16px;
      color: #111;
      margin-bottom: 6px;
    }}

    .craft-card p {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    /* ───────── 1+1 АКЦИЯ БАННЕР / БЛОК ───────── */
    .promo-banner-section {{
      background: linear-gradient(135deg, #fdfaf3 0%, #fff6e9 100%);
      border: 1.5px solid var(--accent-gold);
      border-radius: 28px;
      padding: 40px;
      margin-bottom: 50px;
      box-shadow: var(--shadow-md);
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 36px;
      align-items: center;
    }}

    .promo-badge {{
      background: var(--accent-red);
      color: #fff;
      display: inline-block;
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 14px;
    }}

    .promo-title {{
      font-family: var(--font-serif);
      font-size: 34px;
      line-height: 1.2;
      margin-bottom: 14px;
      color: #111;
    }}

    .promo-title span {{
      color: var(--accent-gold);
      font-style: italic;
    }}

    .promo-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 22px;
    }}

    .promo-list li {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      color: #374151;
    }}

    .promo-list svg {{
      width: 18px;
      height: 18px;
      stroke: var(--accent-green);
      flex-shrink: 0;
    }}

    .promo-bonus-visual {{
      background: #fff;
      border: 1px solid rgba(184, 142, 79, 0.3);
      border-radius: 20px;
      padding: 18px;
      text-align: center;
      position: relative;
      cursor: pointer;
    }}

    .promo-bonus-visual img {{
      width: 100%;
      height: 310px;
      object-fit: cover;
      border-radius: 14px;
      margin-bottom: 12px;
      transition: var(--transition);
    }}

    .promo-bonus-visual:hover img {{
      transform: scale(1.02);
    }}

    .bonus-tag-pill {{
      position: absolute;
      top: 28px;
      right: 28px;
      background: var(--accent-red);
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 20px;
      box-shadow: 0 4px 12px rgba(225, 29, 72, 0.4);
    }}

    /* ───────── ШЫНАЙЫ ДАЙЫН ЖҰМЫСТАР ГАЛЕРЕЯСЫ (SHOWCASE) ───────── */
    .showcase-slider-wrap {{
      margin-bottom: 60px;
    }}

    .showcase-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
    }}

    .showcase-item {{
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 18px;
      overflow: hidden;
      transition: var(--transition);
      box-shadow: var(--shadow-sm);
      cursor: pointer;
    }}

    .showcase-item:hover {{
      transform: translateY(-6px);
      box-shadow: var(--shadow-md);
      border-color: var(--accent-gold);
    }}

    .showcase-item img {{
      width: 100%;
      height: 220px;
      object-fit: cover;
      display: block;
      transition: transform 0.4s ease;
    }}

    .showcase-item:hover img {{
      transform: scale(1.05);
    }}

    .showcase-caption {{
      padding: 12px;
      text-align: center;
    }}

    .showcase-caption h5 {{
      font-size: 13px;
      color: #111;
      margin-bottom: 2px;
    }}

    .showcase-caption p {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    /* ───────── КАТАЛОГ С ПЛАШКОЙ (КАК В DELINE / TITON) ───────── */
    .catalog-bar-sticky {{
      position: sticky;
      top: var(--nav-height);
      z-index: 40;
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: saturate(180%) blur(20px);
      -webkit-backdrop-filter: saturate(180%) blur(20px);
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
      margin-bottom: 36px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }}

    .catalog-bar-inner {{
      max-width: 1300px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .catalog-bar-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .search-box {{
      position: relative;
      flex: 1;
      min-width: 260px;
      max-width: 460px;
    }}

    .search-box svg {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      width: 18px;
      height: 18px;
      stroke: #9ca3af;
    }}

    .search-input {{
      width: 100%;
      padding: 10px 16px 10px 42px;
      border: 1px solid var(--border);
      border-radius: 30px;
      font-size: 14px;
      font-family: var(--font-sans);
      outline: none;
      background: var(--bg-alt);
      transition: var(--transition);
    }}

    .search-input:focus {{
      background: #fff;
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(184, 142, 79, 0.12);
    }}

    .sort-select {{
      padding: 9px 16px;
      border: 1px solid var(--border);
      border-radius: 20px;
      background: #fff;
      font-size: 13px;
      color: #374151;
      font-family: var(--font-sans);
      outline: none;
      cursor: pointer;
    }}

    .category-chips {{
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 4px;
      scrollbar-width: none;
    }}

    .category-chips::-webkit-scrollbar {{
      display: none;
    }}

    .chip-btn {{
      white-space: nowrap;
      padding: 8px 16px;
      border-radius: 30px;
      background: var(--bg-alt);
      border: 1px solid var(--border);
      font-size: 13px;
      font-weight: 500;
      color: #4b5563;
      cursor: pointer;
      transition: var(--transition);
    }}

    .chip-btn:hover {{
      background: #e5e7eb;
      color: #111;
    }}

    .chip-btn.active {{
      background: #111827;
      color: #fff;
      border-color: #111827;
    }}

    /* Product Grid */
    .product-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(295px, 1fr));
      gap: 24px;
    }}

    .product-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 22px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: var(--transition);
      position: relative;
      box-shadow: var(--shadow-sm);
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
      z-index: 2;
      background: rgba(17, 24, 39, 0.88);
      backdrop-filter: blur(8px);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 20px;
      letter-spacing: 0.5px;
    }}

    /* Card Image Box with improved height and zoom hint */
    .card-img-box {{
      width: 100%;
      height: 340px;
      background: #fbfbfc;
      overflow: hidden;
      position: relative;
      cursor: pointer;
    }}

    .card-img-box img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 25%;
      transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .product-card:hover .card-img-box img {{
      transform: scale(1.05);
    }}

    .zoom-hint {{
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(17, 24, 39, 0.78);
      backdrop-filter: blur(6px);
      color: #fff;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 14px;
      opacity: 0;
      transition: opacity 0.25s ease;
      pointer-events: none;
    }}

    .card-img-box:hover .zoom-hint {{
      opacity: 1;
    }}

    .card-body {{
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .card-category-tag {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--accent-gold);
      margin-bottom: 6px;
    }}

    .card-title {{
      font-family: var(--font-serif);
      font-size: 21px;
      font-weight: 600;
      color: #111;
      margin-bottom: 8px;
      line-height: 1.25;
    }}

    .card-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 12px;
      flex: 1;
    }}

    /* Kaspi installment pill */
    .installment-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #fdfaf3;
      border: 1px solid var(--border-gold);
      color: var(--accent-gold-dark);
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 11px;
      margin-bottom: 14px;
    }}

    .installment-pill svg {{
      stroke: var(--accent-gold);
      flex-shrink: 0;
    }}

    .card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--border);
      padding-top: 14px;
      margin-top: auto;
    }}

    .card-price {{
      font-family: var(--font-sans);
      font-size: 21px;
      font-weight: 800;
      color: #111;
      letter-spacing: -0.5px;
    }}

    .btn-card-action {{
      background: #111827;
      color: #fff;
      border: none;
      padding: 9px 18px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }}

    .btn-card-action:hover {{
      background: var(--accent-gold);
      transform: scale(1.02);
    }}

    /* ───────── ИНТЕРАКТИВНЫЙ КОНСТРУКТОР ГРАВИРОВКИ (С ЖИВЫМИ СТРЕЛКАМИ) ───────── */
    .engrave-section {{
      background: var(--bg-alt);
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      padding: 80px 24px;
    }}

    .engrave-container {{
      max-width: 1200px;
      margin: 0 auto;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 28px;
      padding: 40px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 46px;
      align-items: center;
      box-shadow: var(--shadow-md);
    }}

    .engrave-stage {{
      background: radial-gradient(circle at center, #ffffff 0%, #f1f3f5 100%);
      border: 1px solid var(--border);
      border-radius: 20px;
      height: 490px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
      perspective: 1000px;
    }}

    .watch-dial-frame {{
      width: 290px;
      height: 350px;
      border-radius: 28px;
      background: linear-gradient(135deg, #e5b95c 0%, #9c7b2a 50%, #e5b95c 100%);
      padding: 16px;
      box-shadow: 0 25px 50px rgba(0,0,0,0.22);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.3s ease, transform 0.2s ease;
      transform-style: preserve-3d;
    }}

    .watch-dial-inner {{
      width: 100%;
      height: 100%;
      background: radial-gradient(circle, #1a1b24 0%, #0b0c10 100%);
      border-radius: 18px;
      border: 2px solid rgba(220, 180, 80, 0.5);
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 30px 16px;
      overflow: hidden;
    }}

    .dial-mark-12 {{
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 11px;
      color: rgba(220, 180, 80, 0.7);
      font-weight: 700;
    }}
    .dial-mark-6 {{
      position: absolute;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 11px;
      color: rgba(220, 180, 80, 0.7);
      font-weight: 700;
    }}
    .dial-mark-3 {{
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 11px;
      color: rgba(220, 180, 80, 0.7);
      font-weight: 700;
    }}
    .dial-mark-9 {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 11px;
      color: rgba(220, 180, 80, 0.7);
      font-weight: 700;
    }}

    .dial-center-pin {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #dcb450;
      z-index: 6;
      box-shadow: 0 0 6px rgba(0,0,0,0.5);
    }}

    .dial-hand-hour {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: 4.5px;
      height: 52px;
      background: #dcb450;
      transform-origin: bottom center;
      transform: translate(-50%, -100%) rotate(45deg);
      border-radius: 4px;
      z-index: 4;
      box-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }}

    .dial-hand-min {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: 3px;
      height: 78px;
      background: #ffffff;
      transform-origin: bottom center;
      transform: translate(-50%, -100%) rotate(220deg);
      border-radius: 4px;
      z-index: 4;
      box-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }}

    .dial-hand-sec {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: 1.5px;
      height: 94px;
      background: #f43f5e;
      transform-origin: bottom center;
      transform: translate(-50%, -100%) rotate(0deg);
      border-radius: 2px;
      z-index: 5;
      animation: sweepSecond 60s linear infinite;
    }}

    @keyframes sweepSecond {{
      0% {{ transform: translate(-50%, -100%) rotate(0deg); }}
      100% {{ transform: translate(-50%, -100%) rotate(360deg); }}
    }}

    .dial-text-top {{
      font-family: var(--font-serif);
      font-size: 24px;
      font-weight: 700;
      color: #f7e7b4;
      letter-spacing: 2px;
      text-align: center;
      text-transform: uppercase;
      z-index: 2;
      text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }}

    .dial-ornament {{
      font-size: 16px;
      color: #dcb450;
      letter-spacing: 4px;
      margin: 4px 0;
      opacity: 0.85;
      z-index: 2;
    }}

    .dial-text-bottom {{
      font-family: var(--font-serif);
      font-size: 22px;
      color: #fff;
      letter-spacing: 2px;
      text-align: center;
      z-index: 2;
      text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }}

    .dial-sub-date {{
      font-size: 11px;
      color: #dcb450;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-top: 2px;
    }}

    .engrave-form {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .form-label {{
      font-size: 13px;
      font-weight: 600;
      color: #374151;
    }}

    .form-input, .form-select {{
      background: #f9fafb;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 11px 16px;
      font-size: 14px;
      color: #111;
      outline: none;
      transition: var(--transition);
      font-family: var(--font-sans);
    }}

    .form-input:focus, .form-select:focus {{
      background: #fff;
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(184, 142, 79, 0.12);
    }}

    .color-case-select {{
      display: flex;
      gap: 8px;
    }}

    .case-color-btn {{
      flex: 1;
      padding: 9px;
      border-radius: 12px;
      background: #f9fafb;
      border: 1px solid var(--border);
      color: #374151;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      text-align: center;
      transition: var(--transition);
    }}

    .case-color-btn.active {{
      border-color: var(--accent-gold);
      background: var(--accent-gold-soft);
      color: var(--accent-gold-dark);
    }}

    /* ───────── ШЫНАЙЫ ПІКІРЛЕР (WHATSAPP, INSTAGRAM, TIKTOK) ───────── */
    .reviews-section {{
      padding: 80px 24px;
      max-width: 1300px;
      margin: 0 auto;
    }}

    .reviews-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
    }}

    .review-card {{
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: var(--shadow-sm);
      transition: var(--transition);
    }}

    .review-card:hover {{
      transform: translateY(-4px);
      box-shadow: var(--shadow-md);
    }}

    .review-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .reviewer-info h4 {{
      font-size: 15px;
      color: #111;
      margin-bottom: 2px;
    }}

    .reviewer-meta {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .source-tag {{
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 12px;
    }}

    .review-stars {{
      color: #f59e0b;
      font-size: 14px;
      margin-bottom: 10px;
    }}

    .review-text {{
      font-size: 14px;
      color: #374151;
      line-height: 1.6;
      margin-bottom: 14px;
    }}

    .review-product-tag {{
      font-size: 12px;
      color: var(--accent-gold-dark);
      background: var(--accent-gold-soft);
      padding: 4px 10px;
      border-radius: 6px;
      display: inline-block;
      margin-top: auto;
    }}

    /* ───────── FAQ АККОРДЕОН ───────── */
    .faq-section {{
      padding: 70px 24px;
      max-width: 900px;
      margin: 0 auto;
    }}

    .faq-item {{
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 16px;
      margin-bottom: 12px;
      overflow: hidden;
      transition: var(--transition);
    }}

    .faq-item.active {{
      border-color: var(--accent-gold);
    }}

    .faq-question {{
      padding: 18px 22px;
      font-weight: 600;
      font-size: 15px;
      color: #111;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      user-select: none;
    }}

    .faq-icon {{
      transition: transform 0.3s ease;
      font-size: 18px;
      color: var(--accent-gold);
    }}

    .faq-item.active .faq-icon {{
      transform: rotate(45deg);
    }}

    .faq-answer {{
      padding: 0 22px 18px;
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.7;
      display: none;
    }}

    .faq-item.active .faq-answer {{
      display: block;
    }}

    /* Footer */
    footer {{
      background: #111827;
      color: #9ca3af;
      padding: 60px 24px 30px;
    }}

    .footer-inner {{
      max-width: 1300px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1.5fr 1fr 1fr 1.2fr;
      gap: 40px;
      margin-bottom: 50px;
    }}

    .footer-brand h3 {{
      font-family: var(--font-serif);
      font-size: 26px;
      color: #fff;
      letter-spacing: 2px;
      margin-bottom: 12px;
    }}

    .footer-brand p {{
      font-size: 13px;
      line-height: 1.7;
    }}

    .footer-col h4 {{
      color: #fff;
      font-size: 15px;
      margin-bottom: 16px;
    }}

    .footer-links {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .footer-links a {{
      color: #9ca3af;
      text-decoration: none;
      font-size: 13px;
      transition: var(--transition);
    }}

    .footer-links a:hover {{
      color: #fff;
    }}

    .footer-bottom {{
      max-width: 1300px;
      margin: 0 auto;
      padding-top: 24px;
      border-top: 1px solid #1f2937;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      flex-wrap: wrap;
      gap: 12px;
    }}

    /* Fullscreen Photo Lightbox Modal */
    .lightbox-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.88);
      backdrop-filter: blur(12px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .lightbox-overlay.active {{
      display: flex;
    }}

    .lightbox-content {{
      position: relative;
      max-width: 580px;
      width: 100%;
      background: #111827;
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 25px 60px rgba(0,0,0,0.5);
      border: 1px solid rgba(255,255,255,0.1);
      animation: modalPop 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .lightbox-close {{
      position: absolute;
      top: 16px;
      right: 16px;
      background: rgba(0, 0, 0, 0.6);
      color: #fff;
      border: none;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10;
      transition: var(--transition);
    }}

    .lightbox-close:hover {{
      background: var(--accent-red);
    }}

    .lightbox-img-wrap {{
      width: 100%;
      height: 480px;
      background: #000;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .lightbox-img-wrap img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}

    .lightbox-footer {{
      padding: 20px 24px;
      background: #1f2937;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    /* Quick Order Modal */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(8px);
      z-index: 999;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal-overlay.active {{
      display: flex;
    }}

    .modal-card {{
      background: #fff;
      border-radius: 24px;
      max-width: 500px;
      width: 100%;
      padding: 30px;
      box-shadow: var(--shadow-lg);
      position: relative;
      animation: modalPop 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    @keyframes modalPop {{
      0% {{ transform: scale(0.92); opacity: 0; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}

    .modal-close {{
      position: absolute;
      top: 20px;
      right: 20px;
      background: #f3f4f6;
      border: none;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    /* Floating WhatsApp Action Pill for Mobile */
    .mobile-float-bar {{
      display: none;
      position: fixed;
      bottom: 16px;
      left: 16px;
      right: 16px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      border-radius: 40px;
      padding: 8px 12px 8px 18px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.15);
      z-index: 90;
      align-items: center;
      justify-content: space-between;
    }}

    @media (max-width: 900px) {{
      .hero {{
        grid-template-columns: 1fr;
        padding-top: 30px;
      }}
      .hero-title {{
        font-size: 38px;
      }}
      .craft-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
      .promo-banner-section {{
        grid-template-columns: 1fr;
        padding: 24px;
      }}
      .showcase-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
      .engrave-container {{
        grid-template-columns: 1fr;
        padding: 24px;
      }}
      .lightbox-img-wrap {{
        height: 360px;
      }}
      .footer-inner {{
        grid-template-columns: 1fr;
        gap: 28px;
      }}
      .mobile-float-bar {{
        display: flex;
      }}
      body {{
        padding-bottom: 70px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Owner Presentation Drawer -->
  <div class="pitch-banner">
    <div style="display: flex; align-items: center; gap: 10px;">
      <span class="pitch-badge">КЛИЕНТКЕ ДЕМО</span>
      <span>Бұл сайт UAQYT дүкені үшін арнайы әзірленді (Apple деңгейіндегі ашық дизайн, 1+1 акция, 33 үлгі).</span>
    </div>
    <button class="pitch-btn" onclick="togglePitch()">Толығырақ көру ▾</button>
  </div>

  <div class="pitch-drawer" id="pitchDrawer">
    <div class="pitch-grid">
      <div class="pitch-card">
        <h4>1. Премиум ашық дизайн</h4>
        <p>Қара фоннан ақ, таза «Apple-style» минимализмге көштік. Сағаттардың алтын және болат жылтыры анық көрінеді.</p>
      </div>
      <div class="pitch-card">
        <h4>2. Бағасы: арзаннан қымбатқа</h4>
        <p>Клиенттің аудио-тапсырмасы бойынша барлық модельдер 26 900 ₸ бастап 75 900 ₸ дейін өсу ретімен қойылды.</p>
      </div>
      <div class="pitch-card">
        <h4>3. 1+1 Акциясы және Сыйлық бонустар</h4>
        <p>1 сағат алғанда 2-шісі тегін берілетін бонустық топтама қосылды («при покупке эти в бонус на выбор»).</p>
      </div>
      <div class="pitch-card">
        <h4>4. 2GIS тікелей маршрут</h4>
        <p>Өтеген батыр 11а мекенжайына басқанда клиент бірден 2GIS қосымшасына өтіп, маршрут құра алады.</p>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header>
    <div class="header-inner">
      <a href="#" class="brand-logo">
        <div class="logo-mark">U</div>
        <span class="brand-name">UAQYT</span>
      </a>

      <ul class="nav-links">
        <li><a href="#promo1plus1" class="nav-link">1+1 Акция <span class="nav-tag">Тегін бонус</span></a></li>
        <li><a href="#catalog" class="nav-link">Каталог (33)</a></li>
        <li><a href="#showcase" class="nav-link">Дайын жұмыстар</a></li>
        <li><a href="#constructor" class="nav-link">Конструктор</a></li>
        <li><a href="#faq" class="nav-link">Сұрақ-жауап</a></li>
        <li><a href="#contacts" class="nav-link">Шоурум & 2GIS</a></li>
      </ul>

      <div class="header-actions">
        <a href="https://wa.me/77071340000?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%81%D1%96%D0%B7%20%D0%B1%D0%B5!%20UAQYT%20%D1%81%D0%B0%D2%93%D0%B0%D1%82%D1%82%D0%B0%D1%80%D1%8B%20%D0%B1%D0%BE%D0%B9%D1%8B%D0%BD%D1%88%D0%B0%20%D0%BA%D0%B5%D1%9Block%20%D0%B0%D0%BB%D2%93%D1%8B%D0%BC%20%D0%BA%D0%B5%D0%BB%D0%B5%D0%B4%D1%96" target="_blank" rel="noopener" class="btn-wa-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.076-2.008-.475-1.637-.687-2.701-2.348-2.784-2.459-.082-.111-.664-.883-.664-1.684 0-.8.419-1.196.568-1.356.149-.16.326-.2.435-.2.11 0 .22.002.316.007.102.006.239-.039.373.284.144.35.492 1.2.535 1.288.043.088.072.191.014.306-.058.115-.088.187-.174.288-.087.101-.184.226-.263.303-.088.087-.18.182-.077.359.102.176.455.751.977 1.216.671.597 1.236.782 1.412.87.176.087.279.073.383-.046.104-.12.446-.519.566-.697.12-.178.239-.148.404-.087.165.061 1.044.492 1.224.582.18.09.3.134.344.209.044.075.044.436-.1.841z"/></svg>
          WhatsApp-қа жазу
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div>
      <div class="hero-badge">
        <span class="hero-badge-dot"></span>
        <span>ЖЕКЕ ЛАЗЕРЛІК ГРАВИРОВКА • АЛМАТЫ & ҚАЗАҚСТАН</span>
      </div>

      <h1 class="hero-title">
        Өз есіміңіз бен ру таңбаңыз жазылған <span>мәртебелі сағаттар</span>
      </h1>

      <p class="hero-desc">
        Әрбір сағат — қайталанбас дара туынды. Ерлерге, жұптарға және құқық қорғау органдары мен мемлекеттік қызметкерлерге арналған ресми эмблемалы қол сағаттар.
      </p>

      <div class="hero-pills-row">
        <div class="hero-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>6–12 ай ресми кепілдік</span>
        </div>
        <div class="hero-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
          <span>Қазпошта & Автобус тегін</span>
        </div>
        <div class="hero-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4"/><path d="M4 6v12c0 1.1.9 2 2 2h14v-4"/><circle cx="18" cy="12" r="2"/></svg>
          <span>Kaspi Red & Halyk 0-0-12</span>
        </div>
        <div class="hero-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <span>15 минутта жеке эскиз</span>
        </div>
      </div>

      <div class="hero-cta-group">
        <a href="#catalog" class="btn-gold">Каталогты көру (26 900 ₸ бастап) ➔</a>
        <a href="#constructor" class="btn-outline">Өз дизайныңызды жасау</a>
      </div>
    </div>

    <!-- Hero Showcase Card: Real Showcase Photo with Branded Bag -->
    <div class="hero-visual-card" onclick="openLightbox('./images/showcase/showcase-baglan-aday-gold.jpg', '«Бағлан / Адай» Алтын сағат', '39 900')">
      <img src="./images/showcase/showcase-baglan-aday-gold.jpg" alt="UAQYT Бағлан Адай алтын сағат" class="hero-visual-img">
      <div class="hero-visual-footer">
        <div>
          <strong style="font-size: 15px; color: #111;">«Бағлан / Адай» Алтын сағат 🔍</strong>
          <p style="font-size: 12px; color: var(--text-muted);">UAQYT фирмалық қабы + Сыйлық қорабы (Үлкейту үшін басыңыз)</p>
        </div>
        <span style="font-family: var(--font-sans); font-weight: 800; font-size: 18px; color: var(--accent-gold);">39 900 ₸</span>
      </div>
    </div>
  </section>

  <!-- ───────── ШЕБЕРЛІК ПЕН САПА КЕПІЛІ (CRAFTSMANSHIP) ───────── -->
  <section class="section-wrap" style="padding-top: 0; padding-bottom: 40px;">
    <div class="craft-grid">
      <div class="craft-card">
        <div class="craft-icon">🛡️</div>
        <h4>316L Медициналық болат</h4>
        <p>Коррозияға төзімді, уақыт өте түсі кетпейтін, теріге гипоаллергенді премиум металл.</p>
      </div>

      <div class="craft-card">
        <div class="craft-icon">💎</div>
        <h4>Сапфирлік шыны</h4>
        <p>Алмаздан кейінгі ең қатты минерал — кілттен, металдан және тастан мүлдем сызат түспейді.</p>
      </div>

      <div class="craft-card">
        <div class="craft-icon">⚡</div>
        <h4>Лазерлік нақыштау</h4>
        <p>Микрондық дәлдікпен қашалатын өшпес жазу. Кез келген қазақи ою, ру таңбасы мен елтаңба.</p>
      </div>

      <div class="craft-card">
        <div class="craft-icon">🎁</div>
        <h4>Премиум қаптама</h4>
        <p>Әрбір тапсырыс сәнді барқыт төсенішті қорапқа және брендтік UAQYT ақ қабына салынады.</p>
      </div>
    </div>
  </section>

  <!-- ───────── 1+1 СУПЕР АКЦИЯСЫ: ЕКІНШІ САҒАТ БОНУСКЕ ТЕГІН ───────── -->
  <section class="section-wrap" id="promo1plus1" style="padding-top: 10px;">
    <div class="promo-banner-section">
      <div>
        <span class="promo-badge">🔥 Қараша айының эксклюзивті ұсынысы</span>
        <h2 class="promo-title">1 сағат алсаңыз — <span>2-ші сағат БОНУСҚА ТЕГІН</span></h2>
        <p style="color: #4b5563; font-size: 15px; line-height: 1.6; margin-bottom: 20px;">
          Каталогтан кез келген ерлер немесе қызметтік сағатқа тапсырыс беріңіз, ал <strong>екінші сағатты мына бонустық топтаманың арасынан мүлдем ТЕГІН (0 ₸)</strong> таңдап алыңыз!
        </p>

        <ul class="promo-list">
          <li>
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <span><strong>2 сағатқа да</strong> жеке есім мен ру таңбасы нақышталады</span>
          </li>
          <li>
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <span><strong>2 сыйлықтық қорап</strong> + UAQYT брендтік ақ қапшығы</span>
          </li>
          <li>
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <span>Қазақстанның кез келген қаласына <strong>ТЕГІН жеткізу</strong></span>
          </li>
        </ul>

        <div style="background: rgba(255,255,255,0.7); border: 1px dashed var(--accent-gold); border-radius: 14px; padding: 14px 18px; margin-bottom: 22px;">
          <div style="font-size: 12px; font-weight: 700; color: var(--accent-gold-dark); margin-bottom: 4px;">СЫЙЛЫҚ БОНУСЫН ТАҢДАУ:</div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="pitch-btn" style="background: #111; color: #fff; border-color: #111;" onclick="selectBonus('Бонус №1: Классикалық болат бау')">✓ Бонус №1: Классикалық болат</button>
            <button class="pitch-btn" onclick="selectBonus('Бонус №2: Былғары баулы стиль')">Бонус №2: Былғары бау</button>
            <button class="pitch-btn" onclick="selectBonus('Бонус №3: Қара PVD сағат')">Бонус №3: Қара сағат</button>
          </div>
        </div>

        <button class="btn-gold" onclick="orderPromo1Plus1()">
          1+1 Акциямен WhatsApp-қа жазу ➔
        </button>
      </div>

      <div class="promo-bonus-visual" onclick="openLightbox('./images/bonus/bonus-watch-1.jpg', 'Бонустық сағаттар топтамасы (Тегін)', '0 ₸ Сыйлық')">
        <span class="bonus-tag-pill">0 ₸ СЫЙЛЫҚҚА</span>
        <img src="./images/bonus/bonus-watch-1.jpg" alt="Бонусқа тегін сағаттар UAQYT">
        <div style="font-size: 13px; font-weight: 600; color: #111;">Бонустық сағаттардың ресми топтамасы 🔍</div>
        <p style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Кез келген негізгі сағатты алғанда осылардың ішінен 1 сағат сыйлыққа тегін қосылады (Үлкейту үшін басыңыз).</p>
      </div>
    </div>

    <!-- ───────── ШЫНАЙЫ ДАЙЫН ЖҰМЫСТАР ГАЛЕРЕЯСЫ (SHOWCASE) ───────── -->
    <div class="showcase-slider-wrap" id="showcase">
      <div class="section-head" style="margin-bottom: 28px;">
        <span class="section-kicker">Шынайы дайын тапсырыстар</span>
        <h3 style="font-family: var(--font-serif); font-size: 32px; color: #111;">Біздің шеберханадан шыққан жұмыстар</h3>
        <p class="section-sub">Брендтік UAQYT ақ қабы мен сыйлық қорабындағы нақты клиенттердің сағаттары (Фотоны үлкейтіп көру үшін басыңыз).</p>
      </div>

      <div class="showcase-grid">
        <div class="showcase-item" onclick="openLightbox('./images/showcase/showcase-baglan-aday-gold.jpg', '«Бағлан / Адай» Алтын сағат', '39 900')">
          <img src="./images/showcase/showcase-baglan-aday-gold.jpg" alt="Бағлан Адай">
          <div class="showcase-caption">
            <h5>«Бағлан / Адай» 🔍</h5>
            <p>Алтын сегізқырлы • 39 900 ₸</p>
          </div>
        </div>

        <div class="showcase-item" onclick="openLightbox('./images/showcase/showcase-temir-zhanbolat-service.jpg', '«Темір Жанболат» Офицерлік болат', '39 900')">
          <img src="./images/showcase/showcase-temir-zhanbolat-service.jpg" alt="Темір Жанболат">
          <div class="showcase-caption">
            <h5>«Темір Жанболат» 🔍</h5>
            <p>Офицерлік болат • 39 900 ₸</p>
          </div>
        </div>

        <div class="showcase-item" onclick="openLightbox('./images/showcase/showcase-rahat-ardana-woodbox.jpg', '«Рахат Шекті / Ардана 13.11.1979» Люкс ағаш қорап', '75 900')">
          <img src="./images/showcase/showcase-rahat-ardana-woodbox.jpg" alt="Рахат Шекті Ағаш қорапта">
          <div class="showcase-caption">
            <h5>«Рахат Шекті / Ардана» 🔍</h5>
            <p>Люкс ағаш қорап • 75 900 ₸</p>
          </div>
        </div>

        <div class="showcase-item" onclick="openLightbox('./images/showcase/showcase-arman-shapyrashty-twotone.jpg', '«Арман / Шапырашты» Two-Tone', '39 900')">
          <img src="./images/showcase/showcase-arman-shapyrashty-twotone.jpg" alt="Арман Шапырашты Two-Tone">
          <div class="showcase-caption">
            <h5>«Арман / Шапырашты» 🔍</h5>
            <p>Two-Tone Комби • 39 900 ₸</p>
          </div>
        </div>

        <div class="showcase-item" onclick="openLightbox('./images/showcase/showcase-zhangeldi-erketay-black.jpg', '«Жангелді ❤️ Еркетай» Жұптық Stealth', '42 900')">
          <img src="./images/showcase/showcase-zhangeldi-erketay-black.jpg" alt="Жангелді Еркетай Black">
          <div class="showcase-caption">
            <h5>«Жангелді ❤️ Еркетай» 🔍</h5>
            <p>Жұптық Stealth • 42 900 ₸</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ───────── КАТАЛОГ БӨЛІМІ ───────── -->
  <section class="catalog-section" id="catalog">
    <div class="section-head">
      <span class="section-kicker">Ресми топтама</span>
      <h2 class="section-title">Барлық сағаттар каталогы</h2>
      <p class="section-sub">Бағалар 26 900 ₸ бастап 75 900 ₸ дейін өсу ретімен қойылған. Фотоны үлкейтіп көру үшін суретке басыңыз.</p>
    </div>

    <!-- Sticky Catalog Filter Bar (Плашка) -->
    <div class="catalog-bar-sticky">
      <div class="catalog-bar-inner">
        <div class="catalog-bar-top">
          <div class="search-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            <input type="text" class="search-input" id="catalogSearch" placeholder="Сағатты, руды немесе қызметті іздеу..." oninput="handleSearch()">
          </div>

          <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 13px; color: var(--text-muted); font-weight: 600;" id="catalogCounter">{total_count} модель табылды</span>
            <select class="sort-select" id="catalogSort" onchange="handleSort()">
              <option value="asc" selected>Бағасы: арзаннан қымбатқа (26.900 ₸ ➔)</option>
              <option value="desc">Бағасы: қымбаттан арзанға</option>
              <option value="popular">Танымал үлгілер</option>
            </select>
          </div>
        </div>

        <!-- Category Pills (Плашка санаттары) -->
        <div class="category-chips">
          <button class="chip-btn active" onclick="filterCategory('all', this)">Барлық топтама ({total_count})</button>
          <button class="chip-btn" onclick="filterCategory('promo', this)">🎁 1+1 Акция (Сыйлықпен)</button>
          <button class="chip-btn" onclick="filterCategory('couples', this)">❤️ Жұптық сағаттар (1+1 Раушан)</button>
          <button class="chip-btn" onclick="filterCategory('service', this)">🛡️ Қызметтік / Органдарға (ІІМ, ҰҚК, ТЖМ)</button>
          <button class="chip-btn" onclick="filterCategory('mens', this)">Ерлер сағаты</button>
          <button class="chip-btn" onclick="filterCategory('mechanic', this)">⚙️ Механикалық сағаттар</button>
          <button class="chip-btn" onclick="filterCategory('woodbox', this)">🪵 Ағаш қораптағы люкс</button>
          <button class="chip-btn" onclick="filterCategory('ornament', this)">❖ Ұлттық ою / Шежіре-Ру</button>
        </div>
      </div>
    </div>

    <!-- Product Grid -->
    <div class="section-wrap" style="padding-top: 0;">
      <div class="product-grid" id="productGrid">
{all_cards_str}
      </div>

      <!-- Departmental Special Banner -->
      <div style="margin-top: 46px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 24px; padding: 40px; color: #fff; display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 30px; align-items: center; box-shadow: var(--shadow-md);">
        <div>
          <div style="display: inline-block; background: rgba(220,180,80,0.2); border: 1px solid var(--accent-gold); color: #f7e7b4; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 12px;">
            ✦ Мемлекеттік қызметкерлер мен құқық қорғау органдарына
          </div>
          <h3 style="font-family: var(--font-serif); font-size: 32px; line-height: 1.2; margin-bottom: 12px; color: #fff;">
            ІІМ, ҰҚК, ТЖМ, Прокуратура және ҚР ҚК сағаттары
          </h3>
          <p style="color: #94a3b8; font-size: 14px; line-height: 1.6; margin-bottom: 20px;">
            Жаңа шен (звание) алуға, мерейтойға, зейнетке шығуға немесе кәсіби мерекелерге арналған құрметті сағаттар. Ведомство эмблемасын, қызметкердің тегі мен жеке нөмірін сағат циферблатына түсіріп береміз.
          </p>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.08); padding: 4px 12px; border-radius: 8px; font-size: 12px;">ІІМ (МВД)</span>
            <span style="background: rgba(255,255,255,0.08); padding: 4px 12px; border-radius: 8px; font-size: 12px;">ҰҚК (КНБ)</span>
            <span style="background: rgba(255,255,255,0.08); padding: 4px 12px; border-radius: 8px; font-size: 12px;">ТЖМ (МЧС)</span>
            <span style="background: rgba(255,255,255,0.08); padding: 4px 12px; border-radius: 8px; font-size: 12px;">Қорғаныс министрлігі</span>
            <span style="background: rgba(255,255,255,0.08); padding: 4px 12px; border-radius: 8px; font-size: 12px;">Прокуратура & Антикор</span>
          </div>
        </div>
        <div style="text-align: center; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 26px;">
          <div style="font-size: 36px; margin-bottom: 8px;">🎖️</div>
          <h4 style="font-size: 17px; margin-bottom: 6px;">Корпоративтік & Жеке тапсырыс</h4>
          <p style="font-size: 12px; color: #94a3b8; margin-bottom: 18px;">
            1 данадан бастап ұжымдық партияға дейін жасаймыз. WhatsApp арқылы эскизін 15 минутта дайындаймыз.
          </p>
          <a href="https://wa.me/77071340000?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%81%D1%96%D0%B7%20%D0%B1%D0%B5!%20%D2%9A%D1%8B%D0%B7%D0%BC%D0%B5%D1%82%D1%82%D1%96%D0%BA%20%D0%B2%D0%B5%D0%B4%D0%BE%D0%BC%D1%81%D1%82%D0%B2%D0%BE%D0%BB%D1%8B%D2%9B%20%D1%81%D0%B0%D2%93%D0%B0%D1%82%D2%9B%D0%B0%20%D1%82%D0%B0%D0%BF%D1%81%D1%8B%D1%80%D1%8B%D1%81%20%D0%B1%D0%B5%D1%80%D0%B3%D1%96%D0%BC%20%D0%BA%D0%B5%D0%BB%D0%B5%D0%B4%D1%96" target="_blank" rel="noopener" class="btn-gold" style="width: 100%; justify-content: center;">
            Ведомстволық сағатқа тапсырыс беру ➔
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- ───────── ИНТЕРАКТИВНЫЙ КОНСТРУКТОР ГРАВИРОВКИ (С ЖИВЫМИ СТРЕЛКАМИ) ───────── -->
  <section class="engrave-section" id="constructor">
    <div class="section-head">
      <span class="section-kicker">Интерактивті конструктор</span>
      <h2 class="section-title">Өз сағатыңыздың дизайнын жасаңыз</h2>
      <p class="section-sub">Төменге өз есіміңіз бен руыңызды таңдаңыз — сағат циферблатында қалай көрінетінін дәл қазір көріңіз.</p>
    </div>

    <div class="engrave-container">
      <div class="engrave-stage" id="engraveStage">
        <div class="watch-dial-frame" id="watchDialFrame">
          <div class="watch-dial-inner">
            <div class="dial-mark-12">XII</div>
            <div class="dial-mark-3">III</div>
            <div class="dial-mark-6">VI</div>
            <div class="dial-mark-9">IX</div>

            <div class="dial-center-pin"></div>
            <div class="dial-hand-hour" id="dialHourHand"></div>
            <div class="dial-hand-min" id="dialMinHand"></div>
            <div class="dial-hand-sec"></div>

            <div class="dial-text-top" id="dialNameDisplay">БАҒЛАН</div>
            
            <div style="text-align: center; z-index: 2;">
              <div class="dial-ornament" id="dialOrnamentDisplay">❖ ❖ ❖</div>
              <div class="dial-text-bottom" id="dialSubDisplay">АДАЙ</div>
              <div class="dial-sub-date" id="dialDateDisplay">UAQYT ATELIER</div>
            </div>
          </div>
        </div>
      </div>

      <div class="engrave-form">
        <div class="form-group">
          <label class="form-label">Қазақ руларын таңдау (Шежіре сүзгісі):</label>
          <select class="form-select" id="tribeSelector" onchange="handleTribeSelect(this.value)">
            <option value="">-- Руыңызды таңдаңыз (автоматты түрде қойылады) --</option>
            <optgroup label="Кіші жүз">
              <option value="Адай|❖ ❖ ❖">Адай</option>
              <option value="Беріш|★ ★ ★">Беріш</option>
              <option value="Шекті|⚔ ⚔ ⚔">Шекті (Әлімұлы)</option>
              <option value="Тана|❖ ❖ ❖">Тана</option>
              <option value="Төртқара|◆ ◆ ◆">Төртқара</option>
              <option value="Шәркеш|❖ ❖ ❖">Шәркеш</option>
              <option value="Алшын|❖ ❖ ❖">Алшын</option>
            </optgroup>
            <optgroup label="Орта жүз">
              <option value="Арғын|◎ ◎ ◎">Арғын (Көз таңба)</option>
              <option value="Найман|Ү Ү Ү">Найман (Бақан таңба)</option>
              <option value="Қыпшақ|I I I">Қыпшақ (Қос алып)</option>
              <option value="Қоңырат|П П П">Қоңырат (Босаға)</option>
              <option value="Керей|✚ ✚ ✚">Керей (Ашамай)</option>
              <option value="Уақ|❖ ❖ ❖">Уақ</option>
            </optgroup>
            <optgroup label="Ұлы жүз">
              <option value="Шапырашты|☾ ☾ ☾">Шапырашты (Ай таңба)</option>
              <option value="Дулат|◯ ◯ ◯">Дулат</option>
              <option value="Албан|🔔 🔔 🔔">Албан (Қоңырау)</option>
              <option value="Ысты|❖ ❖ ❖">Ысты</option>
              <option value="Суан|❖ ❖ ❖">Суан</option>
            </optgroup>
            <optgroup label="Ақсүйек & Басқа">
              <option value="Төре|👑 👑 👑">Төре (Шыңғысхан ұрпағы)</option>
              <option value="Қожа|☪ ☪ ☪">Қожа</option>
              <option value="Төлеңгіт|🛡️ 🛡️ 🛡️">Төлеңгіт</option>
            </optgroup>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Дайын тақырыптық үлгіні таңдау:</label>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button type="button" class="case-color-btn active" style="flex: initial; padding: 6px 14px;" onclick="applyEngravePreset('Бағлан', 'Адай', '❖ ❖ ❖', 'UAQYT ATELIER')">❖ Ру / Есім</button>
            <button type="button" class="case-color-btn" style="flex: initial; padding: 6px 14px;" onclick="applyEngravePreset('ҚАЗАҚСТАН', 'ПОЛИЦИЯ', '🛡️ ІІМ', 'МАЙОР АХМЕТОВ')">👮 ІІМ (МВД)</button>
            <button type="button" class="case-color-btn" style="flex: initial; padding: 6px 14px;" onclick="applyEngravePreset('ҰҚК / КНБ', 'ҚАУІПСІЗДІК', '⚔️ ҚАЛҚАН', 'ҚР ОФИЦЕРІ')">🛡️ ҰҚК (КНБ)</button>
            <button type="button" class="case-color-btn" style="flex: initial; padding: 6px 14px;" onclick="applyEngravePreset('ҚҰТҚАРУШЫ', 'ТЖМ / МЧС', '🚒 112 ҚЫЗМЕТІ', 'ҚАЗАҚСТАН')">🚒 ТЖМ (МЧС)</button>
            <button type="button" class="case-color-btn" style="flex: initial; padding: 6px 14px;" onclick="applyEngravePreset('ҚАРУЛЫ КҮШТЕР', 'ҚОРҒАНЫС', '🎖️ ОФИЦЕР', 'ҚР ӘСКЕРІ')">🎖️ ҚР ҚК (Әскер)</button>
            <button type="button" class="case-color-btn" style="flex: initial; padding: 6px 14px;" onclick="applyEngravePreset('ЖАНГЕЛДІ', 'ЕРКЕТАЙ', '❤️ МӘҢГІЛІК', '13.11.2024')">❤️ Жұптық</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">1. Сағатқа жазылатын есім немесе орган (Имя/Ведомство):</label>
          <input type="text" class="form-input" id="inputName" value="Бағлан" placeholder="Мысалы: Бағлан, ІІМ, ҰҚК, Қазақстан" oninput="updateDialPreview()">
        </div>

        <div class="form-group">
          <label class="form-label">2. Руыңыз, шеніңіз немесе жұптың есімі (Ру / Звание / Жұп):</label>
          <input type="text" class="form-input" id="inputSub" value="Адай" placeholder="Мысалы: Адай, Полиция, Майор немесе Еркетай ❤️" oninput="updateDialPreview()">
        </div>

        <div class="form-group">
          <label class="form-label">3. Қосымша мәтін, жетон нөмірі немесе күн (Дата / Жетон / Қызмет):</label>
          <input type="text" class="form-input" id="inputDate" value="UAQYT KZT" placeholder="Мысалы: №04812, 13.11.1979 немесе UAQYT KZT" oninput="updateDialPreview()">
        </div>

        <div class="form-group">
          <label class="form-label">4. Корпус түсі:</label>
          <div class="color-case-select">
            <div class="case-color-btn active" onclick="setCaseColor('gold', this)">Алтын (Gold)</div>
            <div class="case-color-btn" onclick="setCaseColor('silver', this)">Күміс (Silver)</div>
            <div class="case-color-btn" onclick="setCaseColor('twotone', this)">Комби (Two-Tone)</div>
            <div class="case-color-btn" onclick="setCaseColor('black', this)">Қара (Black)</div>
          </div>
        </div>

        <button class="btn-gold" style="justify-content: center; width: 100%; margin-top: 10px;" onclick="orderCustomWatch()">
          Осы дизайнмен WhatsApp-қа тапсырыс беру ➔
        </button>
      </div>
    </div>
  </section>

  <!-- ───────── ШЫНАЙЫ ФОТО-ПІКІРЛЕР МЕН ЖЕТКІЗІЛІМДЕР ───────── -->
  <section class="reviews-section" id="reviews">
    <div class="section-head" style="margin-bottom: 24px;">
      <span class="section-kicker">Сатып алушылардың шынайы пікірлері</span>
      <h2 class="section-title">Қазақстан бойынша 1 200+ риза клиент</h2>
      <p class="section-sub">Нақты WhatsApp скриншоттары мен жеткізілген сағаттардың шынайы фото-есептері (Үлкейту үшін кез келген фотоға басыңыз).</p>
    </div>

    <!-- Stats Bar -->
    <div style="max-width: 1000px; margin: 0 auto 40px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; text-align: center;">
      <div style="background: var(--bg-alt); border: 1px solid var(--border); padding: 14px; border-radius: 16px;">
        <div style="font-size: 22px; font-weight: 800; color: #111;">4.9 ★★★★★</div>
        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600;">Орташа бағалау</div>
      </div>
      <div style="background: var(--bg-alt); border: 1px solid var(--border); padding: 14px; border-radius: 16px;">
        <div style="font-size: 22px; font-weight: 800; color: #111;">1 200+</div>
        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600;">Жеткізілген сағат</div>
      </div>
      <div style="background: var(--bg-alt); border: 1px solid var(--border); padding: 14px; border-radius: 16px;">
        <div style="font-size: 22px; font-weight: 800; color: #111;">15 минут</div>
        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600;">Тегін эскиз уақыты</div>
      </div>
      <div style="background: var(--bg-alt); border: 1px solid var(--border); padding: 14px; border-radius: 16px;">
        <div style="font-size: 22px; font-weight: 800; color: var(--accent-green);">100%</div>
        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600;">Өшпейтін лазер кепілі</div>
      </div>
    </div>

    <!-- 6 Rich Photo Review Cards -->
    <div class="reviews-grid">
      <!-- Review 1: Real WhatsApp Screenshot: Matluba -->
      <div class="review-card" style="border: 1.5px solid var(--accent-gold);">
        <div class="review-header">
          <div class="reviewer-info">
            <h4 style="display:flex; align-items:center; gap:6px;">Матлуба (Алматы) <span style="font-size:10px; background:#dcfce7; color:#166534; padding:2px 8px; border-radius:10px;">Расталған сатып алушы</span></h4>
            <div class="reviewer-meta">WhatsApp арқылы жеткізілді • Бүгін</div>
          </div>
          <span class="source-tag" style="background:#25D366; color:#fff;">WhatsApp</span>
        </div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text" style="font-style:italic; font-weight:500;">
          «Сәлеметсізбе! Алдым заказымды, рахмет! Көп-көп клиенттеріңіз көп болсын! 🥰 Жұптық сағат өте әдемі шығыпты: «Шынар / Кіші жүз» және «Әділбек / Кіші жүз». Яндекс доставкамен тез жеткізді!»
        </p>
        <div style="margin: 10px 0; border-radius: 14px; overflow: hidden; height: 220px; border: 1px solid var(--border); cursor: pointer;" onclick="openLightbox('./images/reviews/review-matluba.jpg', 'Матлуба ханымның WhatsApp пікірі', 'Шынайы отзыв')">
          <img src="./images/reviews/review-matluba.jpg" alt="WhatsApp отзыв Матлуба" style="width: 100%; height: 100%; object-fit: cover; object-position: center bottom;">
        </div>
        <div class="review-product-tag">Тапсырыс: 1+1 Жұптық сағат (Кіші жүз) 🔍</div>
      </div>

      <!-- Review 2: Baglan (Gold Aday) -->
      <div class="review-card">
        <div class="review-header">
          <div class="reviewer-info">
            <h4 style="display:flex; align-items:center; gap:6px;">Бағлан Нұрболұлы (Ақтау) <span style="font-size:10px; background:#dcfce7; color:#166534; padding:2px 8px; border-radius:10px;">1+1 Акция</span></h4>
            <div class="reviewer-meta">Қазпоштамен жеткізілді • Кеше</div>
          </div>
          <span class="source-tag" style="background:#b88e4f; color:#fff;">Алтын сағат</span>
        </div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">
          «Адай руының таңбасымен алтын сегізқырлы сағат алдым. 1+1 акциясымен ініме екінші сағатты тегін сыйлыққа таңдадым. Қорабы мен UAQYT фирмалық ақ қабы өте мәртебелі көрінеді!»
        </p>
        <div style="margin: 10px 0; border-radius: 14px; overflow: hidden; height: 220px; border: 1px solid var(--border); cursor: pointer;" onclick="openLightbox('./images/showcase/showcase-baglan-aday-gold.jpg', '«Бағлан / Адай» Алтын сағат', '39 900 ₸')">
          <img src="./images/showcase/showcase-baglan-aday-gold.jpg" alt="Бағлан Адай алтын сағат" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div class="review-product-tag">Тапсырыс: «Бағлан / Адай» Алтын үлгі 🔍</div>
      </div>

      <!-- Review 3: Daulet (Police Officer) -->
      <div class="review-card">
        <div class="review-header">
          <div class="reviewer-info">
            <h4 style="display:flex; align-items:center; gap:6px;">Дәулет капитан (Астана) <span style="font-size:10px; background:#dbeafe; color:#1e40af; padding:2px 8px; border-radius:10px;">ІІМ Қызметкері</span></h4>
            <div class="reviewer-meta">Арнайы ведомстволық • 2 күн бұрын</div>
          </div>
          <span class="source-tag" style="background:#1e3a8a; color:#fff;">ІІМ Тапсырыс</span>
        </div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">
          «Жаңа шен (звание) алуға офицерлік сағат алдық. Қыран мен күн гербі, қызметкердің аты-жөні дәл қашалған. Сапасы мықты, болат бауы салқындап қолға жақсы отырады.»
        </p>
        <div style="margin: 10px 0; border-radius: 14px; overflow: hidden; height: 220px; border: 1px solid var(--border); cursor: pointer;" onclick="openLightbox('./images/showcase/showcase-temir-zhanbolat-service.jpg', '«Темір Жанболат» Офицерлік болат', '39 900 ₸')">
          <img src="./images/showcase/showcase-temir-zhanbolat-service.jpg" alt="Темір Жанболат офицерлік" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div class="review-product-tag">Тапсырыс: Офицерлік болат «Темір Жанболат» 🔍</div>
      </div>

      <!-- Review 4: Rahat & Ardana (Luxury Woodbox) -->
      <div class="review-card">
        <div class="review-header">
          <div class="reviewer-info">
            <h4 style="display:flex; align-items:center; gap:6px;">Ардана (Шымкент) <span style="font-size:10px; background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:10px;">Мерейтой</span></h4>
            <div class="reviewer-meta">Ағаш шкатулка • 3 күн бұрын</div>
          </div>
          <span class="source-tag" style="background:#854d0e; color:#fff;">Люкс Ағаш</span>
        </div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">
          «Жолдасыма мерейтойына ағаш шкатулкадағы сапфир механика сағат алдым. Табиғи лакталған вишня ағашының жылтыры керемет! Жазуы да, күн мен қыран да өте сапалы шықты.»
        </p>
        <div style="margin: 10px 0; border-radius: 14px; overflow: hidden; height: 220px; border: 1px solid var(--border); cursor: pointer;" onclick="openLightbox('./images/showcase/showcase-rahat-ardana-woodbox.jpg', '«Рахат Шекті / Ардана 13.11.1979» Люкс ағаш қорап', '75 900 ₸')">
          <img src="./images/showcase/showcase-rahat-ardana-woodbox.jpg" alt="Рахат Шекті ағаш қорап" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div class="review-product-tag">Тапсырыс: Люкс ағаш қорап (Сапфир механика) 🔍</div>
      </div>

      <!-- Review 5: Zhangeldi & Erketay (Couple Stealth) -->
      <div class="review-card">
        <div class="review-header">
          <div class="reviewer-info">
            <h4 style="display:flex; align-items:center; gap:6px;">Еркетай (Қарағанды) <span style="font-size:10px; background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:10px;">Жұптық сағат</span></h4>
            <div class="reviewer-meta">Instagram арқылы • 4 күн бұрын</div>
          </div>
          <span class="source-tag" style="background:#e11d48; color:#fff;">❤️ Жұптық</span>
        </div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">
          «Жұптық қара Stealth моделін алдық. Рим сандары мен есімдеріміздің ортасында қызыл жүрек өрнегі бар. Қазпоштамен басқа қалаға тегін жеткізіп берді. 10/10!»
        </p>
        <div style="margin: 10px 0; border-radius: 14px; overflow: hidden; height: 220px; border: 1px solid var(--border); cursor: pointer;" onclick="openLightbox('./images/showcase/showcase-zhangeldi-erketay-black.jpg', '«Жангелді ❤️ Еркетай» Жұптық Stealth', '42 900 ₸')">
          <img src="./images/showcase/showcase-zhangeldi-erketay-black.jpg" alt="Жангелді Еркетай Black" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div class="review-product-tag">Тапсырыс: Жұптық «Жангелді ❤️ Еркетай» 🔍</div>
      </div>

      <!-- Review 6: Arman (Two-Tone Shapyrashty) -->
      <div class="review-card">
        <div class="review-header">
          <div class="reviewer-info">
            <h4 style="display:flex; align-items:center; gap:6px;">Арман Серікбай (Алматы) <span style="font-size:10px; background:#f3e8ff; color:#6b21a8; padding:2px 8px; border-radius:10px;">2GIS Шоурум</span></h4>
            <div class="reviewer-meta">Сайран Сити 320 кеңседен • Бүгін</div>
          </div>
          <span class="source-tag" style="background:#7c3aed; color:#fff;">2GIS Сатып алу</span>
        </div>
        <div class="review-stars">★★★★★</div>
        <p class="review-text">
          «2GIS арқылы Сайран Ситидегі 320 кеңселеріне барып, өз көзіммен көріп алдым. Алтын мен күміс комби бау өте бай көрінеді, Шапырашты руының таңбасы дәл ойылған!»
        </p>
        <div style="margin: 10px 0; border-radius: 14px; overflow: hidden; height: 220px; border: 1px solid var(--border); cursor: pointer;" onclick="openLightbox('./images/showcase/showcase-arman-shapyrashty-twotone.jpg', '«Арман / Шапырашты» Two-Tone Комби', '39 900 ₸')">
          <img src="./images/showcase/showcase-arman-shapyrashty-twotone.jpg" alt="Арман Шапырашты Two-Tone" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div class="review-product-tag">Тапсырыс: Two-Tone «Арман / Шапырашты» 🔍</div>
      </div>
    </div>

    <!-- Additional Real Client Photo Proof Wall -->
    <div style="margin-top: 40px; background: #fff; border: 1px solid var(--border); border-radius: 24px; padding: 30px;">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 10px;">
        <div>
          <h4 style="font-size: 18px; color: #111;">📸 Жеткізілген тапсырыстардан фото-есептер</h4>
          <p style="font-size: 13px; color: var(--text-muted);">Нақты клиенттердің қолына тиген сағаттардың тікелей түсірілімдері.</p>
        </div>
        <span style="font-size: 12px; background: var(--accent-gold-soft); color: var(--accent-gold-dark); padding: 4px 12px; border-radius: 20px; font-weight: 600;">Шынайы фотолар</span>
      </div>

      <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px;">
        <div style="border-radius: 14px; overflow: hidden; height: 160px; cursor: pointer; border: 1px solid var(--border);" onclick="openLightbox('./images/couples/couple-1.jpg', '1+1 Жұптық сағат раушан гүлдерімен', '39 900 ₸')">
          <img src="./images/couples/couple-1.jpg" alt="Жұптық раушан гүлдермен" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div style="border-radius: 14px; overflow: hidden; height: 160px; cursor: pointer; border: 1px solid var(--border);" onclick="openLightbox('./images/couples/couple-2.jpg', '1+1 Жұптық болат сағат', '39 900 ₸')">
          <img src="./images/couples/couple-2.jpg" alt="Жұптық болат сағат" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div style="border-radius: 14px; overflow: hidden; height: 160px; cursor: pointer; border: 1px solid var(--border);" onclick="openLightbox('./images/couples/couple-3.jpg', 'Two-Tone Жұптық сағат', '42 900 ₸')">
          <img src="./images/couples/couple-3.jpg" alt="Two-Tone Жұптық" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div style="border-radius: 14px; overflow: hidden; height: 160px; cursor: pointer; border: 1px solid var(--border);" onclick="openLightbox('./images/couples/couple-4.jpg', 'Үйлену тойына арналған сағат', '45 900 ₸')">
          <img src="./images/couples/couple-4.jpg" alt="Үйлену тойы сағаты" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div style="border-radius: 14px; overflow: hidden; height: 160px; cursor: pointer; border: 1px solid var(--border);" onclick="openLightbox('./images/watch-38900-mvd-abdullin.jpg', 'ІІМ Ағаш футлярдағы сағат', '38 900 ₸')">
          <img src="./images/watch-38900-mvd-abdullin.jpg" alt="ІІМ Ағаш футляр" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'">
        </div>
        <div style="border-radius: 14px; overflow: hidden; height: 160px; cursor: pointer; border: 1px solid var(--border);" onclick="openLightbox('./images/watch-52900-royaloak-blue.jpg', 'Royal Oak көк циферблат', '52 900 ₸')">
          <img src="./images/watch-52900-royaloak-blue.jpg" alt="Royal Oak сағаты" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'">
        </div>
      </div>
    </div>
  </section>

  <!-- ───────── ЖИІ ҚОЙЫЛАТЫН СҰРАҚТАР (FAQ) ───────── -->
  <section class="faq-section" id="faq">
    <div class="section-head" style="margin-bottom: 30px;">
      <span class="section-kicker">Күмәніңіз бар ма?</span>
      <h2 class="section-title">Жиі қойылатын сұрақтар</h2>
      <p class="section-sub">Тапсырыс берушілерден жиі түсетін сауалдарға нақты жауаптар.</p>
    </div>

    <div class="faq-item active">
      <div class="faq-question" onclick="toggleFaq(this)">
        <span>1. Лазерлік жазу (гравировка) уақыт өте өшіп қалмай ма?</span>
        <span class="faq-icon">+</span>
      </div>
      <div class="faq-answer">
        Жоқ, ешқашан өшпейді. Біз жай ғана бояумен жақпаймыз, жоғары температуралы микрондық лазерлік сәулемен металдың өз қабатына терең қашаймыз. 10–20 жыл өтсе де, су тисе де, сабын тисе де жазу анық сақталады.
      </div>
    </div>

    <div class="faq-item">
      <div class="faq-question" onclick="toggleFaq(this)">
        <span>2. Басқа қалаларға қалай және неше күнде жетеді?</span>
        <span class="faq-icon">+</span>
      </div>
      <div class="faq-answer">
        Қазақстанның кез келген қаласына Қазпошта немесе автобус арқылы жеткізу — мүлдем ТЕГІН (орташа есеппен 2–4 күн). Егер сізге шұғыл (1 күнде) қажет болса, есікке дейін жедел курьерлік қызметпен жібереміз.
      </div>
    </div>

    <div class="faq-item">
      <div class="faq-question" onclick="toggleFaq(this)">
        <span>3. Kaspi Red немесе 0-0-12 арқылы бөліп төлеуге бола ма?</span>
        <span class="faq-icon">+</span>
      </div>
      <div class="faq-answer">
        Иә! Барлық сағаттарды Kaspi Red (3 айға пайызсыз), Kaspi бөліп төлеу (0-0-12) және Halyk Bank арқылы айына небәрі 2 240 теңгеден бастап сатып ала аласыз. Ешқандай артық үстемеақысыз.
      </div>
    </div>

    <div class="faq-item">
      <div class="faq-question" onclick="toggleFaq(this)">
        <span>4. Сағатқа ресми кепілдік беріле ме?</span>
        <span class="faq-icon">+</span>
      </div>
      <div class="faq-answer">
        Әрине. Әрбір сағатпен бірге 6 айдан 12 айға дейінгі ресми кепілдік талоны мөр басылып беріледі. Механизмнің дұрыс жүруіне және сапасына 100% жауапкершілік аламыз.
      </div>
    </div>
  </section>

  <!-- ───────── ШОУРУМ ЖӘНЕ 2GIS КАРТАСЫ ───────── -->
  <section class="section-wrap" id="contacts" style="background: var(--bg-alt); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
    <div class="section-head" style="margin-bottom: 30px;">
      <span class="section-kicker">Ресми мекенжайымыз</span>
      <h2 class="section-title">Шоурумға келіп көріңіз</h2>
      <p class="section-sub">Алматы қаласындағы кеңсенің үлгілерін өз қолыңызбен ұстап көре аласыз.</p>
    </div>

    <div style="background: #fff; border: 1px solid var(--border); border-radius: 24px; padding: 36px; max-width: 900px; margin: 0 auto; box-shadow: var(--shadow-sm); display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
      <div>
        <h4 style="font-size: 18px; margin-bottom: 12px; color: #111;">📍 Алматы шоурумы:</h4>
        <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" style="text-decoration: none; color: inherit; display: block; margin-bottom: 14px;">
          <div style="font-size: 15px; color: #111; line-height: 1.6; background: #fdfaf3; padding: 14px 18px; border-radius: 14px; border: 1px solid var(--border-gold); transition: var(--transition);">
            <strong style="color: var(--accent-gold-dark); border-bottom: 1.5px dashed var(--accent-gold); display: inline-block; margin-bottom: 4px;">
              Алматы қаласы, Өтеген батыр көшесі 11а ↗ (2GIS картасы)
            </strong><br>
            <span style="color: #4b5563;">«Сайран Сити» Бизнес-орталығы, 3-қабат, <strong>320-кеңсе</strong></span>
          </div>
        </a>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 18px;">
          Жұмыс уақыты: Күн сайын 10:00 – 20:00 (демалыссыз)
        </p>
        <div style="display: flex; gap: 10px;">
          <a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener" class="btn-gold" style="padding: 10px 20px; font-size: 13px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            2GIS-те ашу және маршрут құру ➔
          </a>
        </div>
      </div>

      <div style="border-left: 1px solid var(--border); padding-left: 30px;">
        <h4 style="font-size: 18px; margin-bottom: 12px; color: #111;">🚚 Жеткізу және Төлем:</h4>
        <ul style="list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 14px; color: #4b5563;">
          <li>✓ <strong>Басқа қалаларға:</strong> Қазпошта және Автобус арқылы <strong>ТЕГІН</strong></li>
          <li>✓ <strong>Курьермен:</strong> Есікке дейін жедел жеткізу (ақылы)</li>
          <li>✓ <strong>Кепілдік:</strong> 6–12 айға ресми кепілдік талоны</li>
          <li>✓ <strong>Бөліп төлеу:</strong> Kaspi Red, Kaspi 0-0-12 және Halyk Bank</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <div class="footer-inner">
      <div class="footer-brand">
        <h3>UAQYT</h3>
        <p>Жеке жазуы мен қазақи шежіре-ру таңбалары бар есімді қол сағаттар бутігі. Әр бұйым — жоғары шеберлікпен жасалған статус белгісі.</p>
      </div>

      <div class="footer-col">
        <h4>Санаттар</h4>
        <ul class="footer-links">
          <li><a href="#promo1plus1">1+1 Бонус акциясы</a></li>
          <li><a href="#catalog">Ерлер сағаттары</a></li>
          <li><a href="#catalog">Жұптық сағаттар (1+1)</a></li>
          <li><a href="#catalog">Қызметтік сағаттар (ІІМ, ҰҚК)</a></li>
          <li><a href="#catalog">Механикалық сағаттар</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Шоурум</h4>
        <ul class="footer-links">
          <li><a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener">📍 Алматы, Өтеген батыр 11а (2GIS)</a></li>
          <li><a href="https://2gis.kz/almaty/search/%D0%A3%D1%82%D0%B5%D0%B3%D0%B5%D0%BD%20%D0%B1%D0%B0%D1%82%D1%8B%D1%80%D0%B0%2011%D0%B0" target="_blank" rel="noopener">БЦ «Сайран Сити», 320 офис</a></li>
          <li><a href="https://www.instagram.com/uaqyt.kzt" target="_blank" rel="noopener">Instagram: @uaqyt.kzt</a></li>
          <li><a href="https://www.tiktok.com/@uaqyt.kzz2" target="_blank" rel="noopener">TikTok: @uaqyt.kzz2</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Тапсырыс</h4>
        <p style="font-size: 13px; line-height: 1.6; margin-bottom: 16px;">
          Эскиз дайындау — мүлдем тегін. WhatsApp арқылы өз есіміңізді жазып жіберіңіз:
        </p>
        <a href="https://wa.me/77071340000" target="_blank" rel="noopener" class="btn-gold" style="padding: 10px 20px; font-size: 13px;">
          WhatsApp-қа жазу ➔
        </a>
      </div>
    </div>

    <div class="footer-bottom">
      <div>© 2026 UAQYT.KZT — Барлық құқықтар қорғалған.</div>
      <div>Сайт Apple стилінде өңделген. Демо-презентация.</div>
    </div>
  </footer>

  <!-- Fullscreen Photo Lightbox Modal -->
  <div class="lightbox-overlay" id="lightboxModal" onclick="closeLightbox()">
    <div class="lightbox-content" onclick="event.stopPropagation()">
      <button class="lightbox-close" onclick="closeLightbox()">✕</button>
      <div class="lightbox-img-wrap">
        <img id="lightboxImg" src="" alt="Enlarge View">
      </div>
      <div class="lightbox-footer">
        <div>
          <h4 id="lightboxTitle" style="color: #fff; font-size: 18px; margin-bottom: 2px;">Сағат үлгісі</h4>
          <div id="lightboxPrice" style="color: var(--accent-gold); font-size: 16px; font-weight: 700;">39 900 ₸</div>
        </div>
        <button class="btn-gold" style="padding: 10px 20px; font-size: 13px;" onclick="orderFromLightbox()">
          Тапсырыс беру ➔
        </button>
      </div>
    </div>
  </div>

  <!-- Quick Order Modal -->
  <div class="modal-overlay" id="orderModal">
    <div class="modal-card">
      <button class="modal-close" onclick="closeOrderModal()">✕</button>
      <h3 style="font-family: var(--font-serif); font-size: 24px; margin-bottom: 6px; color: #111;" id="modalTitle">Сағатқа тапсырыс беру</h3>
      <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 18px;" id="modalSubtitle">Бағасы: 39 900 ₸</p>

      <div style="display: flex; gap: 16px; margin-bottom: 20px; background: #f8f9fa; padding: 12px; border-radius: 14px; align-items: center;">
        <img id="modalImg" src="" alt="Watch" style="width: 70px; height: 70px; object-fit: cover; border-radius: 10px;">
        <div>
          <div style="font-size: 14px; font-weight: 700; color: #111;" id="modalProdName">Сағат үлгісі</div>
          <div style="font-size: 12px; color: var(--accent-gold); font-weight: 600;">+ Тегін лазерлік гравюра сыйлыққа</div>
        </div>
      </div>

      <div class="form-group" style="margin-bottom: 12px;">
        <label class="form-label">Сағатқа қандай есім немесе ру жазылсын?</label>
        <input type="text" class="form-input" id="modalEngraveText" placeholder="Мысалы: Бағлан / Адай немесе ІІМ капитан">
      </div>

      <div class="form-group" style="margin-bottom: 20px;">
        <label class="form-label">Сіздің телефон нөміріңіз:</label>
        <input type="tel" class="form-input" id="modalPhone" placeholder="+7 (___) ___-__-__">
      </div>

      <button class="btn-gold" style="width: 100%; justify-content: center;" onclick="submitOrderModal()">
        WhatsApp арқылы тапсырысты растау ➔
      </button>
    </div>
  </div>

  <!-- Mobile Floating Action Bar -->
  <div class="mobile-float-bar">
    <div>
      <div style="font-size: 12px; color: var(--text-muted);">Жеке гравюрамен:</div>
      <strong style="font-size: 14px; color: #111;">26 900 ₸ бастап</strong>
    </div>
    <a href="https://wa.me/77071340000?text=%D0%A1%D3%99%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%81%D1%96%D0%B7%20%D0%B1%D0%B5!%20UAQYT%20%D1%81%D0%B0%D2%93%D0%B0%D1%82%D1%8B%D0%BD%D0%B0%20%D1%82%D0%B0%D0%BF%D1%81%D1%8B%D1%80%D1%8B%D1%81%20%D0%B1%D0%B5%D1%80%D0%B3%D1%96%D0%BC%20%D0%BA%D0%B5%D0%BB%D0%B5%D0%B4%D1%96" target="_blank" rel="noopener" class="btn-wa-header" style="padding: 10px 18px;">
      WhatsApp-қа жазу
    </a>
  </div>

  <script>
    let selectedBonusModel = 'Бонус №1: Классикалық болат бау';

    function togglePitch() {{
      const d = document.getElementById('pitchDrawer');
      d.classList.toggle('active');
    }}

    function selectBonus(name) {{
      selectedBonusModel = name;
      alert('Таңдалған сыйлық сағат: ' + name + '\\nНегізгі сағатпен бірге 0 ₸ бонуске қосылады!');
    }}

    function orderPromo1Plus1() {{
      const msg = `Сәлеметсіз бе! UAQYT дүкенінен «1+1 СУПЕР АКЦИЯСЫ» бойынша тапсырыс бергім келеді:\\n\\n` +
                  `1. Негізгі сағат: Каталогтан таңдау\\n` +
                  `2. Бонус сыйлық сағат: ${{selectedBonusModel}} (0 ₸ тегін)\\n` +
                  `3. Екеуіне де тегін жеке лазерлік гравюра қажет.\\n\\nМаған эскиздерін көрсете аласыз ба?`;
      window.open(`https://wa.me/77071340000?text=${{encodeURIComponent(msg)}}`, '_blank');
    }}

    // Filter Category
    function filterCategory(cat, btn) {{
      document.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const cards = document.querySelectorAll('.product-card');
      let visible = 0;
      cards.forEach(card => {{
        const cardCat = card.getAttribute('data-category') || '';
        if (cat === 'all' || cardCat.includes(cat)) {{
          card.style.display = 'flex';
          visible++;
        }} else {{
          card.style.display = 'none';
        }}
      }});
      document.getElementById('catalogCounter').innerText = `${{visible}} модель табылды`;
    }}

    // Search
    function handleSearch() {{
      const q = document.getElementById('catalogSearch').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.product-card');
      let visible = 0;
      cards.forEach(card => {{
        const name = (card.getAttribute('data-name') || '').toLowerCase();
        const desc = card.innerText.toLowerCase();
        if (!q || name.includes(q) || desc.includes(q)) {{
          card.style.display = 'flex';
          visible++;
        }} else {{
          card.style.display = 'none';
        }}
      }});
      document.getElementById('catalogCounter').innerText = `${{visible}} модель табылды`;
    }}

    // Sort: Cheap to Expensive default!
    function handleSort() {{
      const val = document.getElementById('catalogSort').value;
      const grid = document.getElementById('productGrid');
      const cards = Array.from(grid.querySelectorAll('.product-card'));

      cards.sort((a, b) => {{
        const priceA = parseInt(a.getAttribute('data-price') || '0', 10);
        const priceB = parseInt(b.getAttribute('data-price') || '0', 10);

        if (val === 'asc') return priceA - priceB;
        if (val === 'desc') return priceB - priceA;
        return 0;
      }});

      cards.forEach(c => grid.appendChild(c));
    }}

    // Engraving Simulator
    function updateDialPreview() {{
      const name = document.getElementById('inputName').value.trim() || 'БАҒЛАН';
      const sub = document.getElementById('inputSub').value.trim() || 'АДАЙ';
      const date = document.getElementById('inputDate').value.trim() || 'UAQYT KZT';

      document.getElementById('dialNameDisplay').innerText = name.toUpperCase();
      document.getElementById('dialSubDisplay').innerText = sub.toUpperCase();
      document.getElementById('dialDateDisplay').innerText = date.toUpperCase();
    }}

    function applyEngravePreset(name, sub, ornament, date) {{
      document.getElementById('inputName').value = name;
      document.getElementById('inputSub').value = sub;
      document.getElementById('dialOrnamentDisplay').innerText = ornament;
      document.getElementById('inputDate').value = date;
      updateDialPreview();
    }}

    function handleTribeSelect(val) {{
      if (!val) return;
      const parts = val.split('|');
      const tribe = parts[0];
      const ornament = parts[1] || '❖ ❖ ❖';
      document.getElementById('inputSub').value = tribe;
      document.getElementById('dialOrnamentDisplay').innerText = ornament;
      updateDialPreview();
    }}

    function setCaseColor(color, btn) {{
      document.querySelectorAll('.case-color-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const frame = document.getElementById('watchDialFrame');
      if (color === 'gold') {{
        frame.style.background = 'linear-gradient(135deg, #e5b95c 0%, #9c7b2a 50%, #e5b95c 100%)';
      }} else if (color === 'silver') {{
        frame.style.background = 'linear-gradient(135deg, #e2e8f0 0%, #94a3b8 50%, #e2e8f0 100%)';
      }} else if (color === 'twotone') {{
        frame.style.background = 'linear-gradient(135deg, #e5b95c 0%, #cbd5e1 50%, #e5b95c 100%)';
      }} else if (color === 'black') {{
        frame.style.background = 'linear-gradient(135deg, #374151 0%, #111827 50%, #374151 100%)';
      }}
    }}

    // Subtle 3D Tilt Parallax on Watch Dial Frame
    const stage = document.getElementById('engraveStage');
    const dialFrame = document.getElementById('watchDialFrame');
    if (stage && dialFrame) {{
      stage.addEventListener('mousemove', (e) => {{
        const rect = stage.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        dialFrame.style.transform = `perspective(1000px) rotateY(${{x * 20}}deg) rotateX(${{-y * 20}}deg)`;
      }});
      stage.addEventListener('mouseleave', () => {{
        dialFrame.style.transform = 'perspective(1000px) rotateY(0deg) rotateX(0deg)';
      }});
    }}

    function orderCustomWatch() {{
      const name = document.getElementById('inputName').value || 'Бағлан';
      const sub = document.getElementById('inputSub').value || 'Адай';
      const date = document.getElementById('inputDate').value || 'UAQYT KZT';

      const msg = `Сәлеметсіз бе! Мен UAQYT сайтындағы конструктор арқылы өз дизайнымды жасадым:\\n\\n` +
                  `1. Сағатқа жазу: ${{name}}\\n` +
                  `2. Ру / Орган / Жұп: ${{sub}}\\n` +
                  `3. Қосымша: ${{date}}\\n\\nМаған осы үлгідегі сағаттың эскизі мен дайын бағасын айта аласыз ба?`;
      window.open(`https://wa.me/77071340000?text=${{encodeURIComponent(msg)}}`, '_blank');
    }}

    // Lightbox Modal
    let lightboxCurrentImg = '';
    let lightboxCurrentTitle = '';
    let lightboxCurrentPrice = '';

    function openLightbox(img, title, price) {{
      lightboxCurrentImg = img;
      lightboxCurrentTitle = title;
      lightboxCurrentPrice = price;
      document.getElementById('lightboxImg').src = img;
      document.getElementById('lightboxTitle').innerText = title;
      document.getElementById('lightboxPrice').innerText = price.includes('₸') ? price : price + ' ₸';
      document.getElementById('lightboxModal').classList.add('active');
    }}

    function closeLightbox() {{
      document.getElementById('lightboxModal').classList.remove('active');
    }}

    function orderFromLightbox() {{
      closeLightbox();
      const numPrice = parseInt(lightboxCurrentPrice.replace(/\\D/g, '') || '0', 10);
      openOrderModal(lightboxCurrentTitle, numPrice, lightboxCurrentImg);
    }}

    // Quick Order Modal
    let currentOrderName = '';
    let currentOrderPrice = 0;

    function openOrderModal(name, price, img) {{
      currentOrderName = name;
      currentOrderPrice = price;
      document.getElementById('modalTitle').innerText = name;
      document.getElementById('modalProdName').innerText = name;
      document.getElementById('modalSubtitle').innerText = `Бағасы: ${{price.toLocaleString('kk-KZ')}} ₸`;
      document.getElementById('modalImg').src = img;
      document.getElementById('orderModal').classList.add('active');
    }}

    function closeOrderModal() {{
      document.getElementById('orderModal').classList.remove('active');
    }}

    function submitOrderModal() {{
      const engrave = document.getElementById('modalEngraveText').value.trim() || 'Есім жазылсын';
      const phone = document.getElementById('modalPhone').value.trim() || '';

      const msg = `Сәлеметсіз бе! UAQYT дүкенінен мына сағатқа тапсырыс бергім келеді:\\n\\n` +
                  `⌚ Үлгі: ${{currentOrderName}}\\n` +
                  `💰 Бағасы: ${{currentOrderPrice.toLocaleString('kk-KZ')}} ₸\\n` +
                  `✍️ Жазылатын мәтін (гравюра): ${{engrave}}\\n` +
                  `📞 Байланыс: ${{phone}}\\n\\nТапсырысты рәсімдеп, эскизін жібересіз бе?`;
      window.open(`https://wa.me/77071340000?text=${{encodeURIComponent(msg)}}`, '_blank');
      closeOrderModal();
    }}

    // FAQ Toggle
    function toggleFaq(el) {{
      const item = el.parentElement;
      item.classList.toggle('active');
    }}
  </script>
</body>
</html>
"""

final_html = html_template.format(
    total_count=len(all_products),
    all_cards_str=all_cards_str
)

with open(r'D:\watch-boutique\index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Generated D:\watch-boutique\index.html successfully!')
print(f'HTML Size: {len(final_html)} bytes')
