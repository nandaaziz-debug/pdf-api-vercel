from flask import Flask, jsonify
import PyPDF2  # <-- Kita tes import ini
import io      # <-- Kita tes import ini

app = Flask(__name__)

# Endpoint tes baru
@app.route("/api/test-imports", methods=["GET"])
def test_imports_endpoint():
    try:
        # Kita coba gunakan library-nya secara minimal
        fiktif_pdf = io.BytesIO() 
        pembaca = PyPDF2.PdfReader(fiktif_pdf) 

        # Jika baris di atas tidak error, berarti import berhasil
        return jsonify({
            "message": "BERHASIL! Flask, io, dan PyPDF2 sukses di-import.",
        })
    except Exception as e:
        # Jika gagal, kirim pesan error
        return jsonify({"error": f"Gagal meng-import atau menggunakan library: {str(e)}"}), 500

# Rute root (hanya untuk /api)
@app.route("/api", methods=["GET"])
def health_check():
    return jsonify({"status": "running"})
