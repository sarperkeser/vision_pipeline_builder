from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeView, 
                             QPushButton, QGroupBox, QSpinBox, QCheckBox, QFormLayout, QLabel, QHBoxLayout)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 1. Veri Seti Ayarları (Üst Kısım)
        settings_group = QGroupBox("Veri Seti ve Giriş Ayarları")
        form_layout = QFormLayout()
        
        self.btn_select_folder = QPushButton("Klasör Seç")
        
        # Algılanan Sınıf Sayısı Göstergesi
        self.lbl_num_classes = QLabel("0 (Klasör Seçilmedi)")
        self.lbl_num_classes.setStyleSheet("font-weight: bold; color: #4CAF50;")

        # Input Size (Görsel Boyutu: Genişlik x Yükseklik)
        size_box = QHBoxLayout()
        self.spin_img_width = QSpinBox()
        self.spin_img_width.setRange(16, 4096)
        self.spin_img_width.setValue(224)
        
        self.spin_img_height = QSpinBox()
        self.spin_img_height.setRange(16, 4096)
        self.spin_img_height.setValue(224)

        size_box.addWidget(self.spin_img_width)
        size_box.addWidget(QLabel("x"))
        size_box.addWidget(self.spin_img_height)

        # Batch Size ve Shuffle
        self.spin_batch_size = QSpinBox()
        self.spin_batch_size.setRange(1, 256)
        self.spin_batch_size.setValue(32)
        
        self.check_shuffle = QCheckBox("Shuffle (Karıştır)")
        self.check_shuffle.setChecked(True)

        form_layout.addRow(self.btn_select_folder)
        form_layout.addRow("Tespit Edilen Sınıf:", self.lbl_num_classes)
        form_layout.addRow("Input Size (WxH):", size_box)
        form_layout.addRow("Batch Size:", self.spin_batch_size)
        form_layout.addRow(self.check_shuffle)
        settings_group.setLayout(form_layout)

        # 2. Klasör Ağacı (Alt Kısım)
        self.tree_view = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(QDir.rootPath()))
        
        for i in range(1, 4):
            self.tree_view.hideColumn(i)

        layout.addWidget(settings_group)
        layout.addWidget(self.tree_view)