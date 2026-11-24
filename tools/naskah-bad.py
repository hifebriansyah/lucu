#!/usr/bin/env python3
"""Builds the two volumes of book 3, Berhenti Jadi Orang Baik yang Miskin: bad/naskah.md (Jilid 1) and bad/naskah-2.md (Jilid 2).

Each story lives in its own file, bad/stories/<slug>.md, starting with `# <Title>` (no number).
VOLUMES below says which stories go in which volume and section, in reading order; each volume
numbers its own stories from 1. The front pages (title, imprint, dedication, Daftar Isi, Kata
Pengantar, Mengenal Dark Triad) and closing pages (Penutup, Tentang Penulis) live in this script.
Run it after changing a story: python3 tools/naskah-bad.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "bad"
BR = '<div style="page-break-after: always;"></div>'

TITLE = "Berhenti Jadi Orang Baik yang Miskin"
SUB = "Belajar dari Kisah si Kaya yang “Jahat”"
AUTHOR = "Febriansyah, S.Kom., PSM, PSPO"

DULU, KINI, BATAS = "Zaman Dulu", "Zaman Sekarang", "Melewati Batas Legal"

VOLUMES = {
    1: [
        (DULU, ["rockefeller", "raden-wijaya", "coen", "daendels", "rhodes", "kroc", "liem-sioe-liong"]),
        (KINI, ["dunlap", "singer", "paulson", "shkreli", "thiel"]),
        (BATAS, ["ponzi", "leeson", "madoff", "holmes", "efishery"]),
    ],
    2: [
        (DULU, ["raffles", "van-den-bosch", "oei-tiong-ham", "frick", "thomas-hicks", "kennedy", "welch", "arnault"]),
        (KINI, ["bppc", "sackler", "hicks-gillett", "bresch"]),
        (BATAS, ["belfort", "tansil", "skilling", "bankman-fried"]),
    ],
}

PART_NO = ["Satu", "Dua", "Tiga"]

FOREWORD = {
    1: """Kita sering membayangkan orang jahat sebagai pencuri, penipu, atau koruptor, yaitu orang yang melanggar hukum dan suatu hari akan tertangkap. Buku ini tentang jenis orang jahat yang lain: yang tidak melanggar apa-apa.

Mereka membaca kontrak lebih teliti daripada lawannya. Mereka menemukan pasar yang tidak punya pilihan. Mereka berjanji secara lisan, lalu hanya menepati yang tertulis. Mereka memakai izin resmi, kebijakan pemerintah, atau celah yang belum ditutup. Dan hampir semuanya menjadi sangat kaya, atau sangat berkuasa.

Buku ini adalah jilid pertama dari dua jilid, dan dibagi menjadi tiga bagian. *Zaman Dulu* berisi kisah dari masa ketika aturannya belum ada atau ditulis oleh pihak yang kuat, dari seorang raja yang mendirikan Majapahit dengan tipu muslihat, sampai seorang penjual mesin milkshake yang mengambil alih nama McDonald's. *Zaman Sekarang* berisi kisah dari pasar modal, rumah sakit, dan ruang pengadilan modern, ketika celahnya lebih rumit tetapi caranya sama. Dan *Melewati Batas Legal* berisi kisah orang-orang yang memulai dengan cara yang sah atau hampir sah, lalu terus melangkah sampai jauh melewati garis itu, termasuk satu kisah dari Indonesia, dan apa yang menunggu mereka di sana.""",
    2: """Jilid pertama buku ini berisi tujuh belas kisah tentang orang-orang yang menjadi kaya atau berkuasa tanpa melanggar hukum, atau hampir tanpa melanggarnya. Jilid kedua ini melanjutkannya dengan enam belas kisah lagi, dengan susunan yang sama, dan bisa dibaca tanpa membaca jilid pertama lebih dulu.

*Zaman Dulu* berisi kisah dari masa ketika aturannya ditulis oleh pihak yang kuat: penjarahan keraton Yogyakarta, Tanam Paksa, candu yang dijual secara resmi, pemogokan yang dipatahkan dengan senjata, juara maraton Olimpiade yang menang dengan racun tikus, dan para eksekutif yang memecat ribuan orang di hari harga saham naik. *Zaman Sekarang* berisi kisah tentang monopoli cengkih, obat penghilang rasa sakit yang membuat kecanduan, klub sepak bola yang dibeli dengan utangnya sendiri, dan harga obat yang naik pelan-pelan sampai enam kali lipat. Dan *Melewati Batas Legal* berisi kisah orang-orang yang tidak berhenti di garis hukum, termasuk satu kisah dari Indonesia, dan apa yang menunggu mereka di sana.""",
}

FOREWORD_END = """Setiap kisah disusun dengan urutan yang sama: kisahnya, harga yang harus dibayar, hasil yang didapat, pelajaran yang bisa kita ambil, lalu analisa Dark Triad. Analisa itu mencoba menjawab satu pertanyaan: apakah perilaku mereka menunjukkan sifat-sifat gelap yang dikenal dalam psikologi, atau apakah orang biasa pun bisa sampai ke sana?

Tujuan buku ini bukan untuk ditiru, dan bukan juga sekadar untuk dibenci. Kalau kita paham cara mereka berpikir dan cara mereka menang, kita jadi lebih sulit dikalahkan dengan cara yang sama, dan lebih cepat sadar kalau kita sendiri mulai bergeser ke arah mereka.

Selamat membaca."""

DARK_TRIAD = """Pada 2002, dua peneliti psikologi dari University of British Columbia, Kanada, Delroy Paulhus dan Kevin Williams, memperkenalkan istilah *Dark Triad*, tiga serangkai gelap. Mereka menunjukkan bahwa tiga sifat kepribadian yang selama ini dipelajari terpisah saling berkaitan dan sama-sama berpusat pada satu hal, yaitu mendahulukan diri sendiri dengan mengorbankan orang lain, walaupun tetap merupakan sifat yang berbeda.

**Narsisisme** adalah rasa diri yang dibesar-besarkan. Orang dengan narsisisme tinggi merasa istimewa, berhak atas perlakuan khusus, dan sangat membutuhkan kekaguman. Mereka senang menjadi pusat perhatian, sulit menerima kritik, dan sering menulis ulang cerita supaya dirinya menjadi tokoh utama.

**Machiavellianisme** dinamai dari Niccolò Machiavelli, penulis Italia abad ke-16 yang dalam bukunya *Il Principe* menasihati para penguasa untuk memakai cara apa pun demi mempertahankan kekuasaan. Orang dengan Machiavellianisme tinggi bersifat strategis, sinis terhadap sifat manusia, pandai memanipulasi, dan sabar. Mereka berpikir jangka panjang, menyembunyikan niat, dan memperlakukan orang lain sebagai alat.

**Psikopati** ditandai oleh kurangnya empati dan penyesalan, ditambah sifat impulsif dan gemar mengambil risiko. Orang dengan psikopati tinggi bisa menyakiti orang lain tanpa merasa bersalah, dan sering bertindak tanpa memikirkan akibatnya, termasuk akibat bagi dirinya sendiri.

Ketiga sifat ini tidak sama dengan gangguan jiwa. Dalam penelitian, mereka diukur sebagai sifat *subklinis*, yang ada dalam kadar berbeda pada setiap orang, termasuk kita. Para peneliti mengukurnya dengan kuesioner, seperti Short Dark Triad yang dikembangkan Paulhus bersama Daniel Jones. Beberapa penelitian menemukan bahwa sifat-sifat ini sedikit lebih sering muncul di kalangan pemimpin bisnis daripada di masyarakat umum, karena dalam kadar tertentu, keberanian mengambil keputusan tidak populer, ketenangan di bawah tekanan, dan kepercayaan diri yang tinggi justru dihargai.

Analisa dalam buku ini tidak dimaksudkan sebagai diagnosis. Tidak ada satu pun tokoh di sini yang pernah kami uji. Yang kami lakukan hanyalah membaca perilaku mereka yang tercatat di publik, lalu bertanya: sifat mana yang paling terlihat? Kadang jawabannya jelas. Kadang jawabannya justru mengejutkan: orang biasa, dalam sistem yang salah, bisa melakukan hal yang sama gelapnya."""

CLOSING = {
    1: """Tujuh belas kisah, tujuh belas cara menjadi kaya, berkuasa, atau sekadar menang. Sebagian besar di antaranya sah, atau hampir sah, pada saat itu. Sisanya melewati garis hukum, dan hampir semuanya berakhir di ruang sidang.

Hukum selalu tertinggal satu langkah. Ia ditulis setelah ada korban, dan dibuat untuk menutup celah yang sudah dipakai. Rockefeller melahirkan undang-undang antimonopoli. Ponzi memberi nama pada jenis penipuan yang masih memakan korban sampai hari ini. Setiap kali, orang yang memakai celah itu sudah kaya sebelum celahnya ditutup. Dan di Nusantara, dari Banda sampai Batavia, "hukum" sering kali hanyalah izin yang ditulis oleh pihak yang memegang senjata.

Analisa Dark Triad di buku ini juga menunjukkan sebuah pola. Sifat yang paling sering muncul adalah Machiavellianisme: kesabaran, kerahasiaan, dan kemampuan membaca aturan lebih teliti daripada orang lain. Sifat inilah yang paling cocok untuk menjadi "jahat tapi legal", karena orang Machiavellian tahu persis di mana garisnya dan berhenti tepat sebelum itu. Sebaliknya, mereka yang menunjukkan psikopati dan narsisisme yang kuat, seperti Al Dunlap dan Martin Shkreli, cenderung tidak bisa berhenti, dan akhirnya melewati garis itu. Dan kisah Nick Leeson serta Gibran Huzaifah di eFishery mengingatkan bahwa orang tanpa sifat gelap yang menonjol pun bisa sampai ke tempat yang sama, kalau tekanan, kesempatan, dan alasannya cukup kuat.

Karena itu, "legal" bukan ukuran yang cukup. Pertanyaan yang lebih jujur adalah apakah kita masih nyaman kalau cara kita menang diketahui semua orang, terutama oleh orang yang kita kalahkan.

Dan untuk kita yang lebih sering berada di sisi lain meja, pelajarannya praktis: tulis setiap janji, baca setiap kontrak, tanyakan siapa yang untung kalau kita rugi, dan jangan pernah merasa aman hanya karena lawan kita "tidak melanggar apa-apa".""",
    2: """Enam belas kisah lagi, dan polanya tetap sama. Hukum selalu tertinggal satu langkah. Kennedy dan kawan-kawannya melahirkan aturan pasar modal. Paul Singer, di jilid pertama, mengubah cara negara-negara menulis surat utang. Enron melahirkan undang-undang yang mewajibkan para CEO menjamin sendiri kebenaran laporan keuangannya. Setiap kali, orang yang memakai celah itu sudah kaya sebelum celahnya ditutup.

Jilid ini juga menunjukkan bahwa "jahat tapi legal" tidak selalu membutuhkan satu orang yang jahat. Tanam Paksa, monopoli cengkih, dan harga EpiPen adalah sistem: aturan yang memberi hadiah kepada orang yang paling tega, dan menyebarkan tanggung jawab ke begitu banyak tangan sehingga tidak ada yang merasa bersalah. Dark Triad membantu menjelaskan orang-orang seperti Frick, Belfort, dan Skilling. Tetapi untuk memahami sistem, kita perlu bertanya hal yang lain: siapa yang menulis aturannya, dan siapa yang dibayar untuk menjalankannya?

Karena itu, "legal" bukan ukuran yang cukup. Pertanyaan yang lebih jujur adalah apakah kita masih nyaman kalau cara kita menang diketahui semua orang, terutama oleh orang yang kita kalahkan.

Dan untuk kita yang lebih sering berada di sisi lain meja, pelajarannya praktis: tulis setiap janji, baca setiap kontrak, tanyakan siapa yang untung kalau kita rugi, dan jangan pernah merasa aman hanya karena lawan kita "tidak melanggar apa-apa".""",
}

ABOUT = """Febriansyah sudah lima belas tahun bekerja di dunia teknologi di Jakarta, dari PHP developer, software engineer di agen perjalanan dan bursa kripto, Head of IT, CTO, sampai komisaris. Ia lulusan Telematika PNJ dan Sistem Informasi BINUS, sedang S2 di Universitas Nasional, dan bersertifikat Scrum Master dan Product Owner.

Di sepanjang kariernya ia membaca banyak kontrak, ikut banyak rapat restrukturisasi, dan bertemu orang-orang yang yakin bahwa semua yang tidak dilarang berarti boleh. Buku ini lahir dari pertanyaan yang terus muncul di rapat-rapat itu: boleh, tapi apakah benar?

febri.id"""


def story(slug, n):
    text = (ROOT / "stories" / f"{slug}.md").read_text(encoding="utf-8").strip()
    title = re.match(r"#\s+(.+)", text).group(1).strip()
    return title, re.sub(r"^#\s+.+", f"## {n}. {title}", text, count=1)


def build(vol, parts):
    jilid = f"Jilid {vol}"
    n, toc, body = 0, [], ""
    for i, (section, slugs) in enumerate(parts):
        name = f"Bagian {PART_NO[i]}: {section}"
        lines = []
        body += f"# {name}\n\n{BR}\n\n"
        for slug in slugs:
            n += 1
            title, text = story(slug, n)
            lines.append(f"{n}. {title}")
            body += f"{text}\n\n{BR}\n\n"
        toc.append(f"**{name}**\n\n" + "\n".join(lines))
    front = f"""# {TITLE}

### {jilid}: {SUB}

&nbsp;

**{AUTHOR}**

{BR}

**{TITLE}, {jilid}**
{SUB}

Penulis: {AUTHOR}
Penyunting: [Nama Penyunting]
Desain sampul: [Nama Desainer]

Cetakan pertama, 2026

ISBN: [Nomor ISBN]

Diterbitkan oleh:
[Nama Penerbit]
[Alamat Penerbit]

Hak cipta dilindungi undang-undang. Dilarang memperbanyak sebagian atau seluruh isi buku ini dalam bentuk apa pun tanpa izin tertulis dari penerbit.

Kisah-kisah dalam buku ini disusun dari pemberitaan, buku, dan dokumen pengadilan yang terbuka untuk umum. Angka dibulatkan. Analisa Dark Triad adalah pembacaan penulis atas perilaku yang dilaporkan publik, bukan diagnosis psikologis. Penilaian tentang benar dan salah adalah pendapat penulis.

{BR}

*Untuk semua yang pernah kalah*
*oleh orang yang tidak melanggar apa-apa.*

{BR}

## Daftar Isi

**Kata Pengantar**

**Mengenal Dark Triad**

""" + "\n\n".join(toc) + f"""

**Penutup**

**Tentang Penulis**

{BR}

## Kata Pengantar

{FOREWORD[vol]}

{FOREWORD_END}

{BR}

## Mengenal Dark Triad

{DARK_TRIAD}

{BR}

"""
    back = f"## Penutup\n\n{CLOSING[vol]}\n\n{BR}\n\n## Tentang Penulis\n\n{ABOUT}\n"
    out = ROOT / ("naskah.md" if vol == 1 else f"naskah-{vol}.md")
    out.write_text(front + body + back, encoding="utf-8")
    return out.name, n


missing = [s for parts in VOLUMES.values() for _, slugs in parts for s in slugs if not (ROOT / "stories" / f"{s}.md").exists()]
if missing:
    raise SystemExit(f"missing story files: {', '.join(missing)}")
for vol, parts in VOLUMES.items():
    name, n = build(vol, parts)
    print(f"wrote bad/{name}: Jilid {vol}, {n} stories")
