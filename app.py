from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import qrcode
from io import BytesIO
import os
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def sanitize_filename(text):
    # Dosya adı için geçersiz karakterleri temizle
    invalid_chars = '<>:"/\\|?*'
    filename = ''.join(c if c not in invalid_chars else '_' for c in text)
    # Uzunluğu sınırla
    return filename[:50] if len(filename) > 50 else filename

def get_platform_logo(text):
    """URL'ye göre platform logosunu döndürür"""
    # URL pattern'leri ve logo dosyaları
    platforms = {
        r'instagram\.com': 'logos/instagram.png',
        r'facebook\.com': 'logos/facebook.png',
        r'twitter\.com|x\.com': 'logos/twitter.png',
        r'youtube\.com': 'logos/youtube.png'
    }
    
    for pattern, logo in platforms.items():
        if re.search(pattern, text.lower()):
            logo_path = os.path.join('static', logo)
            if os.path.exists(logo_path):
                return logo_path
    return None

def add_logo_to_qr(qr_img, logo_path, size_factor=0.25):
    """QR kodun ortasına logo ekler"""
    # Logo boyutunu QR kodunun boyutuna göre ayarla
    qr_width, qr_height = qr_img.size
    logo_size = int(min(qr_width, qr_height) * size_factor)
    
    # Logoyu yükle ve yeniden boyutlandır
    logo = Image.open(logo_path)
    logo = logo.convert('RGBA')
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    # Logonun yerleştirileceği pozisyonu hesapla (orta nokta)
    pos_x = (qr_width - logo_size) // 2
    pos_y = (qr_height - logo_size) // 2
    
    # QR kodu RGBA moduna çevir
    qr_img = qr_img.convert('RGBA')
    
    # Yeni bir boş resim oluştur
    new_img = Image.new('RGBA', qr_img.size, (255, 255, 255, 0))
    
    # Logoyu yeni resme yapıştır
    new_img.paste(logo, (pos_x, pos_y), logo)
    
    # QR kod ve logoyu birleştir
    return Image.alpha_composite(qr_img, new_img)

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.json
    text = data.get('text', '')
    color = data.get('color', 'black')
    size = int(data.get('size', 300))
    
    if not text:
        return jsonify({'error': 'Please enter a text'}), 400
    
    try:
        # QR kodu oluştur
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Yüksek hata düzeltme
            box_size=10,
            border=4
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color=color, back_color="white")
        qr_img = qr_img.resize((size, size))
        
        # Platform logosunu kontrol et ve ekle
        logo_path = get_platform_logo(text)
        if logo_path:
            qr_img = add_logo_to_qr(qr_img, logo_path)
        
        # Dosya kaydetme işlemleri
        if not os.path.exists('static/qrcodes'):
            os.makedirs('static/qrcodes')
        
        safe_text = sanitize_filename(text)
        filename = f"qr_{safe_text}.png"
        filepath = os.path.join('static/qrcodes', filename)
        qr_img.save(filepath)
        
        download_url = f'/download/{filename}'
        
        return jsonify({
            'success': True,
            'filename': filename,
            'url': download_url
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}, 500)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        f'static/qrcodes/{filename}',
        as_attachment=True,
        download_name=filename
    )

@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__': 
    app.run(debug=True)
