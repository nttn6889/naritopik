"""Sinh site tĩnh naritopik.com (tầng miễn phí, cho Google đọc).
- Bài viết tay: noi-dung/*.html, dòng đầu là chú thích JSON {"path", "title", "desc", "h1"?, "lead"?, "crumb"?, "type": page|article, "nav"?}.
- Trang ngữ pháp câu 1–2 / 3–4 sinh từ data/ngu-phap.json (lấy bằng tools/lay_du_lieu.py).
- Ghi ra thư mục gốc repo (GitHub Pages) + sitemap.xml, robots.txt.
Chạy: python3 tools/build.py"""
import json, os, re, html, unicodedata, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://naritopik.com'
ZALO = 'https://zalo.me/0399214554'
TODAY = datetime.date.today().isoformat()
PAGES = []  # (path, lastmod) cho sitemap

NAV = [('/ngu-phap-topik/', 'Ngữ pháp', 'np'), ('/viet-topik/', 'Viết 51–54', 'viet'),
       ('/de-thi-topik/', 'Đề thi', 'de'), ('/bang-gia/', 'Bảng giá', 'gia'),
       ('https://hoc.naritopik.com/ve-co/', 'Về cô', 'co')]


def esc(s):
    return html.escape(s, quote=True)


def slug(s):
    s = unicodedata.normalize('NFD', s.replace('đ', 'd').replace('Đ', 'D'))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def layout(path, title, desc, body, nav='', ld=None, typ='website'):
    url = SITE + path
    navh = ''.join(f'<a href="{h}"{" class=on" if k == nav else ""}>{t}</a>' for h, t, k in NAV)
    navh += f'<a class="cta" href="{ZALO}" rel="nofollow">Học thử với cô</a>'
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    full = title if 'Nari TOPIK' in title else f'{title} | Nari TOPIK'
    return f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{typ}"><meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/og.jpg"><meta property="og:site_name" content="Nari TOPIK"><meta property="og:locale" content="vi_VN">
<link rel="icon" href="/assets/favicon-64.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&family=Noto+Sans+KR:wght@400;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{lds}
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="/" aria-label="Nari TOPIK – trang chủ"><img src="/assets/nari-topik-ngang.svg" alt="Nari TOPIK" width="124" height="42"></a>
<button class="menu-btn" aria-label="Mở menu" onclick="this.nextElementSibling.classList.toggle('open')">☰</button>
<nav>{navh}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div class="cols">
<div><span class="logo"><img src="/assets/nari-topik-ngang.svg" alt="Nari TOPIK" width="118" height="40"></span>
<p>Hiểu từng câu – Vững từng cấp. Luyện thi TOPIK II cùng cô Ngân: cử nhân Đại học Daegu (Hàn Quốc), gần 10 năm sống và làm biên phiên dịch tại Hàn.
Dạy trực tiếp tại Quỳnh Lưu (Nghệ An) và online toàn quốc.</p>
<p>Zalo cô Ngân: <a href="{ZALO}" rel="nofollow">0399 214 554</a></p></div>
<div><h4>Học miễn phí</h4><ul>
<li><a href="/ngu-phap-topik/cau-1-2/">Ngữ pháp câu 1–2</a></li><li><a href="/ngu-phap-topik/cau-3-4/">Ngữ pháp tương đồng câu 3–4</a></li>
<li><a href="/viet-topik/cau-51/">Cách viết câu 51</a></li><li><a href="/viet-topik/cau-52/">Cách viết câu 52</a></li>
<li><a href="/de-thi-topik/cau-truc-de-topik-2/">Cấu trúc đề TOPIK II</a></li></ul></div>
<div><h4>Nari TOPIK</h4><ul><li><a href="/bang-gia/">Bảng giá</a></li><li><a href="https://hoc.naritopik.com/ve-co/">Về cô Ngân</a></li>
<li><a href="https://hoc.naritopik.com/hoc-cung-co/">Học cùng cô</a></li><li><a href="https://hoc.naritopik.com/thi-thu/">Phòng thi thử</a></li></ul></div>
</div>
<div class="copy">© {datetime.date.today().year} Nari TOPIK · naritopik.com</div>
</div></footer>
<a class="zalo-fab" href="{ZALO}" rel="nofollow">💬 Zalo cô</a>
</body></html>
'''


def write(path, text, lastmod=TODAY):
    out = os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(text)
    PAGES.append((path, lastmod))


def crumbs(items):
    """items: [(tên, path)] — phần tử cuối là trang hiện tại."""
    h = ' › '.join(f'<a href="{p}">{esc(t)}</a>' if i < len(items) - 1 else esc(t) for i, (t, p) in enumerate(items))
    ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
          'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': t, 'item': SITE + p} for i, (t, p) in enumerate(items)]}
    return f'<div class="crumb">{h}</div>', ld


def article_ld(path, title, desc):
    return {'@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': desc,
            'inLanguage': 'vi', 'mainEntityOfPage': SITE + path, 'image': SITE + '/assets/og.jpg',
            'author': {'@type': 'Person', 'name': 'Cô Ngân – Nari TOPIK', 'url': 'https://hoc.naritopik.com/ve-co/'},
            'publisher': {'@type': 'Organization', 'name': 'Nari TOPIK', 'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/favicon-64.png'}},
            'dateModified': TODAY}


UPSELL = f'''<div class="upsell"><h2>Biết rồi, giờ luyện cho quen tay</h2>
<p>Trang này là phần <b>kiến thức miễn phí</b>. Muốn làm đề có chấm điểm và giải thích từng đáp án sai thì dùng <b>VIP tự học</b>.
Muốn được cô dạy chiến thuật từng dạng và sửa bài viết thì <b>học với cô</b> (đã gồm VIP).</p>
<div class="btns"><a class="btn gold" href="/bang-gia/">Xem 3 cách học</a><a class="btn ghost" href="{ZALO}" rel="nofollow">Nhắn Zalo cô</a></div></div>'''


def toc(body):
    hs = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    if len(hs) < 3:
        return ''
    return '<nav class="toc"><b>Nội dung bài</b><ol>' + ''.join(
        f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in hs) + '</ol></nav>'


def ids_h2(body):
    """Gắn id cho <h2> chưa có id."""
    return re.sub(r'<h2>(.*?)</h2>', lambda m: f'<h2 id="{slug(re.sub("<[^>]+>", "", m.group(1)))[:60]}">{m.group(1)}</h2>', body)


def article(path, title, desc, inner, crumb_items, nav, lead='', h1=None, related=''):
    inner = ids_h2(inner)
    cr, cld = crumbs(crumb_items)
    body = f'''<div class="wrap narrow"><article>{cr}
<h1>{h1 or esc(title)}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}
<div class="meta"><span>✍️ Cô Ngân · Nari TOPIK</span><span>Cập nhật {datetime.date.today().strftime("%d/%m/%Y")}</span></div>
{toc(inner)}{inner}{UPSELL}{related}</article></div>'''
    write(path, layout(path, title, desc, body, nav, [article_ld(path, title, desc), cld], 'article'))


# ---------- bài viết tay ----------
def build_noi_dung():
    d = os.path.join(ROOT, 'noi-dung')
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'):
            continue
        t = open(os.path.join(d, f)).read()
        m = re.match(r'\s*<!--(.*?)-->', t, re.S)
        meta = json.loads(m.group(1))
        inner = t[m.end():]
        if meta.get('type') == 'page':
            write(meta['path'], layout(meta['path'], meta['title'], meta['desc'], inner, meta.get('nav', ''), meta.get('ld')))
        else:
            article(meta['path'], meta['title'], meta['desc'], inner, [tuple(x) for x in meta['crumb']], meta.get('nav', ''),
                    meta.get('lead', ''), meta.get('h1'), meta.get('related', ''))


# ---------- ngữ pháp ----------
def ex_html(w):
    ko = esc(w['ex']).replace('__', '\x00')
    parts = ko.split('\x00')
    ko = ''.join(p if i % 2 == 0 else f'<u>{p}</u>' for i, p in enumerate(parts))
    vi = re.sub(r'\[(.*?)\]', r'<b>\1</b>', esc(w['v']))
    if not w['ex']:
        return ''
    return f'<div class="ex"><span class="ko" lang="ko">{ko}</span>{f"<span class=vi>{vi}</span>" if vi else ""}</div>'


LBL = {'T': 'Thay thế được cho nhau', 'C': 'Thay được có điều kiện', 'L': 'Mỗi mẫu một nghĩa – không thay cho nhau'}
KIND = {'12': ('cau-1-2', 'Ngữ pháp TOPIK II câu 1–2', 'câu 1–2', 'điền ngữ pháp vào chỗ trống'),
        '34': ('cau-3-4', 'Ngữ pháp tương đồng TOPIK II câu 3–4', 'câu 3–4', 'chọn ngữ pháp đồng nghĩa với phần gạch chân')}


def grp_name(g):
    return re.sub(r'^Nhóm \d+ · ', '', g['vi'])


def grp_block(g, h='h2', link=None):
    pats = ''.join(f'''<div class="pat"><h3 lang="ko">{esc(w["p"])}</h3><p class="m">{esc(w["m"])}</p>{ex_html(w)}</div>''' for w in g['w'])
    note = ''
    if g.get('gn'):
        k, t = g['gn']
        note = f'<div class="box info"><span class="lbl {k}">{LBL[k]}</span><p>{esc(t)}</p></div>'
    title = f'<a href="{link}">{esc(grp_name(g))}</a>' if link else esc(grp_name(g))
    if not h:
        return note + pats
    return f'<{h} id="{slug(grp_name(g))}">{title} <span class="ko" style="color:var(--muted);font-weight:400">{esc(g["ko"])}</span></{h}>{note}{pats}'


def build_ngu_phap():
    data = json.load(open(os.path.join(ROOT, 'data/ngu-phap.json')))
    hub_cards = []
    for k, (sl, name, cau, dang) in KIND.items():
        groups = data[k]
        base = f'/ngu-phap-topik/{sl}/'
        npat = sum(len(g['w']) for g in groups)
        # trang từng nhóm
        for i, g in enumerate(groups):
            gp = base + slug(grp_name(g)) + '/'
            title = f'{grp_name(g)}: {" · ".join(w["p"] for w in g["w"][:4])} – {name}'
            desc = f'{len(g["w"])} mẫu ngữ pháp nhóm “{grp_name(g)}” hay ra ở TOPIK II {cau}: nghĩa tiếng Việt, câu ví dụ có dịch, mẫu nào thay được cho nhau.'
            nav_pn = ''
            if i > 0:
                nav_pn += f'<a class="btn" href="{base + slug(grp_name(groups[i-1])) + "/"}">‹ {esc(grp_name(groups[i-1]))}</a>'
            if i < len(groups) - 1:
                nav_pn += f'<a class="btn" href="{base + slug(grp_name(groups[i+1])) + "/"}">{esc(grp_name(groups[i+1]))} ›</a>'
            inner = (f'<p>Đây là nhóm <b>{esc(grp_name(g))}</b> trong bảng {npat} mẫu ngữ pháp TOPIK II {cau} ({dang}). '
                     f'Mỗi mẫu có nghĩa tiếng Việt và một câu ví dụ, chữ tô vàng là phần ngữ pháp.</p>'
                     + grp_block(g, None) + f'<div class="btns" style="justify-content:space-between;margin:24px 0">{nav_pn}</div>'
                     + f'<p><a href="{base}">← Xem cả bảng {npat} mẫu {cau}</a></p>')
            article(gp, title, desc, inner,
                    [('Trang chủ', '/'), ('Ngữ pháp TOPIK', '/ngu-phap-topik/'), (name, base), (grp_name(g), gp)], 'np',
                    h1=f'{esc(grp_name(g))} <span class="ko" style="font-weight:600;color:var(--muted);font-size:.7em">{esc(g["ko"])}</span>')
        # trang tổng của dạng
        lst = ''.join(f'<li><a href="#{slug(grp_name(g))}">{esc(grp_name(g))}</a> <span style="color:var(--muted)">({len(g["w"])} mẫu)</span></li>' for g in groups)
        if k == '12':
            intro = ('<p>Câu 1–2 của đề Đọc TOPIK II cho một câu có chỗ trống ( ), em chọn ngữ pháp đúng trong 4 lựa chọn. '
                     'Mỗi câu 2 điểm, chỉ nên mất khoảng 30 giây. Ngữ pháp hay ra xoay quanh nối câu (thời gian, mục đích, điều kiện, nhượng bộ, lý do) '
                     'và đuôi câu (phỏng đoán, kinh nghiệm, trạng thái).</p>'
                     '<div class="box tip"><p><b>Cách làm nhanh:</b> đọc vế sau trước (thì, kiểu câu, có phủ định không), gọi tên quan hệ giữa hai vế bằng tiếng Việt '
                     '(“để”, “nếu”, “dù”, “vì”…), rồi mới nhìn 4 lựa chọn. Bảng dưới xếp theo đúng các quan hệ đó.</p></div>')
        else:
            intro = ('<p>Câu 3–4 của đề Đọc TOPIK II gạch chân một ngữ pháp, em chọn lựa chọn <b>có nghĩa giống nhất</b>. '
                     'Đề thật hay ra các cặp như <span class="mau">-고자 = -기 위해</span>, <span class="mau">-는 바람에 = -는 탓에</span>, '
                     '<span class="mau">-아/어 봤자 = -아/어도 소용없다</span>. Học theo nhóm đồng nghĩa dưới đây thì gặp mẫu nào cũng nhận ra “anh em” của nó.</p>'
                     '<div class="box tip"><p><b>Mẹo:</b> mỗi nhóm có nhãn cho biết các mẫu <b>thay được cho nhau</b> hay chỉ thay được trong một số trường hợp. '
                     'Đáp án đúng của câu 3–4 luôn nằm trong cùng một nhóm với phần gạch chân.</p></div>')
        inner = (intro + f'<div class="toc"><b>{len(groups)} nhóm · {npat} mẫu</b><ol>{lst}</ol></div>'
                 + ''.join(grp_block(g, 'h2', base + slug(grp_name(g)) + '/') for g in groups))
        desc = f'Bảng {npat} mẫu ngữ pháp TOPIK II {cau} chia {len(groups)} nhóm, có nghĩa tiếng Việt, câu ví dụ có dịch và mẫu nào thay được cho nhau. Miễn phí.'
        article(base, f'{name}: {npat} mẫu theo nhóm (có ví dụ, dịch)', desc, inner,
                [('Trang chủ', '/'), ('Ngữ pháp TOPIK', '/ngu-phap-topik/'), (name, base)], 'np',
                lead=f'{npat} mẫu chia {len(groups)} nhóm theo chức năng, rút từ đề thật và đề luyện TOPIK II.', h1=esc(name))
        hub_cards.append(f'<a class="card" href="{base}"><div class="ic">📘</div><h3>{name}</h3><p>{npat} mẫu · {len(groups)} nhóm · nghĩa tiếng Việt + ví dụ có dịch</p><span class="more">Xem bảng ›</span></a>')
    inner = ('<p>Ngữ pháp chiếm 4 câu đầu đề Đọc (8 điểm) nhưng cũng là nền để đọc hiểu cả bài và viết câu 51–54. '
             'Hai bảng dưới đây gom các mẫu hay ra theo đúng dạng câu hỏi của đề.</p>'
             f'<div class="grid">{"".join(hub_cards)}</div>')
    article('/ngu-phap-topik/', 'Ngữ pháp TOPIK II theo dạng câu', 'Ngữ pháp TOPIK II câu 1–2 và câu 3–4 (tương đồng) xếp theo nhóm, có nghĩa tiếng Việt và câu ví dụ có dịch.',
            inner, [('Trang chủ', '/'), ('Ngữ pháp TOPIK', '/ngu-phap-topik/')], 'np')


def build_sitemap():
    xs = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{m}</lastmod></url>' for p, m in sorted(PAGES))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xs}</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')


if __name__ == '__main__':
    build_noi_dung()
    build_ngu_phap()
    build_sitemap()
    print(len(PAGES), 'trang')
