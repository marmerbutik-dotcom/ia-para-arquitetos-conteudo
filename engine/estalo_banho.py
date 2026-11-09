# Reel "estalo" Marmer Butik: obra crua -> seixos de rio -> spa com banheira e cuba Riverstone
# Saída 2160x3840 (4K vertical), 30 fps, sem áudio (a música entra pelo Instagram).
import cv2, numpy as np, subprocess, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS = 30; T = 13.5; N = int(T * FPS)
W, H = 2160, 3840; K = 2.0               # coordenadas do roteiro em 1080x1920, multiplicadas por K
F = '/home/claude/ia-para-arquitetos-conteudo/assets/fonts-ttf/'
SERIF = F + 'cormorant-garamond-latin-500-normal.ttf'; SERIF_I = F + 'cormorant-garamond-latin-500-italic.ttf'
MONO = F + 'ibm-plex-mono-latin-400-normal.ttf'; SANS = F + 'manrope-latin-500-normal.ttf'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out/banho-4k.mp4'
PREVIEW = '--preview' in sys.argv

def up(path):
    im = cv2.imread(path)[:, :, ::-1]
    im = cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    bl = cv2.GaussianBlur(im, (0, 0), 2.2)
    return np.clip(im + 0.55 * (im - bl), 0, 255)

S1, S2, S3 = up('s1-obra.jpg'), up('s2-seixos.jpg'), up('s3-pronto.jpg')
# brilho das luzes do S3 (bloom) calculado uma vez
lum = S3.mean(axis=2, keepdims=True)
hi = np.clip((lum - 150) / 90, 0, 1) * S3
small = cv2.resize(hi, (W // 8, H // 8), interpolation=cv2.INTER_AREA)
BLOOM = cv2.resize(cv2.GaussianBlur(small, (0, 0), 9), (W, H), interpolation=cv2.INTER_LINEAR)

yy_ = np.arange(H, dtype=np.float32)[:, None, None] / K
TOPG = 1 - 0.55 * np.clip(1 - (yy_ - 180) / 720, 0, 1) ** 1.6
LABG = 1 - 0.30 * np.clip(1 - np.abs(yy_ - 1010) / 260, 0, 1)

def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def eout(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def lerp(a, b, x): return a + (b - a) * x

def cam_M(z, cx, cy, dx=0, dy=0):
    # escala z em torno de (cx,cy) (coords 1080) e mantém (cx,cy) no mesmo lugar da tela
    cx, cy = cx * K, cy * K
    return np.float32([[z, 0, cx - z * cx + dx * K], [0, z, cy - z * cy + dy * K]])

def warp(img, M):
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def pt(M, x, y):  # ponto do quadro-fonte (1080) para tela (4K)
    return (M[0, 0] * x * K + M[0, 2], M[1, 1] * y * K + M[1, 2])

def shake(t, t0, amp=9, dur=0.32):
    u = t - t0
    if u < 0 or u > dur: return 0, 0
    d = (1 - u / dur) ** 2
    return amp * d * math.sin(u * 95), amp * d * math.cos(u * 71)

# ---------- sprites de texto ----------
def text_sprite(lines, shadow=True, pad=40):
    # lines: [(texto, fonte, tamanho_1080, cor, tracking)]
    fonts = [ImageFont.truetype(f, int(s * K)) for (_, f, s, _, _) in lines]
    ws, hs = [], []
    for (txt, _, s, _, tr), fo in zip(lines, fonts):
        w = sum(fo.getlength(c) for c in txt) + tr * K * max(len(txt) - 1, 0)
        a, d = fo.getmetrics(); ws.append(w); hs.append(a + d)
    gap = int(8 * K)
    Wd = int(max(ws)) + 2 * pad; Hd = int(sum(hs) + gap * (len(lines) - 1)) + 2 * pad
    im = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    y = pad
    for (txt, _, s, col, tr), fo, w, h in zip(lines, fonts, ws, hs):
        x = pad
        for c in txt:
            dr.text((x, y), c, font=fo, fill=col); x += fo.getlength(c) + tr * K
        y += h + gap
    if shadow:
        a = im.split()[3].filter(ImageFilter.GaussianBlur(10 * K / 2))
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.75)))
        sh.alpha_composite(im); im = sh
    return np.array(im).astype(np.float32), pad, ws

def blit(frame, spr, x, y, alpha=1.0, anchor='l'):
    arr, pad, ws = spr
    h, w = arr.shape[:2]
    x = int(x - pad - (w - 2 * pad if anchor == 'r' else (w - 2 * pad) / 2 if anchor == 'c' else 0)); y = int(y - pad)
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0 or alpha <= 0: return
    s = arr[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[:, :, 3:4] / 255 * alpha
    frame[y0:y1, x0:x1] = frame[y0:y1, x0:x1] * (1 - a) + s[:, :, :3] * a

WH = (255, 255, 255, 255); CREAM = (240, 228, 210, 255); GOLD = (214, 182, 132, 255)
T_HOOK = text_sprite([('Um estalo…', SERIF_I, 112, WH, 0)])
T_RIO = text_sprite([('…e o chão vira rio.', SERIF_I, 96, WH, 0)])
T_MAIS = text_sprite([('Mais um.', SERIF_I, 112, WH, 0)])
T_SPA = text_sprite([('Agora é spa.', SERIF_I, 112, WH, 0)])
T_TAG = text_sprite([('MARMER BUTIK', MONO, 30, CREAM, 10)])
L_BAN = text_sprite([('Banheira Riverstone', SERIF, 66, WH, 0), ('172 × 116 × 65 cm', MONO, 33, CREAM, 3)])
L_CUBA = text_sprite([('Cuba de apoio Riverstone', SERIF, 60, WH, 0), ('56 × 28 × 15 cm', MONO, 33, CREAM, 3)])
P_HEAD = text_sprite([('As peças são reais.', SERIF_I, 76, WH, 0)])
P_BAN = text_sprite([('Banheira Riverstone', SERIF, 64, WH, 0)])
P_BAN2 = text_sprite([('PEDRA DE RIO · 172 × 116 × 65 CM', MONO, 31, GOLD, 4)])
P_CUBA = text_sprite([('Cuba de apoio Riverstone', SERIF, 64, WH, 0)])
P_CUBA2 = text_sprite([('PEDRA DE RIO · 56 × 28 × 15 CM', MONO, 31, GOLD, 4)])
E_1 = text_sprite([('Banheiras e cubas em pedra natural', SERIF_I, 56, WH, 0)])
E_2 = text_sprite([('MARMERBUTIK.COM', MONO, 34, GOLD, 8)])

# ---------- fotos reais ----------
def card(path, size):
    im = cv2.imread(path)[:, :, ::-1]
    im = cv2.resize(im, (size, size), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    bl = cv2.GaussianBlur(im, (0, 0), 2.0)
    return np.clip(im + 0.5 * (im - bl), 0, 255)
PB = card('prod/banheira_em_pedra_natural_172x116x65cm_brs01_1_20260328143103_c11d048c0892.jpg', int(860 * K))
PC = card('prod/cuba_pedra_de_rio_56x28x15cm_3_20261030161236_1128c15f274f.jpg', int(860 * K))

logo = Image.open('logo-mb-branco.png').convert('RGBA')
lw = int(470 * K); logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
LOGO = (np.array(logo).astype(np.float32), 0, [lw])

# ---------- partículas ----------
rng = np.random.default_rng(7)
DUST = dict(x=rng.uniform(150, 930, 220), y=rng.uniform(1450, 1900, 220), vx=rng.normal(0, 140, 220),
            vy=rng.uniform(-520, -120, 220), r=rng.uniform(1.5, 4.5, 220), l=rng.uniform(0.7, 1.6, 220))
FIRE = dict(x=rng.uniform(0, 1080, 70), y=rng.uniform(900, 1800, 70), vx=rng.normal(0, 18, 70),
            vy=rng.uniform(-60, -15, 70), r=rng.uniform(1.5, 3.5, 70), ph=rng.uniform(0, 6.28, 70))

def particles(frame, t):
    lay = np.zeros((H // 2, W // 2, 3), np.float32); any_ = False
    u = t - 2.0
    if 0 <= u <= 1.7:
        any_ = True
        for i in range(220):
            if u > DUST['l'][i]: continue
            a = (1 - u / DUST['l'][i]) ** 1.5
            x = DUST['x'][i] + DUST['vx'][i] * u; y = DUST['y'][i] + DUST['vy'][i] * u + 160 * u * u
            cv2.circle(lay, (int(x), int(y)), int(DUST['r'][i]), (230 * a, 222 * a, 205 * a), -1, cv2.LINE_AA)
    u = t - 5.2
    if 0 <= u and t < 9.8:
        any_ = True; fade = ease(u / 0.8) * (1 - ease((t - 9.3) / 0.5))
        for i in range(70):
            x = (FIRE['x'][i] + FIRE['vx'][i] * u) % 1080; y = FIRE['y'][i] + FIRE['vy'][i] * u
            a = fade * (0.55 + 0.45 * math.sin(FIRE['ph'][i] + u * 3.1))
            cv2.circle(lay, (int(x), int(y)), int(FIRE['r'][i]), (255 * a, 196 * a, 120 * a), -1, cv2.LINE_AA)
    if not any_: return
    lay = cv2.GaussianBlur(lay, (0, 0), 1.6) * 1.6 + cv2.GaussianBlur(lay, (0, 0), 7) * 2.2
    frame += cv2.resize(lay, (W, H), interpolation=cv2.INTER_LINEAR)

def ring(frame, t, t0, cx, cy, col):
    u = t - t0
    if not (0 <= u <= 0.6): return
    lay = np.zeros((H // 2, W // 2, 3), np.float32)
    r = int(eout(u / 0.6) * 900); a = (1 - u / 0.6) ** 1.4
    cv2.circle(lay, (int(cx), int(cy)), max(r, 1), tuple(c * a for c in col), int(10 + 30 * (1 - u / 0.6)), cv2.LINE_AA)
    lay = cv2.GaussianBlur(lay, (0, 0), 6)
    frame += cv2.resize(lay, (W, H))

def flash(frame, t, t0, col, peak, dur=0.38):
    u = t - t0
    if -0.05 <= u <= dur:
        a = peak * (1 + u / 0.05) if u < 0 else peak * math.exp(-u / (dur / 3.2))
        frame[:] = frame * (1 - a) + np.float32(col) * a

def label(frame, t, t0, M, px, py, spr, tx, ty, anchor):
    u = t - t0
    if u < 0: return
    a = ease(u / 0.45) * (1 - ease((t - 9.25) / 0.3))
    if a <= 0: return
    sx, sy = pt(M, px, py)
    ex, ey = tx * K, (ty + 150) * K   # ponta da linha logo abaixo do texto
    # linha que cresce do produto até o texto
    g = eout(u / 0.5)
    lay = np.zeros((H, W, 3), np.uint8)
    cv2.line(lay, (int(sx), int(sy)), (int(lerp(sx, ex, g)), int(lerp(sy, ey, g))), (255, 255, 255), int(2.2 * K), cv2.LINE_AA)
    pul = 1 + 0.25 * math.sin(u * 6)
    cv2.circle(lay, (int(sx), int(sy)), int(9 * K * pul), (255, 255, 255), -1, cv2.LINE_AA)
    cv2.circle(lay, (int(sx), int(sy)), int(19 * K * pul), (255, 255, 255), int(1.6 * K), cv2.LINE_AA)
    y0, y1 = int(max(min(sy, ey) - 60 * K, 0)), int(min(max(sy, ey) + 60 * K, H))
    x0, x1 = int(max(min(sx, ex) - 60 * K, 0)), int(min(max(sx, ex) + 60 * K, W))
    sub = lay[y0:y1, x0:x1].astype(np.float32) / 255 * a
    frame[y0:y1, x0:x1] = frame[y0:y1, x0:x1] * (1 - sub) + 255 * sub
    blit(frame, spr, tx * K, (ty + 18 * (1 - ease(u / 0.5))) * K, a * ease((u - 0.15) / 0.4), anchor)

def scene(t):
    if t < 5.0:
        z = lerp(1.03, 1.10, t / 5.0); dx, dy = shake(t, 2.0)
        M = cam_M(z, 540, 1150, dx, dy)
        f = warp(S1, M)
        if t >= 2.0:
            # seixos se espalham a partir do chão, em onda radial com borda suave
            s2 = warp(S2, M)
            r = eout((t - 2.0) / 0.95) * 2300 * K
            yy, xx = np.ogrid[:H, :W]
            d = np.sqrt((xx - 540 * K) ** 2 + ((yy - 1820 * K) * 0.9) ** 2)
            m = np.clip((r - d) / (140 * K), 0, 1)[..., None].astype(np.float32)
            f = f * (1 - m) + s2 * m
        return f, M
    # S3: luzes acendem
    z = lerp(1.04, 1.15, ease((t - 5.0) / 4.8)); dx, dy = shake(t, 5.0, 8)
    M = cam_M(z, 560, 1230, dx, dy)
    f = warp(S3, M)
    u = t - 5.0
    if u < 1.4:
        on = ease((u - 0.12) / 0.75)
        flick = 1.0 if u > 0.55 else (0.82 + 0.18 * math.sin(u * 60))
        br = lerp(0.18, 1.0, on) * flick
        g = math.sin(min(u / 1.4, 1) * math.pi) * 0.9
        f = f * br + warp(BLOOM, M) * g
        if u < 0.25:   # o último instante do S2 some no clarão
            m = ease(u / 0.25)
            z2 = lerp(1.03, 1.10, 1.0); M2 = cam_M(z2, 540, 1150, dx, dy)
            f = warp(S2, M2) * (1 - m) + f * m
    return f, M

def frame_at(t):
    if t < 9.75:
        f, M = scene(t)
        flash(f, t, 2.0, (255, 252, 246), 0.85)
        flash(f, t, 5.0, (255, 226, 178), 0.92, 0.45)
        ring(f, t, 2.0, 540, 1700, (255, 250, 240))
        ring(f, t, 5.0, 540, 1300, (150, 120, 85))
        particles(f, t)
        f *= TOPG
        la = ease((t - 6.3) / 0.5) * (1 - ease((t - 9.2) / 0.3))
        if la > 0: f *= 1 - (1 - LABG) * la
        # textos (zona segura: y 230-1440, 230 px livres à direita)
        tag_a = ease(t / 0.3) * (1 - ease((t - 9.2) / 0.4))
        blit(f, T_TAG, 540 * K, 300 * K, tag_a, 'c')
        def show(spr, a0, a1, y=360):
            a = ease((t - a0) / 0.25) * (1 - ease((t - a1) / 0.2))
            blit(f, spr, 540 * K, (y + 14 * (1 - ease((t - a0) / 0.3))) * K, a, 'c')
        show(T_HOOK, 0.0, 1.85, 400); show(T_RIO, 2.35, 4.25, 400); show(T_MAIS, 4.35, 4.95, 400); show(T_SPA, 5.55, 6.35, 400)
        label(f, t, 6.55, M, 215, 1310, L_BAN, 70, 1050, 'l')
        label(f, t, 7.45, M, 925, 1185, L_CUBA, 830, 880, 'r')
        if t > 9.45:   # transição para as fotos reais
            a = ease((t - 9.45) / 0.3); f = f * (1 - a) + 10 * a
        return f
    f = np.full((H, W, 3), 10.0, np.float32)
    if t < 12.0:
        u = t - 9.75
        a_in = ease(u / 0.3)
        blit(f, P_HEAD, 540 * K, 290 * K, a_in, 'c')
        if u < 1.15: P, n1, n2, v = PB, P_BAN, P_BAN2, u
        else: P, n1, n2, v = PC, P_CUBA, P_CUBA2, u - 1.15
        a = ease(v / 0.22) * (1 - ease((t - 11.8) / 0.2))
        z = lerp(1.0, 1.05, v / 1.15); s = int(860 * K * z)
        img = cv2.resize(P, (s, s), interpolation=cv2.INTER_LINEAR)
        c = (s - int(860 * K)) // 2; img = img[c:c + int(860 * K), c:c + int(860 * K)]
        x0, y0 = int(110 * K), int(420 * K)
        f[y0:y0 + img.shape[0], x0:x0 + img.shape[1]] = f[y0:y0 + img.shape[0], x0:x0 + img.shape[1]] * (1 - a) + img * a
        blit(f, n1, 540 * K, 1295 * K, a, 'c'); blit(f, n2, 540 * K, 1385 * K, a, 'c')
        return f
    u = t - 12.0
    a = ease(u / 0.5)
    blit(f, LOGO, 540 * K, (560 + 20 * (1 - ease(u / 0.6))) * K, a, 'c')
    blit(f, E_1, 540 * K, 1110 * K, ease((u - 0.25) / 0.5), 'c')
    blit(f, E_2, 540 * K, 1200 * K, ease((u - 0.45) / 0.5), 'c')
    return f

if PREVIEW:
    ts = [float(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]
    for t in ts:
        im = np.clip(frame_at(t), 0, 255).astype(np.uint8)
        Image.fromarray(im).resize((540, 960), Image.LANCZOS).save(f'prev/p{t:05.2f}.jpg', quality=85)
    sys.exit()

p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                      '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p',
                      '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
import time; t0 = time.time()
for i in range(N):
    p.stdin.write(np.clip(frame_at(i / FPS), 0, 255).astype(np.uint8).tobytes())
    if i % 30 == 0: print(i, '/', N, int(time.time() - t0), 's', flush=True)
p.stdin.close(); p.wait(); print('ok')
