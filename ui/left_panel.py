from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeView, 
                             QPushButton, QGroupBox, QSpinBox, QCheckBox, QFormLayout)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 1. Veri Seti Ayarları (Üst Kısım)
        settings_group = QGroupBox("Veri Seti Ayarları")
        form_layout = QFormLayout()
        
        self.btn_select_folder = QPushButton("Klasör Seç")
        self.spin_batch_size = QSpinBox()
        self.spin_batch_size.setRange(1, 256)
        self.spin_batch_size.setValue(32)
        
        self.check_shuffle = QCheckBox("Shuffle (Karıştır)")
        self.check_shuffle.setChecked(True)

        form_layout.addRow(self.btn_select_folder)
        form_layout.addRow("Batch Size:", self.spin_batch_size)
        form_layout.addRow(self.check_shuffle)
        settings_group.setLayout(form_layout)

        # 2. Klasör Ağacı (Alt Kısım)
        self.tree_view = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath()) # Şimdilik bilgisayarın ana dizinini gösterir
        
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(QDir.rootPath()))
        
        # Ağaçtaki boyut, tarih gibi gereksiz kolonları gizle, sadece isim kalsın
        for i in range(1, 4):
            self.tree_view.hideColumn(i)

        # Elemanları ana layout'a ekle
        layout.addWidget(settings_group)
        layout.addWidget(self.tree_view)