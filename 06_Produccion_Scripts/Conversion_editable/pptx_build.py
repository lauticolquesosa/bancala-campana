"""presentacion.html -> PPTX 100% nativo (texto, formas, imagenes) para importar en Canva"""
import json, os, sys, copy, urllib.parse, hashlib
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image
from extract import extract, render_bg, browser, HERE
from make import glyph_fallback, blank_lines

PX = 6350  # EMU per css px (1920px = 13.333in)
MET = {'Titan': (0.97, 0.175), 'Brico': (0.93, 0.27)}
FAM = {'Titan': 'Titan One', 'Brico': 'Bricolage Grotesque'}
IMG = HERE + '/pptx_img'; os.makedirs(IMG, exist_ok=True)


def E(v): return Emu(int(round(v * PX)))


def hexc(c): return '%02X%02X%02X' % tuple(int(x) for x in c[:3])


def set_alpha(fill_xml_parent, a):
    """add <a:alpha> to the srgbClr inside a solidFill"""
    for clr in fill_xml_parent.iter(qn('a:srgbClr')):
        for old in clr.findall(qn('a:alpha')): clr.remove(old)
        al = etree.SubElement(clr, qn('a:alpha')); al.set('val', str(int(a * 100000)))


def flatten(items, op=1.0, out=None, gclip=None):
    out = [] if out is None else out
    for it in items:
        if it['k'] == 'g':
            flatten(it['ch'], op * it.get('op', 1), out, it.get('clip') or gclip)
        else:
            it = dict(it); it['_op'] = op
            if gclip and it['k'] == 'img': it['_gclip'] = gclip
            out.append(it)
    return out


def intersect(a, b):
    x0, y0 = max(a['x'], b['x']), max(a['y'], b['y'])
    x1, y1 = min(a['x'] + a['w'], b['x'] + b['w']), min(a['y'] + a['h'], b['y'] + b['h'])
    return dict(x=x0, y=y0, w=max(1, x1 - x0), h=max(1, y1 - y0), rad=b.get('rad') if b.get('rad') else a.get('rad'))


def local(src): return urllib.parse.unquote(src.replace('file:///', ''))


def svg_png(path, w, h):
    out = f"{IMG}/{hashlib.md5((path + str(w)).encode()).hexdigest()[:10]}.png"
    if not os.path.exists(out):
        html = IMG + '/_svg.html'
        open(html, 'w', encoding='utf8').write(f'<body style="margin:0;background:transparent"><img src="file:///{path}" style="width:{w}px;height:{h}px;display:block"></body>')
        pg = browser().new_page(viewport={'width': max(1, int(w + 1)), 'height': max(1, int(h + 1))}, device_scale_factor=4)
        pg.goto('file:///' + html); pg.wait_for_timeout(150)
        pg.screenshot(path=out, omit_background=True, clip={'x': 0, 'y': 0, 'width': w, 'height': h}); pg.close()
    return out


def optimize(path, dw, dh):
    """copy sized to ~2x its on-slide size (keeps quality, keeps the deck light)"""
    im = Image.open(path); W, H = im.size
    k = min(1.0, max(dw * 1.8 / W, dh * 1.8 / H))
    alpha = im.mode in ('RGBA', 'LA', 'P') and (im.mode != 'P' or 'transparency' in im.info)
    key = hashlib.md5((path + '%.3f' % k).encode()).hexdigest()[:10]
    out = f"{IMG}/o_{key}." + ('png' if alpha else 'jpg')
    if not os.path.exists(out):
        if k < 0.98: im = im.resize((max(1, int(W * k)), max(1, int(H * k))), Image.LANCZOS)
        if alpha:
            im = im.convert('RGBA'); im.save(out, optimize=True)
            if os.path.getsize(out) > 150_000:  # illustrations: 256-colour palette with alpha, visually lossless
                im.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(out, optimize=True)
        else: im.convert('RGB').save(out, quality=84, optimize=True, progressive=True)
    return out


def shadow_xml(sp_pr, dx, dy, blur, color, alpha):
    eff = etree.SubElement(sp_pr, qn('a:effectLst'))
    sh = etree.SubElement(eff, qn('a:outerShdw'))
    import math
    dist = math.hypot(dx, dy); ang = (math.degrees(math.atan2(dy, dx)) % 360)
    sh.set('blurRad', str(int(blur * PX))); sh.set('dist', str(int(dist * PX))); sh.set('dir', str(int(ang * 60000))); sh.set('algn', 'ctr'); sh.set('rotWithShape', '0')
    c = etree.SubElement(sh, qn('a:srgbClr')); c.set('val', hexc(color))
    a = etree.SubElement(c, qn('a:alpha')); a.set('val', str(int(alpha * 100000)))


def add_rect(sl, it):
    rad = it.get('rad'); w, h = it['w'], it['h']
    shp_t = MSO_SHAPE.RECTANGLE
    if rad:
        r = rad[0][0]
        if all(abs(c[0] - w / 2) < 0.6 and abs(c[1] - h / 2) < 0.6 for c in rad): shp_t = MSO_SHAPE.OVAL
        else: shp_t = MSO_SHAPE.ROUNDED_RECTANGLE
    sw = it['stroke']['w'] if it.get('stroke') else 0
    x, y = it['x'] + sw / 2, it['y'] + sw / 2; w -= sw; h -= sw
    sp = sl.shapes.add_shape(shp_t, E(x), E(y), E(w), E(h))
    sp.name = it.get('name', 'Forma')
    if shp_t == MSO_SHAPE.ROUNDED_RECTANGLE:
        sp.adjustments[0] = min(0.5, max(0, (rad[0][0] - sw / 2)) / max(1, min(w, h)))
    sp.shadow.inherit = False
    op = it.get('_op', 1)
    if it.get('fill'):
        sp.fill.solid(); sp.fill.fore_color.rgb = RGBColor.from_string(hexc(it['fill']))
        a = it['fill'][3] * op
        if a < 0.999: set_alpha(sp.fill._xPr.find(qn('a:solidFill')), a)
    else:
        sp.fill.background()
    if it.get('stroke') and it['stroke'].get('c'):
        ln = sp.line; ln.color.rgb = RGBColor.from_string(hexc(it['stroke']['c'])); ln.width = E(sw)
        a = it['stroke']['c'][3] * op
        if a < 0.999: set_alpha(sp.line._get_or_add_ln().find(qn('a:solidFill')), a)
        if it['stroke'].get('dash'):
            from pptx.enum.dml import MSO_LINE
            ln.dash_style = MSO_LINE.DASH
    else:
        sp.line.fill.background()
    if sp.has_text_frame: sp.text_frame.text = ''
    return sp


def add_img(sl, it, shadow=None):
    op = it.get('_op', 1)
    if it['k'] == 'img':
        path = local(it['src']); pl = it['place']; clip = it.get('clip')
        if it.get('_gclip'):
            vis = intersect(clip or pl, it['_gclip'])
            if abs(vis['w'] - (clip or pl)['w']) > 1 or abs(vis['h'] - (clip or pl)['h']) > 1: clip = vis
    else:
        path = it['file']; pl = dict(x=it['x'], y=it['y'], w=it['w'], h=it['h']); clip = None
    if path.lower().endswith('.svg'):
        path = svg_png(path, pl['w'], pl['h'])
    else:
        path = optimize(path, pl['w'], pl['h'])
    box = clip or pl
    pic = sl.shapes.add_picture(path, E(box['x']), E(box['y']), E(box['w']), E(box['h']))
    pic.name = it.get('name', 'Imagen')
    if clip:  # non-destructive crop (re-editable in Canva)
        pic.crop_left = (clip['x'] - pl['x']) / pl['w']; pic.crop_top = (clip['y'] - pl['y']) / pl['h']
        pic.crop_right = (pl['x'] + pl['w'] - clip['x'] - clip['w']) / pl['w']; pic.crop_bottom = (pl['y'] + pl['h'] - clip['y'] - clip['h']) / pl['h']
        rad = clip.get('rad')
        if rad and rad[0][0] > 0.5:
            pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
            pg = pic._element.spPr.find(qn('a:prstGeom'))
            av = pg.find(qn('a:avLst'))
            gd = etree.SubElement(av, qn('a:gd')); gd.set('name', 'adj'); gd.set('fmla', 'val %d' % int(min(50000, rad[0][0] / min(clip['w'], clip['h']) * 100000)))
    if op < 0.999:
        blip = pic._element.find('.//' + qn('a:blip'))
        am = etree.SubElement(blip, qn('a:alphaModFix')); am.set('amt', str(int(op * 100000)))
    if shadow:
        shadow_xml(pic._element.spPr, shadow['x'], shadow['y'], shadow['blur'], shadow['fill'], shadow['fill'][3])
    return pic


def add_text(sl, it):
    L = it['lines']
    if not L: return
    st0 = next(l['runs'][0]['st'] for l in L if l['runs'])
    lead = it.get('lead') or it.get('lh') or st0['s'] * 1.2
    asc, desc = MET[st0['f'] if st0['f'] in MET else 'Brico']
    s = st0['s']
    top = L[0]['bl'] - ((lead - (asc + desc) * s) / 2 + asc * s)
    align = it['align']
    xs = [l['x0'] for l in L if l['runs']]; xe = [l['x1'] for l in L if l['runs']]
    if it['wrapped']:
        x = it['box']['x'] if align in ('center', 'right', 'end') else min(xs); w = it['box']['x'] + it['box']['w'] - x
        w *= 1.03
        if align == 'center': x -= it['box']['w'] * 0.015
    else:
        x, w = min(xs), max(xe) - min(xs)
        pad = s * 0.3
        if align == 'center': x -= pad; w += 2 * pad
        elif align in ('right', 'end'): x -= 2 * pad; w += 2 * pad
        else: w += 2 * pad
    h = (L[-1]['bl'] - L[0]['bl']) + lead
    tb = sl.shapes.add_textbox(E(x), E(top), E(w), E(h))
    tf = tb.text_frame; tf.word_wrap = bool(it['wrapped']); tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    # paragraphs: hard breaks between different <br> groups, soft wrap otherwise
    paras = []; cur = None
    for i, l in enumerate(L):
        if cur is None or l['br'] != L[i - 1]['br'] or not it['wrapped']:
            cur = []; paras.append(cur)
        elif cur: cur.append({'t': ' ', 'st': l['runs'][0]['st'] if l['runs'] else st0})
        cur.extend(l['runs'])
    al = {'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT, 'end': PP_ALIGN.RIGHT}.get(align, PP_ALIGN.LEFT)
    op = it.get('_op', 1)
    for pi, runs in enumerate(paras):
        p = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
        p.alignment = al; p.line_spacing = Pt(lead * 0.5); p.space_before = Pt(0); p.space_after = Pt(0)
        if not runs:
            p.font.size = Pt(s * 0.5); continue
        # merge consecutive runs with identical style (bounce letters)
        merged = []
        for r in runs:
            k = json.dumps(r['st'], sort_keys=True)
            if merged and merged[-1][0] == k: merged[-1][1]['t'] += r['t']
            else: merged.append((k, {'t': r['t'], 'st': r['st']}))
        for _, r in merged:
            st = r['st']; rn = p.add_run(); rn.text = r['t']
            f = rn.font; f.size = Pt(st['s'] * 0.5)
            f.name = FAM.get(st['f'], 'Segoe UI Symbol'); f.bold = st['w'] >= 650 and st['f'] == 'Brico'
            f.color.rgb = RGBColor.from_string(hexc(st['c']))
            a = st['c'][3] * op
            rPr = rn._r.get_or_add_rPr()
            if a < 0.999: set_alpha(rPr.find(qn('a:solidFill')), a)
            if st.get('ls'): rPr.set('spc', str(int(st['ls'] * 0.5 * 100)))
            if st.get('sw'):  # outline (Canva: efecto Contorno)
                ln = etree.Element(qn('a:ln')); ln.set('w', str(int(st['sw'] / 2 * PX)))
                sf = etree.SubElement(ln, qn('a:solidFill')); c = etree.SubElement(sf, qn('a:srgbClr')); c.set('val', hexc(st['sc']))
                rPr.insert(0, ln)
            if st.get('ts'):
                t0 = st['ts'][0]
                eff = etree.SubElement(rPr, qn('a:effectLst')); sh = etree.SubElement(eff, qn('a:outerShdw'))
                import math
                sh.set('blurRad', str(int(t0['blur'] * PX))); sh.set('dist', str(int(math.hypot(t0['x'], t0['y']) * PX)))
                sh.set('dir', str(int((math.degrees(math.atan2(t0['y'], t0['x'])) % 360) * 60000))); sh.set('algn', 'ctr'); sh.set('rotWithShape', '0')
                c = etree.SubElement(sh, qn('a:srgbClr')); c.set('val', hexc(t0['c'])); aa = etree.SubElement(c, qn('a:alpha')); aa.set('val', str(int(t0['c'][3] * 100000)))
            # keep rPr child order valid: ln, fill, effectLst, latin...
            order = [qn('a:ln'), qn('a:solidFill'), qn('a:effectLst'), qn('a:latin'), qn('a:ea'), qn('a:cs')]
            kids = sorted(list(rPr), key=lambda e: order.index(e.tag) if e.tag in order else 99)
            for k_ in kids: rPr.remove(k_)
            for k_ in kids: rPr.append(k_)
    tb.name = (''.join(r['t'] for r in L[0]['runs']))[:40] or 'Texto'
    return tb


def build(out):
    d = json.load(open(HERE + '/x_pres2.json', encoding='utf8'))
    ras = {r['id']: r for r in d['raster']}
    prs = Presentation(); prs.slide_width = E(1920); prs.slide_height = E(1080)
    blank = prs.slide_layouts[6]
    for pi, pg in enumerate(d['pages']):
        sl = prs.slides.add_slide(blank)
        items = flatten(pg['items'])
        for t in items:
            if t['k'] == 't': glyph_fallback(t); blank_lines(t)
        i = 0
        while i < len(items):
            it = items[i]
            try:
                if it['k'] == 'r':
                    if it.get('blur'):  # soft shadow: attach to the following picture
                        nxt = next((j for j in range(i + 1, min(i + 4, len(items))) if items[j]['k'] in ('img',)), None)
                        if nxt is not None: items[nxt]['_shadow'] = it
                        i += 1; continue
                    if it.get('grad'):
                        rid = f'g{pi}_{i}'
                        ras[rid] = dict(id=rid, css=dict(backgroundImage=gradcss(it['grad']), backgroundColor='transparent'), w=it['w'], h=it['h'])
                        it = dict(it, k='ras', id=rid, name='Degradé')
                    else:
                        add_rect(sl, it)
                if it['k'] == 'ras':
                    f = f"{IMG}/{it['id']}_{pi}.png"
                    if not os.path.exists(f): render_bg(ras[it['id']], f, scale=1)
                    it['file'] = f; add_img(sl, it)
                elif it['k'] == 'img':
                    add_img(sl, it, it.get('_shadow'))
                elif it['k'] == 't':
                    add_text(sl, it)
            except Exception as e:
                print('slide', pi + 1, it['k'], it.get('name'), e)
            i += 1
    prs.save(out); print('saved', out, os.path.getsize(out) // 1024, 'KB')


def gradcss(g):
    st = ','.join(f"rgba({c['c'][0]},{c['c'][1]},{c['c'][2]},{c['c'][3]}) {c['p']}%" for c in g['stops'])
    return f"linear-gradient({g['angle']}deg,{st})" if g['type'] == 'linear' else f"radial-gradient(closest-side,{st})"


if __name__ == '__main__':
    build(sys.argv[1])
