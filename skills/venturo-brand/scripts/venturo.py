#!/usr/bin/env python3
"""
venturo.py — pipeline konten video Venturo (preview tanpa render → render setelah approve).

  init      <proyek> [--wide]          folder proyek + script.json & scenes.js contoh
  check-tts <proyek>                   tes koneksi TTS (env TTS_API_KEY; TTS_URL opsional)
  tts       <proyek> [--force]         VO TTS per segmen motion (cache di build/tts)
  cut       <proyek> [--force]         potong & reframe footage → preview/media/<id>.mp4 (+ wav ucapan)
  timeline  <proyek>                   hitung durasi & timing kata → build/timeline.json
  audio     <proyek>                   mix VO + suara footage + SFX + backsound (ducking) → preview/media/audio.mp3
  build     <proyek>                   preview/index.html (player, tinggal play)
  all       <proyek>                   tts → cut → timeline → audio → build
  shots     <proyek> --at 1,4.5,9      contact sheet frame → build/shots.png
  render    <proyek> [--fps 60]        render MP4 final + versi tanpa musik + VO saja → renders/

Kebutuhan: python3, ffmpeg, numpy, scipy, playwright (chromium). TTS: env TTS_API_KEY (jangan ditulis di file).
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, urllib.request, urllib.error, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
SR = 48000
DEFAULT_TTS_URL = "https://tts.venturo.pro/v1/audio/speech"


# ------------------------------------------------------------------ util
def die(m): print("✗", m); sys.exit(1)
def run(cmd, **kw):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)
    if r.returncode: die(f"perintah gagal:\n{cmd if isinstance(cmd, str) else ' '.join(cmd)}\n{r.stderr[-1500:]}")
    return r
def probe_dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout.strip())
def sha(*xs): h = hashlib.sha1(); [h.update(str(x).encode()) for x in xs]; return h.hexdigest()[:10]
def load(d): p = Path(d) / "script.json"; return json.loads(p.read_text()) if p.exists() else die(f"{p} tidak ada (jalankan init)")
def clean(t): return re.sub(r"[*_]", "", t).strip()
def words_of(t): return [{"w": x.replace("*", "").replace("_", ""), "em": "*" in x} for x in t.split() if x.replace("*", "")]


# ------------------------------------------------------------------ timing kata (sinkron ke jeda nyata)
def silences(path, noise="-35dB", dmin=0.12):
    err = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-af", f"silencedetect=noise={noise}:d={dmin}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(st, en + [None] * (len(st) - len(en))))

def time_words(words, dur, audio=None):
    """Rentang bicara dari silencedetect, bobot per panjang kata + tanda baca, titik jeda di-warp ke jeda nyata."""
    if not words: return words
    s0, s1, pauses = 0.0, dur, []
    if audio:
        for a, b in silences(audio):
            b = dur if b is None else b
            if a <= 0.02: s0 = max(s0, b)
            elif b >= dur - 0.02: s1 = min(s1, a)
            else: pauses.append((a, b))
    span = max(0.2, s1 - s0)
    ws = [len(w["w"]) + 2.2 + (4 if re.search(r"[,;:]$", w["w"]) else 0) + (7 if re.search(r"[.!?…]$", w["w"]) else 0) for w in words]
    tot, cum, prop = sum(ws), 0.0, []
    for w in ws: prop.append((s0 + span * cum / tot, s0 + span * (cum + w * .92) / tot)); cum += w
    anchors, used = [(s0, s0), (s1, s1)], set()
    for bi in [i for i, w in enumerate(words[:-1]) if re.search(r"[,;:.!?…]$", w["w"])]:
        exp, best = (prop[bi][1] + prop[bi + 1][0]) / 2, None
        for j, (a, b) in enumerate(pauses):
            if j in used: continue
            if abs((a + b) / 2 - exp) < .7 and (best is None or abs((a + b) / 2 - exp) < abs(sum(pauses[best]) / 2 - exp)): best = j
        if best is not None: used.add(best); anchors.append((exp, sum(pauses[best]) / 2))
    anchors.sort(); cl = [anchors[0]]
    for x, y in anchors[1:]:
        if x > cl[-1][0] + 1e-3 and y > cl[-1][1] + 1e-3: cl.append((x, y))
    def warp(x):
        for (x0, y0), (x1, y1) in zip(cl, cl[1:]):
            if x <= x1: return y0 + (y1 - y0) * (x - x0) / max(1e-6, x1 - x0)
        return cl[-1][1]
    for w, (a, b) in zip(words, prop): w["s"], w["e"] = round(warp(a), 3), round(warp(b), 3)
    return words


# ------------------------------------------------------------------ init
def cmd_init(a):
    d = Path(a.dir)
    for sub in ["footage", "konten", "sound", "production", "build", "preview/media", "renders"]: (d / sub).mkdir(parents=True, exist_ok=True)
    if not (d / "script.json").exists():
        sc = json.loads((BRAND / "templates" / "script-contoh.json").read_text())
        if a.wide: sc["w"], sc["h"] = 1920, 1080
        (d / "script.json").write_text(json.dumps(sc, indent=2, ensure_ascii=False))
    if not (d / "scenes.js").exists(): shutil.copy(BRAND / "templates" / "scenes-contoh.js", d / "scenes.js")
    for f in ["storyboard.md", "qc.md"]:
        src = BRAND / "templates" / f
        if src.exists() and not (d / "production" / f).exists(): shutil.copy(src, d / "production" / f)
    print(f"✓ proyek {d} siap. Isi script.json (segmen) & scenes.js, lalu: venturo.py all {d}")


# ------------------------------------------------------------------ TTS
def tts_conf(sc):
    return os.environ.get("TTS_URL", sc.get("ttsUrl", DEFAULT_TTS_URL)), os.environ.get("TTS_API_KEY", "")

def tts_request(text, voice, out, url, key, extra):
    body = json.dumps({"input": text, "voice": voice, **extra}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                                                                         "User-Agent": "curl/8.5.0", "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
    except urllib.error.HTTPError as e: die(f"TTS HTTP {e.code}: {e.read()[:200]!r}")
    except urllib.error.URLError as e: die(f"tidak bisa konek ke {url}: {e.reason} (cek allowlist jaringan / server TTS)")
    if len(data) < 500: die(f"respons TTS bukan audio: {data[:200]!r}")
    Path(out).write_bytes(data)

def cmd_check_tts(a):
    sc = load(a.dir); url, key = tts_conf(sc)
    if not key: die("TTS_API_KEY belum di-set: export TTS_API_KEY=... (jangan tulis di file proyek)")
    out = Path(a.dir) / "build" / "tts-check.mp3"; out.parent.mkdir(parents=True, exist_ok=True)
    tts_request("Tes suara satu dua tiga.", sc.get("voice", "gilang"), out, url, key, sc.get("ttsExtra", {}))
    print(f"✓ TTS OK — voice {sc.get('voice')} — {probe_dur(out):.2f}s ({url})")

def cmd_tts(a):
    d = Path(a.dir); sc = load(d); url, key = tts_conf(sc); (d / "build/tts").mkdir(parents=True, exist_ok=True)
    for s in sc["segments"]:
        if s.get("kind") != "mg" or not s.get("vo"): continue
        voice = s.get("voice", sc.get("voice", "gilang")); text = clean(s["vo"])
        f = d / "build/tts" / f"{s['id']}-{sha(voice, text, json.dumps(sc.get('ttsExtra', {})))}.mp3"
        if f.exists() and not a.force: print(f"  · {s['id']} (cache)"); continue
        if not key: die("TTS_API_KEY belum di-set")
        for old in (d / "build/tts").glob(f"{s['id']}-*.mp3"): old.unlink()
        tts_request(text, voice, f, url, key, sc.get("ttsExtra", {})); print(f"  ♪ {s['id']}: {text[:60]}")
    print("✓ TTS selesai")


# ------------------------------------------------------------------ footage
def cmd_cut(a):
    d = Path(a.dir); sc = load(d); W, H = sc.get("w", 1080), sc.get("h", 1920); fps = sc.get("mediaFps", 30)
    (d / "build/ft").mkdir(parents=True, exist_ok=True); (d / "preview/media").mkdir(parents=True, exist_ok=True)
    for s in sc["segments"]:
        if s.get("kind") != "ft": continue
        src = d / s["src"]
        if not src.exists(): die(f"footage {src} tidak ada")
        dur = round(s["to"] - s["ss"], 3); z0, z1 = s.get("zoom", [1.0, 1.04]); fy = s.get("focusY", 0.4)
        key = sha(src.stat().st_size, s["ss"], s["to"], z0, z1, fy, s.get("grade"), W, H, fps)
        out, stamp = d / "preview/media" / f"{s['id']}.mp4", d / "build/ft" / f"{s['id']}.key"
        if out.exists() and stamp.exists() and stamp.read_text() == key and not a.force: print(f"  · {s['id']} (cache)"); continue
        n = int(round(dur * fps)); BW, BH = int(W * 1.5) // 2 * 2, int(H * 1.5) // 2 * 2
        grade = {"redup": ",eq=saturation=0.75:contrast=1.06:brightness=-0.03", "hangat": ",eq=saturation=1.05:contrast=1.03"}.get(s.get("grade"), "")
        vf = (f"scale={BW}:{BH}:force_original_aspect_ratio=increase:flags=lanczos,crop={BW}:{BH},"
              f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih*{fy}-(ih/zoom*{fy})':d=1:s={W}x{H}:fps={fps}{grade},format=yuv420p")
        run(f"ffmpeg -v error -y -ss {s['ss']} -t {dur} -i '{src}' -vf \"{vf}\" -an -c:v libx264 -preset medium -crf 21 -g {fps} -movflags +faststart '{out}'")
        if not s.get("mute"):
            run(f"ffmpeg -v error -y -ss {s['ss']} -t {dur} -i '{src}' -vn -af \"highpass=f=80,loudnorm=I=-16:TP=-2:LRA=7,"
                f"afade=t=in:d=0.02,afade=t=out:st={dur - 0.04:.3f}:d=0.04\" -ar {SR} -ac 2 '{d}/build/ft/{s['id']}.wav'")
        stamp.write_text(key); print(f"  ▶ {s['id']} {dur:.2f}s")
    # B-roll untuk kartu (tanpa suara): dipotong & di-crop ke ukuran kartu
    for b in sc.get("broll", []):
        src = d / b["src"]
        if not src.exists(): die(f"B-roll {src} tidak ada")
        bw, bh = b.get("w", 920), b.get("h", 518); dur = round(b.get("to", b.get("ss", 0) + 8) - b.get("ss", 0), 3)
        key = sha(src.stat().st_size, b.get("ss", 0), dur, bw, bh, b.get("crop"), fps)
        out, stamp = d / "preview/media" / f"{b['id']}.mp4", d / "build/ft" / f"{b['id']}.key"
        if out.exists() and stamp.exists() and stamp.read_text() == key and not a.force: print(f"  · {b['id']} (cache)"); continue
        crop = f"crop={b['crop']}," if b.get("crop") else ""
        vf = f"{crop}scale={bw}:{bh}:force_original_aspect_ratio=increase:flags=lanczos,crop={bw}:{bh},fps={fps},format=yuv420p"
        run(f"ffmpeg -v error -y -stream_loop -1 -ss {b.get('ss', 0)} -i '{src}' -t {dur} -vf \"{vf}\" -an -c:v libx264 -preset medium -crf 21 -g {fps} -movflags +faststart '{out}'")
        stamp.write_text(key); print(f"  ▶ B-roll {b['id']} {dur:.2f}s")
    print("✓ footage siap")


# ------------------------------------------------------------------ timeline
def cmd_timeline(a):
    d = Path(a.dir); sc = load(d); t, segs = 0.0, []
    for s in sc["segments"]:
        x = {k: v for k, v in s.items() if k not in ("vo", "src", "text")}
        if s["kind"] == "mg":
            pre, post = s.get("pre", 0.3), s.get("post", 0.35)
            f = sorted((d / "build/tts").glob(f"{s['id']}-*.mp3")) if s.get("vo") else []
            if s.get("vo") and not f: die(f"VO {s['id']} belum ada: jalankan tts")
            if f:
                vd = probe_dur(f[0]); ws = time_words(words_of(s["vo"]), vd, f[0])
                for w in ws: w["s"] += pre; w["e"] += pre
                x.update(dur=round(s.get("dur", pre + vd + post), 3), words=ws, audio=str(f[0].relative_to(d)), voStart=pre)
            else: x.update(dur=s.get("dur", 3.0), words=[])
        else:
            dur = round(s["to"] - s["ss"], 3); wav = d / "build/ft" / f"{s['id']}.wav"
            ws = time_words(words_of(s["text"]), dur, wav if wav.exists() else None) if s.get("text") else []
            x.update(dur=dur, words=ws)
        x["t0"] = round(t, 3); t += x["dur"]; segs.append(x)
    look = lambda x: "mg" if x["kind"] == "mg" or x.get("slide") else "ft"   # footage bersuara tapi tampil sebagai slide = "mg"
    for i, x in enumerate(segs): x["swipe"] = x.get("swipe", i > 0 and (look(x) == "mg" or look(segs[i - 1]) == "mg"))
    tl = {"title": sc.get("title", "Venturo"), "w": sc.get("w", 1080), "h": sc.get("h", 1920), "total": round(t, 3), "segs": segs}
    (d / "build/timeline.json").write_text(json.dumps(tl, indent=1, ensure_ascii=False))
    print(f"✓ timeline {len(segs)} segmen, total {t:.2f}s")
    for x in segs: print(f"   {x['t0']:6.2f}  {x['kind']}  {x['id']:<12} {x['dur']:.2f}s")


# ------------------------------------------------------------------ audio
def cmd_audio(a):
    import numpy as np
    from scipy.signal import butter, sosfilt
    d = Path(a.dir); sc = load(d); tl = json.loads((d / "build/timeline.json").read_text()); TOTAL = tl["total"]; N = int(TOTAL * SR) + SR
    rng = np.random.default_rng(7)
    def rd(p, norm_i=None):
        tmp = d / "build/_tmp.wav"; af = f"-af loudnorm=I={norm_i}:TP=-2:LRA=9" if norm_i else ""
        run(f"ffmpeg -v error -y -i '{p}' -vn {af} -ar {SR} -ac 2 -f wav '{tmp}'")
        w = wave.open(str(tmp)); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768
    def place(buf, sig, t, g=1.0):
        i = int(round(t * SR)); j = min(len(buf), i + len(sig))
        if 0 <= i < len(buf): buf[i:j] += sig[: j - i] * g
    def st(m, pan=0.0): return np.stack([m * np.cos((pan + 1) * np.pi / 4) * 1.414, m * np.sin((pan + 1) * np.pi / 4) * 1.414], 1)
    def flt(x, kind, f, o=2): return sosfilt(butter(o, f, kind, fs=SR, output="sos"), x, axis=0)
    T = lambda dd: np.arange(int(dd * SR)) / SR
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    nrm = lambda x: x / (np.abs(x).max() + 1e-9)

    # --- suara: VO TTS + ucapan footage
    voice = np.zeros((N, 2), np.float32)
    for s in tl["segs"]:
        if s["kind"] == "mg" and s.get("audio"): place(voice, rd(d / s["audio"], -16), s["t0"] + s.get("voStart", .3), s.get("gain", 1))
        if s["kind"] == "ft" and (d / "build/ft" / f"{s['id']}.wav").exists() and not s.get("mute"):
            place(voice, rd(d / "build/ft" / f"{s['id']}.wav"), s["t0"], s.get("gain", 1))
    mono = np.abs(voice).mean(1); win = int(.05 * SR)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(win) / win, "same")); act = np.clip((env - .012) / .03, 0, 1)
    sm, v = np.zeros_like(act), 0.0
    up, dn = 1 - np.exp(-64 / (.04 * SR)), 1 - np.exp(-64 / (.45 * SR))
    for i in range(0, len(act), 64): tg = act[i]; v += (tg - v) * (up if tg > v else dn); sm[i:i + 64] = v
    duck = 1 - .62 * sm

    # --- SFX halus
    def swipe(dd=.42):
        t = T(dd); n = flt(rng.standard_normal((len(t), 2)), "band", [500, 3800]); k = t / dd
        return n * (np.sin(np.pi * np.clip(k, 0, 1) ** .75) ** 2)[:, None] * np.stack([1 - .5 * k, .5 + .5 * k], 1) * .5
    def tap():
        t = T(.05); return st(flt(rng.standard_normal(len(t)), "band", [2200, 6000]) * np.exp(-t * 160) * .6 + .35 * np.sin(2 * np.pi * 1750 * t) * np.exp(-t * 110))
    def pop():
        t = T(.12); ph = 2 * np.pi * np.cumsum(480 + 520 * np.clip(t / .045, 0, 1)) / SR; return st(np.sin(ph) * np.exp(-t * 38) * np.clip(t / .003, 0, 1))
    def thump():
        t = T(.4); ph = 2 * np.pi * np.cumsum(52 + 60 * np.exp(-t * 25)) / SR
        return st(np.sin(ph) * np.exp(-t * 9) + flt(rng.standard_normal(len(t)), "low", 1800) * np.exp(-t * 90) * .35)
    def chime(f=1568):
        t = T(1.4); s = np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 2) + .12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 4)
        return st(s * np.exp(-t * 3.2) * np.clip(t / .004, 0, 1))
    LIB = {"swipe": (nrm(swipe()), .11), "tap": (nrm(tap()), .09), "pop": (nrm(pop()), .10), "thump": (nrm(thump()), .25), "chime": (nrm(chime()), .06)}
    sfx = np.zeros((N, 2), np.float32); gs = sc.get("sfxVolume", 1.0)
    for s in tl["segs"]:
        if s.get("swipe"): place(sfx, LIB["swipe"][0], s["t0"] - .22, LIB["swipe"][1] * gs)
        for item in s.get("sfx", []):
            anchor, kind, g = (item + [None])[:3]
            if isinstance(anchor, str):
                hit = [w for w in s.get("words", []) if w["w"].lower().strip(".,!?:").startswith(anchor.lower())]
                if not hit: print(f"  ! sfx {s['id']}: kata '{anchor}' tidak ditemukan"); continue
                lt = hit[0]["s"]
            else: lt = anchor
            place(sfx, LIB[kind][0], s["t0"] + lt, (g if g is not None else LIB[kind][1]) * gs)

    # --- backsound: file dari sound/ (diulang) atau "synth" (lo-fi orisinal 92 BPM)
    bgm = np.zeros((N, 2), np.float32); mode = sc.get("bgm", "synth")
    if mode and mode != "synth":
        p = d / "sound" / mode
        if not p.exists() and os.environ.get("BACKSOUND_DIR"): p = Path(os.environ["BACKSOUND_DIR"]) / mode
        if not p.exists(): die(f"backsound {mode} tidak ada di sound/ atau $BACKSOUND_DIR")
        m = rd(p, -20); reps = int(np.ceil(N / len(m))); bgm = np.tile(m, (reps, 1))[:N] * 1.6
    elif mode == "synth":
        beat = 60 / 92; bar = 4 * beat
        CH = [(41, [53, 57, 60, 64]), (40, [52, 55, 59, 62]), (38, [53, 57, 60, 64]), (34, [53, 57, 58, 62])]
        def ep(f, dd=1.6, vel=1.):
            t = T(dd); s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 1.9) + .42 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3.2) + .12 * np.sin(6 * np.pi * f * t) * np.exp(-t * 5))
            return s * np.clip(t / .004, 0, 1) * (1 + .08 * np.sin(2 * np.pi * 4.6 * t)) * np.clip((dd - t) / .15, 0, 1) * vel
        def pad(fr, dd):
            t = T(dd); e = np.clip(t / .9, 0, 1) * np.clip((dd - t) / .9, 0, 1)
            L = sum(np.sin(2 * np.pi * f * .998 * t) for f in fr); R = sum(np.sin(2 * np.pi * f * 1.002 * t + .7) for f in fr)
            return np.stack([L, R], 1) * e[:, None] / len(fr)
        def bass(f, dd): t = T(dd); return (np.sin(2 * np.pi * f * t) + .22 * np.sin(4 * np.pi * f * t)) * np.clip(t / .01, 0, 1) * np.exp(-t * 2.2) * np.clip((dd - t) / .05, 0, 1)
        def kick(): t = T(.35); return np.sin(2 * np.pi * np.cumsum(48 + 70 * np.exp(-t * 32)) / SR) * np.exp(-t * 11)
        def rim(): t = T(.18); return flt(rng.standard_normal(len(t)), "band", [900, 4500]) * np.exp(-t * 32) * .6 + .4 * np.sin(2 * np.pi * 330 * t) * np.exp(-t * 45)
        def shk(): t = T(.08); return flt(rng.standard_normal(len(t)), "high", 6000, 4) * np.exp(-t * 70)
        segs = tl["segs"]; d_in = segs[1]["t0"] if len(segs) > 1 else 0; d_out = segs[-1]["t0"] if segs[-1]["kind"] == "mg" and len(segs) > 2 else TOTAL
        for b in range(int(np.ceil(TOTAL / bar)) + 1):
            t0 = b * bar; bs, vc = CH[b % 4]
            place(bgm, pad([mtof(m) for m in vc], bar + .6), t0, .10)
            for k, m in enumerate(vc):
                place(bgm, st(ep(mtof(m), 1.8, .9), -.3 + .2 * k), t0 + .012 * k, .085)
                if k % 2 == 0: place(bgm, st(ep(mtof(m + 12 if k == 0 else m), 1., .5), .25), t0 + 1.5 * beat + .01 * k, .07)
            place(bgm, st(ep(mtof(vc[-1] + 12), .9, .4), .4), t0 + 3 * beat, .05)
            if t0 >= d_in - bar: place(bgm, st(bass(mtof(bs), 1.1 * beat)), t0, .32); place(bgm, st(bass(mtof(bs), .8 * beat)), t0 + 2.5 * beat, .22)
            if d_in - .05 <= t0 < d_out:
                for q in range(4):
                    if q in (0, 2): place(bgm, st(kick()), t0 + q * beat, .42)
                    if q in (1, 3): place(bgm, st(rim(), .1), t0 + q * beat, .10)
                place(bgm, st(kick()), t0 + 2.5 * beat, .22)
                for e in range(8): place(bgm, st(shk(), .35), t0 + e * beat / 2 + (.035 if e % 2 else 0), .05 if e % 2 else .032)
        bgm = np.tanh(flt(bgm, "low", 7000) * 1.4) / 1.4
    fin = np.clip(np.arange(N) / (.6 * SR), 0, 1) * np.clip((TOTAL - np.arange(N) / SR) / 1.6, 0, 1)
    bgm *= fin[:, None]

    def wr(p, x):
        x = np.clip(x[: int(TOTAL * SR)] * .5, -1, 1); w = wave.open(str(p), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
    g = sc.get("bgmVolume", .26)
    mixes = {"full": voice + sfx + bgm * g * duck[:, None], "tanpa-musik": voice + sfx, "vo-saja": voice}
    for k, m in mixes.items():
        wr(d / f"build/audio-{k}.wav", m)
        run(f"ffmpeg -v error -y -i '{d}/build/audio-{k}.wav' -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar {SR} '{d}/build/audio-{k}-norm.wav'")
    run(f"ffmpeg -v error -y -i '{d}/build/audio-full-norm.wav' -c:a libmp3lame -b:a 160k '{d}/preview/media/audio.mp3'")
    print("✓ audio: preview/media/audio.mp3 (+ versi tanpa musik & VO saja di build/)")


# ------------------------------------------------------------------ build preview
def cmd_build(a):
    d = Path(a.dir); tl = json.loads((d / "build/timeline.json").read_text()); pv = d / "preview"; (pv / "media").mkdir(parents=True, exist_ok=True)
    wide = tl["w"] > tl["h"]
    shutil.copy(BRAND / "assets" / ("bg-16x9.jpg" if wide else "bg-9x16.jpg"), pv / "media/bg.jpg")
    shutil.copy(BRAND / "assets" / "logo-web.png", pv / "media/logo.png")
    tpl = (BRAND / "templates/player.html").read_text()
    scenes = (BRAND / "templates/pola.js").read_text() + "\n/* ---- scenes.js proyek ---- */\n" + (d / "scenes.js").read_text()
    css = (d / "style.css").read_text() if (d / "style.css").exists() else ""
    html = tpl.replace("/*TITLE*/", tl["title"]).replace("/*DATA*/", json.dumps(tl, ensure_ascii=False)).replace("/*SCENES*/", scenes).replace("/*CSS*/", css)
    (pv / "index.html").write_text(html)
    miss = [s["id"] for s in tl["segs"] if s["kind"] == "ft" and not (pv / "media" / f"{s['id']}.mp4").exists()]
    if miss: print("  ! footage belum dipotong:", miss)
    if not (pv / "media/audio.mp3").exists(): print("  ! audio belum dibuat (jalankan audio)")
    print(f"✓ preview: {pv / 'index.html'}  (buka di browser, atau publish folder preview/ sebagai halaman)")

def cmd_all(a):
    for f in (cmd_tts, cmd_cut, cmd_timeline, cmd_audio, cmd_build): f(a)


# ------------------------------------------------------------------ shots & render (Playwright)
def page_ctx(d, p, scale=1.0):
    tl = json.loads((d / "build/timeline.json").read_text())
    b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg = b.new_page(viewport={"width": tl["w"], "height": tl["h"]}, device_scale_factor=scale)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((d / "preview/index.html").resolve().as_uri() + "?render=1"); pg.wait_for_timeout(1500)
    pg.evaluate("document.fonts && document.fonts.ready")
    return b, pg, tl, errs

def cmd_shots(a):
    import io
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageDraw
    d = Path(a.dir); ts = [float(x) for x in a.at.split(",")] if a.at else None
    with sync_playwright() as p:
        b, pg, tl, errs = page_ctx(d, p, .5)
        ts = ts or [round(s["t0"] + min(s["dur"] * .7, s["dur"] - .1), 2) for s in tl["segs"]]
        ims = []
        for t in ts:
            pg.evaluate(f"window.__renderAsync({t})"); pg.wait_for_timeout(120)
            ims.append(Image.open(io.BytesIO(pg.screenshot(type="jpeg", quality=80))))
        b.close()
    w, h = ims[0].size; n = min(6, len(ims)); rows = (len(ims) + n - 1) // n
    sh = Image.new("RGB", (w * n, (h + 24) * rows), "white"); dr = ImageDraw.Draw(sh)
    for i, (t, im) in enumerate(zip(ts, ims)):
        x, y = (i % n) * w, (i // n) * (h + 24); sh.paste(im, (x, y + 24)); dr.text((x + 6, y + 6), f"{t}s", fill="black")
    out = d / "build/shots.png"; sh.save(out); print(f"✓ {out}  {errs[:3] if errs else ''}")

def cmd_render(a):
    from playwright.sync_api import sync_playwright
    d = Path(a.dir); fps = a.fps; (d / "renders").mkdir(exist_ok=True)
    name = a.name or json.loads((d / "script.json").read_text()).get("slug", d.name)
    silent = d / "build/_video.mp4"
    with sync_playwright() as p:
        b, pg, tl, errs = page_ctx(d, p)
        nf = int(round(tl["total"] * fps))
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), str(silent)], stdin=subprocess.PIPE)
        for f in range(nf):
            pg.evaluate(f"window.__renderAsync({f / fps})")
            enc.stdin.write(pg.screenshot(type="jpeg", quality=93))
            if f % (fps * 5) == 0: print(f"  {f / fps:5.1f}s / {tl['total']:.1f}s")
        enc.stdin.close(); enc.wait(); b.close()
    if errs: print("  ! error halaman:", errs[:3])
    for k, suf in [("full", ""), ("tanpa-musik", "-tanpa-musik"), ("vo-saja", "-vo-saja")]:
        aud = d / f"build/audio-{k}-norm.wav"
        if not aud.exists(): continue
        run(f"ffmpeg -v error -y -i '{silent}' -i '{aud}' -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart '{d}/renders/{name}{suf}.mp4'")
        print(f"✓ renders/{name}{suf}.mp4")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    for c in ["init", "check-tts", "tts", "cut", "timeline", "audio", "build", "all", "shots", "render"]:
        q = sp.add_parser(c); q.add_argument("dir")
        if c in ("tts", "cut", "all"): q.add_argument("--force", action="store_true")
        if c == "init": q.add_argument("--wide", action="store_true", help="16:9 1920x1080")
        if c == "shots": q.add_argument("--at", default="")
        if c == "render": q.add_argument("--fps", type=int, default=60); q.add_argument("--name", default="")
    a = ap.parse_args()
    if a.cmd == "all" and not hasattr(a, "force"): a.force = False
    {"init": cmd_init, "check-tts": cmd_check_tts, "tts": cmd_tts, "cut": cmd_cut, "timeline": cmd_timeline, "audio": cmd_audio,
     "build": cmd_build, "all": cmd_all, "shots": cmd_shots, "render": cmd_render}[a.cmd](a)

if __name__ == "__main__":
    main()
