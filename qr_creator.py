import customtkinter as ctk
import qrcode
from PIL import Image
import os

class QRCodeGenerator:
    def __init__(self):
        # Ana pencere ayarları
        self.window = ctk.CTk()
        self.window.title("Modern QR Kod Oluşturucu")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        
        # Tema ayarı
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Bileşenler
        self.create_widgets()
        
    def create_widgets(self):
        # Başlık
        title = ctk.CTkLabel(self.window, text="QR Kod Oluşturucu", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Metin girişi
        self.text_frame = ctk.CTkFrame(self.window)
        self.text_frame.pack(pady=20, padx=40, fill="x")
        
        self.text_input = ctk.CTkTextbox(self.text_frame, height=100)
        self.text_input.pack(pady=10, padx=10, fill="x")
        
        # QR Kod ayarları
        settings_frame = ctk.CTkFrame(self.window)
        settings_frame.pack(pady=20, padx=40, fill="x")
        
        # Renk seçimi
        color_label = ctk.CTkLabel(settings_frame, text="QR Kod Rengi:")
        color_label.pack(pady=5)
        
        self.color_var = ctk.StringVar(value="black")
        self.color_menu = ctk.CTkOptionMenu(settings_frame, 
                                          values=["black", "blue", "red", "green"],
                                          variable=self.color_var)
        self.color_menu.pack(pady=5)
        
        # Boyut seçimi
        size_label = ctk.CTkLabel(settings_frame, text="QR Kod Boyutu:")
        size_label.pack(pady=5)
        
        self.size_var = ctk.StringVar(value="300")
        self.size_menu = ctk.CTkOptionMenu(settings_frame,
                                         values=["200", "300", "400", "500"],
                                         variable=self.size_var)
        self.size_menu.pack(pady=5)
        
        # Oluştur butonu
        self.generate_button = ctk.CTkButton(self.window, text="QR Kod Oluştur",
                                           command=self.generate_qr)
        self.generate_button.pack(pady=20)
        
        # Durum mesajı
        self.status_label = ctk.CTkLabel(self.window, text="")
        self.status_label.pack(pady=10)
        
    def generate_qr(self):
        if os.path.exists("./static/qrcodes"): os.rmdir("./static/qrcodes")
        text = self.text_input.get("1.0", "end-1c")
        if not text:
            self.status_label.configure(text="Lütfen bir metin girin!")
            return
            
        try:
            # QR kod oluştur
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            # QR kodu seçilen renkte oluştur
            qr_image = qr.make_image(fill_color=self.color_var.get(), 
                                   back_color="white")
            
            # Boyutlandır
            size = int(self.size_var.get())
            qr_image = qr_image.resize((size, size))
            
            # Kaydet
            if not os.path.exists("qrcodes"):
                os.makedirs("qrcodes")
                
            save_path = f"qrcodes/qr_code_{len(os.listdir('qrcodes')) + 1}.png"
            qr_image.save(save_path)
            
            self.status_label.configure(
                text=f"QR kod başarıyla oluşturuldu!\nKonum: {save_path}")
            
        except Exception as e:
            self.status_label.configure(text=f"Hata oluştu: {str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = QRCodeGenerator()
    app.run()
