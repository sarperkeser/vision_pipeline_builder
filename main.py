import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # QApplication PyQt uygulamalarının kalbidir, her projede 1 tane olmalıdır.
    app = QApplication(sys.argv)
    
    # Kendi yazdığımız pencereyi çağırıyoruz
    window = MainWindow()
    window.show()
    
    # Event loop'u (kullanıcı tıklamalarını dinleyen döngü) başlatıyoruz
    sys.exit(app.exec())

if __name__ == "__main__":
    main()