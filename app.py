from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import models

app = Flask(__name__)
app.secret_key = "uangsadar-rahasia-2024"

models.init_db()


def fmt_rupiah(angka):
    """Format angka ke format Rupiah Indonesia."""
    return "Rp {:,.0f}".format(angka).replace(",", ".")


app.jinja_env.filters["rupiah"] = fmt_rupiah


# ── Coach AI (rule-based) ──────────────────────────────────────────────────

TIPS_UMUM = [
    "Catat setiap pengeluaran, sekecil apapun. Kebiasaan ini mengubah cara pandang Anda.",
    "Terapkan aturan 50/30/20: 50% kebutuhan, 30% keinginan, 20% tabungan.",
    "Hindari belanja impulsif. Tunggu 24 jam sebelum membeli barang non-esensial.",
    "Bandingkan harga sebelum membeli. Aplikasi perbandingan harga bisa membantu.",
    "Bawa bekal makan siang — bisa hemat jutaan per bulan.",
]

RESPONSES = {
    "saldo":    "Cek dashboard untuk melihat saldo terkini Anda. Pastikan pemasukan selalu lebih besar dari pengeluaran! 💪",
    "boros":    "Untuk mengurangi pengeluaran boros, coba terapkan aturan 50/30/20: 50% kebutuhan, 30% keinginan, 20% tabungan.",
    "hemat":    "Tips hemat: buat anggaran bulanan, bawa bekal, dan tunda pembelian non-esensial selama 24 jam sebelum membelinya.",
    "target":   "Membuat target tabungan adalah langkah pertama yang hebat! Buka halaman Target untuk menambah dan memantau progress Anda.",
    "tabungan": "Idealnya sisihkan minimal 20% dari pendapatan untuk tabungan. Mulai dari yang kecil, konsistensi lebih penting dari jumlah.",
    "utang":    "Prioritaskan melunasi utang berbunga tinggi terlebih dahulu (metode avalanche). Hindari menambah utang baru sambil melunasi yang lama.",
    "investasi":"Setelah dana darurat terpenuhi (3-6x pengeluaran bulanan), pertimbangkan reksa dana pasar uang sebagai investasi pertama.",
    "darurat":  "Dana darurat ideal adalah 3-6x pengeluaran bulanan. Simpan di rekening terpisah agar tidak tergoda memakai.",
    "gaji":     "Setiap menerima gaji, langsung transfer ke rekening tabungan sesuai rencana. Prinsipnya: bayar diri sendiri dulu!",
    "tips":     "",
    "halo":     "Halo! Saya Coach UangSadar 🤖. Tanyakan apa saja tentang keuangan — saldo, hemat, tabungan, investasi, atau minta tips!",
    "hi":       "Halo! Saya Coach UangSadar 🤖. Tanyakan apa saja tentang keuangan — saldo, hemat, tabungan, investasi, atau minta tips!",
    "bantuan":  "Saya bisa membantu soal: saldo, boros, hemat, target, tabungan, utang, investasi, dana darurat, gaji. Ketik salah satu!",
}

_tip_index = [0]


def coach_reply(pesan: str) -> str:
    p = pesan.lower().strip()
    for kunci, balasan in RESPONSES.items():
        if kunci in p:
            if kunci == "tips" or not balasan:
                tip = TIPS_UMUM[_tip_index[0] % len(TIPS_UMUM)]
                _tip_index[0] += 1
                return f"💡 Tips: {tip}"
            return balasan
    return (
        "Hmm, saya belum paham pertanyaan itu. Coba tanyakan soal: "
        "saldo, hemat, boros, target, tabungan, utang, investasi, atau minta tips! 😊"
    )


# ── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    ringkasan = models.get_ringkasan()
    saldo = ringkasan["total_masuk"] - ringkasan["total_keluar"]
    transaksi = models.get_transaksi_semua()[:10]  # 10 terbaru
    target_list = models.get_target_semua()
    return render_template(
        "dashboard.html",
        saldo=saldo,
        ringkasan=ringkasan,
        transaksi=transaksi,
        target_list=target_list,
    )


KATEGORI_PEMASUKAN = ["Gaji", "Freelance", "Bonus", "Bisnis", "Investasi", "Lainnya"]
KATEGORI_PENGELUARAN = [
    "Makanan & Minuman", "Transportasi", "Belanja", "Tagihan",
    "Kesehatan", "Hiburan", "Pendidikan", "Cicilan", "Lainnya",
]


@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        tipe = request.form.get("tipe", "pengeluaran")
        kategori = request.form.get("kategori", "Lainnya")
        jumlah_raw = request.form.get("jumlah", "0").replace(".", "").replace(",", "")
        catatan = request.form.get("catatan", "")
        tanggal = request.form.get("tanggal") or datetime.now().strftime("%Y-%m-%d")

        try:
            jumlah = float(jumlah_raw)
            if jumlah <= 0:
                raise ValueError
        except ValueError:
            flash("Jumlah tidak valid. Masukkan angka lebih dari 0.", "error")
            return redirect(url_for("tambah"))

        models.tambah_transaksi(tipe, kategori, jumlah, catatan, tanggal)
        flash("Transaksi berhasil ditambahkan! ✅", "success")
        return redirect(url_for("dashboard"))

    hari_ini = datetime.now().strftime("%Y-%m-%d")
    return render_template(
        "tambah.html",
        kategori_pemasukan=KATEGORI_PEMASUKAN,
        kategori_pengeluaran=KATEGORI_PENGELUARAN,
        hari_ini=hari_ini,
    )


@app.route("/hapus/<int:tid>", methods=["POST"])
def hapus_transaksi(tid):
    models.hapus_transaksi(tid)
    flash("Transaksi dihapus.", "info")
    return redirect(url_for("dashboard"))


@app.route("/target", methods=["GET", "POST"])
def target():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        jumlah_target_raw = request.form.get("jumlah_target", "0").replace(".", "").replace(",", "")
        deadline = request.form.get("deadline", "")

        try:
            jumlah_target = float(jumlah_target_raw)
            if jumlah_target <= 0:
                raise ValueError
        except ValueError:
            flash("Jumlah target tidak valid.", "error")
            return redirect(url_for("target"))

        if not nama:
            flash("Nama target tidak boleh kosong.", "error")
            return redirect(url_for("target"))

        models.tambah_target(nama, jumlah_target, deadline)
        flash(f"Target '{nama}' berhasil dibuat! 🎯", "success")
        return redirect(url_for("target"))

    target_list = models.get_target_semua()
    return render_template("target.html", target_list=target_list)


@app.route("/target/setor/<int:tid>", methods=["POST"])
def setor_target(tid):
    jumlah_raw = request.form.get("jumlah_setor", "0").replace(".", "").replace(",", "")
    try:
        jumlah = float(jumlah_raw)
        if jumlah <= 0:
            raise ValueError
    except ValueError:
        flash("Jumlah setor tidak valid.", "error")
        return redirect(url_for("target"))

    models.setor_target(tid, jumlah)
    flash("Setoran berhasil dicatat! 💰", "success")
    return redirect(url_for("target"))


@app.route("/target/hapus/<int:tid>", methods=["POST"])
def hapus_target(tid):
    models.hapus_target(tid)
    flash("Target dihapus.", "info")
    return redirect(url_for("target"))


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        pesan = request.form.get("pesan", "").strip()
        if pesan:
            balasan = coach_reply(pesan)
            models.simpan_chat(pesan, balasan)
        return redirect(url_for("chat"))

    log = models.get_chat_log()
    return render_template("chat.html", log=log)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
