from PyQt6.QtWidgets import QMainWindow, QSplitter, QTabWidget
from PyQt6.QtCore import Qt
from ui.left_panel import LeftPanel
from ui.data_tab import DataTab
from ui.model_tab import ModelTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vision Pipeline Builder - Sekmeli Tasarım Modu")
        self.setGeometry(100, 100, 1400, 800)
        
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sol Panel (Sabit)
        self.left_panel = LeftPanel()
        
        # Sağ Taraf: Sekmeler (Tabs)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { padding: 10px 30px; font-weight: bold; font-size: 14px; }")
        
        self.data_tab = DataTab()
        self.model_tab = ModelTab()
        
        self.tabs.addTab(self.data_tab, "Veri & Augmentation")
        self.tabs.addTab(self.model_tab, "Model Tasarımı")
        
        main_splitter.addWidget(self.left_panel)
        main_splitter.addWidget(self.tabs)
        main_splitter.setSizes([250, 1150])
        main_splitter.setHandleWidth(3)
        
        self.setCentralWidget(main_splitter)