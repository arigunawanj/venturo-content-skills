/* =====================================================================
   POLA SCENE VENTURO — fungsi siap pakai, diambil dari carousel IG Venturo.
   Dipakai di scenes.js proyek:  SC.hook = POLA.chat({...});
   Waktu "at" boleh angka (detik lokal segmen) atau kata VO/ucapan ('bukan') → otomatis sinkron.
   ===================================================================== */
const at = (s, x, dflt = 0) => typeof x === 'string' ? (wd(s.id, x) || dflt) : (x ?? dflt);
const tint = { teal: ['#E3F1F3', '#168897'], green: ['#E8F6EE', '#2F9E63'], amber: ['#FFF3E0', '#D9822B'], lime: ['#F0F8E8', '#5E9E3A'] };
const POLA = {};

/** Judul dua baris: h1 gelap + h2 teal (atau h1b teal besar). */
function judul(o) {
  return `<div class="abs h1">${words(o.h1)}</div>` +
    (o.h1b ? `<div class="abs h1 teal" data-r="h1b" style="top:${o.top2 || 512}px">${o.h1b}</div>` : '') +
    (o.h2 ? `<div class="abs h2" data-r="h2" style="top:${o.top2 || 520}px">${o.h2}</div>` : '');
}
function judulIn(r, t, s, o) {
  r.hw.forEach((w, i) => enter(w, t, at(s, o.h1At, .12) + i * .1, { from: 'up', d: 60 }));
  enter(r.h1b, t, at(s, o.h2At, .35), { from: 'up', d: 50 });
  enter(r.h2, t, at(s, o.h2At, .5), { from: 'up', d: 30 });
}

/** MITOS: kutipan keyakinan salah dicoret garis teal, lalu bantahan teal. (ref IG 01) */
POLA.mitos = o => ({
  build: el => el.innerHTML = LOGO + `<div class="abs" data-r="tg" style="left:80px;top:360px;display:flex;gap:20px;align-items:center">
      <span class="tag">${o.tag || 'MITOS'}</span><span class="caps">${o.label || ''}</span></div>
    <div class="abs h1" data-r="q" style="top:450px;font-size:${o.size || 84}px">${o.kutipan.split('|').map(l => `<span class="strike" data-r="st[]" style="white-space:nowrap">${l}</span>`).join('<br>')}</div>
    <div class="abs h2" data-r="h2" style="top:${o.top2 || 450 + o.kutipan.split('|').length * (o.size || 84) * 1.06 + 50}px">${o.bantah}</div>`,
  update(r, t, s) {
    head(r, t); enter(r.tg, t, .1, { from: 'left', d: 40 }); enter(r.q, t, .25, { from: 'up', d: 50 });
    const k0 = at(s, o.coretAt, 1.2); r.st.forEach((x, i) => x.style.setProperty('--k', P(t, k0 + i * .2, k0 + .45 + i * .2, 'io')));
    enter(r.h2, t, at(s, o.bantahAt, k0 + .6), { from: 'up', d: 30 });
  },
});

/** CHAT: kartu chat (klien/HP owner) + pill miring di kanan. (ref IG 02) */
POLA.chat = o => ({
  build: el => el.innerHTML = LOGO + LBL(o.label) + (o.counter ? CNT(o.counter) : '') + judul(o) + `
    <div class="abs card chat" data-r="chat" style="left:80px;top:${o.top || 720}px"><div class="hd"><div class="av">${ICON.user}</div><div><div class="nm">${o.nama}</div><div class="st">${o.status || ''}</div></div></div>
      ${o.bubble.map(b => `<div class="bub" data-r="b[]">“${b.t}”</div>`).join('')}</div>` +
    (o.pills ? `<div class="abs caps" data-r="rk" style="left:720px;top:${(o.top || 720) + 40}px">${o.pillsLabel || ''}</div>` +
      o.pills.map((p, i) => `<div class="abs pill ${['t', 'g', 'l'][i % 3]}" data-r="p[]" style="left:${[720, 770, 735][i % 3]}px;top:${(o.top || 720) + 110 + i * 120}px">${p.t}</div>`).join('') : ''),
  update(r, t, s) {
    head(r, t); judulIn(r, t, s, o);
    enter(r.chat, t, .5, { from: 'up', d: 70, r: -2 });
    o.bubble.forEach((b, i) => enter(r.b[i], t, at(s, b.at, 1 + i * .6), { from: 'up', d: 24, dur: .35 }));
    if (o.pills) { const p0 = at(s, o.pills[0].at, 2.5); enter(r.rk, t, p0 - .1, { from: 'left', d: 30 });
      o.pills.forEach((p, i) => enter(r.p[i], t, at(s, p.at, p0 + i * .3), { from: 'pop', dur: .4, r: [-5, 4, -3][i % 3] })); }
  },
});

/** DAFTAR: 2–4 kartu putih miring, ikon bulat ber-tint, judul + sub. (ref IG 01 kartu) */
POLA.daftar = o => ({
  build: el => el.innerHTML = LOGO + LBL(o.label) + (o.counter ? CNT(o.counter) : '') + judul(o) +
    o.items.map((it, i) => { const [bg, col] = tint[it.warna || ['amber', 'green', 'teal', 'lime'][i % 4]];
      return `<div class="abs card item" data-r="it[]" style="left:${[80, 140, 95, 125][i % 4]}px;top:${(o.top || 700) + i * 200}px">
        <div class="ic" style="background:${bg}">${ICON[it.ikon || 'check'].replace('<svg', `<svg style="stroke:${col}"`)}</div>
        <div><div class="tt">${it.judul}</div><div class="ss">${it.sub || ''}</div></div></div>`; }).join(''),
  update(r, t, s) {
    head(r, t); judulIn(r, t, s, o);
    o.items.forEach((it, i) => {   // kartu muncul samar dulu (ghost), menyala saat kata diucapkan
      const a = at(s, it.at, .9 + i * .5), rot = [-1.5, 1, -1, 1.2][i % 4];
      if (o.ghost === false) return enter(r.it[i], t, a - .15, { from: 'right', d: 140, dur: .55, r: rot });
      enter(r.it[i], t, .45 + i * .12, { from: 'right', d: 140, dur: .55, r: rot });
      const on = P(t, a - .2, a + .1); r.it[i].style.opacity = Math.min(+r.it[i].style.opacity, lerp(.35, 1, on));
      if (t > a - .2) tf(r.it[i], { r: rot, s: lerp(1.05, 1, P(t, a - .2, a + .25, 'back')), o: r.it[i].style.opacity });
    });
  },
});

/** BANDING: tabel "tanpa X vs dengan X". (ref IG 03) rows: [[hal, tanpa, dengan, at?]] */
POLA.banding = o => ({
  build: el => el.innerHTML = LOGO + LBL(o.label) + (o.counter ? CNT(o.counter) : '') + judul(o) + `
    <div class="abs card tbl" data-r="tb" style="left:80px;top:${o.top || 660}px"><div class="tr"><div class="th">${o.kolom?.[0] || 'HAL'}</div><div class="hp x">× ${o.kolom?.[1] || 'TANPA'}</div><div class="hp v">✓ ${o.kolom?.[2] || 'DENGAN'}</div></div>` +
    o.rows.map(([k, a, b]) => `<div class="tr"><div class="k">${k}</div><div class="c x" data-r="cx[]">${a}</div><div class="c v" data-r="cv[]">${b}</div></div>`).join('') + `</div>`,
  update(r, t, s) {
    head(r, t); judulIn(r, t, s, o);
    enter(r.tb, t, .35, { from: 'up', d: 60, r: -.6 });
    r.cx.forEach((x, i) => enter(x, t, .6 + i * .12, { from: 'up', d: 16, dur: .3 }));
    o.rows.forEach((row, i) => enter(r.cv[i], t, at(s, row[3], 1.2 + i * .5), { from: 'pop', dur: .38 }));
  },
});

/** PANEL: kesimpulan di panel gelap (label hijau). Bisa ditempel ke pola lain via o.panel. */
POLA.panel = o => ({
  build: el => el.innerHTML = LOGO + LBL(o.label) + judul(o) +
    `<div class="abs panel" data-r="pn" style="left:80px;top:${o.top || 760}px;width:920px"><div class="caps">${o.panelLabel || 'Intinya'}</div><div class="tx">${o.teks}</div></div>`,
  update(r, t, s) { head(r, t); judulIn(r, t, s, o); enter(r.pn, t, at(s, o.panelAt, .9), { from: 'up', d: 50, r: -.8 }); },
});

/** CTA: kolom komentar mengetik keyword + pill. Soft selling: tawarkan yang gratis & spesifik. */
POLA.cta = o => ({
  build: el => el.innerHTML = LOGO + LBL(o.label || 'Bersambung') + judul(o) + `
    <div class="abs card" data-r="cb" style="left:80px;top:${o.top || 870}px;width:920px;height:150px;padding:0 26px 0 34px;display:flex;align-items:center;gap:26px;border-radius:80px">
      <div style="width:84px;height:84px;border-radius:50%;background:#E3F1F3;flex:none"></div>
      <div data-r="ty" style="flex:1;font:800 66px var(--font);color:var(--ink);letter-spacing:2px;white-space:nowrap"></div>
      <div data-r="sd" style="width:108px;height:108px;border-radius:50%;background:var(--teal);display:flex;align-items:center;justify-content:center;flex:none">${ICON.send.replace('<svg', '<svg style="width:50px;height:50px;fill:#fff"')}</div></div>
    <div class="abs pill g" data-r="ok" style="left:80px;top:${(o.top || 870) + 190}px">${o.pill || 'Ditunggu komennya'}</div>`,
  update(r, t, s) {
    head(r, t); judulIn(r, t, s, o);
    enter(r.cb, t, .3, { from: 'up', d: 50 });
    const k0 = at(s, o.ketikAt, .8), k1 = o.ketikAt && typeof o.ketikAt === 'string' ? wEnd(s.id, o.ketikAt) : k0 + .6;
    const n = Math.floor(o.keyword.length * P(t, k0, k1 + .05) + 1e-6), car = Math.floor(t * 2.5) % 2 ? '' : '<span style="display:inline-block;width:5px;height:62px;background:var(--teal);vertical-align:-8px;margin-left:6px"></span>';
    r.ty.innerHTML = n ? o.keyword.slice(0, n) + car : `<span style="font:500 40px var(--font);color:#A8B4B8;letter-spacing:0">${o.placeholder || 'Tulis komentar…'}</span>`;
    const ks = k1 + .25; r.sd.style.transform = `scale(${t > ks ? lerp(.8, 1, P(t, ks, ks + .3, 'back')) : 1})`;
    enter(r.ok, t, ks + .15, { from: 'pop', dur: .4, r: -3 });
  },
});

/* ---------- pola di atas FOOTAGE (caption dimatikan otomatis bila kartunya memuat kata yang sama) ---------- */
/** Kartu definisi/daftar yang menyala per kata saat diucapkan. rows: [{t:'<b>P</b>roduct', at:'product'}] */
POLA.kartuUcapan = o => ({
  build: (el, s) => { s.caption = false; el.innerHTML = VIDEO(s) + `<div class="abs card" data-r="c" style="left:80px;top:${o.top || 290}px;width:${o.lebar || 760}px;padding:26px 40px 30px">
      <div class="caps">${o.label}</div>${o.rows.map(x => `<div data-r="row[]" style="font:800 ${o.size || 72}px/1.12 var(--font);letter-spacing:-1.5px;color:var(--ink)">${x.t.replace(/<b>/g, '<b style="color:var(--teal);font-weight:900">')}</div>`).join('')}
      ${o.sub ? `<div data-r="sub" style="font:600 32px var(--font);color:var(--body);margin-top:10px">${o.sub}</div>` : ''}</div>`; },
  update(r, t, s) {
    enter(r.c, t, at(s, o.masukAt, .05) - .05, { from: 'up', d: 40, r: -1.5 });
    o.rows.forEach((x, i) => { const a = at(s, x.at, .5 + i * .6), k = P(t, a - .12, a + .25, 'expo');
      r.row[i].style.opacity = lerp(.16, 1, k); r.row[i].style.transform = `translateX(${lerp(-24, 0, k)}px)`; });
    enter(r.sub, t, at(s, o.subAt, at(s, o.rows.at(-1).at) + .45), { from: 'up', d: 20, dur: .4 });
  },
});
/** Kartu angka/label di atas B-roll tanpa suara (mis. counter revisi). */
POLA.kartuBroll = o => ({
  build: (el, s) => { s.caption = false; el.innerHTML = VIDEO(s) + `<div class="abs card" data-r="c" style="left:80px;top:340px;width:470px;padding:28px 36px 30px">
      <div class="caps">${o.label}</div><div data-r="n" style="font:900 150px/1 var(--font);letter-spacing:-4px;color:var(--teal);margin-top:8px">${o.dari}</div>
      <div style="font:600 30px var(--font);color:var(--body);margin-top:6px">${o.sub || ''}</div></div>`; },
  update(r, t, s) {
    enter(r.c, t, .1, { from: 'up', d: 50, r: -2 });
    if (o.hitung) { const [a, b, pre = ''] = o.hitung; r.n.textContent = pre + Math.round(lerp(a, b, P(t, .3, s.dur - .2, 'io'))); }
  },
});
