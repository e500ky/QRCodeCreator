document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const downloadBtn = document.getElementById('download-btn');
    const qrText = document.getElementById('qr-text');
    const qrColor = document.getElementById('qr-color');
    const qrSize = document.getElementById('qr-size');
    const qrImage = document.getElementById('qr-image');
    const emptyState = document.getElementById('empty-state');

    // Son girilen metni saklamak için değişken
    let lastGeneratedText = '';

    generateBtn.addEventListener('click', generateQRCode);
    qrSize.addEventListener('change', () => {
        if (lastGeneratedText) {
            generateQRCode();
        }
    });

    async function generateQRCode() {
        const text = qrText.value;
        if (!text) {
            alert('Please enter a text!');
            return;
        }

        try {
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';

            lastGeneratedText = text; // Metni sakla

            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    color: qrColor.value,
                    size: qrSize.value
                })
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            qrImage.src = data.url;
            qrImage.style.display = 'block';
            emptyState.style.display = 'none';
            downloadBtn.style.display = 'block';
            downloadBtn.onclick = () => {
                // Yeni indirme kodu
                const link = document.createElement('a');
                link.href = data.url;
                link.download = data.filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };

        } catch (error) {
            alert('Error: ' + error.message);
            emptyState.style.display = 'flex';
            qrImage.style.display = 'none';
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate QR Code';
        }
    }
});
