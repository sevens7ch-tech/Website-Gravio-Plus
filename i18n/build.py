#!/usr/bin/env python3
# © 2026 Christian Haake, alle Rechte vorbehalten.
# Erzeugt die Startseite in allen Sprachen der App aus i18n/seite.de.html (Quelle, deutsch):
#   index.html (de), en/index.html, it/index.html, nl/index.html, fr/index.html, es/index.html
# Aufruf: python3 i18n/build.py   – Texte ändern: deutsch in seite.de.html, Übersetzungen in texte.py
import os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
sys.path.insert(0, here)
from texte import L, T

BASE = 'https://sevens7ch-tech.github.io/Website-Gravio-Plus/'
LANGS = ['de'] + L
NAMES = {'de': 'Deutsch', 'en': 'English', 'it': 'Italiano', 'nl': 'Nederlands', 'fr': 'Français', 'es': 'Español'}
src = open(os.path.join(here, 'seite.de.html'), encoding='utf-8').read()

def esc(t):  # wie der Text im HTML steht
    return t.replace('&', '&amp;')

def pat(t):
    return r'\s+'.join(re.escape(w) for w in esc(t).split())

def switch(lang):
    up = '' if lang == 'de' else '../'
    links = []
    for l in LANGS:
        href = up + ('' if l == 'de' else l + '/') or './'
        cur = ' aria-current="page"' if l == lang else ''
        style = 'background: #f59e0b; color: #09090b;' if l == lang else 'background: transparent; color: #f4f4f5;'
        links.append(f'<a href="{href}" hreflang="{l}" lang="{l}" title="{NAMES[l]}"{cur} data-lang="{l}" style="display: inline-flex; align-items: center; justify-content: center; min-width: 36px; min-height: 36px; padding: 0 6px; border-radius: 999px; {style} font-size: 12px; font-weight: 800; letter-spacing: .04em; text-decoration: none">{l.upper()}</a>')
    return ('<div class="lang-switch" role="group" aria-label="Sprache / Language" style="display: inline-flex; flex-wrap: wrap; gap: 2px; padding: 4px; border-radius: 999px; background: #27272a; box-shadow: 0 2px 6px rgba(0,0,0,.3)">'
            + ''.join(links) + '</div>')

def head(lang):
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{"" if l == "de" else l + "/"}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}">'
    js = ("<script>(function(){try{document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-lang]');"
          "if(a)localStorage.setItem('gravio_lang',a.getAttribute('data-lang'));});")
    if lang == 'de':  # erster Besuch: Browsersprache wählen, solange niemand selbst gewählt hat
        js += ("if(!localStorage.getItem('gravio_lang')){var ok=" + repr(L).replace("'", '"') + ";"
               "var p=((navigator.languages&&navigator.languages[0])||navigator.language||'de').slice(0,2).toLowerCase();"
               "if(ok.indexOf(p)>=0){localStorage.setItem('gravio_lang',p);location.replace(p+'/');}else localStorage.setItem('gravio_lang','de');}")
    js += "}catch(e){}})();</script>"
    return alts + '\n' + js

def build(lang):
    h = src.replace('<!--LANG-SWITCH-->', switch(lang)).replace('<!--LANG-HEAD-->', head(lang))
    if lang == 'de':
        return h
    i = L.index(lang)
    h = h.replace('<html lang="de">', f'<html lang="{lang}">', 1)
    missing = []
    for de in sorted(T, key=len, reverse=True):
        tr = esc(T[de][i])
        n = 0
        def txt(m):
            lead = '' if tr[:1] in '.,' else m.group(1)
            return '>' + lead + tr + m.group(2) + '<'
        h, k = re.subn(r'>(\s*)' + pat(de) + r'(\s*)<', txt, h); n += k
        h, k = re.subn(r'((?:alt|aria-label|title|placeholder|content)=")' + pat(de) + '"', lambda m: m.group(1) + tr + '"', h); n += k
        if not n: missing.append(de)
    # Skript: Versionsanzeige
    h = h.replace("'Aktuelle Version ' + u.version", repr(T['Aktuelle Version'][i] + ' ') + ' + u.version')
    # relative Pfade eine Ebene höher
    for a, b in [('src="logo.png"', 'src="../logo.png"'), ('href="logo.png"', 'href="../logo.png"'),
                 ('href="impressum.html"', 'href="../impressum.html"'), ('href="datenschutz.html"', 'href="../datenschutz.html"'),
                 ('href="handbuch/', 'href="../handbuch/'), ("url('fonts/", "url('../fonts/")]:
        h = h.replace(a, b)
    if missing:
        sys.exit(f'{lang}: nicht gefunden: {missing}')
    return h

for lang in LANGS:
    out = os.path.join(root, 'index.html') if lang == 'de' else os.path.join(root, lang, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(build(lang))
    print('OK', lang)
