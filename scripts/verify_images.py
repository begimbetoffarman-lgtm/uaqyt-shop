# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\watch-boutique\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all src in img tags
matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f'Total img src tags: {len(matches)}')

missing = []
valid = []
for src in matches:
    if not src or src == '':
        continue
    clean_src = src.replace('./', '').replace('/', os.sep)
    full_path = os.path.join(r'D:\watch-boutique', clean_src)
    if os.path.exists(full_path):
        valid.append(src)
    else:
        missing.append((src, full_path))

print(f'Valid images on disk: {len(valid)}')
if missing:
    print(f'Missing images: {len(missing)}')
    for s, p in missing:
        print('  MISSING:', s, '->', p)
else:
    print('ALL IMAGES EXIST AND ARE READY!')
