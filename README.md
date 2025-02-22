# QR Code Generator

A modern, web-based QR code generator with platform-specific logo integration and customization options.

![QR Code Generator Demo](static/demo.gif)

## Features

- 🎨 Modern and responsive UI
- 🎯 Platform-specific logo integration (Instagram, Facebook, Twitter, YouTube)
- 🎨 Custom QR code colors
- 📏 Multiple size options
- 💾 Direct download functionality
- 📱 Mobile-friendly design
- 🔍 High error correction level
- 🖼️ Custom file naming based on content

## Technologies Used

- Backend: Python (Flask)
- Frontend: HTML5, CSS3, JavaScript
- QR Code Generation: qrcode
- Image Processing: Pillow
- Deployment: Gunicorn, Nginx

## Installation

1. Clone the repository
```bash
git clone https://github.com/e500ky/QRCodeGenerator.git
cd QR-Code-Generator
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

![How to Use](static/demo.gif)

1. Enter your text or URL in the input field
2. Select desired color and size
3. Click "Generate QR Code"
4. Download the generated QR code

💡 **Pro Tip**: For social media URLs (Instagram, Facebook, Twitter, YouTube), the QR code will automatically include the platform's logo!

Example URLs:
- `https://instagram.com/username`
- `https://facebook.com/profile`
- `https://twitter.com/username`
- `https://youtube.com/channel`

## Project Structure

```
QRCodeCreator/
├── app.py             # Main Flask application
├── static/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   ├── logos/         # Platform logos
│   └── qrcodes/       # Generated QR codes
├── templates/         # HTML templates
└── requirements.txt   # Python dependencies
```

## API Endpoints

- `GET /` - Main application page
- `POST /generate` - Generate QR code
- `GET /download/<filename>` - Download generated QR code

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Instagram - [@firattunaarslann](https://instagram.com/firattunaarslann)

Project Link: [https://github.com/e500ky/QRCodeGenerator](https://github.com/e500ky/QRCodeGenerator)

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [qrcode](https://github.com/lincolnloop/python-qrcode)
- [Pillow](https://python-pillow.org/)
