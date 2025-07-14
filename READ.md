✅ Goal: Website Where Users Upload a PSD → Get a ZIP of Extracted Images
📦 Project Overview
🔧 Tech Stack
Part	Tool
Backend	Python + Flask
PSD Parsing	psd-tools, Pillow
Frontend	HTML (simple upload form)
Output	.zip of image layers
Hosting	Render / Railway / PythonAnywhere

📁 Folder Structure
cpp
Copy
Edit
psd_extractor_web/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css (optional)
├── uploads/
├── extracted/
├── requirements.txt
📄 Step 1: app.py – The Flask App
python
Copy
Edit
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
        return "Invalid file", 400

    session_id = str(uuid.uuid4())
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.psd")
    extract_path = os.path.join(app.config['EXTRACT_FOLDER'], session_id)
    os.makedirs(extract_path, exist_ok=True)

    file.save(upload_path)
    psd = PSDImage.open(upload_path)

    # Extract layers
    count = 0
    def export_layers(layers, parent=""):
        nonlocal count
        for i, layer in enumerate(layers):
            name = layer.name.strip().replace(" ", "_") or f"layer_{i}"
            full_name = f"{parent}_{name}" if parent else name
            if layer.is_group():
                export_layers(layer, full_name)
            elif layer.has_pixels():
                image = layer.composite()
                if image:
                    out_file = os.path.join(extract_path, f"{full_name}.png")
                    image.save(out_file)
                    count += 1

    export_layers(psd)

    # Zip the results
    zip_path = f"{extract_path}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(extract_path):
            zipf.write(os.path.join(extract_path, file), file)

    # Cleanup PSD file and extracted images (optional for persistent hosting)
    os.remove(upload_path)
    shutil.rmtree(extract_path)

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
🖼️ Step 2: templates/index.html
html
Copy
Edit
<!DOCTYPE html>
<html>
<head>
    <title>PSD Image Extractor</title>
</head>
<body>
    <h2>Upload a PSD File to Extract Images</h2>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="psd_file" accept=".psd" required>
        <button type="submit">Upload & Extract</button>
    </form>
</body>
</html>


--------------------------------------------------------------------------------------------------------------------------------
📄 Step 3: requirements.txt
nginx
Copy
Edit
Flask
psd-tools
Pillow
Install them locally if not installed

✅ Option 1: Check with pip show

To check if installed run the given commands one by one in vs code terminal

Open Command Prompt or your terminal and run these one by one:

pip show Flask
pip show psd-tools
pip show Pillow



install them locally if not install, run  the given command in prompt to install flask.
pip install Flask
<!-- To check if installed  -->
pip show Flask



🚀 Step 4: Run Locally

PS C:\Users\pione\OneDrive\Desktop\psd_extractor_web> python app.py

Then go to:
📍 http://127.0.0.1:5000

Upload a PSD, and you’ll get a .zip of extracted image layers.

-------------------------------------------------------------------------------------------------------------------------------

🌍 Step 5: Deploy Online
🔗 Easiest Option: Render
Push your project to GitHub

Go to Render.com

Choose "Web Service"

Connect your GitHub repo

Set:

Runtime: Python 3.x

Start command: gunicorn app:app

You’re live! 🎉

-------------------------------------------------------------------------------------------------------------------

You can’t deploy a Flask‑based site like ours on CheapHosty because it’s a shared Linux/PHP hosting provider—they only support PHP/cPanel setups, not Python/Flask applications




| Provider            | Free Tier  | Custom Domain | Ease of Use     | Recommended For                |
| ------------------- | ---------- | ------------- | --------------- | ------------------------------ |
| **PythonAnywhere**  | ✅          | ✅ Paid tier   | ⭐⭐⭐⭐⭐ Very Easy | Beginners & testing            |
| **Render**          | ✅          | ✅ Free tier   | ⭐⭐⭐⭐ Easy       | Git-based VPS alternative      |
| **Heroku**          | ✅          | ✅ Paid only   | ⭐⭐⭐⭐ Easy       | Hobby projects; DB integration |
| **DigitalOcean**    | ❌ (\$5/mo) | ✅             | ⭐⭐⭐ Moderate    | Full control, scalable apps    |
| **Vercel / Fly.io** | ✅          | ✅ Free tier   | ⭐⭐⭐ Moderate    | Serverless/microservices       |


