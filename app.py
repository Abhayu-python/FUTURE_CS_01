from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from aes_utils import encrypt_file, decrypt_file, load_key

UPLOAD_FOLDER = 'uploads'
DECRYPT_FOLDER = 'decrypted'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'xlsx'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DECRYPT_FOLDER'] = DECRYPT_FOLDER

key = load_key()
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_path = os.path.join(DECRYPT_FOLDER, filename)
        file.save(temp_path)

        encrypted_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
        encrypt_file(temp_path, encrypted_path, key)
        os.remove(temp_path)

        flash('File uploaded and encrypted successfully!')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    enc_path = os.path.join(UPLOAD_FOLDER, filename)
    dec_path = os.path.join(DECRYPT_FOLDER, filename.replace('.enc', ''))
    decrypt_file(enc_path, dec_path, key)
    return send_file(dec_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
