import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # 1. Arayüzü oluştur
    window = MainWindow()
    
    # 2. Controller'ı oluştur ve arayüzü içine ver
    # Bu sayede buton bağlantıları aktif hale gelecek
    controller = MainController(window)
    
    # 3. Pencereyi göster
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()