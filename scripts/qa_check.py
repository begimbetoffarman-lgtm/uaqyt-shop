# -*- coding: utf-8 -*-
"""Quick QA after building the site.   Run:  PYTHONIOENCODING=utf-8 python scripts/qa_check.py
Catches the bugs that kept coming back: duplicate photos, missing files, empty prices, wrong section,
external images, stale price-filter counts."""
import os, re, sys, hashlib, glob, io, contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import compile_data as cd
from PIL import Image

problems, notes = [], []

def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()

def ahash(p):
    im = Image.open(p).convert('L').resize((16, 16)); px = list(im.getdata()); a = sum(px) / 256
    return tuple(1 if x > a else 0 for x in px)

# 1. images exist, no duplicate photos (exact + near duplicates)
items = [(p['id'], p['img']) for p in cd.all_products_sorted] + [(r['id'], r['img']) for r in cd.customer_reviews]
seen, hashes = {}, {}
for pid, img in items:
    f = img.replace('./', '')
    if not os.path.exists(f):
        (notes if pid.startswith('rev_') else problems).append('нет файла %s у %s%s' % (img, pid, ' (отзыв не показывается на сайте)' if pid.startswith('rev_') else '')); continue
    h = md5(f)
    if h in seen: problems.append('одинаковое фото: %s и %s' % (seen[h], pid))
    seen[h] = pid
    hashes[pid] = ahash(f)
ids = list(hashes)
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        if sum(a != b for a, b in zip(hashes[ids[i]], hashes[ids[j]])) <= 4 and seen.get(md5(dict(items)[ids[i]].replace('./', ''))) != ids[j]:
            notes.append('очень похожие фото: %s и %s' % (ids[i], ids[j]))

# 2. sections: men's must not be pairs, pairs must be named as pair/set
for p in cd.mens_all:
    if re.search(r'1\+1|Жұптық', p['name']): problems.append('в «Мужских» парное название: ' + p['id'])
for p in cd.couples_all:
    if not re.search(r'1\+1|Жұптық|couple|pair|roses', p['id'] + p['name'] + p['cat']):
        problems.append('в «Парных» без признака пары: ' + p['id'])
    if p['id'].startswith(('extra_', 'showcase_', 'p75900_rahat')):
        problems.append('одиночная модель в «Парных»: ' + p['id'])

# 3. prices
no_price = [p['id'] for p in cd.all_products_sorted if p.get('is_price_on_request')]
notes.append('моделей «цена по запросу»: %d' % len(no_price))
for p in cd.all_products_sorted:
    if not p.get('is_price_on_request') and not p.get('price'): problems.append('нет цены: ' + p['id'])

# 4. built page
html = open('index.html', encoding='utf-8').read()
if 'unsplash' in html: problems.append('внешняя картинка unsplash в index.html')
for m in set(re.findall(r'<img[^>]+src="(https?://[^"]+)"', html)): problems.append('внешняя картинка: ' + m)
for must in ('id="faq"', 'id="bonus"', 'id="catalog"', 'id="reviews"'):
    if must not in html: problems.append('в index.html нет блока ' + must)
if 'бутіг' in html.lower() or 'БУТІГ' in html: problems.append('опечатка «бутіг»')
n_cards = len(re.findall(r'class="product-card"', html))
if n_cards != len(cd.all_products_sorted): problems.append('карточек %d, моделей %d' % (n_cards, len(cd.all_products_sorted)))

# 5. price filter counts shown on the chips
def bucket(lo, hi):
    return len([p for p in cd.all_products_sorted if not p.get('is_price_on_request') and lo <= p['price'] < hi])
print('Фильтр цены: до 30к=%d, 30–40к=%d, 40–55к=%d, от 55к=%d' % (bucket(0, 30000), bucket(30000, 40000), bucket(40000, 55000), bucket(55000, 10**9)))

print('Мужских %d, Парных %d, всего %d' % (len(cd.mens_all), len(cd.couples_all), len(cd.all_products_sorted)))
for n in notes: print('  инфо:', n)
if problems:
    print('\nПРОБЛЕМЫ (%d):' % len(problems))
    for p in problems: print('  ✗', p)
    sys.exit(1)
print('\nOK: проблем не найдено')
