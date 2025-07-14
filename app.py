from flask import Flask, request, render_template, send_file
from psd_tools import PSDImage
import os, zipfile, shutil
from PIL import Image
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXTRACT_FOLDER'] = 'extracted'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXTRACT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['psd_file']
    if not file or not file.filename.endswith('.psd'):
        print("❌ Invalid file uploaded.")
        return "Invalid file", 400

    session_id = str(uuid.uuid4())
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.psd")
    extract_path = os.path.join(app.config['EXTRACT_FOLDER'], session_id)
    os.makedirs(extract_path, exist_ok=True)

    file.save(upload_path)
    print("✅ PSD file saved to:", upload_path)

    print("🔍 Opening PSD for parsing...")
    psd = PSDImage.open(upload_path)

    # Extract layers
    count = 0
    def export_layers(layers, parent=""):
        nonlocal count
        for i, layer in enumerate(layers):
            name = layer.name.strip().replace(" ", "_") or f"layer_{i}"
            full_name = f"{parent}_{name}" if parent else name
            if layer.is_group():
                print(f"📁 Entering group: {full_name}")
                export_layers(layer, full_name)
            elif layer.has_pixels():
                image = layer.composite()
                if image:
                    out_file = os.path.join(extract_path, f"{full_name}.png")
                    image.save(out_file)
                    print(f"🖼️ Extracted image layer: {full_name}.png")
                    count += 1

    print("🚀 Starting layer extraction...")
    export_layers(psd)

    print(f"✅ Finished extracting {count} image layers.")

    # Zip the results
    zip_path = f"{extract_path}.zip"
    print("📦 Zipping extracted images...")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(extract_path):
            zipf.write(os.path.join(extract_path, file), file)

    # Cleanup temporary files
    print("🧹 Cleaning up temp files...")
    os.remove(upload_path)
    shutil.rmtree(extract_path)

    print("📤 Sending zipped file to user.")
    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    # Only run this locally
    app.run(host="0.0.0.0", port=5000)
