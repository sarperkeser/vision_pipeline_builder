from PyQt6.QtWidgets import QMainWindow, QSplitter
from PyQt6.QtCore import Qt
from ui.left_panel import LeftPanel
from ui.middle_panel import MiddlePanel
from ui.right_panel import RightPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vision Pipeline Builder - Tasarım Modu")
        self.setGeometry(100, 100, 1400, 800) # Ekranı biraz daha genişlettik
        
        # Ekranı yatay olarak bölecek ana Splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panellerden birer obje yarat
        self.left_panel = LeftPanel()
        self.middle_panel = MiddlePanel()
        self.right_panel = RightPanel()
        
        # Panelleri sırasıyla Splitter'a ekle (Sol, Orta, Sağ)
        main_splitter.addWidget(self.left_panel)
        main_splitter.addWidget(self.middle_panel)
        main_splitter.addWidget(self.right_panel)
        
        # Panellerin varsayılan genişlikleri (Piksel cinsinden)
        # Sol: 250, Orta: Geniş (900), Sağ: 250
        main_splitter.setSizes([250, 900, 250])
        
        # Bölücü çizgilerin kalınlığını ayarla (daha rahat tutulup çekilsin diye)
        main_splitter.setHandleWidth(3)
        
        # Ana pencerenin merkezine bu Splitter'ı yerleştir
        self.setCentralWidget(main_splitter)