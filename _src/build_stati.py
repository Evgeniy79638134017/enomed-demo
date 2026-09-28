import os, re, glob, json, difflib, html
import markdown

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'articles')
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = '/enomed-demo'
CTA = BASE + '/#contact'

files = sorted(glob.glob(SRC + '/*.md'))
arts = []
for f in files:
    raw = open(f, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
    fm, body = m.group(1), m.group(2)
    def g(k):
        mm = re.search(rf'^{k}:\s*(.*)$', fm, re.M); return mm.group(1).strip() if mm else ''
    slug = re.sub(r'^\d+-', '', os.path.basename(f)[:-3])
    arts.append(dict(n=int(os.path.basename(f)[:2]), slug=slug, title=json.loads(g('title')), desc=json.loads(g('description')),
                     keywords=json.loads(g('keywords')), body=body))
slugs = [a['slug'] for a in arts]

def fix_link(m):
    s = m.group(1)
    over={'marshruty-v-heihe-cherez-blagoveshchensk':'iz-lyubogo-goroda-v-heihe','otzyvy-o-stomatologiyah-heihe':'heihe-stomatologiya-otzyvy'}
    if s in over: return f'({BASE}/stati/{over[s]}/)'
    best = difflib.get_close_matches(s, slugs, n=1, cutoff=0.0)[0]
    return f'({BASE}/stati/{best}/)'

CSS = """
:root{--forest:#0f3e17;--sage:#b1dbb8;--keylime:#e1f4df;--mint:#cfe7d3;--cream:#fffefc;--charcoal:#222;--border:#efeeeb;--muted:#3d4f40;--r:14px}
*{box-sizing:border-box}html,body{margin:0;background:var(--cream);color:var(--charcoal)}
body{font-family:"Onest",Inter,"Helvetica Neue",Arial,sans-serif;font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:var(--forest)}
.top{position:sticky;top:0;z-index:5;background:rgba(255,254,252,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}
.top .w{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;max-width:1100px;margin:0 auto}
.logo{font-family:"Inter Tight",Onest,sans-serif;font-weight:600;font-size:18px;text-decoration:none;color:var(--forest)}
.btn{display:inline-block;background:var(--forest);color:var(--cream);text-decoration:none;border-radius:999px;padding:10px 18px;font-weight:500;font-size:15px;white-space:nowrap}
.btn.light{background:var(--keylime);color:var(--forest)}
.w{max-width:760px;margin:0 auto;padding:0 16px}
.crumbs{font-size:14px;color:var(--muted);margin:28px 0 8px}.crumbs a{color:var(--muted)}
h1,h2,h3{font-family:"Inter Tight",Onest,sans-serif;letter-spacing:-.02em;color:var(--forest);line-height:1.2}
h1{font-size:clamp(28px,5vw,42px);font-weight:600;margin:8px 0 18px}
h2{font-size:clamp(22px,3.4vw,28px);font-weight:600;margin:40px 0 12px}
p,li{color:var(--charcoal)}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:15px;display:block;overflow-x:auto}
th,td{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top}th{background:var(--keylime)}
.faq{background:var(--keylime);border-radius:var(--r);padding:8px 20px 12px;margin:32px 0}
.cta{background:var(--forest);color:var(--cream);border-radius:var(--r);padding:24px;margin:36px 0}
.cta h2{color:var(--cream);margin-top:0}.cta p{color:var(--cream)}.cta a.btn{background:var(--cream);color:var(--forest)}.cta ul{margin:6px 0 18px;padding-left:20px}.cta li{color:var(--cream);margin:4px 0}.cta .sec{display:inline-block;margin-left:14px;color:var(--sage);font-size:15px}
.disc{font-size:14px;color:var(--muted);border-top:1px solid var(--border);padding-top:14px;margin:28px 0 48px}
.list{list-style:none;padding:0;display:grid;gap:10px;margin:24px 0 48px}
.list a{display:block;border:1px solid var(--border);border-radius:var(--r);padding:14px 16px;text-decoration:none;background:#fff}
.list a:hover{border-color:var(--sage)}.list b{display:block;color:var(--forest);font-family:"Inter Tight",Onest,sans-serif;font-size:18px;font-weight:600}
.list span{font-size:14px;color:var(--muted)}
.more{margin:24px 0}
footer{border-top:1px solid var(--border);font-size:13px;color:var(--muted);padding:20px 0 32px}
"""

HEAD = """<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600&family=Onest:wght@400;500;600&display=swap">
<style>{css}</style>{ld}</head><body>
<header class="top"><div class="w" style="max-width:1100px"><a class="logo" href="{base}/">ЭНО мед</a><span style="display:flex;gap:8px"><a class="btn light" href="{base}/stati/">Статьи</a><a class="btn" href="{base}/">Об ЭНО мед</a></span></div></header>
"""
FOOT = """<footer><div class="w">«ЭНО мед» не является медицинской организацией. Лечение проводит партнёрская клиника в Хэйхэ. ИП Ожегов Р.В., ИНН 280113718085. Концепт подготовлен ИИщенко LAB для встречи ИИщенко CLUB 29.09.2026.</div></footer></body></html>"""

CTA_BLOCK = (f'<section class="cta"><h2>Кто такие «ЭНО мед» и как мы сопровождаем лечение</h2>'
  '<p>Мы из Благовещенска и организуем лечение зубов в Хэйхэ так, чтобы вы заранее понимали каждый шаг:</p>'
  '<ul><li>план лечения и смета — до поездки, без предоплаты;</li><li>русскоговорящий куратор — от границы до кресла врача и после возвращения;</li>'
  '<li>клиника с лицензией и открытыми документами врачей;</li><li>паспорт импланта на руках после лечения.</li></ul>'
  f'<a class="btn" href="{BASE}/">Узнать подробности →</a><a class="sec" href="{CTA}">или сразу получить план лечения</a></section>')
md = markdown.Markdown(extensions=['tables'])
for a in arts:
    body = re.sub(r'\(/stati/([^)]+)\)', fix_link, a['body'])
    body = body.replace('https://eno-med.ru/#contacts', CTA)
    # split parts
    h1 = re.search(r'^# (.+)$', body, re.M).group(1)
    body = re.sub(r'^# .+\n', '', body, count=1, flags=re.M)
    parts = re.split(r'^(?=## )', body, flags=re.M)
    faq_q = []
    out = []
    disc = ''
    for part in parts:
        if part.startswith('## Частые вопросы'):
            qs = re.findall(r'\*\*(.+?\?)\*\*\s*\n(.+?)(?=\n\s*\n\*\*|\n*\Z|\n\s*\n##)', part, re.S)
            faq_q = [(q.strip(), re.sub(r'\s+', ' ', ans).strip()) for q, ans in qs]
            md.reset(); out.append('<section class="faq">' + md.convert(part) + '</section>')
        elif part.startswith('## Получить'):
            seg = part.split('\n---\n')
            out.append(CTA_BLOCK)
            if len(seg) > 1:
                md.reset(); disc = md.convert(seg[1].strip())
        else:
            md.reset(); out.append(md.convert(part))
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'], "inLanguage": "ru",
           "keywords": ", ".join(a['keywords']), "author": {"@type": "Organization", "name": "ЭНО мед"}, "datePublished": "2026-09-28"}]
    if faq_q:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'[\*\[\]]|\(/[^)]*\)', '', ans)}} for q, ans in faq_q]})
    ldh = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    others = [b for b in arts if b is not a][:0]
    page = HEAD.format(title=html.escape(a['title']), desc=html.escape(a['desc']), css=CSS, ld=ldh, base=BASE, cta=CTA)
    page += f'<main class="w"><div class="crumbs"><a href="{BASE}/">Главная</a> · <a href="{BASE}/stati/">Статьи</a></div><h1>{html.escape(h1)}</h1>'
    page += ''.join(out) + f'<div class="disc">{disc}</div></main>' + FOOT
    d = f'{REPO}/stati/{a["slug"]}'; os.makedirs(d, exist_ok=True)
    open(d + '/index.html', 'w', encoding='utf-8').write(page)
    a['faqn'] = len(faq_q)

# index
groups = [('Цены и стоимость', [1, 2, 7, 14, 22, 23, 25]), ('Лечение и процедуры', [5, 6, 8, 10, 18, 19, 20, 30]),
          ('Отзывы и как выбрать клинику', [3, 4, 9, 15, 16, 17, 24]), ('Поездка и организация', [11, 12, 13, 21, 26, 27, 28, 29])]
byn = {a['n']: a for a in arts}
extra = sorted(n for n in byn if n not in sum([g[1] for g in groups], []))
if extra: groups = [('Новое', extra)] + groups
page = HEAD.format(title='Статьи о лечении зубов в Хэйхэ — ЭНО мед', desc='30 статей о лечении зубов в Китае: цены, отзывы, имплантация, протезирование, как добраться до Хэйхэ и как выбрать клинику.', css=CSS, ld='', base=BASE, cta=CTA)
page += f'<main class="w"><div class="crumbs"><a href="{BASE}/">Главная</a> · Статьи</div><h1>Всё о лечении зубов в Хэйхэ</h1><p>30 статей под самые частые вопросы, которые люди задают Яндексу. Без обещаний и рекламы — честно о ценах, страхах и том, как всё устроено.</p>'
for name, ns in groups:
    page += f'<h2>{name}</h2><ul class="list">' + ''.join(f'<li><a href="{BASE}/stati/{byn[n]["slug"]}/"><b>{html.escape(byn[n]["title"])}</b><span>{html.escape(byn[n]["desc"])}</span></a></li>' for n in ns) + '</ul>'
page += CTA_BLOCK + '</main>' + FOOT
os.makedirs(REPO + '/stati', exist_ok=True)
open(REPO + '/stati/index.html', 'w', encoding='utf-8').write(page)
print('ok', len(arts), 'faq per article:', [a['faqn'] for a in arts])
