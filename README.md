# venturo-content-skills

Skill agent khusus untuk membuat konten video **Venturo — Expert Programmers**: reels/Shorts **9:16** atau YouTube **16:9**, dengan template dan bahasa visual Venturo (latar putih, pola biner di pojok, headline Montserrat gelap + teal, kartu & pill miring, transisi geser ala carousel IG).

Alurnya sama untuk semua tipe: **pertanyaan konfirmasi → storyboard → preview yang tinggal di-play (tanpa render) → approve → render → QC.**

| Skill | Konten | Kapan dipakai |
|---|---|---|
| [`venturo-brand`](skills/venturo-brand/SKILL.md) | Dasar semua tipe | Template, aset, design system, aturan konten (tanpa info dobel, soft selling), pipeline `venturo.py` |
| [`venturo-motion-grafik`](skills/venturo-motion-grafik/SKILL.md) | 1. Motion grafik + narasi TTS | Mitos-fakta, tanpa-vs-dengan, tips, kabar berdampak; bisa diselingi footage |
| [`venturo-vlog`](skills/venturo-vlog/SKILL.md) | 2. Vlog | Behind-the-scenes tim, kunjungan klien, event |
| [`venturo-ngobrol`](skills/venturo-ngobrol/SKILL.md) | 3. Talking-head | Rekaman bicara ke kamera + caption, kartu yang menyala per kata, slide & B-roll |
| [`venturo-animasi-2d`](skills/venturo-animasi-2d/SKILL.md) | 4. Animasi 2D | Adegan ilustrasi flat Venturo yang benar-benar bergerak |

## Instal

```bash
git clone <url repo ini> venturo-content-skills
cd venturo-content-skills
./install.sh claude     # ~/.claude/skills
./install.sh codex      # ~/.codex/skills
./install.sh all        # semua target + ~/.agents/skills
./install.sh x --dir /path/ke/folder/skills
```
Kelima folder dipasang berdampingan (skill konten membaca `../venturo-brand`). Restart agent setelah instal.

## Kebutuhan

- Python 3, `ffmpeg`/`ffprobe`
- `pip install numpy scipy pillow playwright faster-whisper` lalu `python3 -m playwright install chromium`
- Internet saat preview/render (font Montserrat dari Google Fonts, server TTS)
- TTS: `export TTS_API_KEY=...` (**jangan pernah ditulis ke file atau di-commit**). Server default `https://tts.venturo.pro/v1/audio/speech`, bisa diganti lewat `TTS_URL`.

## Mulai cepat

```bash
V=skills/venturo-brand/scripts/venturo.py
python3 $V init ~/konten/owner-sistem     # contoh bawaan: "Owner jadi sistem berjalan"
export TTS_API_KEY=...
python3 $V all ~/konten/owner-sistem      # → preview/index.html, tinggal play
python3 $V render ~/konten/owner-sistem --fps 60   # setelah approve
```

## Isi `venturo-brand`

```
assets/        background-biner.jpg (template), logo Venturo, bg 9:16 & 16:9, referensi-ig/ (postingan asli)
templates/     player.html (player preview + mesin render), pola.js (pola scene), contoh script.json & scenes.js, storyboard.md, qc.md
references/    design-system.md, aturan-konten.md, pipeline.md
scripts/       venturo.py (TTS, potong footage, timing kata, audio + backsound lo-fi orisinal, build preview, shots, render)
```

## Catatan

- Logo, template, dan referensi IG adalah aset milik Venturo; pakai hanya untuk konten Venturo.
- Footage berisi wajah orang tidak disimpan di repo ini; taruh di folder `footage/` masing-masing proyek.
- Topik yang sudah ditolak: PRD. Daftar pilar & pola cerita ada di `references/aturan-konten.md`.
