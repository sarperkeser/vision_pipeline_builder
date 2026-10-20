from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.network_visualizer import NetworkVisualizer # YENİ

class MiddlePanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Üst Kısım: Görsel Önizleme
        self.preview_label = QLabel("Görsel Önizleme Alanı")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #2b2b2b; color: white; border: 1px solid #444;")
        self.preview_label.setFont(QFont("Arial", 12))
        
        # YENİ: Liste yerine görselleştirici widget'ı ekliyoruz
        self.visualizer = NetworkVisualizer()
        
        splitter.addWidget(self.preview_label)
        splitter.addWidget(self.visualizer)
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter)