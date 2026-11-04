---
name: "venturo-vlog"
description: "Vlog Venturo dari banyak klip (kegiatan tim, kunjungan klien, event, behind-the-scenes kantor) dengan overlay bergaya template Venturo: label lokasi/jam, caption kotak putih, slide pembuka/penutup carousel. Dipakai saat user mengirim banyak footage aktivitas Venturo untuk dijadikan vlog."
---

# Venturo · Tipe 2 — Vlog (behind-the-scenes Venturo)

**Baca dulu `../venturo-brand/SKILL.md`.** Vlog Venturo membuat penonton melihat tim asli bekerja ("Expert Programmers" yang nyata), bukan video promosi. Rapi, hangat, jujur.

## Gerbang 0 — Scan footage
1. `ffprobe` semua klip, urutkan menurut `creation_time`. Contact sheet 1 fps — **lihat semua**. Tandai shot tajam/stabil, momen bicara, momen kerja (layar coding, diskusi, kunjungan klien).
2. Transkrip ucapan (`faster-whisper`) dan koreksi.
3. `production/story-plan.md`: hanya fakta yang terlihat atau diucapkan. Tebakan (nama klien, lokasi, proyek) masuk daftar "perlu konfirmasi".

## Gerbang 1 — Pertanyaan konfirmasi (maks 4 per ronde)
1. Cerita & momen puncaknya? (tawarkan 2–3 alur dari hasil scan)
2. Rasio & durasi (30–60 dtk disarankan; > 90 dtk tawarkan 2 part)?
3. Suara: ucapan asli + ambient / + narasi TTS penghubung (≤ 12 kata) / musik saja?
4. Apa yang **tidak boleh** tampil: layar berisi data klien, wajah klien, nama proyek NDA?
Ronde B: konfirmasi fakta bertanda tebakan; CTA bernilai; backsound.

## Gaya Venturo untuk vlog
- Pembuka: slide carousel 2–3 dtk (`POLA.chat`/`POLA.mitos` atau headline + label "■ BEHIND THE SCENES"), lalu langsung momen paling menarik.
- Di atas footage: logo kiri atas, label kecil lokasi/jam (pill outline atau `.caps` dalam kartu putih kecil), caption kotak putih hanya saat orang bicara.
- Shot 1.5–4 dtk, jump cut di ucapan, B-roll menutupi potongan. Footage ↔ slide = geser carousel.
- Layar komputer yang memuat kode/data klien: blur atau pakai layar demo.
- Penutup: `POLA.cta` dengan soft selling (mis. "Mau sistemmu dikerjakan tim ini? Konsultasi gratis, WA di bio").

## Produksi, preview, render
Segmen `ft` per shot (ss/to dari scan, `mute` untuk B-roll tanpa suara, `text` untuk yang bicara), segmen `mg` untuk pembuka/penutup/penghubung. `all` → `shots` → kirim `preview/` → setelah approve `render --fps 60` → `qc.md`. Footage tambahan datang belakangan: sisipkan menurut jam rekam, `all` ulang (cache dipakai ulang).
