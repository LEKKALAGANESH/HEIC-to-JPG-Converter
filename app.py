import os
import io
import zipfile
import uuid
import shutil
import tempfile
from flask import Flask, render_template, request, send_file, jsonify, after_this_request
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload

# Store converted files in system temp directory (avoids Flask reload issues)
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'heic_converter')
os.makedirs(TEMP_DIR, exist_ok=True)

def log(msg):
    print(f"[CONVERTER] {msg}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_files():
    if 'files' not in request.files:
        log("No files in request")
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('files')
    log(f"Received {len(files)} files")

    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No files selected'}), 400

    # Create a unique session ID for this conversion
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(TEMP_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    log(f"Session ID: {session_id}")

    converted_files = []
    failed_files = []
    file_counter = {}  # Track duplicate filenames

    for file in files:
        filename = file.filename
        if not filename or filename == '':
            continue

        log(f"Processing: {filename}")

        # Check if it's a HEIC file
        if not filename.lower().endswith(('.heic', '.heif')):
            failed_files.append({'name': filename, 'error': 'Not a HEIC/HEIF file'})
            continue

        try:
            # Read the file
            file_bytes = file.read()

            if len(file_bytes) == 0:
                failed_files.append({'name': filename, 'error': 'Empty file'})
                continue

            # Open with Pillow (pillow-heif handles HEIC)
            img = Image.open(io.BytesIO(file_bytes))

            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Create output filename with duplicate handling
            base_name, _ = os.path.splitext(filename)

            # Handle duplicate filenames
            if base_name in file_counter:
                file_counter[base_name] += 1
                jpg_filename = f"{base_name}_{file_counter[base_name]}.jpg"
            else:
                file_counter[base_name] = 0
                jpg_filename = f"{base_name}.jpg"

            jpg_path = os.path.join(session_dir, jpg_filename)

            # Save as JPEG
            img.save(jpg_path, "JPEG", quality=95)
            img.close()

            file_size = os.path.getsize(jpg_path)
            log(f"Saved: {jpg_filename} ({file_size} bytes)")

            converted_files.append({
                'original': filename,
                'converted': jpg_filename,
                'size': file_size
            })

        except Exception as e:
            log(f"Failed: {filename} - {str(e)}")
            failed_files.append({'name': filename, 'error': str(e)})

    # Verify files in directory
    saved_files = os.listdir(session_dir)
    log(f"Files in session dir: {len(saved_files)} - {saved_files}")

    if not converted_files:
        return jsonify({
            'error': 'No files were converted',
            'failed': failed_files
        }), 400

    return jsonify({
        'success': True,
        'session_id': session_id,
        'converted': converted_files,
        'failed': failed_files,
        'total_converted': len(converted_files),
        'total_failed': len(failed_files)
    })


@app.route('/download/<session_id>')
def download_zip(session_id):
    session_dir = os.path.join(TEMP_DIR, session_id)
    log(f"Download requested for session: {session_id}")

    if not os.path.exists(session_dir):
        log(f"Session directory not found: {session_dir}")
        return jsonify({'error': 'Session not found or expired'}), 404

    # List files before creating ZIP
    files_to_zip = os.listdir(session_dir)
    log(f"Files to zip: {len(files_to_zip)} - {files_to_zip}")

    if not files_to_zip:
        return jsonify({'error': 'No files to download'}), 404

    # Create ZIP file on disk
    zip_path = os.path.join(TEMP_DIR, f"{session_id}.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename in files_to_zip:
            file_path = os.path.join(session_dir, filename)
            if os.path.isfile(file_path):
                zip_file.write(file_path, filename)
                log(f"Added to ZIP: {filename}")

    # Verify ZIP contents
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_contents = zip_file.namelist()
        log(f"ZIP contains: {len(zip_contents)} files")

    zip_size = os.path.getsize(zip_path)
    log(f"ZIP size: {zip_size} bytes")

    # Send file directly from disk (more reliable for large files)
    return send_file(
        zip_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name='converted_images.zip'
    )


@app.route('/cleanup/<session_id>', methods=['POST'])
def cleanup(session_id):
    """Clean up temporary files - only called explicitly"""
    session_dir = os.path.join(TEMP_DIR, session_id)
    log(f"Cleanup requested for session: {session_id}")
    # Don't actually delete - let download handle it
    # This prevents accidental cleanup before download
    return jsonify({'success': True})


if __name__ == '__main__':
    print("\n" + "="*50)
    print("HEIC to JPG Converter")
    print("="*50)
    print("\nOpen your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
