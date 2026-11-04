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
