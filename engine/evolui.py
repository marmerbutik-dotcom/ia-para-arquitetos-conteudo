#!/usr/bin/env python3
"""Reel/story animado de "evolução": a mesma cena passando por etapas (planta → humanizada → obra → render,
planta → estrutura → casa pronta etc.), no estilo dos vídeos de referência que o Marcos aprovou em 08/11/2026.

Cada etapa é uma imagem 9:16 (de preferência gerada no Canva por referência da anterior, para manter a geometria).
As transições são:
  scan     linha de luz de cima para baixo, com grade de prancha
  ergue    linha de luz de baixo para cima (bom para estrutura → casa pronta)
  lateral  linha de luz da esquerda para a direita
  mergulho câmera entra no ponto `foco` [x, y] (0 a 1) da etapa anterior e sai na próxima (planta → interior)
  linhas   as arestas da próxima etapa se desenham sobre a anterior (obra crua → render)
  luz      a anterior (uma planta em papel) acende como prancha luminosa e vira o wireframe da próxima

Uso como módulo:  evolui.render(spec, 'saida.mp4', capa='capa.jpg', som_ofs=0.0)
Uso direto:       python3 engine/evolui.py spec.json saida.mp4
spec = {
  "gancho": ["Da planta ao", "apartamento pronto"],     # 2 linhas; a 2ª sai em itálico bronze
  "rotulo": "DA PLANTA À OBRA",                         # canto superior direito (opcional)
  "etapas": [ {"img": "novas/x/1.jpg", "nome": "PLANTA TÉCNICA"},
              {"img": "novas/x/2.jpg", "nome": "PLANTA HUMANIZADA", "trans": "scan", "prompt": "humanize esta planta..."},
              {"img": "novas/x/3.jpg", "nome": "OBRA CRUA", "trans": "mergulho", "foco": [0.42, 0.52]},
              {"img": "novas/x/4.jpg", "nome": "RENDER FINAL", "trans": "linhas", "prompt": "mesma câmera..."} ],
  "frase": ["O arquiteto decide.", "A IA executa."],   # opcional, sobre a última etapa
  "fim": true,                                          # cartão final com logo e site (reels); false em stories
  "alinha": true                                        # alinha cada etapa à anterior (ECC) quando der certo
}
"""
import cv2, numpy as np, subprocess, sys, os, json, functools
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'assets' / 'img'
FT = ROOT / 'assets' / 'fonts-ttf'
SOM = ROOT / 'assets' / 'media' / 'ia-arq-som.m4a'
LOGO = ROOT / 'assets' / 'img' / 'logo-ia-claro.png'
W, H, FPS = 1080, 1920, 30
OSSO = (250, 247, 242); INK = (31, 29, 26); BRONZE = (168, 129, 79); BZL = (235, 211, 166)
FIM = ('Manual IA para Arquitetos', '7 workflows · 60 prompts · 4 vídeo-aulas', 'iaparaarquitetos.com.br')


def fnt(n, s): return ImageFont.truetype(str(FT / (n + '.ttf')), s)
CORM = lambda s: fnt('cormorant-garamond-latin-600-normal', s)
CORMI = lambda s: fnt('cormorant-garamond-latin-500-italic', s)
MAN = lambda s: fnt('manrope-latin-600-normal', s)
MONO = lambda s: fnt('ibm-plex-mono-latin-500-normal', s)


def clamp(x, a=0., b=1.): return max(a, min(b, x))
def prog(t, t0, t1): return clamp((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t1)
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def ein(x): x = clamp(x); return x ** 3


def carrega(p):
    """lê e enquadra em 1080x1920 (cover)"""
    p = Path(p)
    if not p.is_absolute(): p = IMG / p
    im = cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2RGB)
    h, w = im.shape[:2]; r = max(W / w, H / h)
    im = cv2.resize(im, (round(w * r), round(h * r)), interpolation=cv2.INTER_AREA if r < 1 else cv2.INTER_CUBIC)
    h, w = im.shape[:2]; y, x = (h - H) // 2, (w - W) // 2
    return np.ascontiguousarray(im[y:y + H, x:x + W])


def alinha(src, ref, minimo=0.35):
    """deforma src para casar com ref (mesma câmera); devolve src intacta se não convergir"""
    sc = .25
    def gm(a):
        g = cv2.cvtColor(cv2.resize(a, None, fx=sc, fy=sc), cv2.COLOR_RGB2GRAY).astype(np.float32)
        g = cv2.GaussianBlur(g, (5, 5), 0)
        return cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    Wm = np.eye(3, dtype=np.float32)
    try:
        cc, Wm = cv2.findTransformECC(gm(ref), gm(src), Wm, cv2.MOTION_HOMOGRAPHY,
                                      (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-6), None, 5)
    except cv2.error:
        return src, 0.0
    if cc < minimo: return src, cc
    S = np.diag([sc, sc, 1]).astype(np.float32)
    Hm = np.linalg.inv(S) @ Wm @ S
    # recusa deformações exageradas (escala fora de 0,8–1,25 ou perspectiva forte)
    if not (.8 < Hm[0, 0] < 1.25 and .8 < Hm[1, 1] < 1.25) or abs(Hm[2, 0]) > 4e-4 or abs(Hm[2, 1]) > 4e-4:
        return src, cc
    return cv2.warpPerspective(src, Hm, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT), cc


def kb(img, z, cx=.5, cy=.5):
    h, w = img.shape[:2]
    M = np.float32([[z, 0, W / 2 - z * cx * w], [0, z, H / 2 - z * cy * h]])
    M[0, 2] = min(0, max(W - z * w, M[0, 2])); M[1, 2] = min(0, max(H - z * h, M[1, 2]))
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def mix(a, b, k):
    if k <= 0: return a
    if k >= 1: return b
    return cv2.addWeighted(a, 1 - k, b, k, 0)


YY = np.linspace(0, 1, H, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
XX = np.ones((H, 1), np.float32) * np.linspace(0, 1, W, dtype=np.float32)[None, :]
RUIDO = cv2.resize(np.random.default_rng(3).random((48, 27)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
CAMPO = .75 * YY + .25 * RUIDO
ESCURO = np.full((H, W, 3), (24, 26, 30), np.uint8)


def wipe(a, b, p, eixo='y', inverte=False, cor=BZL):
    G = YY if eixo == 'y' else XX
    if inverte: G = 1 - G
    pos = -0.03 + p * 1.06
    m = np.clip((pos - G) / 0.012, 0, 1)[..., None]
    out = a * (1 - m) + b * m
    if 0 < p < 1:
        d = np.abs(G - pos)
        out += (np.exp(-(d / 0.004) ** 2) + .35 * np.exp(-(d / 0.03) ** 2))[..., None] * np.float32(cor)
    return np.clip(out, 0, 255).astype(np.uint8)


def arestas(img, lo=60, hi=160):
    g = cv2.bilateralFilter(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), 9, 60, 60)
    e = cv2.Canny(g, lo, hi).astype(np.float32) / 255
    return np.minimum(e + cv2.GaussianBlur(e, (0, 0), 7) * 2.2, 1.6)


def tracos(img):
    """traços escuros de uma planta em papel"""
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    e = (cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 18) > 0).astype(np.float32)
    return np.minimum(e + cv2.GaussianBlur(e, (0, 0), 7) * 2.2, 1.6)


def linhas(base, lum, p=1.0, cor=BZL, forca=1.0, escurece=0.0):
    m = 1.0 if p >= 1 else np.clip((p * 1.15 - CAMPO) / 0.08, 0, 1)
    out = base.astype(np.float32) * (1 - escurece) + (lum * m * forca)[..., None] * np.float32(cor)
    return np.clip(out, 0, 255).astype(np.uint8)


def grade(img, k):
    if k <= 0: return img
    out = img.copy(); c = np.float32(BZL) * .18 * k
    out[:, ::54] = out[:, ::54] * (1 - .18 * k) + c
    out[::54, :] = out[::54, :] * (1 - .18 * k) + c
    return out


# ---------------------------------------------------------------- textos (camadas RGBA com faixa de linhas útil)
class Camada:
    def __init__(s):
        s.im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)

    def scrim(s, y0, y1, a0, a1, ex=.55):
        x = np.linspace(0, 1, y1 - y0)
        g = a1 + (a0 - a1) * (1 - x) ** ex if a0 > a1 else a0 + (a1 - a0) * x ** ex
        lay = np.zeros((y1 - y0, W, 4), np.uint8); lay[..., :3] = INK; lay[..., 3] = (g[:, None] * 255).astype(np.uint8)
        s.im.alpha_composite(Image.fromarray(lay), (0, y0))

    def pronta(s):
        a = np.asarray(s.im).astype(np.float32)
        rows = np.where(a[..., 3].max(1) > 0)[0]
        s.y0, s.y1 = (int(rows[0]), int(rows[-1]) + 1) if len(rows) else (0, 0)
        s.al = a[s.y0:s.y1, :, 3:4] / 255; s.cor = a[s.y0:s.y1, :, :3] * s.al
        del s.d; return s


def compoe(f, c, alpha=1.0):
    if c is None or alpha <= 0 or c.y1 <= c.y0: return f
    f = f.copy(); r = f[c.y0:c.y1].astype(np.float32)
    f[c.y0:c.y1] = (r * (1 - c.al * alpha) + c.cor * alpha).astype(np.uint8)
    return f


@functools.lru_cache(None)
def moldura():
    c = Camada(); d = c.d
    d.rectangle([34, 34, W - 35, H - 35], outline=OSSO + (110,), width=2)
    for x, y in [(34, 34), (W - 35, 34), (34, H - 35), (W - 35, H - 35)]:
        d.line([x - 14, y, x + 14, y], fill=OSSO + (200,), width=2); d.line([x, y - 14, x, y + 14], fill=OSSO + (200,), width=2)
    return c.pronta()


@functools.lru_cache(None)
def cabecalho(rotulo):
    c = Camada(); d = c.d
    d.text((72, 236), 'IA PARA ARQUITETOS', font=MONO(26), fill=BZL + (235,))
    if rotulo: d.text((W - 72, 236), rotulo, font=MONO(26), fill=OSSO + (200,), anchor='ra')
    return c.pronta()


@functools.lru_cache(None)
def titulo(l1, l2, grande=True):
    c = Camada(); c.scrim(0, 900, .9, 0); d = c.d
    s1, s2, dy = (104, 112, 112) if grande else (88, 92, 96)
    d.text((72, 300), l1, font=CORM(s1), fill=OSSO + (255,))
    d.text((72, 300 + dy), l2, font=CORMI(s2), fill=BZL + (255,))
    return c.pronta()


def quebra(texto, f, larg):
    out, atual = [], ''
    for w in texto.split(' '):
        t = (atual + ' ' + w).strip()
        if f.getlength(t) <= larg: atual = t
        else: out.append(atual); atual = w
    if atual: out.append(atual)
    return out


@functools.lru_cache(None)
def etiqueta(num, nome, prompt, n):
    c = Camada(); c.scrim(1180, H, 0, .8, 1.0); d = c.d
    y = 1250; fn, fm = MAN(34), MONO(30)
    wn = fm.getlength(num); wo = fn.getlength(nome)
    d.rectangle([72, y, 72 + 40 + wn + 22 + wo + 34, y + 66], fill=INK + (215,), outline=BRONZE + (255,), width=2)
    d.text((94, y + 33), num, font=fm, fill=BZL + (255,), anchor='lm')
    d.text((94 + wn + 22, y + 33), nome, font=fn, fill=OSSO + (255,), anchor='lm')
    if prompt:
        fp = MONO(31); ls = quebra(prompt, fp, 860)[:4]
        y2 = y + 96; hb = 70 + 46 * len(ls)
        d.rectangle([72, y2, W - 72, y2 + hb], fill=INK + (200,)); d.rectangle([72, y2, 78, y2 + hb], fill=BRONZE + (255,))
        d.text((104, y2 + 22), 'PROMPT', font=MONO(22), fill=BZL + (220,))
        resto, yy = n, y2 + 58
        for i, l in enumerate(ls):
            parte = l[:max(0, resto)]
            d.text((104, yy), parte, font=fp, fill=OSSO + (255,))
            if len(parte) < len(l) or i == len(ls) - 1:
                cx = 104 + fp.getlength(parte) + 4
                d.rectangle([cx, yy + 6, cx + 15, yy + 38], fill=BZL + (255,)); break
            resto -= len(l) + 1; yy += 46
    return c.pronta()


@functools.lru_cache(None)
def cartao():
    base = np.full((H, W, 3), INK, np.uint8)
    c = Camada(); d = c.d
    if LOGO.exists():
        lg = Image.open(LOGO).convert('RGBA'); lg = lg.resize((440, int(lg.height * 440 / lg.width)), Image.LANCZOS)
        c.im.alpha_composite(lg, ((W - 440) // 2, 560)); y = 560 + lg.height + 90
    else:
        y = 800
    d.text((W / 2, y), FIM[0], font=CORM(76), fill=OSSO + (255,), anchor='ma')
    d.text((W / 2, y + 100), FIM[1], font=MAN(34), fill=BZL + (255,), anchor='ma')
    d.line([W / 2 - 60, y + 180, W / 2 + 60, y + 180], fill=BRONZE + (255,), width=2)
    d.text((W / 2, y + 214), FIM[2], font=MONO(34), fill=OSSO + (255,), anchor='ma')
    return compoe(base, c.pronta())


# ---------------------------------------------------------------- roteiro
DUR = dict(scan=1.9, ergue=1.9, lateral=1.6, mergulho=1.2, linhas=3.2, luz=3.6)


def zcam(t): return 1.05 + .025 * np.sin(2 * np.pi * t / 9.0)


def monta(spec):
    et = spec['etapas']
    imgs = [carrega(e['img']) for e in et]
    if spec.get('alinha', True):
        for j in range(1, len(imgs)):
            if et[j].get('trans', 'scan') in ('scan', 'ergue', 'lateral', 'linhas', 'luz') and et[j].get('alinha', True):
                imgs[j], cc = alinha(imgs[j], imgs[j - 1])
    lum = {}
    def L(j, tipo):
        k = (j, tipo)
        if k not in lum: lum[k] = tracos(imgs[j]) if tipo == 't' else arestas(imgs[j])
        return lum[k]

    seg = []  # (t0, t1, func(t) -> (frame, [(camada, alpha)]))
    num = lambda j: f'{j + 1:02d}'
    def chip(j, t, t0):
        p = et[j].get('prompt') or None
        n = int(clamp((t - t0 - .35) * 34, 0, len(p))) if p else 0
        return etiqueta(num(j), et[j]['nome'].upper(), p, n)

    T = 0.0
    g1, g2 = spec.get('gancho', ['', ''])
    d0 = 2.6
    def abre(t, t0=T, d0=d0):
        return kb(imgs[0], zcam(t)), [(titulo(g1, g2), ease(prog(t, t0 + .1, t0 + .6)) * (1 - ease(prog(t, t0 + d0 - .4, t0 + d0)))),
                                      (chip(0, t, t0), ease(prog(t, t0 + .3, t0 + .7)))]
    seg.append((T, T + d0, abre)); T += d0

    for j in range(1, len(et)):
        tr = et[j].get('trans', 'scan'); dt = DUR.get(tr, 1.9)
        p_len = len(et[j].get('prompt') or '')
        hold = max(1.3, p_len / 34 + 1.0 - dt)
        a, b = imgs[j - 1], imgs[j]
        t0 = T
        def trans(t, j=j, tr=tr, dt=dt, a=a, b=b, t0=t0):
            u = t - t0; z = zcam(t)
            ch_out = (chip(j - 1, t, t0 - 99), 1 - ease(prog(u, 0, .3)))
            ch_in = (chip(j, t, t0), ease(prog(u, .15, .45)))
            if tr in ('scan', 'ergue', 'lateral'):
                p = ease(prog(u, .1, dt - .1))
                f = wipe(kb(a, z), kb(b, z), p, 'x' if tr == 'lateral' else 'y', tr == 'ergue')
                if tr == 'scan': f = grade(f, .6 * (1 - abs(2 * p - 1)))
                return f, [ch_out, ch_in]
            if tr == 'mergulho':
                fx, fy = et[j].get('foco', [.5, .5]); p = prog(u, 0, dt)
                f = kb(a, z * (1 + 1.6 * ein(p)), fx, fy)
                f = mix(f, kb(b, z * (1 + .3 * (1 - eout(prog(u, dt - .45, dt))))), ease(prog(u, dt - .45, dt)))
                return f, [ch_out, (chip(j, t, t0), ease(prog(u, dt - .3, dt)))]
            if tr == 'linhas':
                lb = kb(L(j, 'a'), z); d1 = dt * .53
                pa = ease(prog(u, .1, d1))
                fa = linhas(kb(a, z), lb, pa, escurece=.35 * pa)
                if u < d1: return fa, [ch_out, ch_in]
                fb = linhas(kb(b, z), lb, 1, forca=.5 * (1 - prog(u, d1, dt + 1)))
                return wipe(fa, fb, ease(prog(u, d1, dt - .05)), 'x'), [ch_in]
            if tr == 'luz':
                planta = lambda zz, k=1.0: linhas(ESCURO, kb(L(j - 1, 't'), zz), 1, forca=k)
                if u < 1.6:
                    return wipe(kb(a, z), grade(planta(z), 1), ease(prog(u, .1, 1.5)), cor=BRONZE), [ch_out, ch_in]
                p = prog(u, 1.6, 2.5)
                fa = grade(planta(z * (1 + .45 * ein(p)), 1 - ease(p)), 1 - ease(prog(u, 1.6, 3.0)))
                zb = z * (.86 + .14 * eout(prog(u, 1.8, dt)))
                lb = kb(L(j, 'a'), zb)
                f = np.maximum(fa, linhas(ESCURO, lb, ease(prog(u, 1.8, 2.8))))
                foto = linhas(kb(b, zb), lb, 1, forca=1 - ease(prog(u, 2.8, dt)))
                return mix(f, foto, ease(prog(u, 2.7, dt))), [ch_in]
            raise ValueError(tr)
        seg.append((T, T + dt, trans)); T += dt
        def fica(t, j=j, b=b, t0=t0):
            z = zcam(t)
            if et[j].get('trans') == 'linhas':
                return linhas(kb(b, z), kb(L(j, 'a'), z), 1, forca=.5 * (1 - prog(t - t0, DUR['linhas'] * .53, DUR['linhas'] + 1))), [(chip(j, t, t0), 1)]
            return kb(b, z), [(chip(j, t, t0), 1)]
        seg.append((T, T + hold, fica)); T += hold

    last = imgs[-1]; nl = len(et) - 1
    if spec.get('frase'):
        l1, l2 = spec['frase']; t0 = T; d = 2.5
        def fr(t, t0=t0):
            u = t - t0
            return kb(last, zcam(t) * (1 + .06 * ease(prog(u, 0, d)))), [(chip(nl, t, -99), 1 - ease(prog(u, 0, .4))),
                                                                         (titulo(l1, l2, False), ease(prog(u, .2, .7)))]
        seg.append((T, T + d, fr)); T += d
    corpo = T
    if spec.get('fim', True):
        t0 = T
        zf = zcam(t0) * (1.06 if spec.get('frase') else 1)
        seg.append((T, T + 2.6, lambda t, t0=t0: (mix(kb(last, zf), cartao(), ease(prog(t, t0, t0 + .5))), []))); T += 2.6
    return T, corpo, seg, imgs


def render(spec, saida, capa=None, som_ofs=0.0, som=True, crf=19):
    T, corpo, seg, imgs = monta(spec)
    rot = spec.get('rotulo', '')
    saida = str(saida); tmp = saida + '.v.mp4'
    pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf), '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    k = 0
    for i in range(int(round(T * FPS))):
        t = i / FPS
        while k < len(seg) - 1 and t >= seg[k][1]: k += 1
        f, cams = seg[k][2](t)
        if t < corpo:
            f = compoe(compoe(f, moldura()), cabecalho(rot))
            for c, a in cams: f = compoe(f, c, a)
        pr.stdin.write(np.ascontiguousarray(f).tobytes())
    pr.stdin.close(); pr.wait()
    if som and SOM.exists():
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-ss', f'{som_ofs:.2f}', '-i', str(SOM), '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-af', f'afade=t=in:d=0.3,afade=t=out:st={max(0, T - 1.2):.2f}:d=1.2',
                        '-t', f'{T:.2f}', '-movflags', '+faststart', saida], check=True)
        os.remove(tmp)
    else:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-c', 'copy', '-movflags', '+faststart', saida], check=True); os.remove(tmp)
    if capa:
        # capa do feed: a última etapa (a mais bonita) com o gancho
        f = kb(imgs[-1], 1.05)
        f = compoe(compoe(compoe(f, moldura()), cabecalho(rot)), titulo(*spec.get('gancho', ['', ''])))
        Image.fromarray(f).save(str(capa), quality=92)
    return T


if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    print(round(render(spec, sys.argv[2], capa=sys.argv[2].replace('.mp4', '-capa.jpg')), 1), 's')
