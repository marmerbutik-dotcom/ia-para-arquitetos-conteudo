"""
Reels "obra ganha vida" (modelos M4 e M5 da seção 5e do GUIA, referências de 13/11/2026).

Dois modos, sem texto sobre o vídeo (só o @ no canto, como nas referências) e com o
cartão final escurecido sobre a última imagem:

  cresce  (M4, referência @render3d.fabiogarcia): a obra crua vira o ambiente pronto
          elemento por elemento, com bordas orgânicas, na mesma câmera; no fim as luzes acendem.
          spec: {"modo":"cresce","base":"novas/x/3-obra.jpg","final":"novas/x/4-render.jpg",
                 "zonas":[{"nome":"piso","box":[x0,y0,x1,y1],"seed":[x,y]}, ...]}
  faixas  (M5, referência @luck_lucky934): etapas trocam em faixas verticais que deslizam
          (planta → estrutura → casa pronta), a casa pronta entra por partes (bandas)
          e termina com um movimento lento de câmera.
          spec: {"modo":"faixas","etapas":["novas/x/1-planta.jpg","novas/x/2-estrutura.jpg","novas/x/3-pronta.jpg"],
                 "bandas":[[y0,y1],...], "camera":[x,y]}

Uso: python3 -c "import sys,json; sys.path.insert(0,'engine'); import constroi; constroi.render(json.load(open('spec.json')),'saida.mp4',capa='capa.jpg')"
"""
import os, subprocess
import numpy as np, cv2
from PIL import Image
import evolui as E

W, H, FPS = E.W, E.H, E.FPS
HANDLE = '@ia.para.arquitetos'
rng = np.random.default_rng(7)
RU = cv2.resize(rng.random((60, 34)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
RU2 = cv2.resize(rng.random((14, 8)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
XX, YY = E.XX, E.YY


def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def caixa(b, mole=.04):
    x0, y0, x1, y1 = b
    return (ss(x0 - mole, x0 + mole, XX) * (1 - ss(x1 - mole, x1 + mole, XX)) *
            ss(y0 - mole, y0 + mole, YY) * (1 - ss(y1 - mole, y1 + mole, YY))).astype(np.float32)


def cresce_mask(seed, p, alcance=1.25):
    """crescimento orgânico a partir de um ponto (0..1); p 0→1"""
    d = np.sqrt(((XX - seed[0]) * W / H) ** 2 + (YY - seed[1]) ** 2)
    r = E.eout(p) * alcance
    borda = r - d + (RU - .5) * .16 + (RU2 - .5) * .10
    return ss(-.012, .012, borda).astype(np.float32)


def assinatura():
    c = E.Camada(); d = c.d
    d.text((W - 64, 120), HANDLE, font=E.MAN(26), fill=E.OSSO + (215,), anchor='ra')
    return c.pronta()


def final_card(f, k):
    """escurece a última imagem e mostra logo, @ e site (como o fecho das referências)"""
    esc = cv2.addWeighted(f, 1 - .72 * k, np.zeros_like(f), .72 * k, 0)
    c = E.Camada(); d = c.d; a = int(255 * k)
    y = 760
    if E.LOGO.exists():
        lg = Image.open(E.LOGO).convert('RGBA'); lg = lg.resize((360, int(lg.height * 360 / lg.width)), Image.LANCZOS)
        if k < 1: lg.putalpha(lg.getchannel('A').point(lambda v: int(v * k)))
        c.im.alpha_composite(lg, ((W - 360) // 2, y)); y += lg.height + 70
    d.text((W / 2, y), HANDLE, font=E.MAN(38), fill=E.OSSO + (a,), anchor='ma')
    d.text((W / 2, y + 70), 'iaparaarquitetos.com.br', font=E.MONO(30), fill=E.BZL + (a,), anchor='ma')
    return E.compoe(esc, c.pronta())


def acende(img, k):
    """luzes acesas: brilho quente nas áreas claras + leve aquecimento geral"""
    if k <= 0: return img
    f = img.astype(np.float32) / 255
    lum = f.max(axis=2)
    alto = np.clip((lum - .72) / .28, 0, 1)[..., None]
    glow = cv2.GaussianBlur(f * alto, (0, 0), 28)
    quente = np.array([1.0, .86, .62], np.float32)
    dourado = np.array([1.08, .98, .82], np.float32)            # luz de fim de tarde
    f = f * (1 + k * (dourado - 1)) + glow * quente * (1.1 * k)
    f = .5 + (f - .5) * (1 + .08 * k)
    return (np.clip(f, 0, 1) * 255).astype(np.uint8)


# ------------------------------------------------------------------ modo cresce
def roteiro_cresce(spec):
    final = E.carrega(spec['final'])
    base = E.carrega(spec['base'])
    if spec.get('alinha', True):
        base, cc = E.alinha(base, final); print('alinhamento', round(float(cc), 3))
    zonas = spec['zonas']
    t0, dz, sobre = .8, .78, .26          # gancho na obra crua, depois 1 elemento a cada ~0,5 s
    st = [t0 + i * (dz - sobre) for i in range(len(zonas))]
    fim_z = st[-1] + dz
    t_luz = fim_z + .1; d_luz = 1.3
    t_hold = t_luz + d_luz; d_hold = 1.6
    t_card = t_hold + d_hold; d_card = 2.4
    T = t_card + d_card
    Z = [caixa(z['box']) for z in zonas]
    acum = np.zeros((H, W), np.float32)
    cache = {}

    def A(t):
        a = np.zeros((H, W), np.float32)
        for z, m, s in zip(zonas, Z, st):
            p = (t - s) / dz
            if p <= 0: continue
            g = 1.0 if p >= 1 else cresce_mask(z['seed'], p)
            a = np.maximum(a, m * g)
        if t >= fim_z: a = np.maximum(a, ss(0, 1, np.full_like(a, (t - fim_z) / .25)))
        return a

    def frame(t):
        a = A(t)[..., None]
        f = (base.astype(np.float32) * (1 - a) + final.astype(np.float32) * a).astype(np.uint8)
        k = E.ease((t - t_luz) / d_luz)
        f = acende(f, k)
        z = 1.0 + .035 * E.ease(t / T)
        f = E.kb(f, z)
        if t >= t_card:
            f = final_card(f, E.ease((t - t_card) / .6))
        else:
            f = E.compoe(f, ASS)
        return f
    return T, frame, acende(final, 1.0)


# ------------------------------------------------------------------ modo faixas
def faixas(a, b, p, n=4, inicio=0):
    """b entra em n faixas verticais que deslizam (alternando de cima e de baixo)"""
    out = a.copy(); cw = W // n
    for c in range(n):
        x0 = c * cw; x1 = W if c == n - 1 else x0 + cw
        q = E.eout(np.clip((p - c * .54 / max(1, n - 1)) / .46, 0, 1))
        if q <= 0: continue
        sh = int((1 - q) * H) * (1 if (c + inicio) % 2 == 0 else -1)
        col = np.roll(b[:, x0:x1], sh, axis=0)
        if sh > 0: col[:sh] = a[:sh, x0:x1]
        elif sh < 0: col[sh:] = a[sh:, x0:x1]
        out[:, x0:x1] = col
        if 0 < q < 1:
            y = sh if sh > 0 else H + sh
            out[max(0, y - 2):min(H, y + 2), x0:x1] = E.BZL
    return out


def roteiro_faixas(spec):
    im = [E.carrega(p) for p in spec['etapas']]
    if spec.get('alinha', True):
        for i in range(len(im) - 1, 0, -1):
            im[i - 1], cc = E.alinha(im[i - 1], im[i]); print('alinhamento', i, round(float(cc), 3))
    bandas = spec.get('bandas', [[0, .5], [.4, .75], [.65, 1]])
    seg = []; t = 0.0
    seg.append((t, t + .8, lambda u: im[0])); t += .8                       # gancho: a planta
    for i in range(1, len(im) - 1):                                          # etapas intermediárias inteiras
        a, b, t0 = im[i - 1], im[i], t
        seg.append((t, t + .9, lambda u, a=a, b=b, t0=t0: faixas(a, b, (u - t0) / .9, inicio=i))); t += .9
        seg.append((t, t + .45, lambda u, b=b: b)); t += .45
    a, b = im[-2], im[-1]                                                    # a última entra por partes
    cur = [a]
    for j, (y0, y1) in enumerate(bandas):
        m = caixa([-.1, y0, 1.1, y1], .03)[..., None]
        prev = cur[-1]
        alvo = (prev.astype(np.float32) * (1 - m) + b.astype(np.float32) * m).astype(np.uint8)
        t0 = t
        seg.append((t, t + .8, lambda u, p=prev, q=alvo, t0=t0, j=j: faixas(p, q, (u - t0) / .8, inicio=j))); t += .8
        cur.append(alvo)
        seg.append((t, t + .2, lambda u, q=alvo: q)); t += .2
    cx, cy = spec.get('camera', [.5, .5])
    t0 = t; dcam = 3.0
    seg.append((t, t + dcam, lambda u, t0=t0: E.kb(b, 1.0 + .12 * E.ease((u - t0) / dcam),
                                                   .5 + (cx - .5) * E.ease((u - t0) / dcam), .5 + (cy - .5) * E.ease((u - t0) / dcam)))); t += dcam
    last = E.kb(b, 1.12, cx, cy)
    t0 = t; dcard = 2.4
    seg.append((t, t + dcard, lambda u, t0=t0: final_card(last, E.ease((u - t0) / .6)))); t += dcard
    T = t

    def frame(u):
        for s0, s1, fn in seg:
            if u < s1:
                f = fn(u)
                return f if s1 > T - dcard + 1e-6 else E.compoe(f, ASS)
        return seg[-1][2](u)
    return T, frame, b


ASS = None


def render(spec, saida, capa=None, som_ofs=0.0, som=True, crf=19):
    global ASS
    ASS = assinatura()
    T, frame, capa_img = (roteiro_cresce if spec['modo'] == 'cresce' else roteiro_faixas)(spec)
    saida = str(saida); tmp = saida + '.v.mp4'
    pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf), '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(int(round(T * FPS))):
        pr.stdin.write(np.ascontiguousarray(frame(i / FPS)).tobytes())
    pr.stdin.close(); pr.wait()
    if som and E.SOM.exists():
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-ss', f'{som_ofs:.2f}', '-i', str(E.SOM), '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-af', f'afade=t=in:d=0.3,afade=t=out:st={max(0, T - 1.2):.2f}:d=1.2',
                        '-t', f'{T:.2f}', '-movflags', '+faststart', saida], check=True)
        os.remove(tmp)
    else:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-c', 'copy', '-movflags', '+faststart', saida], check=True); os.remove(tmp)
    if capa:
        f = E.kb(capa_img, 1.04)
        f = E.compoe(E.compoe(E.compoe(f, E.moldura()), E.cabecalho(spec.get('rotulo', ''))), E.titulo(*spec.get('gancho', ['', ''])))
        Image.fromarray(f).save(str(capa), quality=92)
    return T
