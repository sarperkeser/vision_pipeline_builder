from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                             QLabel, QGroupBox, QFormLayout, QCheckBox, QSpinBox, 
                             QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DataTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # --- ORTA PANEL BÖLÜMÜ (Önizleme ve Grafikler) ---
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)
        
        # Üst: Görsel Önizleme
        self.preview_label = QLabel("Görsel Önizleme Alanı\n(Klasör seçtiğinizde burada belirecek)")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #2b2b2b; color: white; border: 1px solid #444;")
        self.preview_label.setFont(QFont("Arial", 12))

        # YENİ EKLENEN KISIM: Görselin UI'ı zorlayıp büyütmesini tamamen engeller
        self.preview_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.preview_label.setMinimumSize(300, 300)
        
        # Alt: Veri Grafikleri (Placeholder)
        self.graphs_placeholder = QLabel("Veri Seti Dağılımı ve Grafikler\n(Bu alan sonraki aşamalarda doldurulacak)")
        self.graphs_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graphs_placeholder.setStyleSheet("background-color: #1e1e24; color: #888; border: 1px dashed #555;")
        
        middle_layout.addWidget(self.preview_label, stretch=6)
        middle_layout.addWidget(self.graphs_placeholder, stretch=4)
        
# --- SAĞ PANEL BÖLÜMÜ (Data Augmentation) ---
        from PyQt6.QtWidgets import QDoubleSpinBox # En üste import eklemeyi unutma
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        aug_group = QGroupBox("Data Augmentation (Veri Çoğaltma)")
        aug_form = QFormLayout()
        
        self.check_hflip = QCheckBox("Horizontal Flip (Yatay Çevir)")
        self.check_vflip = QCheckBox("Vertical Flip (Dikey Çevir)")
        
        self.spin_rotation = QSpinBox()
        self.spin_rotation.setRange(0, 359)
        self.spin_rotation.setSuffix(" °")
        self.spin_rotation.setValue(0)
        
        # Color Jitter Grubu
        self.check_color_jitter = QCheckBox("Color Jitter Aktif")
        self.check_color_jitter.setStyleSheet("font-weight: bold; margin-top: 10px;")
        
        self.spin_brightness = QDoubleSpinBox()
        self.spin_brightness.setRange(0.0, 2.0)
        self.spin_brightness.setSingleStep(0.1)
        self.spin_brightness.setValue(0.2)
        
        self.spin_contrast = QDoubleSpinBox()
        self.spin_contrast.setRange(0.0, 2.0)
        self.spin_contrast.setSingleStep(0.1)
        self.spin_contrast.setValue(0.2)
        
        self.spin_saturation = QDoubleSpinBox()
        self.spin_saturation.setRange(0.0, 2.0)
        self.spin_saturation.setSingleStep(0.1)
        self.spin_saturation.setValue(0.2)

        # Gaussian Blur Grubu
        self.check_gaussian_blur = QCheckBox("Gaussian Blur Aktif")
        self.check_gaussian_blur.setStyleSheet("font-weight: bold; margin-top: 10px;")
        
        self.spin_blur_kernel = QSpinBox()
        self.spin_blur_kernel.setRange(1, 21)
        self.spin_blur_kernel.setSingleStep(2) # 1, 3, 5, 7 şeklinde artması PyTorch standardıdır
        self.spin_blur_kernel.setValue(3)

        aug_form.addRow(self.check_hflip)
        aug_form.addRow(self.check_vflip)
        aug_form.addRow("Rotation:", self.spin_rotation)
        
        aug_form.addRow(self.check_color_jitter)
        aug_form.addRow("  ↳ Brightness:", self.spin_brightness)
        aug_form.addRow("  ↳ Contrast:", self.spin_contrast)
        aug_form.addRow("  ↳ Saturation:", self.spin_saturation)
        
        aug_form.addRow(self.check_gaussian_blur)
        aug_form.addRow("  ↳ Kernel Size:", self.spin_blur_kernel)
        
        aug_group.setLayout(aug_form)
        right_layout.addWidget(aug_group)
        right_layout.addStretch()
        
        
        # Splitter'a ekle
        splitter.addWidget(middle_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([800, 300]) # Orta panel geniş, sağ panel dar
        
        layout.addWidget(splitter)