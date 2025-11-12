from flask import Flask, jsonify
from pypdf import PdfReader  # <-- PERUBAHAN DI SINI (dari PyPDF2)
import io

app = Flask(__name__)

# Endpoint tes
@app.route("/api/test-imports", methods=["GET"])
def test_imports_endpoint():
    try:
        # Kita coba gunakan library-nya secara minimal
        fiktif_pdf = io.BytesIO() 
        pembaca = PdfReader(fiktif_pdf) # <-- PERUBAHAN DI SINI

        # Jika baris di atas tidak error, berarti import berhasil
        return jsonify({
            "message": "BERHASIL! Flask, io, dan pypdf (versi baru) sukses di-import.",
        })
    except Exception as e:
        # Jika gagal, kirim pesan error
        return jsonify({"error": f"Gagal meng-import atau menggunakan library: {str(e)}"}), 500

# Rute root (hanya untuk /api)
@app.route("/api", methods=["GET"])
def health_check():
    return jsonify({"status": "running"})
