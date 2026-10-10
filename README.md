# UangSadar

Aplikasi pencatatan pengeluaran harian dengan AI Coach yang membantu memahami pola belanja dan memberi saran hemat realistis.

---

## Mengapa Solusi Ini Dibutuhkan

Cara yang dipakai saat ini umumnya ada tiga: mencatat manual di buku atau notes, memakai spreadsheet, atau melihat mutasi rekening dan riwayat dompet digital. Semuanya punya kelemahan yang sama: **berhenti di data mentah**.

- Pencatatan manual jarang bertahan lama
- Spreadsheet butuh keahlian dan waktu
- Mutasi hanya berupa daftar angka yang tidak menjelaskan apa pun

### Mengapa UangSadar Lebih Baik

1. **Hasilnya berupa pemahaman dan aksi, bukan sekadar data.** UangSadar mengubah catatan transaksi menjadi penjelasan "uangmu paling banyak habis ke mana" dan satu saran perubahan yang realistis, lengkap dengan estimasi penghematan dalam rupiah.

2. **Bahasa sehari-hari.** AI Coach menjelaskan pola pengeluaran tanpa istilah keuangan yang rumit, sehingga cocok untuk anak muda yang belum punya latar belakang keuangan.

3. **Bisa ditanya langsung.** Pengguna dapat bertanya, misalnya "Kalau pola ini berlanjut, bagian mana yang bisa aku kurangi?", dan mendapat jawaban berdasarkan datanya sendiri, bukan tips generik.

4. **Angka akurat dan aman.** Perhitungan total, persentase, dan perbandingan antar minggu dikerjakan oleh kode aplikasi, sedangkan AI fokus menjelaskan dan memberi saran. AI juga dibatasi: tidak memberi rekomendasi investasi dan tidak menjanjikan keuntungan.

5. **Langsung ditindaklanjuti.** Atas permintaan pengguna, agent dapat membuat laporan mingguan di Google Docs, pengingat di Google Calendar, dan draf email di Gmail, sehingga insight tidak berhenti sebagai informasi.

---

## Fitur Utama Project

| Fitur | Deskripsi |
|-------|-----------|
| **Pencatatan Transaksi** | Pengguna mencatat pengeluaran secara manual atau mengunggah contoh mutasi yang sudah disamarkan, sehingga data masuk tanpa proses yang merepotkan. |
| **Kategorisasi & Deteksi Pola Boros** | Transaksi otomatis dikelompokkan ke kategori seperti makan, pesan antar, transportasi, belanja, dan langganan. Aplikasi membandingkan pengeluaran antar minggu dan menyorot kategori yang naik mencolok, misalnya pesan antar makanan yang naik dibanding minggu lalu. |
| **Target & Anggaran Mingguan** | Pengguna membuat batas jajan mingguan atau target tabungan untuk kebutuhan tertentu, lengkap dengan progress bar dan peringatan saat pengeluaran mendekati batas. |
| **AI Financial Coach** | Agent berbasis IBM Langflow yang menjelaskan "uangmu paling banyak habis ke mana" dalam bahasa sederhana, menjawab pertanyaan pengguna berdasarkan datanya sendiri, dan memberi satu saran perubahan yang realistis beserta estimasi penghematan. Agent tidak memberi rekomendasi investasi. |
| **Aksi Otomatis via Google Tools** | Atas permintaan pengguna, agent membuat laporan mingguan di Google Docs, pengingat cek anggaran di Google Calendar, dan draf email ringkasan di Gmail. Email hanya dibuat sebagai draf, tidak terkirim otomatis. |

---

## Alur Penggunaan Project

### Alur Singkat
```
User Input → Aplikasi UangSadar (kategorisasi & analisis) → IBM Langflow (AI Agent UangSadar Coach) → Output di Dashboard → User Action
```

### Penjelasan Per Tahap

1. **User Input.** Pengguna mencatat transaksi secara manual atau mengunggah contoh mutasi yang sudah disamarkan, lalu menetapkan batas jajan mingguan.

2. **Pemrosesan di aplikasi.** Aplikasi (dibangun dengan bantuan IBM Bob) mengelompokkan transaksi ke kategori, menghitung total per kategori, membandingkan minggu ini dengan minggu lalu, dan menandai kategori yang naik mencolok. Semua perhitungan dikerjakan kode agar angkanya akurat.

3. **Kirim ke IBM Langflow.** Aplikasi mengirim ringkasan hasil analisis dan pertanyaan pengguna ke flow Langflow melalui API.

4. **AI Agent memproses.** Agent "UangSadar Coach" membaca ringkasan, menjelaskan ke mana uang paling banyak habis, menyoroti pola boros, dan menyusun satu saran perubahan yang realistis beserta estimasi penghematan. Jika pengguna meminta, agent memanggil tool untuk membuat laporan di Google Docs, pengingat di Google Calendar, atau draf email di Gmail.

5. **Output.** Hasil dikembalikan ke aplikasi dan ditampilkan di dashboard: ringkasan pengeluaran, kategori terbesar, pola boros, dan satu saran utama. Jika ada aksi Google, tautan dokumen, event, atau draf ikut ditampilkan.

6. **User Action.** Pengguna menerapkan saran, bertanya lanjutan ke AI Coach (misalnya "Kalau pola ini berlanjut, bagian mana yang bisa aku kurangi?"), menyesuaikan batas anggaran, atau meminta agent membuat laporan, pengingat, dan draf email. Keputusan akhir tetap di tangan pengguna.

### Versi Ringkas
```
User input transaksi → Aplikasi kategorisasi & hitung (dibuat dengan Bob) → API Langflow → AI Agent analisis & saran (+ tool Docs/Calendar/Gmail) → Dashboard → User menerapkan saran atau meminta aksi lanjutan
```

---

## Penggunaan IBM Langflow

### Flow yang Dibuat
Flow bernama **UangSadar Coach**, dibangun dari template Agent di IBM Langflow. Flow ini menjadi mesin AI utama UangSadar: menerima ringkasan pengeluaran dari aplikasi, menganalisisnya, lalu mengembalikan penjelasan dan saran, serta menjalankan aksi lanjutan bila diminta pengguna.

### Node/Component yang Digunakan

| Node | Fungsi |
|------|--------|
| **Chat Input** | Titik masuk pesan dari aplikasi (ringkasan pengeluaran dalam format JSON dan pertanyaan pengguna). |
| **Agent** | Otak flow. Berisi Agent Instructions UangSadar Coach (peran, gaya bahasa santai, tugas, dan aturan ketat) serta language model yang mendukung tool calling. |
| **Google Docs (via Composio)** | Membuat dokumen "Laporan Mingguan UangSadar". |
| **Google Calendar (via Composio)** | Membuat pengingat cek anggaran atau tagihan langganan. |
| **Gmail (via Composio)** | Membuat draf email ringkasan mingguan. Aksi kirim langsung dinonaktifkan, hanya `CREATE_EMAIL_DRAFT` yang aktif. |
| **Chat Output** | Mengembalikan respons agent ke aplikasi. |

### Input & Output

**Input:** JSON berisi periode, total pengeluaran minggu ini dan minggu lalu, total per kategori, batas jajan mingguan, dan pertanyaan pengguna (bila ada).

**Output:** Ringkasan "uangmu paling banyak habis ke mana", kategori terbesar, pola boros, satu saran utama beserta estimasi penghematan, atau jawaban singkat untuk pertanyaan bebas. Bila ada aksi tool, output memuat konfirmasi dokumen, event, atau draf yang dibuat.

### Proses AI Agent

1. Agent menerima ringkasan dan membaca data yang sudah dihitung oleh aplikasi.
2. Agent menjelaskan pola pengeluaran dengan bahasa sehari-hari dan menyoroti kategori yang naik.
3. Agent menyusun tepat satu saran perubahan yang realistis dengan estimasi hemat dalam rupiah.
4. Bila pengguna meminta, agent memilih tool yang sesuai (Docs, Calendar, atau Gmail), menyebutkan apa yang akan dibuat, lalu menjalankannya.
5. **Guardrail di instruksi:** tidak memberi rekomendasi investasi, tidak menjanjikan keuntungan, tidak mengarang angka, dan menolak sopan permintaan di luar cakupan.

### Fungsi Langflow dalam Sistem
Langflow adalah lapisan AI dan orkestrasi. Prompt, guardrail, model, dan tool dikelola di satu tempat secara visual, sehingga perilaku coach bisa diubah tanpa menulis ulang aplikasi. Aplikasi memanggilnya lewat endpoint API flow.

> **Catatan:** Model yang digunakan: **Gemini**

---

## Penggunaan IBM Bob

### Fungsi IBM Bob
IBM Bob digunakan sebagai **AI development partner** untuk membangun aplikasi web UangSadar. Bob membantu merancang struktur proyek, menulis dan memperbaiki kode, membuat pengujian, mereview keamanan, dan menyusun dokumentasi. Dengan Bob, aplikasi yang membungkus AI Agent Langflow bisa selesai lebih cepat, dari rancangan sampai bisa dijalankan.

### Proses/Task yang Dikerjakan dengan Bob

- Merancang kerangka aplikasi. Bob menyusun rencana struktur file dan membuat aplikasi web berbasis **Python Flask** dengan halaman Dashboard, Tambah Transaksi, Target, dan Chat Coach dalam bahasa Indonesia dan tampilan mobile-friendly.
- Membuat data contoh. Bob membuat `sample_transactions.csv` berisi transaksi fiktif selama 4 minggu tanpa data pribadi, dengan pesan antar makanan yang naik di minggu terakhir untuk keperluan demo.
- Membuat logika kategorisasi dan analisis. Bob menulis fungsi kategorisasi berbasis kata kunci (makan, pesan antar, transportasi, belanja, langganan, lainnya), fungsi penghitung total per kategori per minggu, selisih persen, dan penanda kategori yang naik lebih dari 30%, lengkap dengan unit test.
- Membuat fitur target. Bob membuat batas jajan mingguan dengan progress bar dan peringatan saat pengeluaran mencapai 80% dari batas.
- Membuat modul integrasi. Bob menulis `langflow_client.py` yang memanggil endpoint API Langflow, dengan konfigurasi dari file `.env`, timeout, dan error handling.
- Debugging, review, dan dokumentasi. Bob membantu memperbaiki error saat aplikasi dijalankan, mereview kode untuk bug dan keamanan (memastikan API key tidak ditulis langsung di kode), dan menyusun README.

> **Contoh nyata:** Saat integrasi, Bob menemukan dan memperbaiki error format respons Langflow.

### Bagaimana Bob Berinteraksi dengan Sistem
Bob bekerja langsung di folder proyek `uangsadar`. Bob membaca, membuat, dan mengubah file kode, serta membantu menjalankan dan menguji aplikasi. Bob tidak berjalan di dalam aplikasi saat pengguna memakainya. Perannya ada di tahap pembangunan: kode yang ia hasilkan-lah yang kemudian berkomunikasi dengan Langflow lewat API.

### Output yang Dihasilkan

- Aplikasi web UangSadar yang berjalan (dashboard, input transaksi, target, chat coach)
- Fungsi kategorisasi dan analisis mingguan beserta unit test
- Modul `langflow_client.py` yang menghubungkan aplikasi ke flow Langflow
- Dataset contoh `sample_transactions.csv`
- README berisi tujuan, arsitektur, cara menjalankan, dan batasan AI

---

## Integrasi Langflow + Bob

### Gambaran Hubungan
IBM Langflow dan IBM Bob bekerja di dua lapisan yang saling melengkapi. **Langflow adalah otak AI yang dipanggil saat aplikasi berjalan. Bob adalah pembangun aplikasi yang menulis kode untuk memanggil otak itu.** Keduanya bertemu di satu titik: endpoint API flow Langflow yang dipanggil oleh kode buatan Bob.

### 1. Apa yang Dilakukan Langflow?
Langflow menjalankan flow "UangSadar Coach". Agent di dalamnya menerima ringkasan pengeluaran, menjelaskan pola dalam bahasa sederhana, menyoroti pola boros, memberi satu saran realistis beserta estimasi hemat, dan bila diminta pengguna, menjalankan tool Google Docs, Calendar, atau Gmail (draf saja). Guardrail agent melarang rekomendasi investasi dan janji keuntungan.

### 2. Apa yang Dilakukan Bob?
Bob membangun aplikasi web UangSadar dan semua kode yang berinteraksi dengan Langflow. Bob menulis fungsi kategorisasi dan analisis mingguan, sehingga angka (total, persen, selisih) dihitung oleh kode. Bob juga menulis modul `langflow_client.py` yang memformat hasil analisis menjadi JSON, mengirimnya ke endpoint Langflow dengan API key dari `.env`, menangani timeout dan error, lalu membaca respons untuk ditampilkan di dashboard dan halaman Chat Coach.

### 3. Bagaimana Data Berpindah di Antara Keduanya?

```
Pengguna mencatat transaksi di aplikasi
        ↓
Kode hasil Bob mengategorikan dan menghitung, lalu menyusun ringkasan JSON
(total per kategori, perbandingan minggu, batas jajan, pertanyaan pengguna)
        ↓
langflow_client.py mengirim ringkasan lewat POST /api/v1/run/{FLOW_ID} ke Langflow
        ↓
Agent memproses dan, bila perlu, memanggil tool Google
        ↓
Langflow mengembalikan hasil lewat Chat Output sebagai respons API
        ↓
langflow_client.py mem-parsing respons, dan aplikasi menampilkannya di dashboard
```

**Pembagian tugasnya sengaja dibuat tegas:** kode (hasil Bob) menghitung, Langflow menjelaskan dan bertindak. Dengan begitu angka akurat, dan perilaku AI bisa diubah dari Langflow tanpa menulis ulang aplikasi.

### 4. Apa Output Akhir Integrasi?
Pengguna melihat dalam satu antarmuka: ringkasan "uangmu paling banyak habis ke mana", kategori terbesar, pola boros, dan satu saran utama beserta estimasi penghematan. Pengguna juga bisa bertanya lanjutan ke AI Coach dan meminta laporan Docs, pengingat Calendar, atau draf Gmail.

---

## Dampak, Skalabilitas, Pembeda, dan Kemampuan AI Agent

> **Bagian ini belum diisi. Silakan tambahkan konten untuk:**
> - **Dampak:** Apa dampak nyata bagi pengguna/komunitas?
> - **Skalabilitas:** Bagaimana sistem bisa diskalakan (lebih banyak user, fitur baru, dll)?
> - **Pembeda:** Apa yang membedakan UangSadar dari solusi serupa yang sudah ada?
> - **Kemampuan AI Agent:** Detail kemampuan khusus AI Agent yang tidak tercakup di bagian sebelumnya.

---

## Teknologi yang Digunakan

- **Backend:** Python Flask
- **AI Orchestration:** IBM Langflow
- **AI Development Partner:** IBM Bob
- **Integrasi Google:** Composio (Google Docs, Calendar, Gmail)
- **Frontend:** HTML, CSS (mobile-first), JavaScript vanilla
- **Data:** CSV untuk penyimpanan transaksi

---

## Cara Menjalankan

### Prasyarat
- Python 3.10+
- Akun IBM Cloud (untuk Langflow)
- Kunci API Composio (untuk Google Tools)

### Instalasi

```bash
# Clone repository
git clone <repository-url>
cd uangsadar

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependensi
pip install -r requirements.txt

# Konfigurasi environment
cp .env.example .env
# Edit .env dengan API key dan konfigurasi Langflow
```

### Menjalankan Aplikasi

```bash
flask run
# Atau
python app.py
```

Akses di `http://localhost:5000`

---

## Struktur Proyek

```
uangsadar/
├── app.py                 # Entry point Flask
├── langflow_client.py     # Modul integrasi Langflow API
├── categorize.py          # Logika kategorisasi & analisis
├── test_categorize.py     # Unit test
├── sample_transactions.csv # Data contoh
├── templates/             # Template HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── add_transaction.html
│   ├── target.html
│   └── chat_coach.html
├── static/                # CSS, JS
├── .env                   # Konfigurasi (tidak di-commit)
└── requirements.txt
```

---

## Batasan & Keamanan

- **AI tidak memberi rekomendasi investasi** dan tidak menjanjikan keuntungan
- **API key disimpan di `.env`**, tidak pernah ditulis langsung di kode
- **Email hanya dibuat sebagai draf**, tidak terkirim otomatis
- **Data transaksi disimpan lokal** (CSV), tidak dikirim ke pihak ketiga selain ringkasan ke Langflow
- **Perhitungan angka dilakukan oleh kode**, bukan AI, untuk memastikan akurasi

---

## Lisensi

[MIT License](LICENSE) / [Sesuaikan dengan lisensi project Anda]

---

## Kontak & Kontribusi

- **Author:** [Muhammad Kevin Efendy]
- **Email:** [kevefendy@gmail.com]
- **Repository:** [https://github.com/kevinefendy/Uang-Sadar]

Pull request dan issue sangat diterima!
