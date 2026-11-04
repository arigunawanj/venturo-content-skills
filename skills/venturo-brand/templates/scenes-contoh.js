/* scenes.js proyek — satu entri SC.<id> per segmen di script.json.
   Pakai POLA.* (templates/pola.js) supaya gaya Venturo konsisten. Waktu "at" boleh kata VO ('benarkah') atau detik.
   Segmen footage tanpa entri di sini otomatis tampil: video + logo + caption.
   ATURAN: teks layar tidak boleh mengulang kalimat yang sedang diucapkan (lihat references/aturan-konten.md). */

SC.hook = POLA.mitos({
  label: 'Sistem untuk UMKM',
  kutipan: '“Bisnis kecil belum|butuh sistem.”',
  bantah: 'Faktanya, justru sebaliknya.',
  coretAt: 'padahal', bantahAt: 'benarkah',
});

SC.chat = POLA.chat({
  label: 'Fakta 1', counter: '1 / 3',
  h1: 'Owner jadi', h1b: '“sistem” berjalan', h2At: 'lagi',
  nama: 'HP Owner', status: 'Sedang libur keluarga',
  bubble: [{ t: 'Stok gula masih ada, Bu?', at: 'libur' }, { t: 'Pelanggan minta diskon, boleh?', at: 'semua' }, { t: 'Harga terbaru yang mana ya?', at: 'lari' }],
  pillsLabel: 'Semua lewat:', pills: [{ t: 'Owner', at: 'pertanyaan' }, { t: 'Owner' }, { t: 'Owner lagi' }],
});

SC.banding = POLA.banding({
  label: 'Bedanya', counter: '2 / 3',
  h1: 'Tanpa sistem vs', h1b: 'dengan sistem',
  kolom: ['HAL', 'TANPA', 'DENGAN'],
  rows: [['Stok', 'Tanya owner', 'Cek di sistem', 'kerasa'], ['Harga', 'Cari di chat', 'Satu daftar resmi', 'sehari'], ['Laporan', 'Rekap manual', 'Otomatis tiap sore', 'nunggu']],
});

SC.mulai = POLA.daftar({
  label: 'Mulai kecil', counter: '3 / 3',
  h1: 'Satu alur dulu,', h2: 'baru berkembang',
  items: [
    { judul: 'Order', sub: 'Pesanan tercatat, tidak terselip di chat', ikon: 'chat', at: 'order' },
    { judul: 'Stok', sub: 'Tim cek sendiri tanpa tanya owner', ikon: 'book', at: 'stok' },
    { judul: 'Laporan harian', sub: 'Angka penting terkirim tiap sore', ikon: 'file', at: 'laporan' },
  ],
});

SC.cta = POLA.cta({
  label: 'Konsultasi gratis',
  h1: 'Mau mulai', h1b: 'dari mana?',
  keyword: 'SISTEM', ketikAt: 'sistem', pill: 'Kami bantu cek, gratis',
});
