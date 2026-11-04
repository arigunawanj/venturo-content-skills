# QC sebelum kirim

## Otomatis
- [ ] `ffprobe renders/<nama>.mp4`: 1080×1920 (atau 1920×1080), fps sesuai (60 untuk final), durasi = timeline, ada audio.
- [ ] Loudness ±-14 LUFS (`ffmpeg -i x.mp4 -af ebur128 -f null -`), puncak ≤ -1 dBFS.
- [ ] `venturo.py shots` di tiap segmen: dilihat sendiri, tidak hanya dibuat.

## Tampilan
- [ ] Latar putih + biner hanya di dua pojok; logo EXPERT PROGRAMMERS kiri atas; Montserrat termuat (bukan font cadangan).
- [ ] Tidak ada teks di zona UI (atas < 230, bawah > 1520, kanan bawah 150 px).
- [ ] Tidak ada teks tabrakan/terpotong; headline ≤ 2 baris; caption 1 baris per potongan.
- [ ] Tidak ada slide kosong > 1.5 dtk; tidak ada gaya di luar design system (neon, gradasi, 3D, emoji).

## Isi
- [ ] Tidak ada informasi dobel (layar vs VO vs caption).
- [ ] Soft selling: bukti nyata + CTA bernilai; Venturo ≤ 2×; tanpa harga/diskon.
- [ ] Ejaan & istilah benar; caption footage sesuai ucapan (bukan mentah Whisper).
- [ ] Fakta luar bersumber; tidak ada data klien sensitif terlihat.

## Audio
- [ ] Suara orang & VO jelas, musik turun saat bicara, SFX tidak berisik.
- [ ] Tersedia versi `-tanpa-musik` dan `-vo-saja`.
