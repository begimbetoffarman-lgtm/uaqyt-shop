# -*- coding: utf-8 -*-
import os, sys, re, base64, io
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'D:\watch-boutique'
index_path = os.path.join(base_dir, 'index.html')
output_path = os.path.join(base_dir, 'uaqyt-single.html')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Build a cache of all embedded images
image_cache = {}

def get_base64_for_path(rel_path):
    if rel_path in image_cache:
        return image_cache[rel_path]
    
    clean = rel_path.replace('./', '').replace('/', os.sep)
    full = os.path.join(base_dir, clean)
    if os.path.exists(full):
        try:
            im = Image.open(full)
            if im.mode in ('RGBA', 'P'):
                im = im.convert('RGB')
            # Resize to max 750px to keep file reasonable
            im.thumbnail((750, 750), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format='JPEG', quality=80)
            b64_str = f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
            image_cache[rel_path] = b64_str
            return b64_str
        except Exception as e:
            print(f"Error {rel_path}: {e}")
            return rel_path
    return rel_path

print("Scanning and converting all images...")
# Find all image paths in html
matches = set(re.findall(r'(\./images/[^"\'\s]+\.jpg)', html))
print(f"Found {len(matches)} distinct image references.")

for m in sorted(matches):
    get_base64_for_path(m)

print(f"Successfully converted {len(image_cache)} images to base64.")

# Replace in html
def replace_all(match):
    src = match.group(0)
    for k, v in image_cache.items():
        if k in src:
            return src.replace(k, v)
    return src

# Replace in JSON data and in HTML tags
single_html = html
for k, v in image_cache.items():
    single_html = single_html.replace(f'"{k}"', f'"{v}"')
    single_html = single_html.replace(f"'{k}'", f"'{v}'")
    single_html = single_html.replace(f'src="{k}"', f'src="{v}"')
    single_html = single_html.replace(f"src='{k}'", f"src='{v}'")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(single_html)

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Standalone single-file created: {output_path} ({size_mb:.2f} MB)")
