---
name: "venturo-brand"
description: "Template, bahasa visual, aturan konten, dan pipeline produksi video Venturo (Expert Programmers). Wajib dibaca sebelum membuat konten Venturo jenis apa pun: reels/carousel, motion grafik, talking-head, vlog, atau animasi 2D."
---

# Venturo Brand — dasar semua konten Venturo

Skill ini adalah "buku brand" yang dipakai keempat skill konten Venturo (`venturo-motion-grafik`, `venturo-ngobrol`, `venturo-vlog`, `venturo-animasi-2d`). Isinya tiga hal: **tampilan** (template + komponen), **isi** (aturan konten), dan **cara produksi** (preview dulu, render setelah approve).

## 1. Tampilan: ikuti template Venturo, bukan gaya "AI"
Baca `references/design-system.md`. Ringkasnya:
- Latar **putih**, pola angka biner (`assets/background-biner.jpg`) **hanya di pojok kanan atas & kiri bawah**, memudar ke tengah.
- Logo **Venturo EXPERT PROGRAMMERS** (`assets/logo-web.png`) kiri atas tiap slide.
- Font **Montserrat**: headline ExtraBold gelap `#1E2A2E`, baris kedua teal `#168897`; label kecil *italic* kapital berspasi dengan kotak teal (■ FAKTA 1).
- Kartu putih datar yang sedikit miring, pill miring teal/hijau/lime, tabel "tanpa vs dengan", panel gelap untuk kesimpulan.
- Transisi antar slide = **geser ala carousel IG**. Antar klip footage = jump cut.
- Dilarang: gradasi pelangi, glow/neon, 3D, emoji sebagai visual, tema gelap editorial, logo/brand AGJ.
Contoh tampilan asli Venturo ada di `assets/referensi-ig/` — lihat semuanya sebelum mendesain.

## 2. Isi: aturan wajib (detail di `references/aturan-konten.md`)
1. **Tidak ada informasi dobel.** Caption hanya untuk orang yang bicara di footage. Saat layar menampilkan kartu/headline yang memuat kata yang sama dengan ucapan, caption dimatikan (kartunya yang menyala per kata). Narasi TTS **melengkapi** teks layar, tidak membacakannya ulang.
2. **Bahasa pemilik bisnis**, bukan istilah developer. Contoh masalah nyata: chat WA tercecer, `Rekap_FINAL_fix2.xlsx`, owner ditanya terus saat libur.
3. **Soft selling**: 80% masalah & solusi, Venturo muncul di satu scene bukti (sistem/demo/kasus nyata) + CTA bernilai (cek gratis, checklist, konsultasi gratis via WA). Tanpa harga, diskon, atau "pesan sekarang".
4. **Jangan mengarang** testimoni, nama klien, angka hasil, atau statistik. Fakta luar wajib ada sumbernya; data klien hanya yang nyata dan diizinkan.
5. Topik yang sudah ditolak boss: **PRD**. Jangan diusulkan lagi.

## 3. Produksi: preview tanpa render → approve → render
Pipeline ada di `scripts/venturo.py` (lihat `references/pipeline.md`):
```bash
V=<folder skill ini>/scripts/venturo.py
python3 $V init <proyek>            # folder: footage/ konten/ sound/ production/ + script.json & scenes.js contoh
export TTS_API_KEY=...               # jangan pernah ditulis ke file
python3 $V all <proyek>             # TTS → potong footage → timing kata → audio → preview/index.html
python3 $V shots <proyek>           # contact sheet untuk dicek sendiri
python3 $V render <proyek> --fps 60 # HANYA setelah user approve preview
```
- `preview/` adalah **halaman player yang tinggal di-play** (audio, footage, motion tersinkron, tombol lompat per scene). Kirim/publish folder ini untuk direview — tidak perlu render dulu.
- Scene ditulis di `scenes.js` memakai **pola siap pakai** `POLA.mitos / chat / daftar / banding / panel / cta / kartuUcapan / kartuBroll` (`templates/pola.js`). Buat pola baru hanya bila tidak ada yang cocok, dan tetap pakai token & komponen design system.
- Render menghasilkan 3 versi: lengkap, `-tanpa-musik` (untuk sound trending di aplikasi), `-vo-saja`.
- Backsound: file dari `sound/` (atau `$BACKSOUND_DIR`) bila ada; kalau tidak, `"bgm": "synth"` = musik lo-fi orisinal (bebas klaim). SFX halus & jarang: swipe otomatis di transisi, pop/tap/chime di momen penting saja.

## Gerbang yang sama untuk semua tipe
1. **Brief** — pilar konten, tujuan, CTA, rasio, durasi, voice (tanya bila kosong).
2. **Naskah & storyboard** (`production/storyboard.md`) — cek aturan dobel informasi & soft selling sebelum minta approval.
3. **Preview** — kirim halaman player + ringkasan 1–2 kalimat, minta komentar.
4. **Render & QC** (`templates/qc.md`) — baru setelah approve.
