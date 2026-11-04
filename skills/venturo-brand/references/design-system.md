# Design system Venturo (video & carousel)

Sumber: template resmi Venturo (`assets/background-biner.jpg`, logo) dan postingan IG Venturo (`assets/referensi-ig/`). Semua sudah dipasang di `templates/player.html`; dokumen ini untuk memahami dan menjaga konsistensinya.

## Warna (token CSS)
| Token | Hex | Dipakai untuk |
|---|---|---|
| `--ink` | `#1E2A2E` | headline, teks utama, caption |
| `--body` | `#46555A` | teks pendukung, label |
| `--muted` | `#7C8B90` | keterangan kecil |
| `--teal` | `#168897` | baris kedua headline, aksen, kata aktif caption, garis coret |
| `--tealD` | `#0F6F7A` | pill utama, header kolom "DENGAN" |
| `--green` | `#4CBD8A` | pill kedua |
| `--lime` | `#8FCB6B` | pill ketiga, border sel "dengan", label di panel gelap |
| `--tag` | `#DCE5E8` | tag "MITOS", header kolom "TANPA" |
| `--soft` | `#F1F4F5` | bubble chat, sel "tanpa" |
| `--okbg` | `#EEF8F1` | latar sel "dengan" |
| `--dark` | `#1F2B2F` | panel kesimpulan |
Gradasi hanya ada di logo. Maksimal 2 warna aksen per slide (teal + satu pill).

## Tipografi
- **Montserrat** (Google Fonts). Headline 800, 96 px (9:16), spasi huruf -2.5px, maksimal 2 baris.
- Baris kedua: teal, 60 px 700 (sub) atau 96 px 800 (lanjutan headline).
- Label: *italic* 500, 26–30 px, KAPITAL, letter-spacing 4px, didahului kotak teal 22 px.
- Isi kartu: judul 46 px 800, sub 31 px 500 `--body`.
- Angka besar: 150 px 900 teal.

## Tata letak 9:16 (1080×1920)
```
  0 ┌───────────────────────────────┐  UI aplikasi (hindari ±0–230)
232 │ [logo 300px]          [1 / 3] │  header slide
360 │ ■ LABEL KECIL                 │
412 │ Headline gelap 2 baris        │
512 │ baris kedua teal              │
660 │ ┌ kartu / tabel / chat ──┐ ○  │  konten utama 660–1300
    │ └────────────────────────┘ ○  │  pill miring di kanan (x 720–930)
1330│ [caption footage]             │  hanya untuk footage
1520│░░ deskripsi & tombol aplikasi ░│  jangan taruh apa pun penting
1920└───────────────────────────────┘
```
Margin kiri 80 px. Kanan 150 px bawah dipakai tombol aplikasi. 16:9 (1920×1080): logo 90/70, label 190, headline 240, caption 880 (kelas `.wide` otomatis).

## Komponen
- **Kartu**: putih, radius 22, bayangan lembut, rotasi -2°…+2°. Bukan kartu tebal 3D.
- **Pill**: radius penuh, 44 px 800, rotasi -5°…+4°, ditumpuk zig-zag (ref IG 01/02).
- **Tag MITOS**: abu `--tag`, kapital tebal, + label italic di sebelahnya.
- **Coretan**: garis teal 8 px melintang kutipan yang salah (`.strike`).
- **Chat card**: avatar bulat tint teal, nama tebal + status abu, bubble abu berselang kiri-kanan.
- **Tabel banding**: header pill abu "× TANPA" vs teal "✓ DENGAN", sel kiri abu, sel kanan hijau muda berbingkai lime.
- **Panel gelap**: `--dark`, label lime italic, teks putih tebal, kata penting lime.
- **Counter**: pill outline "1 / 3" kanan atas untuk seri slide.
- **Caption footage**: kotak putih per baris (box-decoration), teks gelap 60 px 800, kata aktif teal, kata berikutnya abu. Rata kiri x 80, y 1330.
- **Latar**: putih + pola biner di dua pojok (mask radial), opacity ±0.85.

## Gerak
- Elemen masuk bertahap (stagger 0.1–0.3 dtk), ease expo-out; pill & tombol pop (back-out).
- Kartu/baris "menyala" saat katanya diucapkan (opacity 0.16–0.35 → 1).
- Transisi slide: geser horizontal 0.38 dtk (carousel). Tidak ada whip blur, flash, shake, glitch.
- Sesuatu harus berubah tiap 1.5–3 dtk; satu slide maksimal ±9 dtk.
