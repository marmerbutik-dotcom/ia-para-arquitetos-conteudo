#!/usr/bin/env python3
"""6 modelos de reel do @ia.para.arquitetos tirados dos vídeos de referência que o Marcos mandou em 14/11/2026
(pasta Videos\\Conteudos\\IA para Arquitetos). Regra fixa: texto sem sombra e sem degradê escuro atrás.

  m1 prancheta  planta na prancheta → linhas de luz → maquete → estrutura na cidade → prédio pronto   (ref. morph0200)
  m2 cozinha    obra crua → piso escorre → marcenaria nasce do centro → luzes acendem              (ref. render3d.fabiogarcia)
  m3 wireframe  obra crua → o desenho branco do projeto se traça → materiais descem → luz          (ref. andre.design06)
  m4 fachada    tijolo → reboco → pintura e esquadrias → paisagismo e luz                          (ref. luck_lucky934)
  m5 estrutura  planta → pilares sobem → estrutura → setas do caminho da carga                     (ref. mpmcivilacademy)
  m6 tutorial   papel quadriculado, passo a passo numerado do prompt em 4 partes                    (ref. ohneis652)

Uso: python3 engine/modelos6.py <pasta-imagens> <pasta-saida> [m1 m2 ...]
"""
import sys, subprocess, functools
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evolui as ev
from evolui import (W, H, FPS, OSSO, INK, BRONZE, BZL, CORM, CORMI, MAN, MONO, carrega, kb, mix, wipe, arestas,
                    linhas, Camada, compoe, cartao, alinha, prog, ease, eout, ein, clamp, quebra, YY, XX, RUIDO)

CIANO = (96, 218, 236)
CORMB = lambda s: ev.fnt('cormorant-garamond-latin-700-normal', s)
CORMBI = lambda s: ev.fnt('cormorant-garamond-latin-600-italic', s)
PAPEL = (238, 233, 224)
SOM = ev.SOM
FIMD = 1.7


# ---------------------------------------------------------------- utilidades
def lum(img, box):
    x0, y0, x1, y1 = [int(v) for v in box]
    r = img[max(0, y0):y1, max(0, x0):x1].astype(np.float32)
    return float((r[..., 0] * .299 + r[..., 1] * .587 + r[..., 2] * .114).mean()) if r.size else 0


def cor_para(img, box, claro=OSSO, escuro=INK, lim=150):
    return escuro if lum(img, box) > lim else claro


def camada(itens):
    """itens: (texto, fonte, cor, (x, y), anchor)  ->  camada RGBA pronta (só texto, sem fundo)"""
    c = Camada(); d = c.d
    for t, f, cor, xy, an in itens:
        d.text(xy, t, font=f, fill=tuple(cor) + (255,), anchor=an)
    return c.pronta()


@functools.lru_cache(None)
def cab(cor):
    return camada([('IA PARA ARQUITETOS', MONO(26), cor, (72, 248), 'la')])


@functools.lru_cache(None)
def gancho(l1, l2, cor1, cor2, y=300, s=(96, 104)):
    return camada([(l1, CORMB(s[0]), cor1, (72, y), 'la'), (l2, CORMBI(s[1]), cor2, (72, y + s[0] + 6), 'la')])


BRZ_D = (120, 86, 44)


def frase(img, l1, l2, y=300, s=(96, 104)):
    """duas linhas; a cor de cada linha sai do fundo que fica atrás dela (sem sombra)"""
    w1 = CORMB(s[0]).getlength(l1); w2 = CORMBI(s[1]).getlength(l2)
    c1 = cor_para(img, (72, y + 10, 72 + w1, y + s[0]), lim=125)
    l = lum(img, (72, y + s[0] + 16, 72 + w2, y + s[0] + 6 + s[1]))
    c2 = BRZ_D if l > 125 else BZL
    return gancho(l1, l2, c1, c2, y, s)


@functools.lru_cache(None)
def etapa(num, nome, cor, y=1330):
    f1, f2 = MONO(28), MAN(36)
    return camada([(num, f1, cor, (72, y), 'lm'), (nome, f2, cor, (72 + f1.getlength(num) + 22, y), 'lm')])


def brilho(img, k, cor=(255, 214, 160), lim=200):
    if k <= 0: return img
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    b = np.clip(g - lim, 0, None) / (255 - lim)
    b = cv2.GaussianBlur(b, (0, 0), 28) * 1.6 + cv2.GaussianBlur(b, (0, 0), 6) * .6
    out = img.astype(np.float32) + (b * k * 90)[..., None] * (np.float32(cor) / 255)
    return np.clip(out, 0, 255).astype(np.uint8)


def mancha(p, centro=(.5, .65), ruido=.22, borda=.035, campo=None):
    """máscara orgânica que cresce a partir de um ponto (0..1)"""
    if campo is None:
        d = np.sqrt(((XX - centro[0]) * W / H) ** 2 + (YY - centro[1]) ** 2)
        campo = d / d.max() * (1 - ruido) + RUIDO * ruido
    return np.clip((p * 1.08 - campo) / borda, 0, 1)


def aplica(a, b, m, aro=None):
    m3 = m[..., None]
    out = a.astype(np.float32) * (1 - m3) + b.astype(np.float32) * m3
    if aro is not None:
        rim = (m > .02) & (m < .98)
        out[rim] += np.float32(aro) * .55
    return np.clip(out, 0, 255).astype(np.uint8)


def push(img, t, d, z0=1.0, z1=1.06, cx=.5, cy=.5):
    return kb(img, z0 + (z1 - z0) * ease(t / d), cx, cy)


def ler(pasta, nome, ref=None):
    im = carrega(Path(pasta) / (nome + '.jpg'))
    if ref is not None:
        im2, cc = alinha(im, ref)
        print(f'   alinha {nome}: {cc:.2f}', flush=True)
        im = im2
    return im


# ---------------------------------------------------------------- saída
def grava(frame, dur, saida, som_ofs=0.0):
    saida = Path(saida); saida.parent.mkdir(parents=True, exist_ok=True)
    tmp = saida.with_suffix('.v.mp4')
    n = int(round(dur * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', str(tmp)], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(np.ascontiguousarray(frame(i / FPS)).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp), '-ss', f'{som_ofs:.2f}', '-i', str(SOM),
                    '-filter_complex', f'[1:a]atrim=0:{dur:.2f},afade=t=in:d=0.4,afade=t=out:st={dur - 1.2:.2f}:d=1.2[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', str(saida)], check=True)
    tmp.unlink()
    # capa
    Image.fromarray(frame(min(dur - FIMD - .5, dur * .62))).save(saida.with_name(saida.stem + '-capa.jpg'), quality=92)


def com_fim(frame, d):
    card = cartao()
    def f(t):
        if t < d: return frame(t)
        return mix(frame(d - 1 / FPS), card, ease(prog(t, d, d + .45)))
    return f, d + FIMD


# ---------------------------------------------------------------- m1 · da prancheta ao prédio
def m1(P):
    a, b, c, e = (ler(P, 'o1-1-prancheta'), ler(P, 'o1-2-maquete'), ler(P, 'o1-3-estrutura'), ler(P, 'o1-4-predio'))
    b, _ = alinha(b, a)
    lb = arestas(b, 50, 140)
    D = 12.6
    cg = cor_para(a, (60, 236, 500, 276))
    g = frase(kb(a, 1.03, .5, .55), 'Da prancheta', 'ao prédio pronto.', y=236, s=(86, 92))
    E = [etapa('01', 'PLANTA E ELEVAÇÃO', cor_para(a, (60, 1290, 700, 1370))),
         etapa('02', 'ESTRUTURA NA MAQUETE', cor_para(b, (60, 1290, 700, 1370))),
         etapa('03', 'ESTRUTURA NA OBRA', cor_para(c, (60, 1290, 700, 1370))),
         etapa('04', 'PRÉDIO PRONTO', cor_para(e, (60, 1290, 700, 1370)))]
    fr = frase(kb(e, 1.01, .5, .4), 'Mesma geometria,', 'do papel à cidade.')

    def frame(t):
        if t < 3.4:
            base = push(a, t, 3.4, 1.0, 1.07, .5, .55)
            bb = push(b, t, 3.4, 1.0, 1.07, .5, .55)
            lbz = cv2.resize(arestas(bb, 50, 140), (W, H)) if t >= 1.0 else None
            if t < 1.0: f = base
            elif t < 2.6: f = linhas(base, lbz, ease(prog(t, 1.0, 2.4)), CIANO, .9)
            else:
                k = ease(prog(t, 2.6, 3.4))
                f = mix(linhas(base, lbz, 1, CIANO, .9), linhas(bb, lbz, 1, CIANO, .9 * (1 - k)), k)
            st = 0 if t < 2.6 else 1
        elif t < 5.4:
            z = 1.07 + .35 * ein(prog(t, 3.4, 5.4))
            f = kb(b, z, .5, .42)
            if t > 4.8:
                f = mix(f, kb(c, 1.18 - .12 * ease(prog(t, 4.8, 5.4)), .5, .4), ease(prog(t, 4.8, 5.4)))
            st = 1 if t < 5.0 else 2
        elif t < 7.4:
            f = push(c, t - 5.4, 2.0, 1.06, 1.03, .5, .4); st = 2
        elif t < 8.8:
            cc = push(c, 2.0, 2.0, 1.06, 1.03, .5, .4)
            f = wipe(cc, kb(e, 1.03, .5, .4), ease(prog(t, 7.4, 8.8)), 'y', inverte=True, cor=CIANO); st = 3 if t > 8.1 else 2
        else:
            f = push(e, t - 8.8, D - 8.8, 1.03, 1.0, .5, .4); st = 3
        f = compoe(f, cab(cor_para(f, (60, 230, 600, 270))), ease(prog(t, 2.7, 3.1)))
        f = compoe(f, g, ease(prog(t, .15, .6)) * (1 - ease(prog(t, 2.3, 2.7))))
        f = compoe(f, E[st], ease(prog(t, .9, 1.3)) if st == 0 else 1)
        f = compoe(f, fr, ease(prog(t, 9.4, 10.0)))
        return f
    return com_fim(frame, D)


# ---------------------------------------------------------------- m2 · cozinha (obra → pronta → luz)
def m2(P):
    d_ = ler(P, 'o2-3-dia')
    a, b, n = ler(P, 'o2-1-obra', d_), ler(P, 'o2-2-vazia', d_), ler(P, 'o2-4-noite', d_)
    D = 11.8
    piso = np.clip((YY - .55) / .45, 0, 1); campo_piso = (1 - piso) * .85 + RUIDO * .1 + (XX * .12)
    campo_piso = (campo_piso - campo_piso.min()) / (campo_piso.max() - campo_piso.min())
    g = frase(a, 'Da obra crua', 'à cozinha pronta.')
    nomes = [('01', 'OBRA CRUA', a), ('02', 'PISO E PAREDES', b), ('03', 'MARCENARIA E PEDRA', d_), ('04', 'LUZ', n)]
    E = [etapa(k, nm, cor_para(im, (60, 1290, 700, 1370))) for k, nm, im in nomes]
    fr = frase(kb(n, 1.05, .5, .55), 'Mesma câmera.', 'Outra hora do dia.')

    def frame(t):
        z = 1.0 + .05 * ease(t / D)
        A, B, C, N = (kb(x, z, .5, .55) for x in (a, b, d_, n))
        if t < 1.3: f, st = A, 0
        elif t < 3.1: f, st = aplica(A, B, mancha(ease(prog(t, 1.3, 3.1)), campo=campo_piso, borda=.03), aro=(255, 255, 255)), 1 if t > 2.0 else 0
        elif t < 3.7: f, st = B, 1
        elif t < 5.7: f, st = aplica(B, C, mancha(ease(prog(t, 3.7, 5.7)), centro=(.45, .62), ruido=.07, borda=.06)), 2 if t > 4.4 else 1
        elif t < 7.3: f, st = C, 2
        elif t < 8.6:
            k = ease(prog(t, 7.3, 8.6)); f, st = brilho(mix(C, N, k), k * 1.2), 3
        else: f, st = brilho(N, 1.2 - .4 * ease(prog(t, 8.6, 9.6))), 3
        f = compoe(f, cab(cor_para(f, (60, 230, 600, 270))), 1)
        f = compoe(f, g, ease(prog(t, .15, .6)) * (1 - ease(prog(t, 2.9, 3.3))))
        f = compoe(f, E[st], 1)
        f = compoe(f, fr, ease(prog(t, 9.0, 9.6)))
        return f
    return com_fim(frame, D)


# ---------------------------------------------------------------- m3 · wireframe (obra → desenho → materiais → luz)
def m3(P):
    b = ler(P, 'o3-2-final'); a = ler(P, 'o3-1-obra', b)
    lb = arestas(b, 25, 80)
    D = 12.4
    g = frase(a, 'A obra crua', 'vira projeto.', y=1010)
    E = [etapa('01', 'OBRA CRUA', cor_para(a, (60, 1290, 700, 1370))),
         etapa('02', 'O DESENHO DO PROJETO', cor_para(a, (60, 1290, 700, 1370))),
         etapa('03', 'MATERIAIS', cor_para(b, (60, 1290, 700, 1370))),
         etapa('04', 'LUZ', cor_para(b, (60, 1290, 700, 1370)))]
    fr = frase(kb(b, 1.06, .5, .55), 'A arquitetura fica.', 'O resto a IA veste.')
    desce = YY * .93 + RUIDO * .07

    def frame(t):
        z = 1.0 + .06 * ease(t / D)
        A, B = kb(a, z, .5, .55), kb(b, z, .5, .55)
        L = kb(lb.astype(np.float32), z, .5, .55)
        if t < 1.4: f, st = A, 0
        elif t < 4.6: f, st = linhas(A, L, ease(prog(t, 1.4, 4.4)), (255, 255, 255), 1.0, .35 * ease(prog(t, 1.4, 2.2))), 1
        elif t < 7.6:
            k = ease(prog(t, 4.6, 7.4))
            m = np.clip((k * 1.1 - desce) / .06, 0, 1)
            base = linhas(A, L, 1, (255, 255, 255), 1.0, .35)
            f = aplica(base, linhas(B, L, 1, (255, 255, 255), .5 * (1 - k)), m); st = 2
        elif t < 9.0: f, st = brilho(B, 1.3 * ease(prog(t, 7.6, 8.6))), 3
        else: f, st = brilho(B, 1.3 - .5 * ease(prog(t, 9.0, 10.0))), 3
        f = compoe(f, cab(cor_para(f, (60, 230, 600, 270))), 1)
        f = compoe(f, g, ease(prog(t, .15, .6)) * (1 - ease(prog(t, 1.5, 1.9))))
        f = compoe(f, E[st], 1)
        f = compoe(f, fr, ease(prog(t, 9.4, 10.0)))
        return f
    return com_fim(frame, D)


# ---------------------------------------------------------------- m4 · fachada em etapas
def m4(P):
    e = ler(P, 'o4-4-final')
    a, b, c = ler(P, 'o4-1-tijolo', e), ler(P, 'o4-2-reboco', e), ler(P, 'o4-3-pintura', e)
    D = 12.2
    g = frase(a, 'Do tijolo', 'à fachada acesa.')
    nomes = [('01', 'TIJOLO', a), ('02', 'REBOCO', b), ('03', 'PINTURA E ESQUADRIAS', c), ('04', 'PAISAGISMO E LUZ', e)]
    E = [etapa(k, nm, cor_para(im, (60, 1290, 700, 1370))) for k, nm, im in nomes]
    fr = frase(kb(e, 1.06, .5, .5), 'Uma fachada,', 'quatro etapas.')

    def frame(t):
        z = 1.0 + .07 * ease(t / D)
        A, B, C, Ee = (kb(x, z, .5, .5) for x in (a, b, c, e))
        if t < 1.4: f, st = A, 0
        elif t < 2.8: f, st = wipe(A, B, ease(prog(t, 1.4, 2.8)), 'x'), 1 if t > 2.1 else 0
        elif t < 3.8: f, st = B, 1
        elif t < 5.2: f, st = wipe(B, C, ease(prog(t, 3.8, 5.2)), 'y'), 2 if t > 4.5 else 1
        elif t < 6.4: f, st = C, 2
        elif t < 8.2:
            k = ease(prog(t, 6.4, 8.2)); f, st = brilho(mix(C, Ee, k), k), 3
        else: f, st = brilho(Ee, 1 - .3 * ease(prog(t, 8.2, 9.2))), 3
        f = compoe(f, cab(cor_para(f, (60, 230, 600, 270))), 1)
        f = compoe(f, g, ease(prog(t, .15, .6)) * (1 - ease(prog(t, 2.6, 3.0))))
        f = compoe(f, E[st], 1)
        f = compoe(f, fr, ease(prog(t, 9.0, 9.6)))
        return f
    return com_fim(frame, D)


# ---------------------------------------------------------------- m5 · estrutura explicada
def seta(d, p0, p1, cor, w=10, cab_=26):
    x0, y0 = p0; x1, y1 = p1
    d.line([p0, p1], fill=cor, width=w)
    ang = np.arctan2(y1 - y0, x1 - x0)
    pts = [(x1 + cab_ * np.cos(ang), y1 + cab_ * np.sin(ang)),
           (x1 + cab_ * np.cos(ang + 2.5), y1 + cab_ * np.sin(ang + 2.5)),
           (x1 + cab_ * np.cos(ang - 2.5), y1 + cab_ * np.sin(ang - 2.5))]
    d.polygon(pts, fill=cor)


def setas_lay(grupo, k):
    """grupo de setas com animação k (0..1): o traço avança ao longo de cada seta"""
    c = Camada(); d = c.d
    for p0, p1 in grupo:
        x = p0[0] + (p1[0] - p0[0]) * k; y = p0[1] + (p1[1] - p0[1]) * k
        if k > .02: seta(d, p0, (x, y), CIANO + (240,))
    return c.pronta()


def m5(P):
    c = ler(P, 'o5-3-estrutura')
    a, b = ler(P, 'o5-1-planta', c), ler(P, 'o5-2-pilares', c)
    D = 14.6
    g = gancho('Como a carga', 'chega ao chão.', INK, BRONZE)
    E = [etapa('01', 'PLANTA', INK), etapa('02', 'PILARES', INK), etapa('03', 'VIGAS E LAJES', INK)]
    # caminho da carga (coordenadas na imagem 1080x1920 da estrutura)
    G = [('LAJE', 'recebe o peso do piso', [((600, 560), (470, 610)), ((600, 560), (760, 545)), ((600, 560), (610, 640))]),
         ('VIGA', 'leva a carga até o pilar', [((360, 660), (640, 655)), ((960, 620), (735, 640))]),
         ('PILAR', 'desce a carga', [((680, 700), (680, 1180))]),
         ('FUNDAÇÃO', 'entrega ao solo', [((680, 1290), (600, 1340)), ((680, 1290), (760, 1340)), ((680, 1290), (680, 1360))])]
    T0 = 6.4; DS = 1.7
    rot = [camada([(f'{i + 1:02d}  {nm}', MAN(44), INK, (72, 238), 'la'), (tx, CORMBI(60), BRZ_D, (72, 296), 'la')])
           for i, (nm, tx, _) in enumerate(G)]

    def frame(t):
        z = 1.0 + .04 * ease(t / D)
        A, B, C = (kb(x, z, .5, .5) for x in (a, b, c))
        if t < 1.4: f, st = A, 0
        elif t < 3.2: f, st = wipe(A, B, ease(prog(t, 1.4, 3.2)), 'y', inverte=True, cor=CIANO), 1 if t > 2.2 else 0
        elif t < 4.0: f, st = B, 1
        elif t < 5.8: f, st = wipe(B, C, ease(prog(t, 4.0, 5.8)), 'y', inverte=True, cor=CIANO), 2 if t > 4.9 else 1
        else: f, st = C, 2
        f = compoe(f, cab(INK), 1 - ease(prog(t, T0 - .5, T0 - .1)))
        f = compoe(f, g, ease(prog(t, .15, .6)) * (1 - ease(prog(t, T0 - .5, T0 - .1))))
        if t < T0: f = compoe(f, E[st], 1)
        for i, (_, _, gr) in enumerate(G):
            t0 = T0 + i * DS
            if t >= t0:
                k = eout(prog(t, t0, t0 + .8))
                M = np.float32([[z, 0, W / 2 - z * W / 2], [0, z, H / 2 - z * H / 2]])
                lay = setas_lay(tuple(tuple(map(tuple, s)) for s in gr), k)
                # setas acompanham o zoom
                full = np.zeros((H, W, 4), np.float32); full[lay.y0:lay.y1, :, 3:4] = lay.al; full[lay.y0:lay.y1, :, :3] = lay.cor
                full = cv2.warpAffine(full, M, (W, H))
                al = full[..., 3:4]; f = (f * (1 - al) + full[..., :3]).astype(np.uint8)
            if t0 <= t < t0 + DS or (i == len(G) - 1 and t >= t0):
                f = compoe(f, rot[i], ease(prog(t, t0, t0 + .3)) * (1 if i == len(G) - 1 else 1 - ease(prog(t, t0 + DS - .25, t0 + DS))))
        return f
    return com_fim(frame, D)


# ---------------------------------------------------------------- m6 · tutorial no papel quadriculado
@functools.lru_cache(None)
def papel():
    im = np.full((H, W, 3), PAPEL, np.uint8)
    for x in range(0, W, 54): im[:, x] = (226, 220, 210)
    for y in range(0, H, 54): im[y, :] = (226, 220, 210)
    return im


def cartao_img(img, w, x, y, raio=22):
    """foto recortada com cantos arredondados, sem sombra"""
    h = int(w * img.shape[0] / img.shape[1])
    ph = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], raio, fill=255)
    return ph, np.asarray(m, np.float32)[..., None] / 255, (x, y)


def cola(f, ph, m, xy, a=1.0):
    x, y = xy; h, w = ph.shape[:2]
    y0, y1 = max(0, y), min(H, y + h); x0, x1 = max(0, x), min(W, x + w)
    if y1 <= y0 or x1 <= x0: return f
    r = f[y0:y1, x0:x1].astype(np.float32); mm = m[y0 - y:y1 - y, x0 - x:x1 - x] * a
    f[y0:y1, x0:x1] = (r * (1 - mm) + ph[y0 - y:y1 - y, x0 - x:x1 - x] * mm).astype(np.uint8)
    return f


def recorte(img, cx, cy, w, h):
    return img[cy:cy + h, cx:cx + w]


@functools.lru_cache(None)
def passo_lay(n, nome):
    c = Camada(); d = c.d
    d.ellipse([72, 300, 126, 354], outline=INK + (255,), width=3)
    d.text((99, 327), n, font=MAN(30), fill=INK + (255,), anchor='mm')
    d.text((150, 327), nome, font=MAN(36), fill=INK + (255,), anchor='lm')
    d.line([(72 + 520, 327), (W - 230, 327)], fill=INK + (255,), width=2)
    d.polygon([(W - 230, 317), (W - 212, 327), (W - 230, 337)], fill=INK + (255,))
    return c.pronta()


def texto_lay(l1, l2, y=392, s=60):
    return camada([(l1, CORM(s), INK, (72, y), 'la'), (l2, CORMI(s + 6), BRONZE, (72, y + s + 8), 'la')])


def digita(txt, n, y=1260, larg=760):
    c = Camada(); d = c.d; fp = MONO(30); ls = quebra(txt, fp, larg)
    d.text((72, y - 46), 'PROMPT', font=MONO(22), fill=BRONZE + (255,))
    resto, yy = n, y
    for l in ls:
        parte = l[:max(0, resto)]
        d.text((72, yy), parte, font=fp, fill=INK + (255,))
        if len(parte) < len(l):
            cx = 72 + fp.getlength(parte) + 4; d.rectangle([cx, yy + 4, cx + 14, yy + 34], fill=INK + (255,)); break
        resto -= len(l) + 1; yy += 44
    return c.pronta()


def m6(P):
    ob, dia, noite = ler(P, 'o2-1-obra'), ler(P, 'o2-3-dia'), ler(P, 'o2-4-noite')
    ob, _ = alinha(ob, dia)
    CW, CX, CY = 760, 72, 540
    CH = int(CW * 0.62)
    def janela(img, cy=.5):
        h = int(img.shape[1] * CH / CW); y0 = int((img.shape[0] - h) * cy)
        return img[y0:y0 + h]
    jo, jd, jn = janela(ob, .45), janela(dia, .45), janela(noite, .45)
    card = lambda im: cartao_img(im, CW, CX, CY)
    Co, Cd, Cn = card(jo), card(jd), card(jn)
    hh, ww = Co[0].shape[:2]
    lo6 = np.clip(arestas(Cd[0], 70, 170), 0, 1)
    campo6 = cv2.resize(ev.CAMPO, (ww, hh))
    PRT = ['Mantenha exatamente a geometria, as aberturas e o enquadramento da imagem.',
           'Luz natural do fim da tarde entrando pela janela à direita, sombras longas e suaves.',
           'Marcenaria em nogueira, bancada de mármore claro, piso de porcelanato polido.',
           'Câmera a 1,60 m do piso, lente 24 mm, verticais corrigidas.']
    SW = [(recorte(dia, 170, 520, 170, 170), 'Nogueira'), (recorte(dia, 320, 745, 150, 150), 'Mármore claro'),
          (recorte(dia, 520, 1600, 260, 260), 'Porcelanato')]
    sw = [cartao_img(s, 220, 72 + i * 250, 600, 16) for i, (s, _) in enumerate(SW)]
    swl = camada([(nm, MAN(30), INK, (72 + i * 250, 846), 'la') for i, (_, nm) in enumerate(SW)])
    S = [  # (início, fim)
        (0.0, 3.6), (3.6, 7.6), (7.6, 11.6), (11.6, 15.6), (15.6, 19.6), (19.6, 23.4)]
    D = 23.4
    g0 = camada([('Esta cozinha', CORM(92), INK, (72, 270), 'la'), ('era obra crua.', CORMI(98), BRONZE, (72, 370), 'la')])
    sub0 = camada([('O prompt de render em 4 partes', MAN(36), INK, (72, 1110), 'la')])
    P1, P2, P3, P4 = passo_lay('1', 'O que não muda'), passo_lay('2', 'A luz'), passo_lay('3', 'Os materiais'), passo_lay('4', 'A câmera')
    T1 = texto_lay('Paredes, janelas', 'e o arco do teto.')
    T2 = texto_lay('Hora do dia e', 'de onde vem a luz.')
    T3 = texto_lay('Cada material', 'pelo nome.')
    T4 = texto_lay('Na altura', 'do olho.')
    cta = camada([('Salve para o', CORM(96), INK, (72, 300), 'la'), ('próximo render.', CORMI(104), BRONZE, (72, 402), 'la'),
                  ('A ordem não muda: o que fica, luz,', MAN(34), INK, (72, 1170), 'la'),
                  ('materiais e câmera.', MAN(34), INK, (72, 1214), 'la')])
    cam_l = camada([('1,60 m · 24 mm · verticais retas', MONO(28), INK, (72, CY + CH + 30), 'la')])
    lbl = lambda s: camada([(s, MONO(24), INK, (72, CY + CH + 30), 'la')])
    L_ob, L_fim, L_dia, L_noi = lbl('OBRA CRUA'), lbl('RENDER · IA'), lbl('FIM DA TARDE'), lbl('NOITE')

    def frame(t):
        f = papel().copy()
        f = compoe(f, cab(INK), 1)
        if t < S[0][1]:
            k = ease(prog(t, 1.4, 2.6))
            f = cola(f, *Co[:2], Co[2]); f = cola(f, *Cd[:2], Cd[2], k)
            f = compoe(f, g0, ease(prog(t, .1, .5))); f = compoe(f, sub0, ease(prog(t, 2.4, 2.8)))
            f = compoe(f, L_fim if k > .5 else L_ob, 1)
        elif t < S[1][1]:
            tt = t - S[1][0]
            f = cola(f, *Co[:2], Co[2])
            x, y = Co[2]; hh, ww = Co[0].shape[:2]; reg = f[y:y + hh, x:x + ww]
            mm = np.clip((ease(prog(tt, .5, 2.6)) * 1.15 - campo6[:hh, :ww]) / .08, 0, 1)
            r = reg.astype(np.float32); k6 = (lo6 * mm)[..., None] * .9
            reg[:] = np.clip(r + k6 * (np.float32((40, 150, 175)) - r), 0, 255).astype(np.uint8)
            f = compoe(f, P1, 1); f = compoe(f, T1, ease(prog(tt, .1, .5)))
            f = compoe(f, digita(PRT[0], int(len(PRT[0]) * prog(tt, .8, 3.2))), 1)
        elif t < S[2][1]:
            tt = t - S[2][0]; k = ease(prog(tt, 1.6, 2.4))
            f = cola(f, *Cd[:2], Cd[2]); f = cola(f, *Cn[:2], Cn[2], k)
            f = compoe(f, P2, 1); f = compoe(f, T2, ease(prog(tt, .1, .5)))
            f = compoe(f, L_noi if k > .5 else L_dia, 1)
            f = compoe(f, digita(PRT[1], int(len(PRT[1]) * prog(tt, .5, 3.2))), 1)
        elif t < S[3][1]:
            tt = t - S[3][0]
            for i, s in enumerate(sw):
                f = cola(f, *s[:2], s[2], ease(prog(tt, .3 + i * .35, .7 + i * .35)))
            f = compoe(f, swl, ease(prog(tt, 1.4, 1.8)))
            f = compoe(f, P3, 1); f = compoe(f, T3, ease(prog(tt, .1, .5)))
            f = compoe(f, digita(PRT[2], int(len(PRT[2]) * prog(tt, .6, 3.3))), 1)
        elif t < S[4][1]:
            tt = t - S[4][0]
            f = cola(f, *Cd[:2], Cd[2])
            x, y = Cd[2]; yo = y + int(CH * .52); k = ease(prog(tt, .5, 1.3))
            cv2.line(f, (x, yo), (x + int(CW * k), yo), (40, 150, 175), 3)
            f = compoe(f, cam_l, ease(prog(tt, 1.0, 1.4)))
            f = compoe(f, P4, 1); f = compoe(f, T4, ease(prog(tt, .1, .5)))
            f = compoe(f, digita(PRT[3], int(len(PRT[3]) * prog(tt, .6, 2.8))), 1)
        else:
            tt = t - S[5][0]
            f = cola(f, *Co[:2], Co[2])
            x, y = Co[2]; p = ease(prog(tt, .4, 2.2)); cut = int(CW * p)
            if cut > 0:
                ph, m = Cd[0][:, :cut], Cd[1][:, :cut]; reg = f[y:y + ph.shape[0], x:x + cut]
                reg[:] = (reg * (1 - m) + ph * m).astype(np.uint8)
                if cut < CW: f[y:y + ph.shape[0], x + cut - 2:x + cut + 1] = (40, 150, 175)
            f = compoe(f, cta, ease(prog(tt, .2, .6)))
        return f
    return com_fim(frame, D)


MODELOS = dict(m1=(m1, 'prancheta-ao-predio', 0.0), m2=(m2, 'cozinha-obra-a-luz', 2.0), m3=(m3, 'wireframe-loft', 4.0),
               m4=(m4, 'fachada-em-etapas', 6.0), m5=(m5, 'estrutura-explicada', 8.0), m6=(m6, 'tutorial-prompt-4-partes', 0.0))

if __name__ == '__main__':
    P, OUT = sys.argv[1], Path(sys.argv[2]); quais = sys.argv[3:] or list(MODELOS)
    for k in quais:
        fn, nome, ofs = MODELOS[k]
        print('==', k, nome, flush=True)
        fr, dur = fn(P)
        grava(fr, dur, OUT / f'{k}-{nome}.mp4', ofs)
        print('   ok', dur, flush=True)
