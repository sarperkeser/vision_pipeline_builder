from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MiddlePanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Dikey Splitter (Bölücü)
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Üst Kısım: Görsel Önizleme
        self.preview_label = QLabel("Görsel Önizleme Alanı\n(Klasörden seçilen fotoğraf burada görünecek)")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #2b2b2b; color: white; border: 1px solid #444;")
        self.preview_label.setFont(QFont("Arial", 12))
        
        # Alt Kısım: NodeGraph Alanı
        # Not: Faz 3/4'te burayı gerçek NodeGraphQt widget'ı ile değiştireceğiz.
        self.node_area = QLabel("NodeGraphQt CNN Tasarım Alanı\n(Sürükle-bırak Node'lar buraya eklenecek)")
        self.node_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.node_area.setStyleSheet("background-color: #1e1e1e; color: #888; border: 1px solid #444;")
        
        splitter.addWidget(self.preview_label)
        splitter.addWidget(self.node_area)
        
        # Boyut oranlarını ayarla (Önizleme %40, Node alanı %60 gibi)
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter)