---
name: "venturo-ngobrol"
description: "Konten talking-head Venturo: rekaman orang bicara ke kamera + caption bersih + kartu/teks yang menyala sesuai ucapan + selingan slide motion & B-roll, bergaya template Venturo. Dipakai saat user mengirim rekaman bicara ke kamera untuk akun Venturo."
---

# Venturo · Tipe 3 — Ngobrol (talking-head + kartu + slide + B-roll)

**Baca dulu `../venturo-brand/SKILL.md`** (design system, aturan konten, pipeline). Gaya talking-head Venturo **terang dan bersih**, bukan editorial gelap: footage apa adanya, logo kiri atas, caption kotak putih, kartu putih yang muncul saat kata diucapkan, dan slide motion carousel untuk penjelasan.

## Gerbang 0 — Intake rekaman (sebelum bertanya soal cerita)
1. `ffprobe` semua klip (durasi, fps, rotasi, `creation_time`); contact sheet 1 fps — **lihat semua**.
2. Transkrip kata-per-kata `faster-whisper` (bahasa Indonesia), lalu **koreksi** istilah/nama. Whisper sering salah dengar.
3. Cari awal–akhir ucapan nyata dari energi audio; buang jeda, filler, ulangan. Catat kandidat `ss/to` per kalimat di `production/storyboard.md`.
4. Kalimat yang terpotong/tidak jelas ditandai "perlu konfirmasi", jangan ditebak.

## Gerbang 1 — Pertanyaan konfirmasi (maks 4 per ronde)
**Ronde A**
1. Siapa pembicaranya dan apa pesan utamanya? Ini dari naskah atau improvisasi?
2. Rasio 9:16 (disarankan) / 16:9 / keduanya? Durasi target?
3. Selingan: slide motion + narasi TTS di antara rekaman (disarankan) / kartu di atas rekaman saja / B-roll?
4. Pola cerita & CTA bernilai (keyword + tawaran gratis)?
**Ronde B**
5. Scene bukti Venturo yang boleh tampil (sistem/demo/kasus)?
6. Bagian yang perlu kartu menyala per kata (definisi, daftar, angka) — caption di bagian itu dimatikan.
7. Wajah orang lain / data sensitif di rekaman: blur?
8. Backsound: `sound/` / synth lo-fi / tanpa musik?

## Aturan khusus talking-head
- Setiap kalimat diberi salah satu: **caption** (default), **kartu ucapan** (`POLA.kartuUcapan`, caption mati), **kartu B-roll** (`POLA.kartuBroll`, tanpa suara), atau **pindah ke slide motion** (TTS menjelaskan, wajah tidak tampil).
- Tidak boleh ada elemen yang mengulang ucapan (mis. tombol "Follow" saat ia bilang "follow"). Teks layar hanya menambah: terjemahan istilah, angka, daftar, perbandingan.
- Jump-cut antar potongan footage boleh (tanpa transisi); perpindahan footage ↔ slide = geser carousel (otomatis).
- Push-in ringan per potongan (`zoom: [1.0, 1.06]`, variasikan) supaya tidak statis. `focusY` menjaga wajah tetap di sepertiga atas.
- **Campur footage + teks, bukan motion grafik saja**: selang-seling wajah (caption + kartu angka/chip) dengan B-roll **full 9:16** (`slide: true` + `POLA.brollFull`, teks kotak putih di atas footage) yang tetap memakai suara asli. B-roll tanpa wajah orang (tangan, layar, benda). Pola ini dipakai di konten "Update keamanan Android Nov 2026".
- B-roll stok: Mixkit/Pexels (lihat `references/pipeline.md`), tampil di kartu. Berita/klaim teknis wajib diverifikasi ke sumber resmi; tampilkan sumber kecil di kartu/chip.
- Ucapan asli dinormalisasi otomatis; musik turun saat bicara.

## Produksi, preview, render
Sama dengan pipeline brand: `init` → isi `script.json` (segmen `ft` dengan `text` hasil koreksi + segmen `mg` untuk slide) & `scenes.js` → `all` → `shots` (cek sendiri) → kirim `preview/` untuk di-play → setelah approve `render --fps 60` → checklist `qc.md`. Rekaman horizontal untuk 9:16 direframe otomatis (crop ke wajah lewat `focusY`), jangan letterbox.
