---
name: "venturo-motion-grafik"
description: "Konten motion grafik Venturo (reels 9:16 / YouTube 16:9) bergaya carousel IG Venturo, narasi TTS, bisa diselingi footage. Dipakai saat diminta konten Venturo berupa explainer, mitos-fakta, tanpa-vs-dengan, tips, atau berita yang berdampak ke bisnis."
---

# Venturo · Tipe 1 — Motion Grafik (+ selingan footage)

**Baca dulu `../venturo-brand/SKILL.md`** beserta `references/design-system.md` dan `references/aturan-konten.md`. Semua desain, aturan isi, dan pipeline berasal dari sana. Jangan langsung membuat video; ikuti gerbang.

Bentuk akhirnya seperti carousel IG Venturo yang bergerak: slide putih ber-logo, headline gelap + teal, kartu/pill/tabel yang muncul mengikuti narasi, berpindah slide dengan geser.

## Gerbang 1 — Pertanyaan konfirmasi (maks 4 per ronde, rekomendasi di opsi pertama)
**Ronde A**
1. Topik & pilar (hari-hari owner / AI nyata / kasus Venturo / kabar berdampak)? Satu kalimat masalah yang mau dijawab.
2. Rasio: 9:16 / 16:9 / keduanya? Durasi: 25–40 dtk (disarankan) / 40–60 / > 60?
3. Suara: TTS (sebut voice, mis. gilang) / VO rekaman sendiri di `sound/` / musik + teks saja?
4. Pola cerita: mitos→fakta / detektif masalah / balapan tanpa-vs-dengan / studi kasus?
**Ronde B**
5. Scene bukti Venturo: sistem/demo/kasus nyata mana yang boleh tampil? (screenshot/rekaman layar di `konten/` atau `footage/`)
6. CTA bernilai: keyword komen apa + tawaran gratis apa (cek gratis / checklist / konsultasi WA)?
7. Ada footage untuk diselingkan (talking-head, B-roll kantor)? Bagian mana?
8. Backsound: file di `sound/` / musik lo-fi orisinal (synth) / tanpa musik?
Jangan menebak topik, CTA, dan bukti — tiga hal itu menentukan soft selling.

## Gerbang 2 — Naskah & storyboard
- Isi `production/storyboard.md` (template di brand). Satu ide per slide, slide 3–9 dtk, total ±25–45 dtk.
- Petakan setiap slide ke pola: `POLA.mitos` (hook), `POLA.chat` (pain nyata), `POLA.banding` (tanpa vs dengan), `POLA.daftar` (langkah/isi), `POLA.panel` (kesimpulan), `POLA.cta` (penutup). Footage pakai segmen `ft`.
- Tulis VO yang **melengkapi** teks layar (bukan membacakannya). Kalimat ≤ 12 kata. Hook 2 detik pertama.
- Minta approval.

## Produksi
```bash
V=../venturo-brand/scripts/venturo.py      # sesuaikan path instalasi
python3 $V init <proyek>                   # --wide untuk 16:9
# isi script.json (segments) & scenes.js (SC.<id> = POLA...)
export TTS_API_KEY=...
python3 $V all <proyek> && python3 $V shots <proyek>
```
Lihat `build/shots.png` sendiri: slide kosong, teks tabrakan, zona UI, dobel informasi. Perbaiki di `scenes.js` lalu `build` ulang (TTS tidak dipanggil lagi kalau VO tidak berubah).

## Gerbang 3 — Preview tanpa render
Kirim halaman `preview/` (publish sebagai halaman/artifact atau zip) + 1–2 kalimat. User tinggal play. Revisi per slide → `build`/`all` ulang. Render hanya setelah approve.

## Render & QC
`python3 $V render <proyek> --fps 60` → 3 versi di `renders/`. Jalankan checklist `../venturo-brand/templates/qc.md`, kirim file + 1 kalimat konteks. Kalau 9:16 dan 16:9 diminta, buat proyek 16:9 terpisah (layout dirancang ulang, bukan di-crop).
