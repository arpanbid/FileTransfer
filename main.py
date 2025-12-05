import os
import random
import io
import zipfile
from flask import Flask, request, render_template, send_file, url_for, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store in-memory mapping: code -> list of {path, filename}
transfers = {}


# ---------------- Routes ------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/send")
def send_page():
    code = random.randint(100000, 999999)
    transfers[str(code)] = None  # reserved until upload
    return render_template("send.html", code=code)


@app.route("/upload/<code>", methods=["POST"])
def upload(code):
    # Accept multiple files under the same input name `file`
    files = request.files.getlist("file")
    if not files:
        return "No file", 400

    saved = transfers.get(code)
    if saved is None:
        # initialize list for this code
        transfers[code] = []

    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            # avoid overwriting by prefixing with code + random suffix
            unique_name = f"{code}_{random.randint(1000,9999)}_{filename}"
            path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(path)
            transfers[code].append({"path": path, "filename": filename})

    return render_template("uploaded.html", code=code, files=transfers[code])


@app.route("/receive", methods=["GET", "POST"])
def receive():
    if request.method == "GET":
        return render_template("receive.html")

    code = request.form.get("code")
    files = transfers.get(code)

    if not files:
        return render_template("invalid.html")

    # If only one file, send it directly
    if len(files) == 1:
        file_record = files[0]
        if not os.path.exists(file_record["path"]):
            return render_template("invalid.html")
        return send_file(file_record["path"], as_attachment=True, download_name=file_record["filename"]) 

    # Multiple files: show a page with download links and an option to download all as a zip
    return render_template("downloads.html", code=code, files=files)


@app.route('/download/<code>/<int:idx>')
def download_file(code, idx):
    files = transfers.get(code)
    if not files or idx < 0 or idx >= len(files):
        abort(404)
    record = files[idx]
    if not os.path.exists(record["path"]):
        abort(404)
    return send_file(record["path"], as_attachment=True, download_name=record["filename"]) 


@app.route('/download_all/<code>')
def download_all(code):
    files = transfers.get(code)
    if not files:
        abort(404)

    # Create zip in-memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for record in files:
            if os.path.exists(record["path"]):
                # arcname is the original filename
                zf.write(record["path"], arcname=record["filename"])

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name=f"{code}_files.zip", mimetype='application/zip')


# ---------------- Run ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
