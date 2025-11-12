from flask import Flask, jsonify

# Vercel akan mencari 'app'
app = Flask(__name__)

# Rute tes sederhana
@app.route("/api/test", methods=["GET"])
def test_endpoint():
    # Kirim respons JSON sederhana
    return jsonify({"message": "API ini BERHASIL!"})

# Rute root (hanya untuk /api)
@app.route("/api", methods=["GET"])
def health_check():
    return jsonify({"status": "running"})
