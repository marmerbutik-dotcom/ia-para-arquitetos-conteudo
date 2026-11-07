#!/usr/bin/env python3
"""Gerador diário do Instagram @ia.para.arquitetos.

Uso:  python3 engine/gera.py pautas/AAAA-MM-DD.json
Lê a pauta do dia (reels, carrosséis, stories, com textos e horários) e gera em saida/AAAA-MM-DD/:
  reel-NN.mp4 + reel-NN-capa.jpg, carrossel-NN-SS.jpg, story-NN.jpg|mp4 e manifesto.json
O manifesto lista cada peça com tipo, arquivos, legenda, alt e horário, pronto para agendar no Metricool.
Identidade: a mesma da LP iaparaarquitetos.com.br (osso, tinta, bronze; Cormorant, Manrope, IBM Plex Mono;
moldura de prancha, cotas e escala gráfica).
"""
import json, os, re, sys, random, shutil, subprocess, html as H
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
A = (ROOT / 'assets' / 'img').as_uri() + '/'
F = (ROOT / 'assets' / 'fonts').as_uri() + '/'
SOM = ROOT / 'assets' / 'media' / 'ia-arq-som.m4a'
FONTS = ''.join(
    f"@font-face{{font-family:'{fam}';src:url({F}{f}) format('woff2');font-weight:{w};font-style:{st}}}"
    for fam, f, w, st in [
        ('Cormorant', 'cormorant-garamond-latin-500-normal.woff2', 500, 'normal'),
        ('Cormorant', 'cormorant-garamond-latin-600-normal.woff2', 600, 'normal'),
        ('Cormorant', 'cormorant-garamond-latin-500-italic.woff2', 500, 'italic'),
        ('Manrope', 'manrope-latin-300-normal.woff2', 300, 'normal'),
        ('Manrope', 'manrope-latin-400-normal.woff2', 400, 'normal'),
        ('Manrope', 'manrope-latin-500-normal.woff2', 500, 'normal'),
        ('Manrope', 'manrope-latin-600-normal.woff2', 600, 'normal'),
        ('Plex', 'ibm-plex-mono-latin-400-normal.woff2', 400, 'normal'),
        ('Plex', 'ibm-plex-mono-latin-500-normal.woff2', 500, 'normal')])
BASE = open(ROOT / 'engine' / 'base.css', encoding='utf-8').read()
EXTRA = """
h1,h2,h3{font-variant-numeric:lining-nums}
.pbox{font-family:var(--tech);font-size:33px;line-height:1.55;padding:34px 38px;border-left:4px solid var(--bz);background:rgba(168,129,79,.09);color:var(--ink)}
.dark .pbox,.gridd .pbox,.on .pbox{background:rgba(235,211,166,.10);color:var(--osso);border-color:var(--bzl)}
.pbox .k{display:block;font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:var(--bz);margin-bottom:14px}
.dark .pbox .k,.gridd .pbox .k,.on .pbox .k{color:var(--bzl)}
.big{font-family:var(--disp);font-weight:500;line-height:.8;font-variant-numeric:lining-nums}
.parts{display:flex;gap:10px}.parts span{flex:1;height:8px;background:currentColor;opacity:.18}.parts span.act{opacity:1}
.body{font-size:36px;line-height:1.45;font-weight:400}
.dark .body,.gridd .body{color:rgba(250,247,242,.84);font-weight:300}
.li{display:grid;grid-template-columns:96px 1fr;gap:18px;align-items:baseline;padding:30px 0;border-top:1.5px solid var(--line)}
.dark .li,.gridd .li{border-color:rgba(235,211,166,.24)}
.li .n{font-family:var(--tech);font-size:26px;color:var(--bz)}.dark .li .n,.gridd .li .n{color:var(--bzl)}
.li .t{font-family:var(--disp);font-size:50px;line-height:1.08}
.li .d{display:block;font-family:var(--tech);font-size:22px;letter-spacing:.04em;margin-top:8px;opacity:.72}
"""
SHEET = '<div class="sheet"><i></i><i></i><i></i><i></i></div>'
SCALE = '<div class="scale"><div class="bar"><span></span><span></span><span></span><span></span></div><div class="lb"><span>0</span><span>1</span><span>2</span><span>5 m</span></div></div>'
PARES = {'w1': ('w1-antes.jpg', 'w1-depois.jpg', 'Modelo · sem textura', 'Render · IA'),
         'w2': ('w2-antes.jpg', 'w2-depois-1.jpg', 'Foto da peça', 'Ambiente · IA'),
         'w3': ('w3-antes.jpg', 'w3-depois.jpg', 'Antes · foto do imóvel', 'Depois · mesma arquitetura')}
FUNDOS = ['v-0.jpg', 'v-1.9.jpg', 'v-3.1.jpg', 'v-4.4.jpg', 'v-5.7.jpg', 'v-7.9.jpg',
          'h-1.4.jpg', 'h-5.8.jpg', 'h-13.2.jpg', 'ia-arq-casa.jpg', 'w2-depois-1.jpg', 'w2-depois-2.jpg', 'w2-depois-3.jpg']


def md(s):
    """*itálico* vira <em> (o destaque bronze da identidade); o resto é escapado."""
    s = H.escape(s or '')
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)


def page(w, h, body, extra=''):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{--w:{w}px;--h:{h}px}}{FONTS}{BASE}{EXTRA}{extra}"
            f"</style></head><body>{body}</body></html>")


def foot(col, left_txt='', right_top='IA para arquitetos', right_bot='iaparaarquitetos.com.br', bottom=66):
    return (f'<div class="foot" style="color:{col};bottom:{bottom}px">{SCALE}<div style="text-align:right;line-height:1.6;font-size:20px">'
            f'<div style="opacity:.6">{H.escape(right_top)}</div><div>{H.escape(right_bot)}</div></div></div>')


def fundo_foto(img, shade='rgba(14,11,9,.72) 0,rgba(14,11,9,.45) 32%,rgba(14,11,9,.12) 52%,rgba(14,11,9,.65) 100%'):
    return f'<img class="bg" src="{A}{img}"><div class="shade" style="background:linear-gradient(180deg,{shade})"></div>'


# ------------------------------------------------------------------ CARROSSEL 1080x1350
def slide(s, n, total, tema):
    W, Hh = 1080, 1350
    t = s.get('tipo', 'texto')
    dark = s.get('escuro', n % 2 == 1)
    cls = 'gridd' if dark else 'grid'
    col = '#fff' if dark else 'var(--ink)'
    acc = 'var(--bzl)' if dark else 'var(--bz)'
    eb = f'<span class="pr tech" style="font-size:22px;color:{acc}">{md(s.get("eb", ""))}</span>' if s.get('eb') else ''
    ft = foot(col, right_top=tema, right_bot=f'Prancha {n:02d} / {total:02d}')
    box = 'position:absolute;left:84px;right:84px;top:116px;bottom:190px;display:flex;flex-direction:column;justify-content:center;gap:34px'
    if t == 'capa':
        img = s.get('img')
        if img:
            body = (f'<div class="cv on">{fundo_foto(img)}{SHEET}<div style="position:absolute;left:84px;right:84px;top:116px;display:flex;flex-direction:column;gap:26px">'
                    f'{eb}<h1 style="font-size:{s.get("fs", 104)}px">{md(s["titulo"])}</h1>'
                    f'<p style="font-size:32px;line-height:1.4;font-weight:400;max-width:860px">{md(s.get("sub", ""))}</p></div>'
                    f'<div class="foot" style="color:#fff">{SCALE}<div class="tech" style="font-size:24px">Salve e arraste →</div></div></div>')
        else:
            par = s.get('par')
            pimg = ''
            if par:
                a, b, la, lb = PARES[par]
                pimg = (f'<div style="display:grid;gap:14px;margin-top:10px"><div class="ba" style="height:270px"><img src="{A}{a}"><span class="tag">{la}</span></div>'
                        f'<div class="ba" style="height:270px"><img src="{A}{b}"><span class="tag">{lb}</span></div></div>')
            body = (f'<div class="cv dark">{SHEET}<div style="{box}">{eb}<h1 style="font-size:{s.get("fs", 108)}px">{md(s["titulo"])}</h1>'
                    f'<p class="body">{md(s.get("sub", ""))}</p>{pimg}</div>'
                    f'<div class="foot" style="color:#fff">{SCALE}<div class="tech" style="font-size:24px">Salve e arraste →</div></div></div>')
        return page(W, Hh, body)
    inner = eb
    if s.get('num'):
        inner += f'<span class="big" style="font-size:240px;color:{acc}">{H.escape(s["num"])}</span>'
    if s.get('titulo'):
        inner += f'<h2 style="font-size:{s.get("fs", 92)}px">{md(s["titulo"])}</h2>'
    if s.get('corpo'):
        inner += f'<p class="body" style="max-width:890px">{md(s["corpo"])}</p>'
    if t == 'lista':
        inner += '<div style="border-bottom:1.5px solid ' + ('rgba(235,211,166,.24)' if dark else 'var(--line)') + '">' + ''.join(
            f'<div class="li"><span class="n">{i:02d}</span><span class="t">{md(it if isinstance(it, str) else it[0])}'
            + (f'<span class="d">{md(it[1])}</span>' if not isinstance(it, str) else '') + '</span></div>'
            for i, it in enumerate(s.get('itens', []), 1)) + '</div>'
    if s.get('prompt'):
        inner += f'<div class="pbox"><span class="k">{md(s.get("rotulo", "No prompt"))}</span>{md(s["prompt"])}</div>'
    if t == 'imagem' and s.get('par'):
        a, b, la, lb = PARES[s['par']]
        inner += (f'<div style="display:grid;gap:14px"><div class="ba" style="height:300px"><img src="{A}{a}"><span class="tag">{la}</span></div>'
                  f'<div class="ba" style="height:300px"><img src="{A}{b}"><span class="tag">{lb}</span></div></div>')
    if t == 'cta':
        inner += ('<div style="display:flex;align-items:flex-end;gap:34px;margin-top:10px"><div class="big" style="font-size:160px">'
                  '<span style="font-size:54px;vertical-align:top;margin-right:6px">R$</span>97</div>'
                  f'<div class="tech" style="font-size:22px;line-height:1.7;padding-bottom:6px;opacity:.85">ou 12x de R$ 10,03<br>garantia de 7 dias</div></div>'
                  f'<p class="tech" style="font-size:28px;color:{acc}">Link na bio · iaparaarquitetos.com.br</p>')
    return page(W, Hh, f'<div class="cv {cls}">{SHEET}<div style="{box}">{inner}</div>{ft}</div>')


# ------------------------------------------------------------------ STORY 1080x1920 (topo e base livres)
def story(s):
    W, Hh = 1080, 1920
    t = s.get('tipo', 'dica')
    box = 'position:absolute;left:84px;right:84px;top:250px;bottom:360px;display:flex;flex-direction:column;justify-content:center;gap:34px'
    eb = f'<span class="pr tech" style="font-size:24px;color:var(--bzl)">{md(s.get("eb", ""))}</span>' if s.get('eb') else ''
    if t in ('pergunta', 'foto', 'link'):
        img = s.get('img') or random.choice(FUNDOS)
        top = (f'<div style="position:absolute;left:84px;right:84px;top:280px;display:flex;flex-direction:column;gap:28px">{eb}'
               f'<h2 style="font-size:{s.get("fs", 104)}px">{md(s["titulo"])}</h2>'
               + (f'<p style="font-size:38px;line-height:1.4;font-weight:400">{md(s["corpo"])}</p>' if s.get('corpo') else '') + '</div>')
        low = ''
        if t == 'link':
            low = ('<div style="position:absolute;left:84px;right:84px;top:1250px;display:flex;align-items:flex-end;gap:30px">'
                   '<div class="big" style="font-size:150px"><span style="font-size:52px;vertical-align:top;margin-right:6px">R$</span>97</div>'
                   f'<div class="tech" style="font-size:24px;line-height:1.7;padding-bottom:6px">{md(s.get("sub", "7 workflows · 60 prompts"))}<br>garantia de 7 dias</div></div>')
        sh = 'rgba(14,11,9,.78) 0,rgba(14,11,9,.42) 34%,rgba(14,11,9,.12) 50%,rgba(14,11,9,.55) 62%,rgba(14,11,9,.9) 100%'
        return page(W, Hh, f'<div class="cv on">{fundo_foto(img, sh)}{SHEET}{top}{low}</div>')
    dark = s.get('escuro', t != 'lista')
    cls = 'gridd' if dark else 'grid'
    if not dark:
        eb = eb.replace('var(--bzl)', 'var(--bz)')
    inner = eb + (f'<h2 style="font-size:{s.get("fs", 100)}px">{md(s["titulo"])}</h2>' if s.get('titulo') else '')
    if s.get('num'):
        inner = eb + f'<span class="big" style="font-size:260px;color:var(--bzl)">{H.escape(s["num"])}</span>' + inner[len(eb):]
    if s.get('corpo'):
        inner += f'<p class="body">{md(s["corpo"])}</p>'
    if s.get('itens'):
        inner += '<div style="border-bottom:1.5px solid ' + ('rgba(235,211,166,.24)' if dark else 'var(--line)') + '">' + ''.join(
            f'<div class="li"><span class="n">{i:02d}</span><span class="t">{md(it if isinstance(it, str) else it[0])}'
            + (f'<span class="d">{md(it[1])}</span>' if not isinstance(it, str) else '') + '</span></div>'
            for i, it in enumerate(s['itens'], 1)) + '</div>'
    if s.get('prompt'):
        inner += f'<div class="pbox"><span class="k">{md(s.get("rotulo", "Copie o prompt"))}</span>{md(s["prompt"])}</div>'
    if t == 'imagem' and s.get('par'):
        a, b, la, lb = PARES[s['par']]
        inner += (f'<div style="display:grid;gap:18px"><div class="ba" style="height:480px"><img src="{A}{a}"><span class="tag">{la}</span></div>'
                  f'<div class="ba" style="height:480px"><img src="{A}{b}"><span class="tag">{lb}</span></div></div>')
    return page(W, Hh, f'<div class="cv {cls}">{SHEET}<div style="{box}">{inner}</div></div>')


# ------------------------------------------------------------------ REEL 1080x1920
def reel_cena(c, i, n):
    """Uma cena do reel: camada de texto (transparente se tiver foto de fundo)."""
    W, Hh = 1080, 1920
    fundo = c.get('fundo')
    pos = c.get('pos', 'meio')
    eb = f'<span class="pr tech" style="font-size:26px;color:var(--bzl)">{md(c.get("eb", ""))}</span>' if c.get('eb') else ''
    inner = eb
    if c.get('num'):
        inner += f'<span class="big" style="font-size:250px;color:var(--bzl)">{H.escape(c["num"])}</span>'
    inner += f'<h2 style="font-size:{c.get("fs", 104)}px">{md(c.get("titulo", ""))}</h2>'
    if c.get('corpo'):
        inner += f'<p style="font-size:40px;line-height:1.4;font-weight:400">{md(c["corpo"])}</p>'
    if c.get('prompt'):
        inner += f'<div class="pbox" style="font-size:34px"><span class="k">{md(c.get("rotulo", "No prompt"))}</span>{md(c["prompt"])}</div>'
    if c.get('itens'):
        inner += '<div style="border-bottom:1.5px solid rgba(235,211,166,.24)">' + ''.join(
            f'<div class="li"><span class="n">{k:02d}</span><span class="t" style="font-size:56px">{md(it)}</span></div>'
            for k, it in enumerate(c['itens'], 1)) + '</div>'
    if c.get('preco'):
        inner += ('<div style="display:flex;align-items:flex-end;gap:30px"><div class="big" style="font-size:150px">'
                  '<span style="font-size:52px;vertical-align:top;margin-right:6px">R$</span>97</div>'
                  '<div class="tech" style="font-size:24px;line-height:1.7;padding-bottom:6px">Link na bio<br>garantia de 7 dias</div></div>')
    tops = {'topo': 'top:250px', 'meio': 'top:250px;bottom:420px;justify-content:center', 'baixo': 'bottom:420px'}
    blk = f'<div style="position:absolute;left:84px;right:150px;{tops.get(pos, tops["meio"])};display:flex;flex-direction:column;gap:30px">{inner}</div>'
    prog = f'<div class="tech" style="position:absolute;right:84px;top:250px;font-size:22px;color:rgba(255,255,255,.7)">{i:02d} / {n:02d}</div>'
    ft = foot('#fff', right_top='IA para arquitetos', right_bot='iaparaarquitetos.com.br', bottom=120)
    if fundo:
        sh = {'meio': 'rgba(14,11,9,.55) 0,rgba(14,11,9,.62) 40%,rgba(14,11,9,.62) 66%,rgba(14,11,9,.7) 100%',
              'topo': 'rgba(14,11,9,.8) 0,rgba(14,11,9,.45) 38%,rgba(14,11,9,0) 56%,rgba(14,11,9,.55) 100%',
              'baixo': 'rgba(14,11,9,.4) 0,rgba(14,11,9,0) 30%,rgba(14,11,9,.55) 55%,rgba(14,11,9,.85) 100%'}[pos if pos in ('meio', 'topo', 'baixo') else 'meio']
        return page(W, Hh, f'<div class="cv on"><div class="shade" style="background:linear-gradient(180deg,{sh})"></div>{SHEET}{blk}{prog}{ft}</div>',
                    'html,body{background:transparent}')
    return page(W, Hh, f'<div class="cv gridd">{SHEET}{blk}{prog}{ft}</div>')


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit('ffmpeg falhou: ' + ' '.join(cmd[:6]) + '\n' + r.stderr[-1500:])


def clip_cena(png, fundo, dur, out, zoom_in=True):
    """Cena em vídeo: foto de fundo com zoom lento + camada de texto, ou só o quadro escuro."""
    fps = 30; n = int(dur * fps)
    if fundo:
        z = "min(1+0.0009*on,1.12)" if zoom_in else "max(1.12-0.0009*on,1)"
        flt = (f"[0:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,setsar=1,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={fps}[bg];"
               f"[bg][1:v]overlay=0:0,format=yuv420p[v]")
        run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(dur), '-i', str(ROOT / 'assets' / 'img' / fundo),
             '-loop', '1', '-t', str(dur), '-i', str(png), '-filter_complex', flt, '-map', '[v]', '-frames:v', str(n),
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-r', str(fps), str(out)])
    else:
        run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', str(fps), '-t', str(dur), '-i', str(png),
             '-vf', 'format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-r', str(fps), str(out)])


def junta(clips, durs, out, som_ofs=0.0, xf=0.35):
    if len(clips) == 1:
        shutil.copy(clips[0], out + '.v.mp4')
    else:
        ins = []; [ins.extend(['-i', str(c)]) for c in clips]
        f = ''; last = '[0:v]'; off = 0.0
        for k in range(1, len(clips)):
            off += durs[k - 1] - xf
            lab = f'[x{k}]'
            f += f'{last}[{k}:v]xfade=transition=fade:duration={xf}:offset={off:.3f}{lab};'
            last = lab
        run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', f.rstrip(';'), '-map', last, '-c:v', 'libx264',
             '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', out + '.v.mp4'])
    tot = sum(durs) - xf * (len(durs) - 1)
    run(['ffmpeg', '-v', 'error', '-y', '-i', out + '.v.mp4', '-ss', f'{som_ofs:.2f}', '-stream_loop', '-1', '-i', str(SOM),
         '-filter_complex', f'[1:a]atrim=0:{tot:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=0.4,afade=t=out:st={max(tot - 1.2, 0):.2f}:d=1.2[a]',
         '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out])
    os.remove(out + '.v.mp4')
    return tot


WIPE_JS = """
(st)=>{const $=id=>document.getElementById(id);
$('box').style.setProperty('--x',st.x+'%'); if($('hd').innerHTML!==st.hd)$('hd').innerHTML=st.hd;
$('eb').textContent=st.eb; $('tg').textContent=st.tag; const o=Math.min(1,st.since/.25);
$('hd').style.opacity=o; $('hd').style.transform=`translateY(${(1-o)*14}px)`; $('pp').style.opacity=st.pp;
$('pt').textContent=st.pt; $('pk').textContent=st.pk; $('ln').style.opacity=(st.x>0.5&&st.x<99.5)?1:0;
[...$('parts').children].forEach((s,i)=>s.classList.toggle('act',i<st.k));}
"""


def reel_wipe(r, pg, tmp, out):
    """Antes/depois que se revela a cada passo, com o texto do prompt sendo digitado."""
    a, b, la, lb = PARES[r.get('par', 'w1')]
    passos = r['passos'][:4]
    n = len(passos)
    html = page(1080, 1920, f'''<div class="cv dark">{SHEET}
<div style="position:absolute;left:84px;right:84px;top:250px;display:flex;flex-direction:column;gap:22px">
 <span id="eb" class="pr tech" style="font-size:24px;color:var(--bzl)"></span>
 <h2 id="hd" style="font-size:96px;min-height:300px"></h2></div>
<div class="ba" id="box" style="position:absolute;left:84px;right:84px;top:700px;height:560px">
 <img src="{A}{a}"><img src="{A}{b}" style="clip-path:inset(0 0 0 var(--x,100%))">
 <span id="ln" style="position:absolute;top:0;bottom:0;left:var(--x,100%);width:3px;margin-left:-1.5px;background:#fff"></span>
 <span class="tag" id="tg"></span></div>
<div id="pp" style="position:absolute;left:84px;right:84px;top:1310px">
 <div class="parts" id="parts" style="color:var(--bzl);width:100%;margin-bottom:28px">{"<span></span>" * n}</div>
 <div class="pbox" style="font-size:32px;min-height:200px"><span class="k" id="pk"></span><span id="pt"></span></div></div>
{foot('#fff', bottom=120)}</div>''')
    p = tmp / 'wipe.html'; p.write_text(html, encoding='utf-8')
    pg.set_viewport_size({'width': 1080, 'height': 1920}); pg.goto(p.as_uri()); pg.evaluate('document.fonts.ready')
    fps, H0, P = 30, 1.8, 2.3
    T = H0 + n * P + 1.6
    ease = lambda t: 0 if t <= 0 else 1 if t >= 1 else (2 * t * t if t < .5 else 1 - (-2 * t + 2) ** 2 / 2)
    fr = tmp / 'wf'; fr.mkdir(exist_ok=True)
    for f in range(int(T * fps)):
        t = f / fps
        if t < H0:
            st = dict(eb=r.get('eb', 'Prompt de render'), hd=md(r['gancho']), since=t, x=100, k=0, pt='', pk='', pp=0, tag=la)
        elif t < H0 + n * P:
            k = int((t - H0) // P) + 1; u = t - H0 - (k - 1) * P
            full = passos[k - 1]['prompt']; m = round(len(full) * min(1, max(0, (u - .15) / 1.15)))
            st = dict(eb=f'Parte {k:02d} de {n:02d}', hd=md(passos[k - 1]['titulo']), since=u,
                      x=100 - (k - 1) * 100 / n - (100 / n) * ease(u / .9), k=k, pt=full[:m] + ('▍' if m < len(full) else ''),
                      pk='No prompt', pp=1, tag=la)
        else:
            u = t - H0 - n * P
            st = dict(eb=r.get('eb_fim', 'Resultado'), hd=md(r.get('final', 'Mesmo projeto. *Outro nível.*')), since=u, x=0, k=n,
                      pt=r.get('resumo', ''), pk='Prompt completo', pp=1, tag=lb)
        pg.evaluate(WIPE_JS, st)
        pg.screenshot(path=str(fr / f'f{f:04d}.jpg'), type='jpeg', quality=90)
    v = tmp / 'wipe.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', str(fr / 'f%04d.jpg'), '-c:v', 'libx264', '-preset', 'veryfast',
         '-crf', '21', '-pix_fmt', 'yuv420p', str(v)])
    shutil.copy(fr / f'f{int(T * fps) - 10:04d}.jpg', tmp / 'capa.jpg')
    shutil.rmtree(fr)
    return [v], [T]


def gera(pauta_path):
    pauta = json.load(open(pauta_path, encoding='utf-8'))
    dia = pauta['data']
    out = ROOT / 'saida' / dia
    shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    tmp = out / '_tmp'; tmp.mkdir()
    random.seed(dia)
    man = []
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()

        def shot(html, path, w, h, transp=False):
            hp = tmp / 'p.html'; hp.write_text(html, encoding='utf-8')
            pg.set_viewport_size({'width': w, 'height': h}); pg.goto(hp.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(80)
            pg.screenshot(path=str(path), omit_background=transp, type='png')

        # carrosséis
        for ci, c in enumerate(pauta.get('carrosseis', []), 1):
            files = []
            tot = len(c['slides'])
            for si, s in enumerate(c['slides'], 1):
                png = tmp / f'c{ci}-{si}.png'
                shot(slide(s, si, tot, c.get('tema', 'IA para arquitetos')), png, 1080, 1350)
                jp = out / f'carrossel-{ci:02d}-{si:02d}.jpg'
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(png), '-q:v', '2', str(jp)], check=True)
                files.append(jp.name)
            man.append(dict(tipo='CARROSSEL', id=f'carrossel-{ci:02d}', arquivos=files, legenda=c['legenda'],
                            alt=c.get('alt', ''), horario=c['horario'], ia=c.get('ia', any(s.get('par') or s.get('img') for s in c['slides']))))
        # stories
        for si, s in enumerate(pauta.get('stories', []), 1):
            png = tmp / f's{si}.png'
            shot(story(s), png, 1080, 1920)
            jp = out / f'story-{si:02d}.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(png), '-q:v', '2', str(jp)], check=True)
            man.append(dict(tipo='STORY', id=f'story-{si:02d}', arquivos=[jp.name], horario=s['horario'], link=s.get('link', ''),
                            nota=s.get('nota', ''), ia=bool(s.get('par'))))
        # reels
        for ri, r in enumerate(pauta.get('reels', []), 1):
            rt = tmp / f'r{ri}'; rt.mkdir()
            if r.get('tipo') == 'wipe':
                clips, durs = reel_wipe(r, pg, rt, out)
                fim = r.get('fim')
                if fim:
                    png = rt / 'fim.png'; shot(reel_cena(dict(fim, fundo=None), len(r['passos']) + 1, len(r['passos']) + 1), png, 1080, 1920)
                    clip_cena(png, None, 2.6, rt / 'fim.mp4'); clips.append(rt / 'fim.mp4'); durs.append(2.6)
                capa = rt / 'capa.jpg'
            else:
                cenas = r['cenas']
                clips, durs = [], []
                for k, c in enumerate(cenas, 1):
                    fundo = c.get('fundo')
                    if fundo == 'auto':
                        fundo = FUNDOS[(ri * 3 + k) % len(FUNDOS)]
                    c = dict(c, fundo=fundo)
                    png = rt / f'c{k}.png'; shot(reel_cena(c, k, len(cenas)), png, 1080, 1920, transp=bool(fundo))
                    d = float(c.get('dur', 2.8)); cl = rt / f'c{k}.mp4'
                    clip_cena(png, fundo, d, cl, zoom_in=k % 2 == 1); clips.append(cl); durs.append(d)
                capa = rt / 'capa.png'
                run(['ffmpeg', '-v', 'error', '-y', '-ss', '0.6', '-i', str(clips[0]), '-frames:v', '1', str(capa)])
            mp4 = out / f'reel-{ri:02d}.mp4'
            tot = junta(clips, durs, str(mp4), som_ofs=(ri * 5.3) % 20)
            cj = out / f'reel-{ri:02d}-capa.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(capa), '-q:v', '2', str(cj)], check=True)
            man.append(dict(tipo='REEL', id=f'reel-{ri:02d}', arquivos=[mp4.name], capa=cj.name, duracao=round(tot, 1),
                            legenda=r['legenda'], alt=r.get('alt', ''), horario=r['horario'], ia=r.get('ia', r.get('tipo') == 'wipe')))
        br.close()
    shutil.rmtree(tmp)
    man.sort(key=lambda m: m['horario'])
    json.dump(dict(data=dia, pecas=man), open(out / 'manifesto.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{dia}: {len(man)} peças em {out}')


if __name__ == '__main__':
    gera(sys.argv[1])
