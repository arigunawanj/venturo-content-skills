# Pipeline `scripts/venturo.py`

## Struktur proyek
```
<proyek>/
  script.json      segmen (urutan, VO, footage, SFX) — sumber timeline
  scenes.js        tampilan tiap segmen (SC.<id> = POLA.xxx({...}))
  style.css        (opsional) CSS tambahan khusus video ini
  footage/  konten/  sound/  production/
  build/           cache TTS, wav ucapan, timeline.json, audio mix, shots.png
  preview/         index.html + media/  ← halaman player untuk review (tinggal play)
  renders/         MP4 final (lengkap, -tanpa-musik, -vo-saja)
```

## script.json
```jsonc
{
  "title": "Judul", "slug": "nama-file-render",
  "w": 1080, "h": 1920,                 // 1920x1080 untuk 16:9 (init --wide)
  "voice": "gilang",                    // nama voice server TTS; bisa per segmen
  "ttsExtra": { "instructions": "santai, hangat ..." },
  "bgm": "synth",                       // "synth" | "nama-file.mp3" (di sound/ atau $BACKSOUND_DIR) | null
  "bgmVolume": 0.26, "sfxVolume": 1.0, "mediaFps": 30,
  "segments": [
    { "id": "hook", "kind": "mg", "name": "Hook", "vo": "Narasi TTS, *kata* penekanan.",
      "pre": 0.3, "post": 0.35, "sfx": [["kata", "pop"]] },
    { "id": "s1", "kind": "ft", "name": "Talking head", "src": "footage/IMG_1.MOV", "ss": 5.5, "to": 8.8,
      "text": "Transkrip yang sudah dikoreksi", "caption": true, "zoom": [1.0, 1.06], "focusY": 0.4 },
    { "id": "broll", "kind": "ft", "src": "footage/IMG_2.MOV", "ss": 4.6, "to": 6.4, "mute": true, "grade": "redup", "caption": false },
    { "id": "jeda", "kind": "mg", "dur": 2.5 }
  ]
}
```
- `mg` = slide motion (durasi = VO + pre + post, atau `dur`). `ft` = footage (durasi = `to - ss`), direframe otomatis ke rasio proyek dengan push-in `zoom`.
- `sfx`: `[kata atau detik_lokal, "pop|tap|thump|chime|swipe", gain?]`. Swipe di transisi slide sudah otomatis.
- `swipe: false` pada segmen untuk memaksa cut tanpa geser.

## Transkrip footage
Pakai `faster-whisper` (word timestamps) untuk menemukan bagian yang diucapkan, lalu **koreksi manual** dan tulis ke `text`. `ss/to` dipilih dari energi audio (awal & akhir ucapan nyata, buang jeda). Timing per kata dihitung ulang otomatis dari jeda nyata di rekaman.

## scenes.js
`SC.<id> = POLA.<pola>({...})` atau objek `{ build(el, s), update(r, t, s) }` sendiri. `t` = detik lokal segmen. Waktu `at` di pola boleh berupa kata ucapan ('stok') atau detik. Helper: `enter, tf, P, draw, wd, wEnd, LOGO, LBL, CNT, VIDEO, ICON, words`. Segmen `ft` tanpa entri = video + logo + caption otomatis.

## Perintah
| Perintah | Fungsi |
|---|---|
| `init <p> [--wide]` | buat proyek dari contoh |
| `check-tts <p>` | uji API TTS (`TTS_API_KEY`, `TTS_URL` opsional; default server Venturo) |
| `all <p>` | tts → cut → timeline → audio → build |
| `build <p>` | rakit ulang preview saja (setelah edit scenes.js / style.css) |
| `timeline <p>` + `audio <p>` + `build <p>` | setelah ubah urutan/VO/SFX |
| `shots <p> [--at 1,4.5]` | contact sheet `build/shots.png` |
| `render <p> [--fps 60] [--name x]` | MP4 final + 2 versi audio alternatif |

## Review tanpa render
`preview/` berisi `index.html` + `media/` (audio mp3, footage mp4, bg, logo). Buka lokal di browser, atau publish foldernya sebagai halaman web/artifact; penonton tinggal tekan play dan bisa lompat per scene.

## Kebutuhan
python3, ffmpeg/ffprobe, `pip install numpy scipy playwright pillow faster-whisper`, `python3 -m playwright install chromium`. Font Montserrat dimuat dari Google Fonts (butuh internet saat preview/render).
