# -----------------------------------------------------------------
# KODE API LENGKAP UNTUK PDF PROCESSOR (VERCEL)
# -----------------------------------------------------------------
from flask import Flask, request, jsonify
import PyPDF2
import io
import traceback # Kita tambahkan ini untuk log error yang lebih baik

# Vercel akan otomatis mencari variabel bernama 'app'
app = Flask(__name__)

# --- Definisi Kriteria Anda ---
# (Pastikan teks di sini SAMA PERSIS dengan yang ada di PDF)
KRITERIA = {
    "trombosit_rendah": "Trombosit < 100.000",
    "demam_tinggi": "Suhu > 38",
    "leukosit_turun": "Leukosit < 4.000"
}

# --- Fungsi Bantuan untuk CORS ---
# Ini PENTING agar Kodular diizinkan memanggil API ini
def _build_cors_preflight_response():
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response

def _add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# --- Endpoint API Utama Kita ---
@app.route("/api/process", methods=["POST", "OPTIONS"])
def process_pdf():
    
    # Menangani request 'preflight' CORS
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    # Memastikan ini adalah request POST
    if request.method != "POST":
        return _add_cors_headers(jsonify({"error": "Hanya metode POST yang diizinkan"})), 405

    try:
        # Memeriksa apakah file ada dalam request
        if 'file' not in request.files:
            return _add_cors_headers(jsonify({"error": "Tidak ada file PDF ('file' key tidak ditemukan)"})), 400

        file = request.files['file']

        if file.filename == '':
            return _add_cors_headers(jsonify({"error": "Nama file kosong"})), 400

        # --- Logika Inti Pemrosesan PDF ---
        
        # Membaca file PDF yang di-upload
        pdf_file = io.BytesIO(file.read())
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Ekstrak teks dari semua halaman
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() or "" # Tambah 'or ""' untuk halaman kosong
            
        full_text_lower = full_text.lower()
        
        # Mencari kriteria
        hasil = {}
        for key, kriteria_teks in KRITERIA.items():
            # Cek apakah teks kriteria (sudah di-lowercase) ada di dalam teks PDF
            if kriteria_teks.lower() in full_text_lower:
                hasil[key] = True
            else:
                hasil[key] = False

        # Mengirim kembali hasilnya sebagai JSON
        return _add_cors_headers(jsonify(hasil)), 200

    except Exception as e:
        # Jika terjadi error, catat error lengkapnya
        print(f"ERROR: Terjadi kesalahan: {e}")
        print(traceback.format_exc()) # Mencetak traceback ke Vercel Logs
        return _add_cors_headers(jsonify({"error": "Terjadi kesalahan internal saat memproses PDF", "detail": str(e)})), 500

# (Opsional) Rute 'root' untuk mengecek apakah API hidup
@app.route("/api", methods=["GET"])
def health_check():
    return _add_cors_headers(jsonify({"status": "API PDF Processor sedang berjalan"}))

# -----------------------------------------------------------------
# AKHIR DARI KODE
# -----------------------------------------------------------------
