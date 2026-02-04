# HEIC to JPG Converter

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/LEKKALAGANESH/HEIC-to-JPG-Converter)

A web-based and command-line tool to convert iPhone HEIC photos to JPG format.

## Features

- **Web Interface**: Drag & drop multiple HEIC files for instant conversion
- **Batch Download**: All converted files packaged in a single ZIP
- **CLI Tool**: Command-line script for batch folder conversion
- **High Quality**: 95% JPEG quality preservation
- **No Upload Limits**: Convert as many files as you want
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Screenshots

### Landing Page - Drag & Drop Interface

![Landing Page](work%20Images/landing_page.png)

### After Conversion - Download ZIP

![Download ZIP](work%20Images/downloadable_zip_page.png)

## Quick Start

### Clone the Repository

```bash
git clone https://github.com/LEKKALAGANESH/HEIC-to-JPG-Converter.git
cd HEIC-to-JPG-Converter
```

### Install Dependencies

```bash
pip install flask pillow pillow-heif
```

### Run the Web App

```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Option 1: Clone with Git

```bash
git clone https://github.com/LEKKALAGANESH/HEIC-to-JPG-Converter.git
cd HEIC-to-JPG-Converter
pip install flask pillow pillow-heif
python app.py
```

### Option 2: Download ZIP

1. Download the repository as ZIP from [GitHub](https://github.com/LEKKALAGANESH/HEIC-to-JPG-Converter)
2. Extract the ZIP file
3. Open terminal in the extracted folder
4. Run:
   ```bash
   pip install flask pillow pillow-heif
   python app.py
   ```

## Usage

### Web Interface (Recommended)

1. Open http://localhost:5000 in your browser
2. Drag and drop HEIC files onto the drop zone (or click "Browse Files")
3. Click **"Convert to JPG"**
4. Click **"Download ZIP"** to get all converted files

### Command Line Interface

The CLI tool supports multiple modes:

#### Interactive Mode (no arguments)

```bash
python convert_heic_cli.py
```

This opens a menu where you can choose to convert single files or folders.

#### Convert Single File

```bash
python convert_heic_cli.py photo.heic
```

#### Convert Folder

```bash
python convert_heic_cli.py /path/to/folder
```

#### Convert Folder Recursively (includes subfolders)

```bash
python convert_heic_cli.py -r /path/to/folder
```

#### Custom Output Directory

```bash
python convert_heic_cli.py -o ./output photo.heic
```

#### CLI Options

| Option             | Description                                      |
| ------------------ | ------------------------------------------------ |
| `-r, --recursive`  | Convert files in subfolders too                  |
| `-o, --output`     | Custom output directory                          |
| `-q, --quality`    | JPEG quality 1-100 (default: 95)                 |
| `--no-subfolder`   | Save JPGs in same folder (no 'jpg files' folder) |

## Project Structure

```
HEIC-to-JPG-Converter/
├── app.py                 # Flask web application
├── convert_heic_cli.py    # Command-line batch converter
├── README.md              # This file
├── LICENSE                # MIT License
├── templates/
│   └── index.html         # Web interface (HTML/CSS/JS)
└── work Images/
    ├── landing_page.png           # Screenshot of main page
    └── downloadable_zip_page.png  # Screenshot after conversion
```

## How It Works

### Web Application Flow

```
1. User drops HEIC files
        ↓
2. JavaScript collects files in FormData
        ↓
3. POST to /convert endpoint
        ↓
4. Flask receives files
        ↓
5. pillow-heif decodes HEIC
        ↓
6. Pillow saves as JPG
        ↓
7. Files stored in temp directory
        ↓
8. User clicks Download
        ↓
9. Server creates ZIP file
        ↓
10. ZIP sent to browser
```

### Technologies Used

| Component        | Technology                      |
| ---------------- | ------------------------------- |
| Backend          | Flask (Python)                  |
| Frontend         | HTML5, CSS3, Vanilla JavaScript |
| HEIC Decoding    | pillow-heif                     |
| Image Processing | Pillow (PIL)                    |
| File Compression | zipfile (Python stdlib)         |

## Configuration

### app.py Settings

```python
# Maximum upload size (default: 500MB)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# JPEG quality (1-100, default: 95)
img.save(jpg_path, "JPEG", quality=95)
```

### Temp File Location

Converted files are temporarily stored in:

- **Windows**: `%TEMP%\heic_converter\`
- **Linux/Mac**: `/tmp/heic_converter/`

Files are automatically cleaned up after download.

## Troubleshooting

### "No files uploaded" error

- Make sure you're dropping `.heic` or `.HEIC` files
- Check browser console (F12) for JavaScript errors

### Connection reset during download

- This was fixed by moving temp files outside the app directory
- If issue persists, try disabling Flask debug mode:
  ```python
  app.run(debug=False)
  ```

### Large files taking too long

- HEIC files are typically 2-5MB each
- 100 files ≈ 30-60 seconds conversion time
- Consider using the CLI tool for very large batches

## API Endpoints

| Endpoint                 | Method | Description                     |
| ------------------------ | ------ | ------------------------------- |
| `/`                      | GET    | Web interface                   |
| `/convert`               | POST   | Upload and convert HEIC files   |
| `/download/<session_id>` | GET    | Download ZIP of converted files |

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- [pillow-heif](https://github.com/bigcat88/pillow_heif) - HEIC/HEIF support for Pillow
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [Pillow](https://pillow.readthedocs.io/) - Python Imaging Library

## Author

**LEKKALA GANESH**

- GitHub: [@LEKKALAGANESH](https://github.com/LEKKALAGANESH)

---

If you found this project helpful, please give it a ⭐ on [GitHub](https://github.com/LEKKALAGANESH/HEIC-to-JPG-Converter)!
