import os
from PyQt6.QtCore import QThread, pyqtSignal

class DatasetScanner(QThread):
    # İşlem bitince Controller'a fırlatacağımız sinyal (dictionary taşıyacak)
    scan_completed = pyqtSignal(dict)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        
    def run(self):
        # QThread başlatıldığında (start) çalışacak asıl arka plan metodu
        classes = []
        total_images = 0
        valid_extensions = {".jpg", ".jpeg", ".png"}
        
        # Seçilen klasörün içindeki alt klasörleri (sınıfları) gez
        try:
            for item in os.listdir(self.folder_path):
                item_path = os.path.join(self.folder_path, item)
                
                if os.path.isdir(item_path):
                    classes.append(item)
                    # Alt klasördeki resimleri say
                    images = [f for f in os.listdir(item_path) if os.path.splitext(f)[1].lower() in valid_extensions]
                    total_images += len(images)
                    
            # İşlem bitince sonucu ana arayüze (Controller'a) gönder
            self.scan_completed.emit({
                "classes": classes,
                "total_images": total_images,
                "folder": self.folder_path,
                "status": "success"
            })
        except Exception as e:
            self.scan_completed.emit({"status": "error", "message": str(e)})