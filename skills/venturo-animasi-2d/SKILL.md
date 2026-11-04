---
name: "venturo-animasi-2d"
description: "Animasi 2D ilustrasi vektor bergaya flat Venturo (latar putih, palet teal/hijau/lime, karakter orisinal) untuk cerita masalah bisnis: owner kewalahan, nota menumpuk, data mengalir ke sistem. Dipakai saat konten Venturo butuh adegan yang benar-benar bergerak, bukan hanya kartu dan teks."
---

# Venturo · Tipe 4 — Animasi 2D

**Baca dulu `../venturo-brand/SKILL.md`.** Animasi 2D Venturo memakai bahasa visual yang sama dengan carousel: latar putih + biner di pojok, palet teal `#168897` / tealD `#0F6F7A` / hijau `#4CBD8A` / lime `#8FCB6B` / ink `#1E2A2E`, garis tegas, bentuk flat, tanpa gradasi, glow, atau 3D.

## Gerbang 1 — Pertanyaan konfirmasi (maks 4 per ronde)
1. Adegan apa saja dan **apa yang bergerak** di tiap adegan? (contoh: "nota berjatuhan menumpuk di meja owner, lalu tersedot ke HP dan rapi jadi tabel")
2. Rasio & durasi (15–40 dtk disarankan)?
3. Karakter: owner/admin/kurir orisinal (berapa, ciri umum) atau objek saja? Tidak boleh tokoh/maskot milik orang lain.
4. Narasi TTS / musik + teks / tanpa teks? CTA penutup?

## Teknik (di dalam pipeline brand)
Animasi ditulis sebagai scene `mg` di `scenes.js` dengan `build` (SVG inline) + `update(r, t)` — semua posisi adalah **fungsi waktu** (tanpa `Math.random()` tak ber-seed, tanpa timer), jadi preview dan render identik.
- **Lapisan**: latar (pola biner pojok) → objek jauh (pucat) → objek utama → teks/kartu.
- **Gerak dasar**: `enter()` untuk masuk, `Math.sin(2πft)` untuk goyang/napas, `draw()` untuk garis tergambar, PRNG ber-seed untuk partikel (nota jatuh, notifikasi beterbangan): posisi = `y0 + speed*t`, dihitung ulang tiap frame.
- **Karakter**: grup SVG per bagian (kepala, badan, lengan) dengan `transform-origin` di sendi; antisipasi sebelum gerak besar, follow-through kecil. Ekspresi lewat ganti bentuk mata/mulut.
- **Kamera**: bungkus adegan dalam satu grup dan geser/zoom grupnya (ease in-out), bukan elemen satu per satu.
- Teks tetap mengikuti design system (headline Montserrat, label italic, pill). Akhiri dengan `POLA.cta`.
- Batasi elemen bergerak ±300 per frame supaya preview lancar di HP.

## Gerbang 2 — Storyboard animasi
Tabel per adegan: durasi, lapisan, daftar elemen bergerak + parameternya, teks, SFX (pop/tap/chime, halus), transisi (geser carousel). Minta approval.

## Preview, render, QC
`all` → `shots` (lihat awal/tengah/akhir tiap adegan) → kirim `preview/` → setelah approve `render --fps 60` → `qc.md`. Tambahan QC: tidak ada kedip/lompatan posisi antar frame, partikel tidak menggumpal, gerak karakter tidak meluncur.
