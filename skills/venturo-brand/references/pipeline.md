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
  "bgmVolume": 0.26, "sfxVolume": 1.0, "mediaFps": 60,   // 60 = standar konten Venturo; jangan turunkan
  "segments": [
    { "id": "hook", "kind": "mg", "name": "Hook", "vo": "Narasi TTS, *kata* penekanan.",
      "pre": 0.3, "post": 0.35, "sfx": [["kata", "pop"]] },
    { "id": "s1", "kind": "ft", "name": "Talking head", "src": "footage/IMG_1.MOV", "ss": 5.5, "to": 8.8,
      "text": "Transkrip yang sudah dikoreksi", "caption": true, "zoom": [1.0, 1.06], "focusY": 0.4 },
    { "id": "broll", "kind": "ft", "src": "footage/IMG_2.MOV", "ss": 4.6, "to": 6.4, "mute": true, "grade": "redup", "caption": false },
    { "id": "jeda", "kind": "mg", "dur": 2.5 },
    { "id": "b", "kind": "ft", "slide": true, "src": "footage/IMG_1.MOV", "ss": 9, "to": 14, "text": "…" }
  ],
  "broll": [ { "id": "br_hp", "src": "footage/stock/klip.mp4", "ss": 3, "to": 9.5, "w": 920, "h": 518, "crop": "x:y:w:h (opsional)" } ]
}
```
- `mg` = slide motion (durasi = VO + pre + post, atau `dur`). `ft` = footage (durasi = `to - ss`), direframe otomatis ke rasio proyek dengan push-in `zoom`.
- `sfx`: `[kata atau detik_lokal, "pop|tap|thump|chime|swipe", gain?]`. Swipe di transisi slide sudah otomatis.
- `swipe: false` pada segmen untuk memaksa cut tanpa geser.
- `slide: true` pada segmen `ft`: suara rekaman tetap jalan, tapi layar menampilkan slide (biasanya `POLA.brollSlide` dengan B-roll di kartu). Caption otomatis mati di slide.
- `broll`: klip stok/tambahan tanpa suara, dipotong ke ukuran kartu (default 920×518). Dipakai lewat `BROLL(id)` / `POLA.brollSlide({broll: id})`.

## B-roll stok gratis
Pakai sumber berlisensi bebas komersial: **Mixkit** (`https://assets.mixkit.co/videos/<id>/<id>-720.mp4`, ID dari halaman kategori), **Pexels** (`https://www.pexels.com/download/video/<id>/`). Jangan ambil dari Pinterest/Google Images (hak cipta tidak jelas) dan jangan pakai foto tokoh publik. **B-roll tampil full 9:16 (`POLA.brollFull`)**, teks Venturo dalam kotak putih di atasnya — ini yang sesuai referensi boss; kartu B-roll (`brollSlide`) hanya kalau diminta. Supaya tajam, pakai video 4K/1080p atau foto ≥ 2400 px (Pexels: `https://www.pexels.com/download/video/<id>/`, foto `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?w=2400`); klip 720p jangan dipakai full layar. Atur `focusX/focusY` di entri `broll` supaya objek utama tidak terpotong. **Hindari footage berisi wajah orang** (boss tidak suka model stok) — pilih tangan, layar, benda, suasana. Klip HP layar hijau bisa ditempeli layar buatan sendiri (chroma key dibatasi area layar saja).

## Transkrip footage
Pakai `faster-whisper` (word timestamps) untuk menemukan bagian yang diucapkan, lalu **koreksi manual** dan tulis ke `text`. `ss/to` dipilih dari energi audio (awal & akhir ucapan nyata, buang jeda). Timing per kata dihitung ulang otomatis dari jeda nyata di rekaman.

## scenes.js
`SC.<id> = POLA.<pola>({...})` atau objek `{ build(el, s), update(r, t, s) }` sendiri. `t` = detik lokal segmen. Waktu `at` di pola boleh berupa kata ucapan ('stok') atau detik. Helper: `enter, tf, P, draw, wd, wEnd, LOGO, LBL, CNT, VIDEO, BROLL, ICON, words`. Pola footage: `kartuUcapan` (caption mati, kartu menyala per kata), `kartuAngka` (angka menghitung + caption), `chipFootage` (label/sumber + caption), `kartuBroll`; pola slide B-roll: `brollSlide`. Segmen `ft` tanpa entri = video + logo + caption otomatis.

## Perintah
| Perintah | Fungsi |
|---|---|
| `init <p> [--wide]` | buat proyek dari contoh |
| `check-tts <p>` | uji API TTS (`TTS_API_KEY`, `TTS_URL` opsional; default server Venturo) |
| `all <p>` | tts → cut → timeline → audio → track → build |
| `track <p>` | gabung semua footage + audio jadi satu video (`preview/media/track.mp4` 720p, `build/track-hd.mp4` untuk render) supaya gerak bibir & suara pasti sinkron dan preview tidak tersendat |
| `build <p>` | rakit ulang preview saja (setelah edit scenes.js / style.css) |
| `timeline <p>` + `audio <p>` + `build <p>` | setelah ubah urutan/VO/SFX |
| `shots <p> [--at 1,4.5]` | contact sheet `build/shots.png` |
| `render <p> [--fps 60] [--name x]` | MP4 final + 2 versi audio alternatif |

## Review tanpa render
`preview/` berisi `index.html` + `media/` (track.mp4 = footage + seluruh audio dalam satu file, klip B-roll, bg, logo). Trek ini jadi jam player, jadi gambar dan suara tidak bisa lepas sinkron. Buka lokal di browser, atau publish foldernya sebagai halaman web/artifact; penonton tinggal tekan play dan bisa lompat per scene.

## Kebutuhan
python3, ffmpeg/ffprobe, `pip install numpy scipy playwright pillow faster-whisper`, `python3 -m playwright install chromium`. Font Montserrat dimuat dari Google Fonts (butuh internet saat preview/render).
