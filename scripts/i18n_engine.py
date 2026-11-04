# -*- coding: utf-8 -*-
"""Post-processing of the generated page: Russian becomes the default text, Kazakh stays in data-kk.
Also puts the sections into the conversion-friendly order."""
import re
from bs4 import BeautifulSoup, NavigableString, Comment
from i18n_ui import UI
from i18n_products import PROD_RU, PIECES, STRAP_RU, ru_piece_join

NUM = re.compile(r"\d+(?:[  ]\d{3})*")


def norm(s):
    return " ".join(s.split())


def _numkey(t):
    nums = NUM.findall(t)
    return NUM.sub("#", t), nums


def _fill(tpl, nums):
    it = iter(nums)
    return re.sub(r"#", lambda m: next(it, "#"), tpl)


def build_maps(products):
    exact, numeric = {}, {}
    for kk, ru, kkf in UI:
        key = norm(kk)
        val = (ru, kkf or kk)
        if "#" in key:
            numeric[key] = val
        else:
            exact[key] = val
    for p in products:
        r = p.get("ru") or {}
        for f in ("name", "desc", "badge", "tag"):
            if p.get(f) and r.get(f):
                exact[norm(p[f])] = (r[f], p[f])
    return exact, numeric


ATTRS = ("placeholder", "alt", "title", "aria-label")


def localize(html, products, extra_exact=None):
    exact, numeric = build_maps(products)
    if extra_exact:
        exact.update({norm(k): v for k, v in extra_exact.items()})
    soup = BeautifulSoup(html, "html.parser")
    unmapped = []
    cyr = re.compile(r"[А-Яа-яӘәҒғҚқҢңӨөҰұҮүҺһІі]")

    def lookup(t):
        n = norm(t)
        if n in exact:
            return exact[n]
        key, nums = _numkey(n)
        if key in numeric:
            ru, kk = numeric[key]
            return _fill(ru, nums), _fill(kk, nums)
        return None

    for s in list(soup.find_all(string=True)):
        if isinstance(s, Comment):
            continue
        par = s.parent
        if par is None or par.name in ("script", "style"):
            continue
        n = norm(str(s))
        if not n or not cyr.search(n):
            continue
        hit = lookup(n)
        if not hit:
            if par.name not in ("title",) and re.search(r"[ӘәҒғҚқҢңӨөҰұҮүҺһІі]", n):
                unmapped.append(n)
            continue
        ru, kk = hit
        raw = str(s)
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        if par.name in ("option", "title", "textarea"):
            par["data-bi"] = ""
            par["data-ru"] = ru
            par["data-kk"] = kk
            s.replace_with(NavigableString(lead + ru + trail))
        else:
            span = soup.new_tag("span")
            span["data-bi"] = ""
            span["data-ru"] = ru
            span["data-kk"] = kk
            span.string = ru
            s.replace_with(span)
            if lead:
                span.insert_before(lead)
            if trail:
                span.insert_after(trail)

    # attributes
    for el in soup.find_all(True):
        keys = []
        for a in ATTRS:
            v = el.get(a)
            if isinstance(v, str) and cyr.search(v):
                hit = lookup(v)
                if hit:
                    el[a] = hit[0]
                    el[f"data-ru-{a}"] = hit[0]
                    el[f"data-kk-{a}"] = hit[1]
                    keys.append(a)
                elif re.search(r"[ӘәҒғҚқҢңӨөҰұҮүҺһІі]", v):
                    unmapped.append("[" + a + "] " + v)
        if keys:
            el["data-bia"] = ",".join(keys)
    return soup, sorted(set(unmapped))


def reorder(soup, order):
    body = soup.body
    anchors = {}
    for sid in order:
        node = soup.find(id=sid)
        if node is not None:
            anchors[sid] = node
    nodes = [anchors[s] for s in order if s in anchors]
    if not nodes:
        return
    first = nodes[0]
    marker = soup.new_tag("div")
    marker["id"] = "_reorder_marker"
    first.insert_before(marker)
    for n in nodes:
        n.extract()
    for n in reversed(nodes):
        marker.insert_after(n)
    marker.decompose()


# ───────────────────────── dark theme ─────────────────────────
DARK_ROOT = """:root {
      --bg: #0c1120;
      --bg-alt: #111829;
      --bg-card: #161e33;
      --border: #26304a;
      --border-focus: #d4af37;
      --border-gold: rgba(212, 175, 55, 0.4);
      --text: #f5f6f8;
      --text-muted: #a3acc2;
      --accent-gold: #d4af37;
      --accent-gold-soft: #1f1c12;
      --accent-gold-dark: #e6c65c;
      --accent-green: #15803d;
      --accent-green-dark: #128C7E;
      --accent-red: #e11d48;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.5);
      --shadow-md: 0 10px 30px rgba(0,0,0,0.5);
      --shadow-lg: 0 20px 45px rgba(0,0,0,0.6);
      --font-serif: 'Cormorant Garamond', Georgia, serif;
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --nav-height: 70px;
      --transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }"""

_SOLID_BG = {
    "#fff": "var(--bg-card)", "#ffffff": "var(--bg-card)", "white": "var(--bg-card)",
    "#fafafa": "var(--bg-alt)", "#f8f9fa": "var(--bg-alt)", "#f9fafb": "var(--bg-alt)", "#f8fafc": "var(--bg-alt)",
    "#f1f5f9": "var(--bg-alt)", "#f3f4f6": "var(--bg-alt)", "#f4f4f5": "var(--bg-alt)", "#e2e8f0": "var(--bg-alt)",
    "#fdfaf3": "var(--accent-gold-soft)", "#fdfbf7": "var(--accent-gold-soft)", "#fffdf8": "var(--accent-gold-soft)",
    "#fffbeb": "var(--accent-gold-soft)", "#fdf8ef": "var(--accent-gold-soft)", "#fbf7ee": "var(--accent-gold-soft)",
    "#f0f9ff": "rgba(14,165,233,.14)", "#f0fdf4": "rgba(34,197,94,.14)", "#ecfdf5": "rgba(34,197,94,.14)",
    "#fff1f2": "rgba(225,29,72,.16)", "#fef2f2": "rgba(225,29,72,.16)", "#fdf2f8": "rgba(236,72,153,.16)", "#fce7f3": "rgba(236,72,153,.16)",
    "#fee2e2": "rgba(225,29,72,.2)", "#fef3c7": "rgba(212,175,55,.18)",
}
_TEXT = {
    "#111827": "var(--text)", "#1f2937": "var(--text)", "#374151": "var(--text)", "#4b5563": "var(--text-muted)",
    "#6b7280": "var(--text-muted)", "#9ca3af": "var(--text-muted)", "#000": "var(--text)",
    "#166534": "#86efac", "#047857": "#6ee7b7", "#0284c7": "#7dd3fc", "#92400e": "#e6c65c", "#724c16": "#e6c65c",
    "#be185d": "#f9a8d4", "#9f1239": "#fda4af", "#881337": "#fda4af", "#b91c1c": "#fca5a5", "#9a3412": "#fdba74",
}
_BORDER = {"#bae6fd", "#bbf7d0", "#a7f3d0", "#fecdd3", "#fde68a", "#fbcfe8", "#e5e7eb", "#e9ecef", "#cbd5e1", "#f3f4f6", "#fef3c7"}
_LIGHT = re.compile(r"#(?:f[0-9a-f]{5}|f[0-9a-f]{2}|e[5-9a-f][0-9a-f]{4})\b|#fff\b|white", re.I)
_SKIP_SEL = ("dial", "hand", "center-pin", "tick", "lang-btn", "holiday-ribbon", "story-", "offer-btn", "holiday-btn", "pick-card-btn")


def _decl(prop, val, sel):
    p = prop.strip().lower()
    v = val.strip()
    vl = v.lower()
    if p in ("background", "background-color"):
        if "gradient" in vl:
            if _LIGHT.search(v) and not re.search(r"#(?:e11d48|833ab4|be123c|25d366|d4af37)", vl):
                if re.search(r"#(?:fef2f2|fff1f2|fdf2f8|fce7f3)", vl):
                    return p, "rgba(225,29,72,.14)"
                if re.search(r"#(?:fdf8ef|f6e8d2|fffbeb|fef3c7|fdfaf3)", vl):
                    return p, "var(--accent-gold-soft)"
                return p, "var(--bg-card)"
            return p, v
        if vl in _SOLID_BG:
            return p, _SOLID_BG[vl]
        mh = re.fullmatch(r"#([0-9a-f]{6})", vl)
        if mh:
            r, g, b = (int(mh.group(1)[i:i + 2], 16) for i in (0, 2, 4))
            if (0.2126 * r + 0.7152 * g + 0.0722 * b) > 225:
                return p, "var(--accent-gold-soft)" if r > b + 6 else "var(--bg-alt)"
        if vl in ("#111827", "var(--text)", "#1e293b", "#0f172a"):
            if "footer" in sel:
                return p, "#080c18"
            if "tiktok" in sel:
                return p, "#141b2e"
            return p, "var(--accent-gold)"
    if p == "color":
        if vl in _TEXT:
            return p, _TEXT[vl]
    if p in ("border", "border-top", "border-bottom", "border-left", "border-right", "border-color", "outline"):
        for b in _BORDER:
            if b in vl:
                v = re.sub(re.escape(b), "var(--border)", v, flags=re.I)
        return p, v
    if p == "background" and vl.startswith("rgba(255, 255, 255"):
        return p, "rgba(12, 17, 32, 0.92)"
    return p, v


def darken_css(css):
    def rule(m):
        sel, body = m.group(1), m.group(2)
        s = sel.strip().lower()
        if any(k in s for k in _SKIP_SEL) or s.startswith("@") or s.startswith("from") or s.startswith("to") or "%" in s:
            return m.group(0)
        decls = [d for d in body.split(";")]
        out = []
        flipped = False
        for d in decls:
            if ":" not in d:
                out.append(d)
                continue
            prop, val = d.split(":", 1)
            np_, nv = _decl(prop, val, s)
            if np_ in ("background", "background-color") and nv == "var(--accent-gold)" and val.strip().lower() in ("#111827", "var(--text)", "#1e293b", "#0f172a"):
                flipped = True
            out.append(f"{prop}: {nv}" if nv != val.strip() else d)
        if flipped:
            out = [re.sub(r"color\s*:\s*(#fff(?:fff)?|white)\b", "color: #111", d) if re.match(r"\s*color\s*:", d) else d for d in out]
            out = [d.replace("border-color: var(--text)", "border-color: var(--accent-gold)") for d in out]
        return sel + "{" + ";".join(out) + "}"

    css = re.sub(r":root\s*\{[^{}]*\}", DARK_ROOT, css, count=1)
    css = re.sub(r"([^{}]+)\{([^{}]*)\}", rule, css)
    css = re.sub(r"background(?:-color)?\s*:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0?\.9\d*\s*\)", "background: rgba(12, 17, 32, 0.94)", css)
    return css


def apply_dark(soup):
    style = soup.find("style")
    if style is not None and style.string:
        marker = "/*__DARK_STOP__*/"
        css = str(style.string)
        head, sep, tail = css.partition(marker)
        style.string = darken_css(head) + sep + tail
    for m in soup.find_all("meta", attrs={"name": "theme-color"}):
        m["content"] = "#0c1120"
